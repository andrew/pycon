---
marp: true
theme: anthropic
paginate: true
class: lead
---

# GitHub Actions Security in Python Packages

Andrew Nesbitt
PyCon US 2026, Long Beach

---

## Andrew Nesbitt

- Package Manager Nerd
- Open Source Data Miner
- Software Anthropologist
- Dependency Graph Cartographer
- Critical Infrastructure Hobbyist

<!--
Not a security researcher by trade. I look at package ecosystems
as datasets: who depends on what, how things get published,
where the infrastructure is fragile.
-->

---

## nesbitt.io

- [GitHub Actions is a Package Manager](https://nesbitt.io/2025/12/06/github-actions-package-manager.html)
- [GitHub Actions is the Weakest Link](https://nesbitt.io/2026/04/28/github-actions-is-the-weakest-link.html)
- [How UV Got So Fast](https://nesbitt.io/2025/12/26/how-uv-got-so-fast.html)
- [The C-Shaped Hole in Package Management](https://nesbitt.io/2026/01/27/the-c-shaped-hole-in-package-management.html)
- [Package Managers Need to Cool Down](https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html)
- [If It Quacks Like a Package Manager](https://nesbitt.io/2026/03/08/if-it-quacks-like-a-package-manager.html)
- [Weekend at Bernie's](https://nesbitt.io/2026/05/08/weekend-at-bernies.html)

<!--
The first one is the seed of this talk.
The UV one is the one Python people have probably read.
-->

---

## ecosyste.ms

- 14 million packages
- 157 million versions
- 300 million repositories
- 400 million manifest files
- 24 billion dependency edges

Open data and APIs for every major package registry.

<!--
This is where the dataset for the talk comes from.
PyPI, npm, RubyGems, crates.io, Go, Maven, etc.
For each package: repo URL, CI config, dependents, download counts.
Makes "scan every PyPI package's workflows" a tractable query
rather than a crawling project.
TODO: refresh these numbers closer to the conference.
-->

---

<!-- _class: lead invert -->

# GitHub Actions

The dominant CI for Python
Trusted publishing implications

<!--
5 min.
-->

---

## GitHub Actions is the default CI for Python

- Free for public repos
- Where the code already lives
- 386,957 PyPI packages link a GitHub repo
- 152,318 have `.github/workflows/`
- Travis, CircleCI, Azure Pipelines: single-digit %

<!--
CI-system comparison is from brief data over a ~69k sample
(data/brief/pypi_org/, collected before --no-brief).
Report as percentages, not counts. report_brief.py for the breakdown.
-->

---

## Publishing from Actions

- Tag → workflow runs → wheel built → `twine upload`
- 56,490 repos use `pypa/gh-action-pypi-publish`
- ~22% via OIDC, 44,181 still on a stored `PYPI_API_TOKEN`
- The runner that builds your wheel has your publish credential

<!--
Stat: % of packages that publish from Actions
(pypa/gh-action-pypi-publish or twine in a workflow).
-->

---

## Trusted publishing

- No stored API token
- PyPI accepts a short-lived OIDC token from the workflow
- Identity = repo + workflow filename + environment
- PyPI now trusts the workflow itself

<!--
The workflow's identity IS the credential.
-->

---

## Signing happens after the workflow runs

- Attestations (PEP 740, Sigstore, SLSA) verify the artifact came from the workflow
- They don't verify the workflow wasn't compromised first
- Signing happens last
- Everything upstream of the upload step is in scope

<!--
If an attacker controls any step before signing,
the attestation signs the wrong thing.
-->

---

## zizmor

```
$ uvx zizmor .github/workflows/
```

- Static analyser for Actions workflows
- Named audits, severity + confidence
- Runs locally or in CI
- _woodruffw.github.io/zizmor_

![](images/zizmor-output.png)

<!--
By William Woodruff, who is probably in this room (wave).
I didn't build this, I just pointed it at everything.
TODO: terminal screenshot so audit names aren't abstract.
-->

---

<!-- _class: lead invert -->

# The problem

Actions as a package manager without security features

<!--
5 min.
nesbitt.io/2025/12/06/github-actions-package-manager.html
-->

---

## `uses:` is a dependency declaration

```yaml
- uses: actions/checkout@v4
- uses: astral-sh/setup-uv@v3
- uses: tj-actions/changed-files@v41
```

- Pulls someone else's code and executes it on your runner
- Functionally, that's `pip install`
- Except `@v41` is a git ref, not an immutable version

---

## Missing package-manager features

- No lockfile
- No hash verification
- No signature verification
- No transitive dependency resolution
- No yank / recall

<!--
97% of workflows use actions from unverified creators (USENIX 2022).
-->

---

## Tags are mutable

```
git tag -f v41 <malicious-sha>
git push -f origin v41
```

- Every workflow on `@v41` now runs the attacker's code
- Re-run last week's green build, get different code
- tj-actions, Trivy: exactly this

<!--
Trivy: 75 of 76 tags force-pushed in one go.
-->

---

## Transitive dependencies are invisible

```yaml
# your workflow, pinned
- uses: some/action@<sha>

# inside that action's action.yml
- uses: other/helper@main          # not pinned, you never see it
```

- No resolver, no tree, no `pip lock`
- reviewdog → tj-actions chain went through this

<!--
pip lock = PEP 751 lockfile generation. Seth Larson's suggestion
over pip freeze; better analogy because the point is the missing
lockfile, not the missing snapshot.
-->

---

## Six compromises in eighteen months

| | | |
|---|---|---|
| spotbugs | Nov 2024 | `pull_request_target` ran fork code |
| Ultralytics | Dec 2024 | cache poisoning → **PyPI** |
| tj-actions / reviewdog | Mar 2025 | tags force-pushed, 23k repos |
| Trivy ×2 | Mar 2026 | 75/76 tags force-pushed |
| elementary-data | Apr 2026 | template injection → **PyPI** |
| `@tanstack/*` | 11 May 2026 | cache poison + OIDC theft → **npm** |

<!--
Three put malicious wheels on PyPI or npm.
TanStack happened yesterday: bundle-size.yml pull_request_target
poisoned the pnpm cache, publish workflow restored it,
attacker code extracted id-token from runner memory and uploaded
42 packages / 84 versions. OIDC trusted publishing didn't help
because the attacker was already inside the workflow that had it.
-->

---

## TanStack, 11 May 2026

```
fork PR → bundle-size.yml runs fork code (pull_request_target)
       → fork code poisons pnpm store cache
publish workflow → restores poisoned cache
                → cached code dumps runner memory
                → extracts OIDC token, uploads 42 packages to npm
```

- Three audits chained: `dangerous-triggers`, `cache-poisoning`, and a runtime token extraction
- Trusted publishing didn't help: the attacker was inside the workflow that had `id-token: write`
- **1,348 PyPI repos** have the same `dangerous-triggers` + `cache-poisoning` shape

<!--
Yesterday's news as the audience walks in. The chain isn't npm-specific;
swap pnpm cache for pip/wheel cache and PyPI for npm and it's
identical. Argues for ALL the hardening rules, not just OIDC.
tanstack.com/blog/npm-supply-chain-compromise-postmortem
-->


---

<!-- _class: lead invert -->

# Methodology

ecosyste.ms dataset and zizmor scanning

<!--
3 min.
(zizmor itself already introduced in chapter 1)
-->

---

## PyPI packages with workflows

- Every PyPI package with a linked GitHub repo, via ecosyste.ms
- Dependents + download counts for ranking
- **152,318** packages with `.github/workflows/`
- ~20% of linked repos fail to clone: package still installable, source gone

<!--
A chunk of PyPI links to repos that are deleted, renamed, or private.
You can pip install it, you can't audit it. Separate talk in that.
-->

---

## Running zizmor at scale

- Shallow clone each repo
- `zizmor --format=json .github/workflows/`
- Also extract every `uses:` line for an actions inventory
- Everything into SQLite

_github.com/andrew/pycon_

<!--
9-11 May 2026, zizmor 1.24.1. Resumable.
-->

---

## Limits of static YAML analysis

- Workflow files only
- Repo settings are out of scope: default token permissions, branch protection, environment reviewers
- A finding means the YAML permits the pattern, not that it's exploitable today

<!--
Sets up the precision caveats before the big numbers.
-->

---

<!-- _class: lead invert -->

# Findings

Common misconfigurations across Python packages

<!--
8 min. One slide per audit: pattern, why it's exploitable,
PyPI repos affected, published CVEs of that class.
-->

---

## Six audits

| audit | PyPI repos | GHSA advisories |
|---|---:|---:|
| `excessive-permissions` | 102,235 | 6 |
| `unpinned-uses` | 85,774 | 4 |
| `use-trusted-publishing` | 44,181 | n/a |
| `template-injection` | 21,166 | **27** |
| `cache-poisoning` | 15,371 | 2 |
| `dangerous-triggers` | 7,025 | 8 |

_n = 152,318 · 49 advisories in GHSA ecosystem=actions, overlap allowed_

<!--
27/49 published advisories are injection. The 4 unpinned-uses are
the four real tag-hijack compromises: Trivy, xygeni, reviewdog,
tj-actions. bucket_cves.py regenerates this.
-->

---

## `excessive-permissions`

```yaml
on: push
jobs:
  build:                # no permissions: block
    steps: ...
```

- Without `permissions:`, the job inherits the repo default
- For repos created before Feb 2023 that's `contents: write`, `actions: write`, …
- Any compromised step can push commits and dispatch workflows
- **102,235** repos

<!--
This is the pivot, not the entry. Combine with any of the others
and the attacker owns the repo. Fix: permissions: {} at top of file.
-->

---

## `unpinned-uses`

```yaml
- uses: tj-actions/changed-files@v41
```

- `@v41` is a git tag; the owner (or attacker) can move it
- Next run executes whatever the tag now points at
- **85,774** repos use a third-party action by tag
- 4 published compromises: tj-actions, reviewdog, Trivy, xygeni

<!--
91% of repos that use any third-party action.
Trivy: 75/76 tags force-pushed. 403 PyPI packages still on it by tag.
Fix: pin to 40-char SHA. `zizmor --fix=all` rewrites tags to SHAs
in place (needs GH_TOKEN to resolve refs); say this out loud,
most people don't know there's a one-liner (Seth).
-->

---

## `template-injection`

```yaml
- run: echo "PR title: ${{ github.event.pull_request.title }}"
```

- `${{ }}` expands before bash sees the script
- Attacker-controlled fields (PR title, branch name, issue body) become shell
- **21,166** repos · **27** of 49 published Actions advisories

<!--
elementary-data (Apr 2026): comment.body on issue_comment trigger,
malicious wheel on PyPI in 10 min. We had it in the dataset.
1,396 repos interpolate something attacker-controlled; 99 on
issue/issue_comment triggers where secrets are always in scope.
Biggest in the chain-of-10: sqlglot, 11.6M/month, disclosed.
Other 9 still going through coordinated disclosure, unnamed on stage.
Fix: pass through env:, reference $VAR.
-->

---

## `use-trusted-publishing`

```yaml
- run: twine upload dist/*
  env:
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

- Long-lived token stored as a repo secret
- The credential that makes any of the other audits worth exploiting
- **44,181** repos still on tokens (~78% of `gh-action-pypi-publish` users)
- Including `six` (896M/mo), `fsspec` (616M), `sqlalchemy` (335M)

<!--
Fix: OIDC trusted publishing with an environment.
Caveat (Seth Larson): PyPI TP doesn't support reusable workflows yet,
so some packages have a legitimate excuse. Verified six, fsspec,
sqlalchemy do NOT publish via reusable workflows: plain twine + token,
fair to name. Separately, zizmor MISSES token-via-reusable-workflow
callers entirely (mistralai case, see zizmor_issue.md), so 44,181
is if anything an undercount.
This is the bridge into chapter 5 and hardening.
-->

---

## `cache-poisoning`

```yaml
- uses: actions/cache@v4      # in a release job
  with:
    key: pip-${{ hashFiles('requirements.txt') }}
```

- Cache is shared across workflows in a repo
- A low-privilege job writes a poisoned entry; the release job restores it
- **15,371** repos · 2 advisories

<!--
Ultralytics (Dec 2024): fork PR poisoned cache, release workflow
restored it, crypto miner shipped to PyPI.
TanStack (11 May 2026): pnpm store cache poisoned across PR boundary,
publish workflow restored it, cached code extracted OIDC from runner memory.
Fix: don't restore caches in jobs that publish.
-->

---

## `dangerous-triggers`

```yaml
on: pull_request_target
jobs:
  test:
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: pip install -e . && pytest
```

- `pull_request_target` runs in the base repo with secrets
- Checking out the PR head runs the fork's code with those secrets
- **7,025** repos · 8 advisories

<!--
spotbugs (Nov 2024) stole the maintainer's PAT.
PAT sat unused for four months, used in March 2025 to push
the reviewdog and tj-actions tag-hijack chain.
Ultralytics (Dec 2024) entry point.
TanStack (11 May 2026): bundle-size.yml pull_request_target ran fork code.
Fix: use pull_request, or never check out PR head under _target.
-->

---

## Most popular third-party actions

| action | PyPI repos | unpinned |
|---|---:|---:|
| `pypa/gh-action-pypi-publish` | 56,490 | 84.0% |
| `codecov/codecov-action` | 20,651 | 91.8% |
| `astral-sh/setup-uv` | 17,047 | 85.6% |
| `softprops/action-gh-release` | 9,327 | 91.3% |
| `pypa/cibuildwheel` | 2,650 | 91.7% |
| `actions/create-release` _(archived 2021)_ | 1,956 | 98.7% |

`archived-uses`: **3,625** repos depend on an archived action.

<!--
These are the dependencies of the Python ecosystem's CI.
actions/create-release is the Bernie: GitHub archived it five years
ago, ~2k PyPI repos still on it. upload-release-asset same story, 619.
Status data in data/top_action_repos_status.tsv.
-->

---

## Auditing pypa/cibuildwheel

```yaml
# action.yml (the visible tier)
runs:
  using: composite
  steps:
    - run: python -m cibuildwheel ${{ inputs.package-dir }}
```

- 2,650 PyPI publish workflows depend on it
- Self-audits with zizmor, one Low finding
- Fetches interpreters from **7 upstream hosts** at runtime, no hash pin
- The roadmap lockfile covers `uses:`; this tier stays invisible

<!--
Verbal framing: zizmor stops at the workflow YAML; what an action does
at runtime is a separate problem. cibuildwheel self-audits (issue #2770)
and is clean, but at runtime fetches CPython, PyPy, GraalPy, virtualenv,
Node.js, nuget, python-build-standalone from 7 hosts without hash pinning.
Slide trimmed for overflow (Seth); detail stays here for delivery.
scrutineer scan of cibuildwheel: chmod path traversal in extract_zip,
precondition-subsumed (the zip already gives RCE).
Other popular composites checked (gh-action-pypi-publish, codecov-action,
pre-commit, snok/install-poetry) pin or only use actions/*.
aio-libs/create-release is the counterexample, pulls aio-libs/get-releasenote@v1.4.5,
pypa/gh-action-pypi-publish@v1.5.0, ncipollo/release-action@v1.
TODO: run scrutineer on the rest of top_action_repos.txt.
-->

---

## Third-party actions in publish jobs

| action | repos | unpinned |
|---|---:|---:|
| `astral-sh/setup-uv` | 3,819 | 90.5% |
| `softprops/action-gh-release` | 2,448 | 93.7% |
| `python-semantic-release/python-semantic-release` | 451 | 87.0% |
| `snok/install-poetry` | 381 | 95.9% |
| `salsify/action-detect-and-tag-new-version` | 265 | 99.6% |

One tag-hijack here runs with PyPI credentials across thousands of packages.

<!--
Same job as pypa/gh-action-pypi-publish. 64,324 publish jobs total.
Worth a callout: step-security/harden-runner is in 144 publish jobs
at 2.4% unpinned, an order of magnitude better than everything else.
The audience that would benefit most from pinning is precisely the
one not running the kind of tool that would tell them so.
-->

---

<!-- _class: lead invert -->

# pip's security model

Lockfiles, hashes, verification

<!--
4 min.
-->

---

## Lockfiles

- `requirements.txt`, `uv.lock`, PEP 751
- What you resolved yesterday is what you install tomorrow
- Actions: `@v4` today ≠ `@v4` next week
- No equivalent

---

## Hash verification

```
pip install --require-hashes -r requirements.txt
```

- Refuses anything that doesn't match
- Actions: SHA pin is the closest, but manual, per-reference, no transitive

---

## Yanking and recall

- PEP 592: yank a bad release, resolvers stop picking it
- Actions: hijacked tag stays hijacked until someone force-pushes it back
- tj-actions tags were malicious for hours

---

## GitHub's 2026 roadmap

- Workflow dependency locking, transitive SHAs
- Policy controls on triggers (ban `pull_request_target`)
- Scoped secrets
- Egress firewall for runners

_Direction, not yet delivery. No committed ship dates as of writing._

<!--
The lockfile feature is pip circa 2013.
github.blog/.../github-actions-2026-security-roadmap/
-->

---

<!-- _class: lead invert -->

# Practical hardening

Checklist and zizmor integration

<!--
5 min.
-->

---

## Hardening checklist

1. Trusted publishing with an environment
2. `permissions: {}` on every workflow
3. Pin third-party actions to SHA: `zizmor --fix=all`
4. Never `${{ }}` into `run:`, pass through `env:`
5. Keep the publish job minimal
6. Run zizmor in CI

<!--
Each maps to an audit and an incident.
--fix=all rewrites @v41 → @<sha> # v41 in place. Needs GH_TOKEN.
The unpinned-uses fix is in the unsafe set, so plain --fix won't do it.
-->

---

## Trusted publishing with an environment

```yaml
jobs:
  pypi-publish:
    environment: release        # ← required reviewers here
    permissions:
      id-token: write
    steps:
      - uses: actions/download-artifact@v4
      - uses: pypa/gh-action-pypi-publish@release/v1
```

- OIDC removes the stealable credential
- The environment stops the dispatch pivot
- Bind the publisher on PyPI to the environment name

<!--
intercom-client showed id-token:write without environment is bypassable.
TanStack (11 May 2026) showed that even WITH the environment, an attacker
who gets code into the publish workflow (via cache poisoning here) can
mint the OIDC token from runner memory. The environment closes the
dispatch pivot, not runtime extraction. Rule 5 (minimal publish job)
is what closes that.
-->

---

## Adding zizmor to CI

```yaml
name: zizmor
on: [push, pull_request]
permissions: {}
jobs:
  zizmor:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: zizmorcore/zizmor-action@v0
```

Findings show up in the PR and the Security tab.

<!--
TODO: screenshot of a failing check on a PR.
-->

---

## Zero-finding examples

- `requests`, `pytest`, `stamina`, `flask`, `django`, `boto3`
- Their release workflows are good templates to copy

<!--
Point at one of their workflow files on screen.
-->

---

## Critical-set findings over time

| audit | 6-11 Apr | 28 Apr | 11 May |
|---|---:|---:|---:|
| unpinned-uses | 7,446 | 6,320 | 6,406 |
| artipacked | 2,755 | 2,337 | 2,376 |
| excessive-permissions | 2,186 | 1,887 | 1,900 |

PyPI critical set: ~15% drop in three weeks after Trivy and elementary-data, then flat.

<!--
Deduped by repo. apispec, awscli, babel went to zero entirely.
TODO: refresh with weekend full-scan numbers.
-->

---

# Thanks

Andrew Nesbitt
_nesbitt.io · @andrewnez · ecosyste.ms_

Data + scan tooling: _github.com/andrew/pycon_
zizmor: _woodruffw.github.io/zizmor_
