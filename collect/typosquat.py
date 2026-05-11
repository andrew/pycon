"""Find typosquat variants of popular actions that are actually used in PyPI workflows.

For each top-N action, generate variants with `typosquatting generate -e github_actions`
(github.com/andrew/typosquatting), then check which variants appear in the actions
inventory db. Optionally check which exist as live GitHub repos.
"""

import sqlite3
import subprocess
import sys
from pathlib import Path


DB = Path("data/actions_pypi_org.db")
TOP_N = 40


def variants(action: str) -> set[str]:
    r = subprocess.run(
        ["typosquatting", "generate", action, "-e", "github_actions"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return set()
    return {line.strip() for line in r.stdout.splitlines() if line.strip()}


def repo_exists(slug: str) -> bool:
    r = subprocess.run(["gh", "api", f"repos/{slug}"], capture_output=True, text=True)
    return r.returncode == 0


def main():
    check_live = "--check" in sys.argv
    db = sqlite3.connect(DB)

    targets = [a for (a,) in db.execute(
        "SELECT action FROM actions WHERE action NOT LIKE './%' "
        "AND action NOT LIKE 'docker://%' ORDER BY repo_count DESC LIMIT ?",
        (TOP_N,)
    )]
    in_use = dict(db.execute("SELECT lower(action), repo_count FROM actions"))

    print(f"# typosquat variants of top {TOP_N} actions seen in PyPI workflows\n")
    total_variants = 0
    hits = []
    for t in targets:
        vs = variants(t)
        total_variants += len(vs)
        for v in vs:
            c = in_use.get(v.lower())
            if c:
                hits.append((t, v, c))

    for t, v, c in sorted(hits, key=lambda x: -x[2]):
        live = ""
        if check_live:
            slug = "/".join(v.split("/")[:2])
            live = "  [exists]" if repo_exists(slug) else "  [404]"
        print(f"  {v:<44} {c:>4} repos   (variant of {t}){live}")

    print(f"\n{len(hits)} variants in use out of {total_variants:,} generated "
          f"across {len(targets)} targets")


if __name__ == "__main__":
    main()
