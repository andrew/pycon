"""Compare zizmor findings across registries."""

import sqlite3
import sys
from pathlib import Path


def load_stats(slug: str) -> dict:
    db_path = Path(f"data/{slug}.db")
    db = sqlite3.connect(db_path)

    total_packages = db.execute("SELECT COUNT(*) FROM packages").fetchone()[0]
    unique_repos = db.execute("SELECT COUNT(DISTINCT repository_url) FROM packages").fetchone()[0]

    registry_slug = slug.replace("_critical", "")
    scanned_names = {p.stem for p in (Path("data/zizmor_results") / registry_slug).glob("*.json")}
    scanned_repo_urls = set()
    for row in db.execute("SELECT name, repository_url FROM packages"):
        if row[0] in scanned_names or row[0].replace("/", "__") in scanned_names:
            scanned_repo_urls.add(row[1])
    scanned = len(scanned_repo_urls)

    no_wf_file = Path("data/no_workflows.json")
    import json
    no_wf_urls = set()
    if no_wf_file.exists():
        no_wf_set = set(json.loads(no_wf_file.read_text()))
        for row in db.execute("SELECT name, repository_url FROM packages"):
            if row[1] in no_wf_set:
                no_wf_urls.add(row[1])

    with_findings = db.execute("SELECT COUNT(DISTINCT repository_url) FROM findings").fetchone()[0]
    total_findings = db.execute("SELECT COUNT(*) FROM findings").fetchone()[0]

    severity_repos = {}
    for sev in ("High", "Medium", "Low", "Informational"):
        severity_repos[sev] = db.execute(
            "SELECT COUNT(DISTINCT repository_url) FROM findings WHERE severity = ?", (sev,)
        ).fetchone()[0]

    audit_repos = {}
    for row in db.execute("""
        SELECT audit, COUNT(DISTINCT repository_url) as repos, COUNT(*) as n
        FROM findings GROUP BY audit ORDER BY repos DESC
    """):
        audit_repos[row[0]] = {"repos": row[1], "findings": row[2]}

    pinned = unpinned = 0
    actions_db_path = Path(f"data/actions_{slug}.db")
    if actions_db_path.exists():
        adb = sqlite3.connect(actions_db_path)
        row = adb.execute("SELECT SUM(pinned_count), SUM(unpinned_count) FROM actions").fetchone()
        pinned = row[0] or 0
        unpinned = row[1] or 0
        adb.close()

    db.close()

    return {
        "packages": total_packages,
        "unique_repos": unique_repos,
        "scanned": scanned,
        "no_workflows": len(no_wf_urls),
        "with_findings": with_findings,
        "total_findings": total_findings,
        "severity_repos": severity_repos,
        "audit_repos": audit_repos,
        "pinned": pinned,
        "unpinned": unpinned,
    }


def pct(n, total):
    return f"{round(n * 100 / total, 1)}%" if total else "-"


def main():
    if len(sys.argv) < 3:
        print("Usage: uv run compare.py <slug1> <slug2> [slug3...]")
        print("Example: uv run compare.py pypi_org_critical rubygems_org_critical")
        sys.exit(1)

    slugs = [a for a in sys.argv[1:] if not a.startswith("--")]
    stats = {s: load_stats(s) for s in slugs}

    def md_table(headers, rows, alignments=None):
        if alignments is None:
            alignments = ["left"] + ["right"] * (len(headers) - 1)
        sep = []
        for a in alignments:
            sep.append("---:" if a == "right" else "---")
        lines = ["| " + " | ".join(headers) + " |"]
        lines.append("| " + " | ".join(sep) + " |")
        for r in rows:
            lines.append("| " + " | ".join(str(v) for v in r) + " |")
        return "\n".join(lines)

    def val(fn):
        return [fn(stats[s]) for s in slugs]

    out = []
    out.append("# Registry comparison")
    out.append("")

    headers = [""] + slugs
    rows = []
    rows.append(["Packages"] + val(lambda s: s["packages"]))
    rows.append(["Unique repos"] + val(lambda s: s["unique_repos"]))
    rows.append(["Repos scanned"] + val(lambda s: s["scanned"]))
    rows.append(["No workflows"] + val(lambda s: pct(s["no_workflows"], s["scanned"])))
    rows.append(["Repos with findings"] + val(lambda s: pct(s["with_findings"], s["scanned"])))
    rows.append(["Findings per scanned repo"] + val(lambda s: round(s["total_findings"] / s["scanned"], 1) if s["scanned"] else "-"))
    rows.append(["Total findings"] + val(lambda s: s["total_findings"]))
    out.append(md_table(headers, rows))

    out.append("")
    out.append("## Severity")
    out.append("")
    rows = []
    for sev in ("High", "Medium", "Low", "Informational"):
        rows.append([sev] + val(lambda s, sv=sev: pct(s["severity_repos"].get(sv, 0), s["scanned"])))
    out.append(md_table(headers, rows))

    if any(s["pinned"] + s["unpinned"] > 0 for s in stats.values()):
        out.append("")
        out.append("## Action pinning")
        out.append("")
        rows = [
            ["Pinned (SHA)"] + val(lambda s: pct(s["pinned"], s["pinned"] + s["unpinned"]) if s["pinned"] + s["unpinned"] else "-"),
            ["Unpinned"] + val(lambda s: pct(s["unpinned"], s["pinned"] + s["unpinned"]) if s["pinned"] + s["unpinned"] else "-"),
        ]
        out.append(md_table(headers, rows))

    all_audits = set()
    for s in stats.values():
        all_audits.update(s["audit_repos"].keys())

    out.append("")
    out.append("## Audit types (% of scanned repos)")
    out.append("")
    rows = []
    for audit in sorted(all_audits, key=lambda a: max(stats[s]["audit_repos"].get(a, {}).get("repos", 0) for s in slugs), reverse=True):
        rows.append([audit] + val(lambda s, a=audit: pct(s["audit_repos"].get(a, {}).get("repos", 0), s["scanned"])))
    out.append(md_table(headers, rows))

    report = "\n".join(out) + "\n"
    report_path = Path("data/comparison.md")
    report_path.write_text(report)
    print(report)
    print(f"Written to {report_path}")


if __name__ == "__main__":
    main()
