"""Compute every number that appears on a slide.

Run after a scan to refresh the deck. Reads from data/*.db and data/*.tsv,
prints a labelled report. Each section header maps to a slide title.
"""

import glob
import json
import sqlite3
from pathlib import Path


ACTIONS_DB = Path("data/actions_pypi_org.db")
FINDINGS_DB = Path("data/pypi_org.db")
PUBLISH_TSV = Path("data/slice_actions_in_publish_job.tsv")
TREES_DIR = Path("data/action_trees")
FAILED = Path("data/failed.json")

FIRST_PARTY = ("actions/", "github/", "./")


def h(title):
    print(f"\n## {title}\n")


def adoption():
    h("GitHub Actions is the default CI for Python")
    fdb = sqlite3.connect(FINDINGS_DB)
    total_gh = fdb.execute(
        "SELECT COUNT(*) FROM packages WHERE repository_url LIKE '%github.com%'"
    ).fetchone()[0]
    adb = sqlite3.connect(ACTIONS_DB)
    with_actions = adb.execute(
        "SELECT COUNT(DISTINCT repo_name) FROM action_uses"
    ).fetchone()[0]
    print(f"PyPI packages linking a GitHub repo: {total_gh:,}")
    print(f"Repos with at least one action_uses: {with_actions:,}")
    print(f"=> {with_actions/total_gh:.1%} use Actions (by repo, lower bound)")


def publish_from_actions():
    h("It's also how packages reach PyPI")
    adb = sqlite3.connect(ACTIONS_DB)
    n = adb.execute(
        "SELECT COUNT(DISTINCT repo_name) FROM action_uses "
        "WHERE action='pypa/gh-action-pypi-publish'"
    ).fetchone()[0]
    print(f"Repos using pypa/gh-action-pypi-publish: {n:,}")


def repo_404s():
    h("The dataset (404 rate)")
    failed = json.loads(FAILED.read_text())
    gh = [u for u in failed if "github.com" in u]
    print(f"GitHub URLs in failed.json (all registries, all error types): {len(gh):,}")
    print("TODO: filter to pypi-only and not-found/auth errors for a real %")


def per_audit():
    h("Six audits (per-audit repo counts)")
    fdb = sqlite3.connect(FINDINGS_DB)
    for audit, n in fdb.execute(
        "SELECT audit, COUNT(DISTINCT repository_url) FROM findings "
        "GROUP BY audit ORDER BY 2 DESC"
    ):
        print(f"  {audit:<28} {n:>8,}")


def top_third_party():
    h("Most popular third-party actions")
    adb = sqlite3.connect(ACTIONS_DB)
    where = " AND ".join(f"action NOT LIKE '{p}%'" for p in FIRST_PARTY)
    for row in adb.execute(
        f"SELECT action, repo_count, total_uses, "
        f"ROUND(100.0*unpinned_count/total_uses,1) "
        f"FROM actions WHERE {where} ORDER BY repo_count DESC LIMIT 12"
    ):
        print(f"  {row[0]:<45} {row[1]:>7,} repos  {row[3]:>5}% unpinned")


def publish_job_actions():
    h("Where they concentrate (third-party in publish jobs)")
    if not PUBLISH_TSV.exists():
        print("  slice_actions_in_publish_job.tsv missing")
        return
    rows = []
    for line in PUBLISH_TSV.read_text().splitlines()[1:]:
        action, repos, unpinned, pinned = line.split("\t")
        total = int(unpinned) + int(pinned)
        pct = 100 * int(unpinned) / total if total else 0
        rows.append((action, int(repos), pct))
    for action, repos, pct in sorted(rows, key=lambda r: -r[1])[:12]:
        print(f"  {action:<50} {repos:>6,} jobs  {pct:>5.1f}% unpinned")


def transitive():
    h("Their transitive dependencies")
    if not TREES_DIR.exists():
        print("  no action_trees/")
        return
    composites = unpinned_tp = 0
    examples = []
    for f in glob.glob(str(TREES_DIR / "*.json")):
        d = json.load(open(f))
        if d.get("type") != "composite":
            continue
        composites += 1
        def walk(n, path):
            nonlocal unpinned_tp
            for dep in n.get("deps", []):
                if not dep.get("pinned") and not any(
                    dep["action"].startswith(p) for p in FIRST_PARTY
                ):
                    unpinned_tp += 1
                    examples.append(f"{d['action']} -> {dep['action']}@{dep.get('ref','')}")
                walk(dep, path + [dep["action"]])
        walk(d, [])
    print(f"  composite actions in cache: {composites}")
    print(f"  with unpinned third-party transitive: {unpinned_tp}")
    for e in examples[:10]:
        print(f"    {e}")


def main():
    print("# Slide data (first pass from existing dbs)")
    adoption()
    publish_from_actions()
    repo_404s()
    per_audit()
    top_third_party()
    publish_job_actions()
    transitive()


if __name__ == "__main__":
    main()
