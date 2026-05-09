"""Export workflow files from repos with most exploitable findings for LLM review."""

import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

EXPORT_DIR = Path("data/workflows_export")

SCARY_AUDITS = (
    "template-injection",
    "dangerous-triggers",
    "cache-poisoning",
    "insecure-commands",
    "github-env",
)


def clone_workflows(repo_url: str) -> dict[str, str]:
    """Clone repo and return {filename: content} for all workflow files."""
    tmpdir = tempfile.mkdtemp()
    try:
        env = {
            **subprocess.os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ASKPASS": "",
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        result = subprocess.run(
            ["git", "-c", "credential.helper=", "clone", "--depth=1",
             "--filter=blob:none", "--sparse", repo_url, str(Path(tmpdir) / "repo")],
            capture_output=True, text=True, timeout=60, env=env,
        )
        if result.returncode != 0:
            return {}

        clone_dir = Path(tmpdir) / "repo"
        subprocess.run(
            ["git", "sparse-checkout", "set", ".github/workflows"],
            cwd=clone_dir, capture_output=True, text=True,
        )

        workflows = {}
        wf_dir = clone_dir / ".github" / "workflows"
        if wf_dir.exists():
            for f in wf_dir.glob("*.y*ml"):
                workflows[f.name] = f.read_text()
        return workflows
    except Exception:
        return {}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def get_top_repos(db_path: Path, limit: int) -> list[dict]:
    db = sqlite3.connect(db_path)
    placeholders = ",".join("?" for _ in SCARY_AUDITS)
    rows = db.execute(f"""
        SELECT f.repository_url, COUNT(*) as scary,
            COUNT(DISTINCT f.audit) as audits,
            MAX(p.dependent_packages_count) as dependents,
            MAX(p.downloads) as downloads
        FROM findings f
        JOIN packages p ON p.repository_url = f.repository_url
        WHERE f.severity = 'High'
            AND f.audit IN ({placeholders})
        GROUP BY f.repository_url
        HAVING dependents > 10
        ORDER BY scary * LOG(dependents + 1) DESC
        LIMIT ?
    """, (*SCARY_AUDITS, limit)).fetchall()
    db.close()

    return [{"url": r[0], "scary": r[1], "audits": r[2],
             "dependents": r[3], "downloads": r[4]} for r in rows]


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    limit = 50
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)

    db_path = Path(f"data/{slug}.db")
    if not db_path.exists():
        print(f"No DB at {db_path}")
        sys.exit(1)

    repos = get_top_repos(db_path, limit)
    export_dir = EXPORT_DIR / slug
    export_dir.mkdir(parents=True, exist_ok=True)

    for i, repo in enumerate(repos):
        org_repo = "/".join(repo["url"].rstrip("/").split("/")[-2:])
        safe = org_repo.replace("/", "__")
        repo_dir = export_dir / safe

        if repo_dir.exists() and any(repo_dir.glob("*.y*ml")):
            print(f"[{i+1}/{len(repos)}] {org_repo} (cached)")
            continue

        print(f"[{i+1}/{len(repos)}] {org_repo} ({repo['scary']} findings, {repo['dependents']} dependents)...", end=" ", flush=True)
        workflows = clone_workflows(repo["url"])
        if not workflows:
            print("no workflows")
            continue

        repo_dir.mkdir(parents=True, exist_ok=True)
        for name, content in workflows.items():
            (repo_dir / name).write_text(content)
        print(f"{len(workflows)} files")

    # write index with metadata
    index = []
    for repo in repos:
        org_repo = "/".join(repo["url"].rstrip("/").split("/")[-2:])
        safe = org_repo.replace("/", "__")
        repo_dir = export_dir / safe
        if not repo_dir.exists():
            continue
        files = sorted(f.name for f in repo_dir.glob("*.y*ml"))
        index.append({
            "repo": org_repo,
            "url": repo["url"],
            "scary_findings": repo["scary"],
            "audit_types": repo["audits"],
            "dependents": repo["dependents"],
            "downloads": repo["downloads"],
            "workflows": files,
        })

    (export_dir / "index.json").write_text(json.dumps(index, indent=2))
    print(f"\nExported {len(index)} repos to {export_dir}")


if __name__ == "__main__":
    main()
