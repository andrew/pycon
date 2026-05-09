"""Resolve transitive dependencies for GitHub Actions."""

import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

CACHE_DIR = Path("data/action_manifests")
TREE_DIR = Path("data/action_trees")
MAX_DEPTH = 5


def fetch_manifest(action: str, ref: str = "") -> dict | None:
    """Clone repo and read action.yml or action.yaml."""
    if action.startswith("./") or action.startswith("docker://"):
        return None

    parts = action.split("/")
    if len(parts) < 2:
        return None

    owner = parts[0]
    repo = parts[1]
    subpath = "/".join(parts[2:]) if len(parts) > 2 else ""

    cache_key = action.replace("/", "__")
    if ref:
        safe_ref = ref.replace("/", "_")
        cache_key += f"__{safe_ref[:12]}"
    cache_path = CACHE_DIR / f"{cache_key}.json"
    if cache_path.exists():
        data = json.loads(cache_path.read_text())
        return data if data else None

    repo_url = f"https://github.com/{owner}/{repo}"
    tmpdir = tempfile.mkdtemp()
    try:
        clone_cmd = ["git", "clone", "--depth=1", "--filter=blob:none",
                     "--sparse", repo_url, str(Path(tmpdir) / "repo")]
        if ref:
            clone_cmd.insert(-1, f"--branch={ref}" if not (len(ref) == 40 and all(c in "0123456789abcdef" for c in ref)) else "")
            clone_cmd = [c for c in clone_cmd if c]

        env = {**subprocess.os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": ""}
        for attempt in range(3):
            result = subprocess.run(clone_cmd, capture_output=True, text=True, timeout=30, env=env)
            if result.returncode == 0:
                break
            if "rate limit" in result.stderr.lower() or "429" in result.stderr:
                wait = 2 ** attempt * 30
                print(f"  rate limited, waiting {wait}s...", end=" ", flush=True)
                time.sleep(wait)
                continue
            break
        if result.returncode != 0:
            cache_path.write_text("null")
            return None

        clone_dir = Path(tmpdir) / "repo"

        # if pinned to SHA, fetch that specific commit
        if ref and len(ref) == 40 and all(c in "0123456789abcdef" for c in ref):
            subprocess.run(["git", "fetch", "origin", ref], cwd=clone_dir,
                          capture_output=True, text=True, timeout=30, env=env)
            subprocess.run(["git", "checkout", ref], cwd=clone_dir,
                          capture_output=True, text=True, timeout=30, env=env)

        # sparse checkout the action path
        checkout_path = subpath if subpath else "."
        if checkout_path != ".":
            subprocess.run(["git", "sparse-checkout", "set", checkout_path],
                          cwd=clone_dir, capture_output=True, text=True)

        for filename in ("action.yml", "action.yaml"):
            action_file = clone_dir / subpath / filename if subpath else clone_dir / filename
            if action_file.exists():
                try:
                    manifest = yaml.safe_load(action_file.read_text())
                except Exception:
                    continue
                if manifest:
                    cache_path.write_text(json.dumps(manifest, indent=2))
                    return manifest

        cache_path.write_text("null")
        return None
    except Exception:
        cache_path.write_text("null")
        return None
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def extract_uses(manifest: dict) -> list[dict]:
    """Extract uses: directives from an action manifest."""
    uses = []
    runs = manifest.get("runs") or {}
    if runs.get("using") != "composite":
        return uses

    steps = runs.get("steps") or []
    for step in steps:
        if not isinstance(step, dict):
            continue
        step_uses = step.get("uses")
        if not step_uses or not isinstance(step_uses, str):
            continue
        step_uses = step_uses.strip()
        if step_uses.startswith("./") or step_uses.startswith("docker://"):
            continue
        ref = ""
        action = step_uses
        if "@" in step_uses:
            action, ref = step_uses.rsplit("@", 1)
        pinned = len(ref) == 40 and all(c in "0123456789abcdef" for c in ref)
        uses.append({"action": action, "ref": ref, "pinned": pinned})
    return uses


def resolve_tree(action: str, ref: str = "", depth: int = 0, seen: set = None) -> dict:
    """Recursively resolve the dependency tree for an action."""
    if seen is None:
        seen = set()

    node = {
        "action": action,
        "ref": ref,
        "pinned": len(ref) == 40 and all(c in "0123456789abcdef" for c in ref),
        "type": "unknown",
        "deps": [],
    }

    if action in seen or depth >= MAX_DEPTH:
        node["type"] = "circular" if action in seen else "max_depth"
        return node

    seen = seen | {action}

    manifest = fetch_manifest(action, ref)
    if not manifest:
        node["type"] = "not_found"
        return node

    runs = manifest.get("runs") or {}
    using = runs.get("using", "")
    if using == "composite":
        node["type"] = "composite"
        deps = extract_uses(manifest)
        for dep in deps:
            child = resolve_tree(dep["action"], dep["ref"], depth + 1, seen)
            node["deps"].append(child)
    else:
        node["type"] = using

    return node


def count_tree(tree: dict) -> dict:
    """Count pinned/unpinned across a dependency tree."""
    counts = {"total": 0, "pinned": 0, "unpinned": 0, "depth": 0}

    def walk(node, depth):
        if node["type"] in ("not_found", "circular", "max_depth"):
            return
        counts["total"] += 1
        if node["pinned"]:
            counts["pinned"] += 1
        else:
            counts["unpinned"] += 1
        counts["depth"] = max(counts["depth"], depth)
        for dep in node.get("deps", []):
            walk(dep, depth + 1)

    walk(tree, 0)
    return counts


def print_tree(tree: dict, indent: int = 0):
    """Format a tree for display."""
    prefix = "  " * indent
    pin = "pinned" if tree["pinned"] else "UNPINNED"
    ref_short = tree["ref"][:12] if tree["pinned"] else tree["ref"]
    lines = [f"{prefix}{tree['action']}@{ref_short} ({tree['type']}, {pin})"]
    for dep in tree.get("deps", []):
        lines.extend(print_tree(dep, indent + 1).split("\n"))
    return "\n".join(lines)


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"

    db_path = Path(f"data/actions_{slug}.db")
    if not db_path.exists():
        print(f"No actions DB found at {db_path}")
        sys.exit(1)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TREE_DIR.mkdir(parents=True, exist_ok=True)

    db = sqlite3.connect(db_path)
    # get top actions by repo count
    top_actions = db.execute("""
        SELECT action, repo_count,
            (SELECT ref FROM action_uses WHERE action = a.action GROUP BY ref ORDER BY COUNT(*) DESC LIMIT 1) as top_ref
        FROM actions a
        WHERE a.action NOT LIKE './%' AND a.action NOT LIKE 'docker://%'
        ORDER BY repo_count DESC LIMIT 100
    """).fetchall()
    db.close()

    trees = []
    for action, repo_count, top_ref in top_actions:
        tree_path = TREE_DIR / f"{action.replace('/', '__')}.json"
        if tree_path.exists():
            tree = json.loads(tree_path.read_text())
        else:
            print(f"Resolving {action}...", end=" ", flush=True)
            tree = resolve_tree(action, top_ref or "")
            tree_path.write_text(json.dumps(tree, indent=2))
            counts = count_tree(tree)
            print(f"{counts['total']} deps, depth {counts['depth']}")
            time.sleep(1)

        tree["repo_count"] = repo_count
        trees.append(tree)

    # generate report
    report_path = Path(f"data/report_deps_{slug}.md")
    out = []
    out.append(f"# Action dependency trees: {registry}")
    out.append("")

    # summary table
    out.append("## Summary")
    out.append("")
    out.append("| Action | Repos | Type | Deps | Depth | All pinned |")
    out.append("| --- | ---: | --- | ---: | ---: | --- |")
    for tree in trees:
        counts = count_tree(tree)
        all_pinned = "yes" if counts["unpinned"] == 0 and counts["total"] > 0 else "no"
        if counts["total"] <= 1:
            all_pinned = "-"
        out.append(f"| {tree['action']} | {tree['repo_count']} | {tree['type']} | {counts['total'] - 1} | {counts['depth']} | {all_pinned} |")

    # composite actions with deps
    out.append("")
    out.append("## Dependency trees (composite actions)")
    out.append("")
    for tree in trees:
        if tree["type"] != "composite" or not tree.get("deps"):
            continue
        counts = count_tree(tree)
        out.append(f"### {tree['action']} ({tree['repo_count']} repos)")
        out.append("")
        out.append(f"```")
        out.append(print_tree(tree))
        out.append(f"```")
        out.append("")

    report = "\n".join(out) + "\n"
    report_path.write_text(report)
    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()
