"""Report on brief analysis data."""

import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

BRIEF_BASE = Path("data/brief")


def md_table(headers, rows, alignments=None):
    if alignments is None:
        alignments = ["left"] + ["right"] * (len(headers) - 1)
    sep = ["---:" if a == "right" else "---" for a in alignments]
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
    db_path = Path(f"data/{slug}.db")
    report_path = Path(f"data/report_brief_{slug}.md")
    brief_dir = BRIEF_BASE / registry.replace(".", "_")

    # get the set of repo URLs for this registry
    db = sqlite3.connect(db_path)
    pkg_repos = dict(db.execute("SELECT name, repository_url FROM packages").fetchall())
    db.close()
    registry_repo_urls = set(pkg_repos.values())

    # map brief files to repo URLs
    safe_to_repo = {name.replace("/", "__"): url for name, url in pkg_repos.items()}
    safe_to_repo.update(pkg_repos)

    briefs = []
    for brief_file in sorted(brief_dir.glob("*.json")):
        repo_url = safe_to_repo.get(brief_file.stem)
        if not repo_url or repo_url not in registry_repo_urls:
            continue
        data = json.loads(brief_file.read_text())
        briefs.append(data)

    total = len(briefs)

    out = []
    out.append(f"# Brief report: {registry}")
    out.append("")
    out.append(f"- Repos with brief data: {total}")

    # languages
    lang_counts = Counter()
    for b in briefs:
        for lang in b.get("languages") or []:
            lang_counts[lang["name"]] += 1

    out.append("")
    out.append("## Languages")
    out.append("")
    rows = [[name, count, pct(count, total)] for name, count in lang_counts.most_common(20)]
    out.append(md_table(["Language", "Repos", "% of total"], rows))

    # package managers
    pm_counts = Counter()
    for b in briefs:
        for pm in b.get("package_managers") or []:
            pm_counts[pm["name"]] += 1

    out.append("")
    out.append("## Package managers")
    out.append("")
    rows = [[name, count, pct(count, total)] for name, count in pm_counts.most_common(20)]
    out.append(md_table(["Package manager", "Repos", "% of total"], rows))

    # tools by category
    all_categories = set()
    for b in briefs:
        all_categories.update((b.get("tools") or {}).keys())

    for category in sorted(all_categories):
        tool_counts = Counter()
        for b in briefs:
            for tool in (b.get("tools") or {}).get(category) or []:
                tool_counts[tool["name"]] += 1

        cat_total = sum(1 for b in briefs if (b.get("tools") or {}).get(category))

        out.append("")
        out.append(f"## {category.replace('_', ' ').title()}")
        out.append("")
        out.append(f"{cat_total} repos ({pct(cat_total, total)})")
        out.append("")
        rows = [[name, count, pct(count, total)] for name, count in tool_counts.most_common(20)]
        out.append(md_table(["Tool", "Repos", "% of total"], rows))

    report = "\n".join(out) + "\n"
    report_path.write_text(report)
    print(f"Report written to {report_path}")


if __name__ == "__main__":
    main()
