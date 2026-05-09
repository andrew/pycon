"""Rank packages by PyPI token-hygiene risk based on zizmor findings.

Packages that get taken over almost always had prior zizmor warnings around
secret handling, even when the actual attack was a stolen token rather than
workflow injection. This produces a "who's next" list.
"""

import sqlite3
import sys
from pathlib import Path

TOKEN_AUDITS = ("secrets-outside-env", "overprovisioned-secrets", "secrets-inherit")
OIDC_AUDITS = ("excessive-permissions", "artipacked")

# token findings are rarer and more specific to publish-credential exposure;
# oidc findings are near-universal so weight them down and cap them so
# monorepos with hundreds of workflows don't dominate
TOKEN_WEIGHT = 3
OIDC_WEIGHT = 1
OIDC_CAP = 20

KNOWN_COMPROMISED = {
    "ultralytics": "2024-12",
    "litellm": "2026-03",
    "elementary-data": "2026-04",
    "telnyx": "2026-04",
    "lightning": "2026-04",
    "pytorch-lightning": "2026-04",
    "intercom-client": "2026-04",
    "mbt": "2026-04",
    "@cap-js/db-service": "2026-04",
    "@cap-js/sqlite": "2026-04",
    "@cap-js/postgres": "2026-04",
}


def md_table(headers, rows, alignments=None):
    if alignments is None:
        alignments = ["left"] + ["right"] * (len(headers) - 1)
    sep = ["---:" if a == "right" else "---" for a in alignments]
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(sep) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(lines)


def fmt_int(n):
    return f"{n:,}"


def rank_repos(db):
    all_audits = TOKEN_AUDITS + OIDC_AUDITS
    audit_list = ",".join(f"'{a}'" for a in all_audits)
    cols = ",\n".join(f"SUM(audit = '{a}') AS {a.replace('-', '_')}" for a in all_audits)
    token_sum = " + ".join(a.replace("-", "_") for a in TOKEN_AUDITS)
    oidc_sum = " + ".join(a.replace("-", "_") for a in OIDC_AUDITS)
    sql = f"""
    WITH repo_findings AS (
      SELECT repository_url, {cols}
      FROM findings
      WHERE audit IN ({audit_list}) AND ignored = 0
      GROUP BY repository_url
    ),
    repo_pkg AS (
      SELECT repository_url,
        (SELECT name FROM packages p2 WHERE p2.repository_url = p.repository_url
         ORDER BY downloads DESC LIMIT 1) AS top_pkg,
        MAX(downloads) AS downloads,
        MAX(dependent_packages_count) AS deps,
        COUNT(*) AS pkgs_in_repo
      FROM packages p
      GROUP BY repository_url
    )
    SELECT rp.top_pkg, rp.repository_url, rp.downloads, rp.deps, rp.pkgs_in_repo,
           rf.*,
           ({token_sum}) AS token_findings,
           ({oidc_sum}) AS oidc_findings,
           ({TOKEN_WEIGHT} * ({token_sum}) + {OIDC_WEIGHT} * MIN({oidc_sum}, {OIDC_CAP}))
             * (1 + rp.downloads / 1000000.0) AS score
    FROM repo_findings rf
    JOIN repo_pkg rp ON rp.repository_url = rf.repository_url
    ORDER BY score DESC
    """
    return db.execute(sql).fetchall()


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    limit = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--limit=")), 50)
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    db_path = Path(f"data/{slug}.db")
    report_path = Path(f"data/report_token_risk_{slug}.md")

    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    ranked = rank_repos(db)

    total_repos = db.execute("SELECT COUNT(DISTINCT repository_url) FROM packages").fetchone()[0]
    flagged_repos = len(ranked)
    token_flagged = sum(1 for r in ranked if r["token_findings"] > 0)
    oidc_flagged = sum(1 for r in ranked if r["oidc_findings"] > 0)

    out = []
    out.append(f"# Token-hygiene risk: {registry}")
    out.append("")
    out.append(f"{flagged_repos} of {total_repos} repos flagged "
               f"({token_flagged} via token audits, {oidc_flagged} via oidc audits).")
    out.append("")
    out.append(f"Token audits (×{TOKEN_WEIGHT}): {', '.join(TOKEN_AUDITS)} — stored publish credentials exposed in workflows.")
    out.append("")
    out.append(f"OIDC audits (×{OIDC_WEIGHT}): {', '.join(OIDC_AUDITS)} — weak GitHub-side trust boundary; "
               f"relevant when publishing via trusted-publisher OIDC where there is no token to leak.")
    out.append("")
    out.append(f"Score = ({TOKEN_WEIGHT}×token + {OIDC_WEIGHT}×min(oidc, {OIDC_CAP})) × (1 + downloads/1M).")
    out.append("")

    headers = ["#", "package", "downloads", "deps",
               "out-env", "overprov", "inherit", "ex-perm", "artipack",
               "token", "oidc", "score", "hit"]
    rows = []
    for i, r in enumerate(ranked[:limit], 1):
        hit = KNOWN_COMPROMISED.get(r["top_pkg"], "")
        rows.append([
            i, r["top_pkg"], fmt_int(r["downloads"]), fmt_int(r["deps"]),
            r["secrets_outside_env"], r["overprovisioned_secrets"], r["secrets_inherit"],
            r["excessive_permissions"], r["artipacked"],
            r["token_findings"], r["oidc_findings"], round(r["score"], 1), hit,
        ])
    out.append(md_table(headers, rows, ["right", "left"] + ["right"] * 11))

    out.append("")
    out.append("## Known compromises in this dataset")
    out.append("")
    hit_rows = []
    for i, r in enumerate(ranked, 1):
        if r["top_pkg"] in KNOWN_COMPROMISED:
            tier = "token" if r["token_findings"] else ("oidc" if r["oidc_findings"] else "-")
            if r["token_findings"] and r["oidc_findings"]:
                tier = "both"
            hit_rows.append([i, r["top_pkg"], KNOWN_COMPROMISED[r["top_pkg"]],
                             r["token_findings"], r["oidc_findings"], tier,
                             fmt_int(r["downloads"]), round(r["score"], 1)])
    if hit_rows:
        out.append(md_table(["rank", "package", "compromised", "token", "oidc", "signal", "downloads", "score"],
                            hit_rows, ["right", "left", "left", "right", "right", "left", "right", "right"]))
        out.append("")
        out.append(f"{len(hit_rows)} of {len(KNOWN_COMPROMISED)} known compromises appear in the "
                   f"ranked list (out of {flagged_repos} flagged repos, top "
                   f"{round(max(r[0] for r in hit_rows) * 100 / flagged_repos, 2)}%).")
    else:
        out.append("None found in dataset.")

    report = "\n".join(out) + "\n"
    report_path.write_text(report)
    db.close()

    print(f"Report written to {report_path}")
    print()
    for row in rows[:20]:
        mark = f" <-- {row[12]}" if row[12] else ""
        print(f"{row[0]:>4}  {row[1]:<32} tok={row[9]:<4} oidc={row[10]:<4} {row[2]:>14} dl{mark}")
    print()
    for r in hit_rows:
        print(f"  compromised {r[2]}: {r[1]} ranked #{r[0]} (token={r[3]}, oidc={r[4]}, signal={r[5]})")


if __name__ == "__main__":
    main()
