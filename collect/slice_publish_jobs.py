"""Third-party actions running in jobs that also run pypa/gh-action-pypi-publish.

A tag-hijack on any of these runs with the publish credentials. Writes
data/slice_actions_in_publish_job.tsv.
"""

import sqlite3
from collections import defaultdict
from pathlib import Path


def main():
    db = sqlite3.connect("data/actions_pypi_org.db")
    keys = {(r, w, j) for r, w, j in db.execute(
        "SELECT DISTINCT repo_name, workflow, job FROM action_uses "
        "WHERE action='pypa/gh-action-pypi-publish'"
    )}

    repos = defaultdict(set)
    pinned = defaultdict(int)
    unpinned = defaultdict(int)

    for r, w, j, action, pin in db.execute(
        "SELECT repo_name, workflow, job, action, pinned FROM action_uses "
        "WHERE action != 'pypa/gh-action-pypi-publish' "
        "AND action NOT LIKE 'actions/%' AND action NOT LIKE 'github/%' "
        "AND action NOT LIKE './%' AND action NOT LIKE 'docker://%' "
        "AND instr(action, '/') > 0"
    ):
        if (r, w, j) not in keys:
            continue
        repos[action].add(r)
        if pin:
            pinned[action] += 1
        else:
            unpinned[action] += 1

    out = Path("data/slice_actions_in_publish_job.tsv")
    with out.open("w") as f:
        f.write("action\tpublish_repos\tunpinned_uses\tpinned_uses\n")
        for action, rs in sorted(repos.items(), key=lambda x: -len(x[1])):
            f.write(f"{action}\t{len(rs)}\t{unpinned[action]}\t{pinned[action]}\n")
    print(f"wrote {out} ({len(repos)} actions, {len(keys)} publish jobs)")


if __name__ == "__main__":
    main()
