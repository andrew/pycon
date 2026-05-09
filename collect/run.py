"""Run all scripts in sequence for a given registry."""

import subprocess
import sys


def main():
    args = sys.argv[1:]
    if not args:
        args = ["pypi.org"]

    scripts = [
        "main.py",
        "scan.py",
        "load_db.py",
        "report.py",
        "load_actions_db.py",
        "report_actions.py",
    ]

    for script in scripts:
        cmd = ["uv", "run", script] + args
        print(f"\n{'=' * 60}")
        print(f"Running: {' '.join(cmd)}")
        print(f"{'=' * 60}\n")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"\n{script} failed with exit code {result.returncode}")
            sys.exit(result.returncode)

    print("\nAll done.")


if __name__ == "__main__":
    main()
