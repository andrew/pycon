"""Fetch GitHub Actions advisories from GHSA and bucket by zizmor audit."""

import json
import re
import subprocess
from pathlib import Path

RAW = Path("data/ghsa_actions.json")

AUDITS = {
    "template-injection": [
        r"template.?injection", r"expression.?injection", r"script.?injection",
        r"shell.?injection", r"command.?injection", r"code.?injection",
        r"\$\{\{", r"arbitrary code execut", r"improper neutraliz",
        r"issue.?title", r"issue.?body", r"comment.?body", r"branch.?name",
        r"crafted.?filename", r"argument.?injection",
    ],
    "dangerous-triggers": [
        r"pull_request_target", r"workflow_run", r"fork.*secret",
        r"untrusted.*checkout", r"head\.sha", r"head\.ref",
        r"artifact.?poison", r"symlink.?attack",
    ],
    "unpinned-uses": [
        r"unpinned", r"mutable.?tag", r"tag.?hijack", r"tag.?poison",
        r"force.?push.*tag", r"malicious.?(version|release|tag|commit)",
        r"supply.?chain.*compromis", r"were compromised", r"briefly compromised",
    ],
    "cache-poisoning": [
        r"cache.?poison", r"actions/cache", r"poisoned.?cache",
        r"\bcache\b.*(secret|expose|leak)",
    ],
    "github-env": [
        r"GITHUB_ENV", r"GITHUB_PATH", r"environment.?file.?injection",
        r"set-env", r"::set-", r"runner command",
    ],
    "excessive-permissions": [
        r"GITHUB_TOKEN.*permission", r"permissions:.?write",
        r"overly.?permissive", r"excessive.?permission",
        r"\bPAT\b.*(leak|debug|artifact)", r"token.?leak",
    ],
    "artipacked": [
        r"artifact.*credential", r"persist-credentials", r"\.git/config.*token",
        r"arbitrary file write.*artifact", r"download-artifact",
    ],
    "bot-conditions": [
        r"actor.?spoof", r"dependabot.?spoof", r"github\.actor",
    ],
}

EXCLUDE = {
    "CVE-2023-50245",   # OpenEXR-viewer, mistagged ecosystem
}


def fetch():
    if RAW.exists():
        return json.loads(RAW.read_text())
    out = subprocess.run(
        ["gh", "api", "/advisories?ecosystem=actions&per_page=100", "--paginate"],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    RAW.write_text(json.dumps(data, indent=2))
    return data


def bucket(advisories):
    compiled = {a: [re.compile(p, re.I) for p in ps] for a, ps in AUDITS.items()}
    result = {a: [] for a in AUDITS}
    result["unbucketed"] = []
    for adv in advisories:
        ident = adv.get("cve_id") or adv["ghsa_id"]
        if ident in EXCLUDE:
            continue
        text = " ".join(str(adv.get(k) or "") for k in ("summary", "description"))
        matched = []
        for audit, patterns in compiled.items():
            if any(p.search(text) for p in patterns):
                matched.append(audit)
        if matched:
            for a in matched:
                result[a].append((ident, adv.get("severity"), adv["summary"]))
        else:
            result["unbucketed"].append((ident, adv.get("severity"), adv["summary"]))
    return result


def main():
    advisories = fetch()
    print(f"Fetched {len(advisories)} advisories from GHSA ecosystem=actions\n")
    buckets = bucket(advisories)

    print("# Summary (advisories may match multiple audits)\n")
    for audit in AUDITS:
        print(f"  {audit:<24} {len(buckets[audit]):>3}")
    print(f"  {'unbucketed':<24} {len(buckets['unbucketed']):>3}")
    print()

    for audit in list(AUDITS) + ["unbucketed"]:
        items = buckets[audit]
        print(f"## {audit} ({len(items)})")
        for ident, sev, summary in items:
            print(f"  {ident:<20} {sev or '':<10} {summary[:80]}")
        print()

    Path("data/cve_buckets.json").write_text(json.dumps(
        {a: [i[0] for i in v] for a, v in buckets.items()}, indent=2
    ))


if __name__ == "__main__":
    main()
