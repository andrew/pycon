import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

RESULTS_BASE = Path("data/zizmor_results")
ACTIONS_BASE = Path("data/actions")
BRIEF_BASE = Path("data/brief")
NO_WORKFLOWS_FILE = Path("data/no_workflows.json")
FAILED_FILE = Path("data/failed.json")
MAX_CLONE_RETRIES = 3


def clone_with_backoff(repo_url: str, clone_dir: str) -> subprocess.CompletedProcess:
    for attempt in range(MAX_CLONE_RETRIES):
        env = {
            **subprocess.os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_ASKPASS": "",
            "GIT_CONFIG_NOSYSTEM": "1",
            "SSH_ASKPASS": "",
        }
        result = subprocess.run(
            ["git", "-c", "credential.helper=", "clone", "--depth=1", "--filter=blob:none", repo_url, clone_dir],
            capture_output=True, text=True, timeout=60, env=env,
        )
        if result.returncode == 0:
            return result
        stderr = result.stderr.lower()
        if "rate limit" in stderr or "too many requests" in stderr or "429" in stderr:
            wait = 2 ** attempt * 30
            print(f"rate limited, waiting {wait}s...", end=" ", flush=True)
            time.sleep(wait)
            continue
        # not a rate limit, don't retry
        return result
    return result


def parse_uses(uses: str) -> dict:
    """Parse a uses: directive, matching zizmor's approach.

    Handles three types:
    - local: ./path
    - docker: docker://image
    - repository: owner/repo@ref or owner/repo/subpath@ref
    """
    uses = uses.strip()
    if uses.startswith("./"):
        return {"type": "local", "action": uses, "ref": "", "pinned": False}
    if uses.startswith("docker://"):
        return {"type": "docker", "action": uses, "ref": "", "pinned": False}
    # repository uses: split on last @
    ref = ""
    action = uses
    if "@" in uses:
        action, ref = uses.rsplit("@", 1)
    pinned = len(ref) == 40 and all(c in "0123456789abcdef" for c in ref)
    return {"type": "repository", "action": action, "ref": ref, "pinned": pinned}


def extract_actions(workflows_dir: Path) -> list[dict]:
    """Extract all uses: directives from workflow files."""
    actions = []
    for wf_file in workflows_dir.glob("*.y*ml"):
        try:
            data = yaml.safe_load(wf_file.read_text())
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        jobs = data.get("jobs") or {}
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            # job-level uses (reusable workflows)
            job_uses = job.get("uses")
            if job_uses and isinstance(job_uses, str):
                parsed = parse_uses(job_uses)
                parsed["workflow"] = wf_file.name
                parsed["job"] = job_name
                parsed["level"] = "job"
                actions.append(parsed)
            # step-level uses
            steps = job.get("steps") or []
            for step in steps:
                if not isinstance(step, dict):
                    continue
                uses = step.get("uses")
                if not uses:
                    continue
                parsed = parse_uses(uses)
                parsed["workflow"] = wf_file.name
                parsed["job"] = job_name
                parsed["level"] = "step"
                actions.append(parsed)
    return actions


def safe_name(name: str) -> str:
    return name.replace("/", "__")


