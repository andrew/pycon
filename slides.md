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
- [How UV Got So Fast](https://nesbitt.io/2025/12/26/how-uv-got-so-fast.html)
- [The C-Shaped Hole in Package Management](https://nesbitt.io/2026/01/27/the-c-shaped-hole-in-package-management.html)
- [Package Managers Need to Cool Down](https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html)
- [If It Quacks Like a Package Manager](https://nesbitt.io/2026/03/08/if-it-quacks-like-a-package-manager.html)

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
- 362,899 PyPI packages link a GitHub repo
- 150,274 have `.github/workflows/`
- Travis, CircleCI, Azure Pipelines: single digits

<!--
CI-system comparison is from brief data over a ~69k sample
(data/brief/pypi_org/, collected before --no-brief).
Report as percentages, not counts. report_brief.py for the breakdown.
-->

---

## Publishing from Actions

- Tag → workflow runs → wheel built → `twine upload`
- 53,747 repos use `pypa/gh-action-pypi-publish`
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
- That's `pip install`
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

- No resolver, no tree, no `pip freeze`
- reviewdog → tj-actions chain went through this

---

## Five compromises in eighteen months

| | | |
|---|---|---|
| spotbugs | Nov 2024 | `pull_request_target` ran fork code |
| Ultralytics | Dec 2024 | cache poisoning → **PyPI** |
| tj-actions / reviewdog | Mar 2025 | tags force-pushed, 23k repos |
| Trivy ×2 | Mar 2026 | 75/76 tags force-pushed |
| elementary-data | Apr 2026 | template injection → **PyPI** |

<!--
Two of those put malicious wheels on PyPI.
This is the bridge into "so I went and looked".
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
- **150,274** packages with `.github/workflows/`
- **TODO%** of linked repos 404: package still installable, source gone

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
6-11 April 2026, zizmor 1.23.1. Resumable.
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
| `excessive-permissions` | 99,885 | 6 |
| `unpinned-uses` | 83,751 | 4 |
| `use-trusted-publishing` | 43,758 | n/a |
| `template-injection` | 20,626 | **27** |
| `cache-poisoning` | 14,280 | 2 |
| `dangerous-triggers` | 6,812 | 8 |

_n = 150,274 · 49 advisories in GHSA ecosystem=actions, overlap allowed_

<!--
27/49 published advisories are injection. The 4 unpinned-uses are
the four real tag-hijack compromises: Trivy, xygeni, reviewdog,
tj-actions. bucket_cves.py regenerates this.
-->

---

## `unpinned-uses`

```yaml
- uses: tj-actions/changed-files@v41
```

- `@v41` is a git tag; the owner (or attacker) can move it
- Next run executes whatever the tag now points at
- **83,751** repos use a third-party action by tag
- 4 published compromises: tj-actions, reviewdog, Trivy, xygeni

<!--
91% of repos that use any third-party action.
Trivy: 75/76 tags force-pushed. 403 PyPI packages still on it by tag.
Fix: pin to 40-char SHA.
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
- **99,885** repos

<!--
This is the pivot, not the entry. Combine with any of the others
and the attacker owns the repo. Fix: permissions: {} at top of file.
-->

---

## `template-injection`

```yaml
- run: echo "PR title: ${{ github.event.pull_request.title }}"
```

- `${{ }}` expands before bash sees the script
- Attacker-controlled fields (PR title, branch name, issue body) become shell
- **20,626** repos · **27** of 49 published Actions advisories

<!--
elementary-data (Apr 2026): comment.body on issue_comment trigger,
malicious wheel on PyPI in 10 min. We had it in the dataset.
1,396 repos interpolate something attacker-controlled; 99 on
issue/issue_comment triggers where secrets are always in scope.
Fix: pass through env:, reference $VAR.
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
- **6,812** repos · 8 advisories

<!--
spotbugs (Nov 2024) -> stolen PAT -> reviewdog -> tj-actions chain.
Ultralytics (Dec 2024) entry point.
Fix: use pull_request, or never check out PR head under _target.
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
- **14,280** repos · 2 advisories

<!--
Ultralytics (Dec 2024): fork PR poisoned cache, release workflow
restored it, crypto miner shipped to PyPI.
Fix: don't restore caches in jobs that publish.
-->

---

## `use-trusted-publishing`

```yaml
- run: twine upload dist/*
  env:
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

- Long-lived token stored as a repo secret
- Any of the above gives the attacker something worth taking
- **43,758** repos, including six (896M/mo), fsspec (616M), sqlalchemy (335M)

<!--
Fix: OIDC trusted publishing with an environment.
This is the bridge into chapter 5 and hardening.
-->

---

## Most popular third-party actions

| action | PyPI repos | unpinned |
|---|---:|---:|
| `pypa/gh-action-pypi-publish` | 53,747 | 84.3% |
| `codecov/codecov-action` | 20,182 | 92.7% |
| `astral-sh/setup-uv` | 15,468 | 87.8% |
| `softprops/action-gh-release` | 8,725 | 91.9% |
| `docker/login-action` | 4,751 | 85.5% |
| `pre-commit/action` | 3,561 | 88.2% |
| `pypa/cibuildwheel` | 2,569 | 93.3% |
| `snok/install-poetry` | 2,503 | 97.3% |

<!--
These are the dependencies of the Python ecosystem's CI.
-->

---

## Auditing the actions themselves

| action | zizmor findings | notable |
|---|---:|---|
| `codecov/codecov-action` | TODO | |
| `astral-sh/setup-uv` | TODO | |
| `softprops/action-gh-release` | TODO | |
| `pypa/cibuildwheel` | TODO | |

zizmor on each action repo's own `.github/workflows/`.

<!--
Run zizmor on each top-20 action's own .github/workflows/.
An excessive-permissions or template-injection in setup-uv's
release workflow is upstream of 3,454 PyPI publish jobs.
-->

---

## Transitive dependencies of popular actions

```yaml
# aio-libs/create-release/action.yml
runs:
  using: composite
  steps:
    - uses: aio-libs/get-releasenote@v1.4.5
    - uses: pypa/gh-action-pypi-publish@v1.5.0
    - uses: ncipollo/release-action@v1
```

- The popular composites mostly pin, or only pull `actions/*`
- The long tail has unpinned third-party `uses:` you can't see from your workflow

<!--
Top composites checked: gh-action-pypi-publish, codecov-action,
cibuildwheel, pre-commit, snok/install-poetry. All pin or only
use actions/*. aio-libs/create-release is the counterexample.
TODO: extend resolve_actions.py over more of the long tail.
-->

---

## Third-party actions in publish jobs

| action | repos | unpinned |
|---|---:|---:|
| `astral-sh/setup-uv` | 3,454 | 91.9% |
| `softprops/action-gh-release` | 2,306 | 93.4% |
| `python-semantic-release/python-semantic-release` | 437 | 90.1% |
| `snok/install-poetry` | 377 | 96.8% |
| `ncipollo/release-action` | 336 | 96.2% |
| `salsify/action-detect-and-tag-new-version` | 260 | 100% |

One tag-hijack here runs with PyPI credentials across thousands of packages.

<!--
Same job as pypa/gh-action-pypi-publish.
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
3. Pin third-party actions to SHA
4. Never `${{ }}` into `run:`, pass through `env:`
5. Keep the publish job minimal
6. Run zizmor in CI

<!--
Each maps to an audit and an incident.
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

| audit | 6-11 Apr | 28 Apr | 9 May |
|---|---:|---:|---:|
| unpinned-uses | 7,446 | 6,320 | 6,326 |
| artipacked | 2,755 | 2,337 | 2,329 |
| excessive-permissions | 2,186 | 1,887 | 1,873 |

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
