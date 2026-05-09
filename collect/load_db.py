import json
import sqlite3
import sys
from pathlib import Path

RESULTS_BASE = Path("data/zizmor_results")


def create_tables(db: sqlite3.Connection):
    db.executescript("""
        CREATE TABLE IF NOT EXISTS packages (
            name TEXT PRIMARY KEY,
            repository_url TEXT,
            dependent_packages_count INTEGER,
            dependent_repos_count INTEGER,
            downloads INTEGER,
            versions_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            repository_url TEXT,
            audit TEXT,
            description TEXT,
            url TEXT,
            confidence TEXT,
            severity TEXT,
            workflow_file TEXT,
            annotation TEXT,
            feature TEXT,
            ignored BOOLEAN
        );

        CREATE INDEX IF NOT EXISTS idx_findings_repo ON findings(repository_url);
        CREATE INDEX IF NOT EXISTS idx_findings_audit ON findings(audit);
        CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity);
        CREATE INDEX IF NOT EXISTS idx_packages_repo ON packages(repository_url);
    """)


def workflow_filename(locations: list[dict]) -> str:
    for loc in locations:
        key = loc.get("symbolic", {}).get("key", {})
        local = key.get("Local", {})
        given_path = local.get("given_path", "")
        if given_path:
            return Path(given_path).name
    return ""


def primary_feature(locations: list[dict]) -> tuple[str, str]:
    for loc in locations:
        sym = loc.get("symbolic", {})
        if sym.get("kind") == "Primary":
            annotation = sym.get("annotation", "")
            feature = loc.get("concrete", {}).get("feature", "")
            return annotation, feature
    if locations:
        sym = locations[0].get("symbolic", {})
        annotation = sym.get("annotation", "")
        feature = locations[0].get("concrete", {}).get("feature", "")
        return annotation, feature
    return "", ""


def load_packages(db: sqlite3.Connection, pages_dir: Path):
    page_files = sorted(pages_dir.glob("page_*.json")) if pages_dir.exists() else []
    seen = set()
    total = 0
    for page_file in page_files:
        packages = json.loads(page_file.read_text())
        total += len(packages)
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
                         pkg.get("dependent_packages_count", 0),
                         pkg.get("dependent_repos_count", 0),
                         pkg.get("downloads", 0),
                         pkg.get("versions_count", 0)))
        db.executemany("INSERT OR REPLACE INTO packages VALUES (?, ?, ?, ?, ?, ?)", rows)
    return total


def load_findings(db: sqlite3.Connection, results_dir: Path):
    # build a map of package name -> repo url from the packages table
    pkg_to_repo = dict(db.execute("SELECT name, repository_url FROM packages").fetchall())
    # also map safe names (slashes replaced with __) to repo urls
    safe_to_repo = {name.replace("/", "__"): url for name, url in pkg_to_repo.items()}
    safe_to_repo.update(pkg_to_repo)

    # only load findings once per unique repo
    loaded_repos = set()
    count = 0
    for result_file in sorted(results_dir.glob("*.json")):
        package_name = result_file.stem
        repo_url = safe_to_repo.get(package_name)
        if not repo_url:
            continue
        if repo_url in loaded_repos:
            continue
        loaded_repos.add(repo_url)

        findings = json.loads(result_file.read_text())
        for f in findings:
            dets = f.get("determinations", {})
            locs = f.get("locations", [])
            annotation, feature = primary_feature(locs)
            db.execute(
                "INSERT INTO findings (repository_url, audit, description, url, confidence, severity, workflow_file, annotation, feature, ignored) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (repo_url, f["ident"], f["desc"], f["url"],
                 dets.get("confidence"), dets.get("severity"),
                 workflow_filename(locs), annotation, feature,
                 f.get("ignored", False)),
            )
            count += 1
    return count


def main():
    registry = sys.argv[1] if len(sys.argv) > 1 else "pypi.org"
    critical = "--critical" in sys.argv
    slug = registry.replace(".", "_")
    if critical:
        slug += "_critical"
    pages_dir = Path(f"data/pages/{slug}")
    db_path = Path(f"data/{slug}.db")
    results_dir = RESULTS_BASE / registry.replace(".", "_")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    db = sqlite3.connect(db_path)
    create_tables(db)

    print("Loading packages...")
    total_on_pypi = load_packages(db, pages_dir)

    print("Loading zizmor findings...")
    count = load_findings(db, results_dir)

    db.commit()

    pkg_count = db.execute("SELECT COUNT(*) FROM packages").fetchone()[0]
    repo_count = db.execute("SELECT COUNT(DISTINCT repository_url) FROM packages").fetchone()[0]
    repos_with_findings = db.execute("SELECT COUNT(DISTINCT repository_url) FROM findings").fetchone()[0]

    print(f"\n{total_on_pypi} total packages fetched, {pkg_count} with GitHub repos ({repo_count} unique repos)")
    print(f"{count} findings across {repos_with_findings} repos")

    print("\nFindings by audit type:")
    for row in db.execute("SELECT audit, COUNT(*) as n FROM findings GROUP BY audit ORDER BY n DESC"):
        print(f"  {row[0]}: {row[1]}")

    print("\nFindings by severity:")
    for row in db.execute("SELECT severity, COUNT(*) as n FROM findings GROUP BY severity ORDER BY n DESC"):
        print(f"  {row[0]}: {row[1]}")

    db.close()
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"\nDatabase saved to {db_path} ({size_mb:.1f} MB, {pkg_count + count} rows)")


if __name__ == "__main__":
    main()