def scan_repo(name: str, repo_url: str, results_dir: Path, actions_dir: Path, brief_dir: Path, no_workflows: set) -> str:
    """Returns 'scanned', 'no_workflows', 'failed', or 'skip'."""
    fname = safe_name(name)
    zizmor_path = results_dir / f"{fname}.json"
    actions_path = actions_dir / f"{fname}.json"
    brief_path = brief_dir / f"{fname}.json"
    has_zizmor = zizmor_path.exists()
    has_actions = actions_path.exists()
    has_brief = brief_path.exists()

    if has_zizmor and has_actions and has_brief:
        return "skip"
    if repo_url in no_workflows and has_brief:
        return "skip"

    tmpdir = tempfile.mkdtemp()
    try:
        clone_dir = str(Path(tmpdir) / name)
        print(f"  cloning {repo_url}...", end=" ", flush=True)
        result = clone_with_backoff(repo_url, clone_dir)
        if result.returncode != 0:
            print(f"clone failed")
            return "failed"

        # run brief before sparse checkout (needs full file tree)
        if not has_brief:
            result = subprocess.run(
                ["brief", "-json", clone_dir],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0 and result.stdout.strip():
                brief_dir.mkdir(parents=True, exist_ok=True)
                brief_path.write_text(result.stdout)
                print("brief...", end=" ", flush=True)

        subprocess.run(
            ["git", "sparse-checkout", "set", ".github/workflows"],
            cwd=clone_dir, capture_output=True, text=True,
        )

        workflows_dir = Path(clone_dir) / ".github" / "workflows"
        if not workflows_dir.exists() or not any(workflows_dir.iterdir()):
            print("no workflows")
            return "no_workflows"

        # extract actions
        if not has_actions:
            actions = extract_actions(workflows_dir)
            actions_dir.mkdir(parents=True, exist_ok=True)
            actions_path.write_text(json.dumps(actions, indent=2))
            print(f"{len(actions)} actions...", end=" ", flush=True)

        # run zizmor
        if not has_zizmor:
            print("scanning...", end=" ", flush=True)
            result = subprocess.run(
                ["uvx", "zizmor@1.24.1", "--format=json", str(workflows_dir)],
                capture_output=True, text=True, timeout=120,
            )

            if "crashed" in result.stderr or "panic" in result.stderr.lower():
                print(f"zizmor crashed")
                return "failed"

            output = result.stdout.strip()
            if not output:
                output = "[]"

            try:
                findings = json.loads(output)
            except json.JSONDecodeError:
                print(f"bad json output")
                return "failed"

            zizmor_path.write_text(json.dumps(findings, indent=2))
            print(f"{len(findings)} findings")
        else:
            print("done")

        return "scanned"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def iter_packages_from_pages(pages_dir: Path):
    """Yield (name, repo_url, canonical_name) from page files.

    canonical_name is the first package seen for a given repo url.
    When name == canonical_name, this is the first time we've seen this repo.
    When they differ, results can be copied from the canonical package.
    """
    repo_to_canonical = {}
    seen_names = set()
    for page_file in sorted(pages_dir.glob("page_*.json")):
        packages = json.loads(page_file.read_text())
        for pkg in packages:
            name = pkg["name"]
            if name in seen_names:
                continue
            seen_names.add(name)
            repo_url = pkg.get("repository_url") or ""
            if "github.com" not in repo_url:
                continue
            canonical = repo_to_canonical.get(repo_url)
            if canonical is None:
                repo_to_canonical[repo_url] = name
                canonical = name
            yield name, repo_url, canonical


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    pages_dir = Path(f"data/pages/{slug}")
    registry_slug = registry.replace(".", "_")
    results_dir = RESULTS_BASE / registry_slug
    actions_dir = ACTIONS_BASE / registry_slug
    brief_dir = BRIEF_BASE / registry_slug
    results_dir.mkdir(parents=True, exist_ok=True)

    no_workflows = set()
    if NO_WORKFLOWS_FILE.exists():
        no_workflows = set(json.loads(NO_WORKFLOWS_FILE.read_text()))
    failed_set = set()
    if FAILED_FILE.exists():
        failed_set = set(json.loads(FAILED_FILE.read_text()))

    skipped = 0
    copied = 0
    success = 0
    no_wf = 0
    failed = 0
    for name, repo_url, canonical in iter_packages_from_pages(pages_dir):
        if name != canonical:
            # shared repo - copy results from canonical if available
            canonical_result = results_dir / f"{safe_name(canonical)}.json"
            pkg_result = results_dir / f"{safe_name(name)}.json"
            if canonical_result.exists() and not pkg_result.exists():
                pkg_result.write_text(canonical_result.read_text())
                copied += 1
            skipped += 1
            continue

        try:
            status = scan_repo(name, repo_url, results_dir, actions_dir, brief_dir, no_workflows)
        except Exception as e:
            print(f"  {name} error: {e}")
            failed_set.add(repo_url)
            failed += 1
            continue
        if status == "skip":
            skipped += 1
            if skipped % 500 == 0:
                print(f"  skipped {skipped}...")
            continue
        print(f"  {name}", end=" ")
        if status == "scanned":
            success += 1
        elif status == "no_workflows":
            no_workflows.add(repo_url)
            no_wf += 1
        else:
            failed_set.add(repo_url)
            failed += 1

        # save state periodically
        if (success + no_wf + failed) % 100 == 0:
            NO_WORKFLOWS_FILE.write_text(json.dumps(sorted(no_workflows), indent=2))
            FAILED_FILE.write_text(json.dumps(sorted(failed_set), indent=2))

    NO_WORKFLOWS_FILE.write_text(json.dumps(sorted(no_workflows), indent=2))
    FAILED_FILE.write_text(json.dumps(sorted(failed_set), indent=2))
    print(f"\nDone: {success} scanned, {copied} copied, {no_wf} no workflows, {failed} failed, {skipped} skipped")


if __name__ == "__main__":
    main()
