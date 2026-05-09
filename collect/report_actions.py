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


def pct(n, total):
    return f"{round(n * 100 / total, 1)}%" if total else "0%"


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    db_path = Path(f"data/actions_{slug}.db")
    report_path = Path(f"data/report_actions_{slug}.md")

    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row

    total_repos = db.execute("SELECT COUNT(DISTINCT repo_name) FROM action_uses").fetchone()[0]
    total_uses = db.execute("SELECT COUNT(*) FROM action_uses").fetchone()[0]
    unique_actions = db.execute("SELECT COUNT(*) FROM actions").fetchone()[0]
    unique_owners = db.execute("""
        SELECT COUNT(DISTINCT CASE
            WHEN INSTR(action, '/') > 0 THEN SUBSTR(action, 1, INSTR(action, '/') - 1)
            ELSE action END)
        FROM actions
    """).fetchone()[0]
    total_pinned = db.execute("SELECT SUM(pinned_count) FROM actions").fetchone()[0]
    total_unpinned = db.execute("SELECT SUM(unpinned_count) FROM actions").fetchone()[0]

    out = []
    out.append(f"# Actions report: {registry}")
    out.append("")
    out.append(f"- Repos with actions data: {total_repos}")
    out.append(f"- Total action uses: {total_uses}")
    out.append(f"- Unique actions: {unique_actions} ({unique_owners} unique owners)")
    out.append(f"- Pinned (SHA): {total_pinned} ({pct(total_pinned, total_pinned + total_unpinned)})")
    out.append(f"- Unpinned (tag/branch): {total_unpinned} ({pct(total_unpinned, total_pinned + total_unpinned)})")

    # uses by type
    out.append("")
    out.append("## Uses by type")
    out.append("")
    rows = db.execute("""
        SELECT type, COUNT(*) as n, COUNT(DISTINCT repo_name) as repos
        FROM action_uses GROUP BY type ORDER BY n DESC
    """).fetchall()
    out.append(md_table(
        ["Type", "Uses", "Repos"],
        [[r["type"], r["n"], r["repos"]] for r in rows],
        ["left", "right", "right"],
    ))

    # most popular actions
    out.append("")
    out.append("## Most used actions (top 30)")
    out.append("")
    rows = db.execute("""
        SELECT action, repo_count, total_uses, pinned_count, unpinned_count
        FROM actions ORDER BY repo_count DESC LIMIT 30
    """).fetchall()
    out.append(md_table(
        ["Action", "Repos", "Uses", "Pinned", "Unpinned", "% pinned"],
        [[r["action"], r["repo_count"], r["total_uses"], r["pinned_count"], r["unpinned_count"],
          pct(r["pinned_count"], r["total_uses"])] for r in rows],
        ["left", "right", "right", "right", "right", "right"],
    ))

    # most unpinned
    out.append("")
    out.append("## Most unpinned actions (top 20, by repo count)")
    out.append("")
    rows = db.execute("""
        SELECT action, repo_count, unpinned_count, total_uses,
            ROUND(unpinned_count * 100.0 / total_uses, 1) as unpinned_pct
        FROM actions WHERE unpinned_count > 0
        ORDER BY repo_count DESC LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Action", "Repos", "Unpinned", "Total", "% unpinned"],
        [[r["action"], r["repo_count"], r["unpinned_count"], r["total_uses"],
          f"{r['unpinned_pct']}%"] for r in rows],
        ["left", "right", "right", "right", "right"],
    ))

    # ref diversity
    out.append("")
    out.append("## Ref diversity (top 20)")
    out.append("")
    rows = db.execute("""
        SELECT action, COUNT(DISTINCT ref) as refs, COUNT(DISTINCT repo_name) as repos
        FROM action_uses WHERE type = 'repository' AND ref != ''
        GROUP BY action ORDER BY refs DESC LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Action", "Distinct refs", "Repos"],
        [[r["action"], r["refs"], r["repos"]] for r in rows],
        ["left", "right", "right"],
    ))

    # most popular refs per top actions
    out.append("")
    out.append("## Most common refs for top actions")
    out.append("")
    top_actions = db.execute("SELECT action FROM actions ORDER BY repo_count DESC LIMIT 10").fetchall()
    for action_row in top_actions:
        action = action_row["action"]
        out.append(f"### {action}")
        out.append("")
        rows = db.execute("""
            SELECT ref, pinned, COUNT(*) as uses, COUNT(DISTINCT repo_name) as repos
            FROM action_uses WHERE action = ? AND ref != ''
            GROUP BY ref ORDER BY repos DESC LIMIT 10
        """, (action,)).fetchall()
        out.append(md_table(
            ["Ref", "Pinned", "Uses", "Repos"],
            [[r["ref"], "yes" if r["pinned"] else "no", r["uses"], r["repos"]] for r in rows],
            ["left", "left", "right", "right"],
        ))
        out.append("")

    # github-owned vs third-party
    out.append("## GitHub-owned vs third-party")
    out.append("")
    gh_owned = db.execute("""
        SELECT COUNT(*) as uses, COUNT(DISTINCT repo_name) as repos
        FROM action_uses WHERE type = 'repository' AND action LIKE 'actions/%'
    """).fetchone()
    github_org = db.execute("""
        SELECT COUNT(*) as uses, COUNT(DISTINCT repo_name) as repos
        FROM action_uses WHERE type = 'repository' AND action LIKE 'github/%'
    """).fetchone()
    third_party = db.execute("""
        SELECT COUNT(*) as uses, COUNT(DISTINCT repo_name) as repos
        FROM action_uses WHERE type = 'repository'
            AND action NOT LIKE 'actions/%' AND action NOT LIKE 'github/%'
    """).fetchone()
    out.append(md_table(
        ["Owner", "Uses", "Repos"],
        [
            ["actions/*", gh_owned["uses"], gh_owned["repos"]],
            ["github/*", github_org["uses"], github_org["repos"]],
            ["Third-party", third_party["uses"], third_party["repos"]],
        ],
        ["left", "right", "right"],
    ))

    out.append("")
    out.append("## Top 20 owners by action count")
    out.append("")
    rows = db.execute("""
        SELECT CASE
            WHEN INSTR(action, '/') > 0 THEN SUBSTR(action, 1, INSTR(action, '/') - 1)
            ELSE action END as owner,
            COUNT(DISTINCT action) as actions,
            SUM(total_uses) as uses,
            SUM(repo_count) as repo_uses
        FROM actions
        GROUP BY owner
        ORDER BY actions DESC
        LIMIT 20
    """).fetchall()
    out.append(md_table(
        ["Owner", "Actions", "Uses", "Repo uses"],
        [[r["owner"], r["actions"], r["uses"], r["repo_uses"]] for r in rows],
        ["left", "right", "right", "right"],
    ))

    report = "\n".join(out) + "\n"
    report_path.write_text(report)
    print(f"Report written to {report_path}")

    db.close()


if __name__ == "__main__":
    main()
