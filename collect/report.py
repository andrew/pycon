import json
import sqlite3
import sys
from pathlib import Path


def md_table(headers: list[str], rows: list[list], alignments: list[str] | None = None) -> str:
    if alignments is None:
        alignments = ["left"] * len(headers)
    sep = []
    for a in alignments:
        if a == "right":
            sep.append("---:")
        else:
            sep.append("---")
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(sep) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    db_path = Path(f"data/{slug}.db")
    report_path = Path(f"data/report_{slug}.md")

    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row

    total_packages = db.execute("SELECT COUNT(*) FROM packages").fetchone()[0]
    unique_repos = db.execute("SELECT COUNT(DISTINCT repository_url) FROM packages").fetchone()[0]
    pages_dir = Path(f"data/pages/{slug}")
    total_fetched = 0
    host_counts = {}
    no_repo_count = 0
    if pages_dir.exists():
        seen_names = set()
        for p in sorted(pages_dir.glob("page_*.json")):
            for pkg in json.loads(p.read_text()):
                if pkg["name"] in seen_names:
                    continue
                seen_names.add(pkg["name"])
                total_fetched += 1
                repo_url = pkg.get("repository_url") or ""
                if not repo_url:
                    no_repo_count += 1
                    continue
                try:
                    host = repo_url.split("/")[2].lower()
                except IndexError:
                    host = "other"
                host_counts[host] = host_counts.get(host, 0) + 1
    else:
        total_fetched = total_packages

    # count unique repos that have been scanned (have a results file)
    registry_slug = registry.replace(".", "_")
    scanned_names = {p.stem for p in (Path("data/zizmor_results") / registry_slug).glob("*.json")}
    scanned_repo_urls = set()
    for row in db.execute("SELECT name, repository_url FROM packages"):
        if row["name"] in scanned_names or row["name"].replace("/", "__") in scanned_names:
            scanned_repo_urls.add(row["repository_url"])
    scanned_repos = len(scanned_repo_urls)

    no_workflows_file = Path("data/no_workflows.json")
    no_workflows_names = set(json.loads(no_workflows_file.read_text())) if no_workflows_file.exists() else set()
    no_wf_repo_urls = set()
    for row in db.execute("SELECT name, repository_url FROM packages"):
        if row["name"] in no_workflows_names:
            no_wf_repo_urls.add(row["repository_url"])
    no_workflows_repos = len(no_wf_repo_urls)

    repos_with_findings = db.execute("SELECT COUNT(DISTINCT repository_url) FROM findings").fetchone()[0]
    total_findings = db.execute("SELECT COUNT(*) FROM findings").fetchone()[0]

    out = []
    out.append(f"# Zizmor scan report: {registry}")
    out.append("")
    out.append(f"- Packages fetched from {registry}: {total_fetched}")
    out.append(f"  - No repo URL: {no_repo_count}")
    for host, count in sorted(host_counts.items(), key=lambda x: -x[1])[:10]:
        out.append(f"  - {host}: {count}")
    out.append(f"- Packages with GitHub repos: {total_packages} ({unique_repos} unique repos)")
    out.append(f"- Repos scanned: {scanned_repos}")
    out.append(f"- Repos without workflows: {no_workflows_repos} ({round(no_workflows_repos * 100 / scanned_repos, 1)}%)")
    out.append(f"- Repos with findings: {repos_with_findings} ({round(repos_with_findings * 100 / scanned_repos, 1)}%)")
    out.append(f"- Total findings: {total_findings}")
    for sev in ("High", "Medium", "Low", "Informational"):
        count = db.execute(
            "SELECT COUNT(DISTINCT repository_url) FROM findings WHERE severity = ?", (sev,)
        ).fetchone()[0]
        out.append(f"  - {sev}: {count} repos ({round(count * 100 / scanned_repos, 1)}%)")

    # shared repos
    out.append("")
    out.append("## Shared repositories")
    out.append("")
    rows = db.execute("""
        SELECT repository_url, COUNT(*) as pkgs
        FROM packages GROUP BY repository_url HAVING pkgs > 1 ORDER BY pkgs DESC
        LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Repository", "Packages"],
        [[r["repository_url"], r["pkgs"]] for r in rows],
        ["left", "right"],
    ))

    # by audit type
    out.append("")
    out.append("## Findings by audit type")
    out.append("")
    rows = db.execute("""
        SELECT audit,
            COUNT(DISTINCT repository_url) as repos,
            ROUND(COUNT(DISTINCT repository_url) * 100.0 / ?, 1) as pct,
            COUNT(*) as total,
            (SELECT severity FROM findings f2 WHERE f2.audit = f.audit
             GROUP BY severity ORDER BY COUNT(*) DESC LIMIT 1) as severity
        FROM findings f
        GROUP BY audit
        ORDER BY repos DESC
    """, (scanned_repos,)).fetchall()
    out.append(md_table(
        ["Audit", "Severity", "Repos", "% scanned", "Findings"],
        [[r["audit"], r["severity"], r["repos"], f"{r['pct']}%", r["total"]] for r in rows],
        ["left", "left", "right", "right", "right"],
    ))

    # by severity
    out.append("")
    out.append("## Findings by severity")
    out.append("")
    rows = db.execute("""
        SELECT severity,
            COUNT(DISTINCT repository_url) as repos,
            ROUND(COUNT(DISTINCT repository_url) * 100.0 / ?, 1) as pct,
            COUNT(*) as n
        FROM findings GROUP BY severity ORDER BY repos DESC
    """, (scanned_repos,)).fetchall()
    out.append(md_table(
        ["Severity", "Repos", "% scanned", "Findings"],
        [[r["severity"], r["repos"], f"{r['pct']}%", r["n"]] for r in rows],
        ["left", "right", "right", "right"],
    ))

    # top repos by audit variety
    out.append("")
    out.append("## Top 20 repos by distinct audit types")
    out.append("")
    rows = db.execute("""
        SELECT f.repository_url,
            COUNT(DISTINCT f.audit) as audits,
            COUNT(*) as n,
            (SELECT MAX(p.dependent_packages_count) FROM packages p
             WHERE p.repository_url = f.repository_url) as max_dependents
        FROM findings f
        GROUP BY f.repository_url
        ORDER BY audits DESC, n DESC
        LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Repository", "Audits", "Findings", "Max dependents"],
        [[r["repository_url"], r["audits"], r["n"], r["max_dependents"]] for r in rows],
        ["left", "right", "right", "right"],
    ))

    # high severity excluding unpinned-uses
    hs_filter = "WHERE severity = 'High' AND audit != 'unpinned-uses'"
    hs_repos = db.execute(f"SELECT COUNT(DISTINCT repository_url) FROM findings {hs_filter}").fetchone()[0]
    hs_total = db.execute(f"SELECT COUNT(*) FROM findings {hs_filter}").fetchone()[0]

    out.append("")
    out.append("## High severity (excluding unpinned-uses)")
    out.append("")
    out.append(f"{hs_total} findings across {hs_repos} repos ({round(hs_repos * 100 / scanned_repos, 1)}%)")
    out.append("")
    rows = db.execute(f"""
        SELECT audit, COUNT(DISTINCT repository_url) as repos, COUNT(*) as n
        FROM findings {hs_filter}
        GROUP BY audit ORDER BY repos DESC
    """).fetchall()
    out.append(md_table(
        ["Audit", "Repos", "Findings"],
        [[r["audit"], r["repos"], r["n"]] for r in rows],
        ["left", "right", "right"],
    ))

    out.append("")
    out.append("### Top 20 repos")
    out.append("")
    rows = db.execute(f"""
        SELECT f.repository_url,
            COUNT(DISTINCT f.audit) as audits,
            COUNT(*) as n,
            (SELECT MAX(p.dependent_packages_count) FROM packages p
             WHERE p.repository_url = f.repository_url) as max_dependents
        FROM findings f
        {hs_filter}
        GROUP BY f.repository_url
        ORDER BY audits DESC, n DESC
        LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Repository", "Audits", "Findings", "Max dependents"],
        [[r["repository_url"], r["audits"], r["n"], r["max_dependents"]] for r in rows],
        ["left", "right", "right", "right"],
    ))

    # zizscore
    out.append("")
    out.append("## Zizscore")
    out.append("")
    out.append("Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.")
    out.append("")
    rows = db.execute("""
        SELECT f.repository_url,
            SUM(
                CASE f.severity WHEN 'High' THEN 4 WHEN 'Medium' THEN 3 WHEN 'Low' THEN 2 ELSE 1 END
                * CASE f.confidence WHEN 'High' THEN 3 WHEN 'Medium' THEN 2 ELSE 1 END
            ) as zizscore,
            COUNT(DISTINCT f.audit) as audits,
            COUNT(*) as findings,
            (SELECT MAX(p.dependent_packages_count) FROM packages p
             WHERE p.repository_url = f.repository_url) as max_dependents
        FROM findings f
        GROUP BY f.repository_url
        ORDER BY zizscore DESC
        LIMIT 30
    """).fetchall()
    out.append(md_table(
        ["Repository", "Zizscore", "Audits", "Findings", "Max dependents"],
        [[r["repository_url"], r["zizscore"], r["audits"], r["findings"], r["max_dependents"]] for r in rows],
        ["left", "right", "right", "right", "right"],
    ))

    report = "\n".join(out) + "\n"
    report_path.write_text(report)
    print(f"Report written to {report_path}")

    db.close()


if __name__ == "__main__":
    main()
