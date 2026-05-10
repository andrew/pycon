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

# 1. Introduction

GitHub Actions as the dominant CI for Python
Trusted publishing implications

<!--
5 min.
-->

---

## GitHub Actions is the default CI for Python

- Free for public repos
- Where the code already lives
- **TODO%** of PyPI packages with a GitHub repo use it
- Travis, CircleCI, Azure Pipelines: single digits

<!--
Pull adoption % from actions_pypi_org.db.
Compare to Travis/CircleCI/Azure from brief data if available.
-->

---

## It's also how packages reach PyPI

- Tag → workflow runs → wheel built → `twine upload`
- `pypa/gh-action-pypi-publish` is the documented path
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
- This is good
- It's also a statement that PyPI trusts your workflow

<!--
The workflow's identity IS the credential.
-->

---

## The workflow is part of your supply chain

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

# 2. The problem

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

## What's missing

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

# 3. Methodology

ecosyste.ms dataset and zizmor scanning

<!--
3 min.
(zizmor itself already introduced in chapter 1)
-->

---

## The dataset

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

## What zizmor can and can't see

- YAML only
- Can't see repo settings: default token permissions, branch protection, environment reviewers
- A finding means "the YAML permits this"
- Not "this is exploitable today"

<!--
Sets up the precision caveats before the big numbers.
-->

---

<!-- _class: lead invert -->

# 4. Findings

Common misconfigurations across Python packages

<!--
8 min. The longest section.
-->

---

## Audit results across 150,274 packages

| audit | repos | |
|---|---:|---|
| `excessive-permissions` | 99,885 | no `permissions:` block |
| `unpinned-uses` | 83,751 | third-party action by tag |
| `use-trusted-publishing` | 43,758 | stored PyPI token |
| `template-injection` | 20,626 | `${{ }}` into `run:` |
| `cache-poisoning` | 14,280 | cache restore in privileged job |
| `dangerous-triggers` | 6,812 | `pull_request_target` etc. |

<!--
artipacked 114k and secrets-outside-env 64k omitted to fit.
91% of packages using any third-party action have one unpinned.
-->

---

## Each audit maps to a real incident

| incident | audit | repos exposed |
|---|---|---:|
| Trivy, tj-actions | `unpinned-uses` | 83,751 |
| spotbugs | `dangerous-triggers` | 6,812 |
| Ultralytics | `cache-poisoning` | 14,280 |
| elementary-data | `template-injection` | 20,626 |

<!--
403 PyPI packages still use trivy-action by tag a month after.
336 still use tj-actions/changed-files by tag a year on.
-->

---

## Case study: elementary-data

```yaml
on:
  issue_comment:
    types: [created]
jobs:
  handle_comment:
    steps:
      - run: echo "Comment Body: ${{ github.event.comment.body }}"
```

- 24 April: comment from a 2-day-old account
- `curl | bash` payload, write-scoped `GITHUB_TOKEN`
- Pushed commit, dispatched release workflow
- Malicious `0.23.3` on PyPI in 10 minutes

<!--
.pth payload exfiltrated SSH keys, cloud creds, kube configs.
StepSecurity post-mortem is public.
-->

---

## We scanned it two weeks before the attack

![](images/elementary-zizmor.png)

Any one of these would have stopped it:

- `template-injection`: the comment body in `run:`
- `excessive-permissions`: no `permissions:` block
- `use-trusted-publishing`: stored PyPI token

<!--
TODO: screenshot of the actual finding with the line highlighted.
203 findings total against elementary-data's workflows.
-->

---

## How many more look like elementary-data

| | |
|---|---:|
| attacker-controlled `${{ }}` in `run:` | 1,396 |
| trigger is `issues` / `issue_comment` | 99 |
| also publish with stored PyPI token | 12 |
| injection job has write-scoped token | **10** |

Biggest: sqlglot, 11.6M downloads/month. Disclosed.

<!--
1,396 -> 99: most are head_ref on pull_request, no secrets.
99 -> 12: 64 don't publish from CI, 17 use OIDC.
-->

---

## A false positive, for honesty

```yaml
if: contains(fromJSON('["/pandas_nightly","/mypy_nightly"]'),
             github.event.comment.body)
steps:
  - run: echo "${{ github.event.comment.body }}"
```

pandas-stubs: body must exactly match one of two strings before the interpolation is reached. zizmor can't reason about the `if:`.

<!--
Cut this if running long.
-->

---

## Third-party actions in publish jobs

| action | publish jobs | unpinned |
|---|---:|---:|
| `astral-sh/setup-uv` | 3,454 | 92% |
| `softprops/action-gh-release` | 2,306 | |
| `salsify/action-detect-and-tag-new-version` | 260 | 100% |

A tag-hijack on any of these runs with the publish credential.

<!--
Same job as pypa/gh-action-pypi-publish.
TODO: top 10 from slice_actions_in_publish_job.tsv
-->

---

## 43,758 packages on stored PyPI tokens

| | downloads/month |
|---|---:|
| six | 896M |
| fsspec | 616M |
| annotated-types | 552M |
| pyasn1 | 430M |
| sqlalchemy | 335M |

The credential that makes most of the above worth exploiting.

<!--
Bridge into chapter 5 and hardening.
-->

---

<!-- _class: lead invert -->

# 5. pip's security model

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

## GitHub is catching up

2026 security roadmap:

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

# 6. Practical hardening

Checklist and zizmor integration

<!--
5 min.
-->

---

## The checklist

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

## Trusted publishing, properly

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

## What clean looks like

- `requests`, `pytest`, `stamina`, `flask`, `django`, `boto3`: zero findings
- It's achievable
- Copy their release workflows

<!--
Point at one of their workflow files on screen.
-->

---

## Maintainers are responding

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
