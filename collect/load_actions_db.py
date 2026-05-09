import json
import sqlite3
import sys
from pathlib import Path

ACTIONS_BASE = Path("data/actions")


def create_tables(db: sqlite3.Connection):
    db.executescript("""
        CREATE TABLE IF NOT EXISTS repos (
            name TEXT PRIMARY KEY,
            repository_url TEXT,
            downloads INTEGER,
            dependent_packages_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS action_uses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repo_name TEXT REFERENCES repos(name),
            workflow TEXT,
            job TEXT,
            level TEXT,
            action TEXT,
            ref TEXT,
            pinned BOOLEAN,
            type TEXT
        );

        CREATE TABLE IF NOT EXISTS actions (
            action TEXT PRIMARY KEY,
            total_uses INTEGER,
            repo_count INTEGER,
            pinned_count INTEGER,
            unpinned_count INTEGER
        );

        CREATE INDEX IF NOT EXISTS idx_action_uses_repo ON action_uses(repo_name);
        CREATE INDEX IF NOT EXISTS idx_action_uses_action ON action_uses(action);
        CREATE INDEX IF NOT EXISTS idx_action_uses_ref ON action_uses(ref);
    """)


def load_repos(db: sqlite3.Connection, pages_dir: Path):
    seen = set()
    for page_file in sorted(pages_dir.glob("page_*.json")):
        packages = json.loads(page_file.read_text())
        rows = []
        for pkg in packages:
            name = pkg["name"]
            if name in seen:
                continue
            seen.add(name)
            repo_url = pkg.get("repository_url") or ""
            if "github.com" not in repo_url:
                continue
            rows.append((name, repo_url,
                         pkg.get("downloads", 0),
                         pkg.get("dependent_packages_count", 0)))
        db.executemany("INSERT OR REPLACE INTO repos VALUES (?, ?, ?, ?)", rows)


def load_action_uses(db: sqlite3.Connection, actions_dir: Path):
    count = 0
    loaded_repos = set()
    repo_lookup = dict(db.execute("SELECT name, repository_url FROM repos").fetchall())
    safe_lookup = {name.replace("/", "__"): url for name, url in repo_lookup.items()}
    safe_lookup.update(repo_lookup)

    for actions_file in sorted(actions_dir.glob("*.json")):
        name = actions_file.stem
        repo_url = safe_lookup.get(name)
        if not repo_url:
            continue
        if repo_url in loaded_repos:
            continue
        loaded_repos.add(repo_url)

        actions = json.loads(actions_file.read_text())
        for a in actions:
            db.execute(
                "INSERT INTO action_uses (repo_name, workflow, job, level, action, ref, pinned, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, a["workflow"], a["job"], a["level"],
                 a["action"], a["ref"], a["pinned"], a["type"]),
            )
            count += 1
    return count


def build_actions_summary(db: sqlite3.Connection):
    db.execute("DELETE FROM actions")
    db.execute("""
        INSERT INTO actions (action, total_uses, repo_count, pinned_count, unpinned_count)
        SELECT action,
            COUNT(*) as total_uses,
            COUNT(DISTINCT repo_name) as repo_count,
            SUM(CASE WHEN pinned THEN 1 ELSE 0 END) as pinned_count,
            SUM(CASE WHEN NOT pinned THEN 1 ELSE 0 END) as unpinned_count
        FROM action_uses
        WHERE type = 'repository'
        GROUP BY action
    """)


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    pages_dir = Path(f"data/pages/{slug}")
    db_path = Path(f"data/actions_{slug}.db")
    actions_dir = ACTIONS_BASE / registry.replace(".", "_")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    db = sqlite3.connect(db_path)
    create_tables(db)

    print("Loading repos...")
    load_repos(db, pages_dir)

    print("Loading action uses...")
    count = load_action_uses(db, actions_dir)

    print("Building actions summary...")
    build_actions_summary(db)

    db.commit()

    repo_count = db.execute("SELECT COUNT(DISTINCT repo_name) FROM action_uses").fetchone()[0]
    action_count = db.execute("SELECT COUNT(*) FROM actions").fetchone()[0]

    print(f"\n{count} action uses across {repo_count} repos")
    print(f"{action_count} unique actions")

    print("\nTop 20 actions by repo count:")
    for row in db.execute("SELECT action, repo_count, total_uses, pinned_count, unpinned_count FROM actions ORDER BY repo_count DESC LIMIT 20"):
        pct = round(row[3] * 100 / row[2], 1) if row[2] else 0
        print(f"  {row[0]}: {row[1]} repos, {row[2]} uses ({pct}% pinned)")

    print("\nTop 20 unpinned actions by repo count:")
    for row in db.execute("SELECT action, repo_count, unpinned_count FROM actions WHERE unpinned_count > 0 ORDER BY repo_count DESC LIMIT 20"):
        print(f"  {row[0]}: {row[1]} repos, {row[2]} unpinned uses")

    print("\nRef diversity (top 20 actions by distinct refs):")
    for row in db.execute("""
        SELECT action, COUNT(DISTINCT ref) as refs, COUNT(DISTINCT repo_name) as repos
        FROM action_uses WHERE type = 'repository' AND ref != ''
        GROUP BY action ORDER BY refs DESC LIMIT 20
    """):
        print(f"  {row[0]}: {row[1]} distinct refs across {row[2]} repos")

    db.close()
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"\nDatabase saved to {db_path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
