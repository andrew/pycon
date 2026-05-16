---
marp: true
theme: anthropic
paginate: true
class: lead
---

# GitHub Actions Security in Python Packages

Andrew Nesbitt
PyCon US 2026, Long Beach

<!--
Hello.
What zizmor finds across PyPI, what to do about it.
-->

---

<!-- _class: lead invert -->

## Andrew Nesbitt

- Package Manager Nerd
- Open Source Data Miner
- Dependency Graph Cartographer
- Critical Infrastructure Hobbyist
- Poodle Farmer

<!--
First time speaking at a Python Conference
I normally write ruby and go, but today I'm going to talk about a rust program that analyses yaml config files for a CI written in C#
-->

---

![](images/dogs.gif)

<!--
Farming Poodles is one of my side gigs
-->


---

## [ecosyste.ms](https://ecosyste.ms)

- 14 million packages
- 157 million versions
- 300 million repositories
- 400 million manifest files
- 24 billion dependency edges

Open data and APIs for every major package registry.

<!--
ecosyste.ms is my open dataset and API for package metadata.
-->

---

## nesbitt.io - my blog

- [Package Managers Need to Cool Down](https://nesbitt.io/2026/03/04/package-managers-need-to-cool-down.html)
- [Sandwich Bill of Materials](https://nesbitt.io/2026/02/08/sandwich-bill-of-materials.html)
- [Incident Report: CVE-2024-YIKES](https://nesbitt.io/2026/02/03/incident-report-cve-2024-yikes.html)
- [If It Quacks Like a Package Manager](https://nesbitt.io/2026/03/08/if-it-quacks-like-a-package-manager.html)
- [How to Attract AI Bots to Your Open Source Project](https://nesbitt.io/2026/03/21/how-to-attract-ai-bots-to-your-open-source-project.html)
- [Weekend at Bernie's](https://nesbitt.io/2026/05/08/weekend-at-bernies.html)

---

## nesbitt.io - the relevant bits

- [GitHub Actions Has a Package Manager, and It Might Be the Worst](https://nesbitt.io/2025/12/06/github-actions-package-manager.html)
- [GitHub Actions is the Weakest Link](https://nesbitt.io/2026/04/28/github-actions-is-the-weakest-link.html)

---

<!-- _class: lead invert -->

# GitHub Actions

Let's talk about CI

<!--
Bridge. Establish GHA as the dominant Python CI before showing what's wrong with it.
-->

---

## GitHub Actions in PyPI

- 864,085 PyPI packages total
- 386,957 PyPI packages declare repository on GitHub
- 343,292 unique GitHub repositories
- 152,318 of those repositories have `.github/workflows/`
- Travis CI: 11%, others below 2%

<!--
Side note: Travis CI stopped providing free builds for open source in 2023, so it's basically dead.
-->

---

## Publishing to PyPI from GitHub Actions

- Tag → workflow runs → wheel built → `twine upload`
- 56,490 repos use `pypa/gh-action-pypi-publish`
- ~22% via OIDC, 44,181 still on a stored `PYPI_API_TOKEN`
- The runner that builds your wheel has your publish credential

<!--
Runner holds the publish credential.
Anything that influences the runner can publish.
56,490 = population the rest of the talk works against.
-->

---

## Trusted publishing

- No stored API token
- PyPI accepts a short-lived OIDC token from the workflow
- Identity = repo + workflow filename + environment
- PyPI now trusts the workflow itself
- [docs.pypi.org/trusted-publishers](https://docs.pypi.org/trusted-publishers)

<!--
The workflow's identity IS the credential.
-->

---

## Trusted publishing isn't enough

- Signing happens after the workflow runs
- Attestations (PEP 740, Sigstore, SLSA) verify the artifact came from the workflow
- They don't verify the workflow wasn't compromised first
- Signing happens last
- Everything upstream of the upload step is in scope

<!--
Attestation = signature on the artifact, not on the workflow.
Any compromised step before signing → attestation signs malicious wheel.
-->

---

<!-- _class: lead invert -->

# GitHub Actions is the Weakest Link

Let me list the ways

<!--
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

<!--
These look like dependency declarations because they are.
@v41 is a git ref the maintainer can move.
The tj-actions setup. Comes back in two slides.
-->

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

## Transitive dependencies are not pinned

```yaml
# your workflow, pinned
- uses: some/action@<sha>

# inside that action's action.yml
- uses: other/helper@main          # not pinned, you never see it
```

- No resolver, no tree, no `pip lock`
- reviewdog → tj-actions chain went through this

<!--
pip lock = PEP 751 lockfile generation.
Seth's suggestion over pip freeze.
The missing piece is the lockfile.
-->

---

## Nine compromises in eighteen months

| Project | Date | Compromise |
|---|---|---|
| spotbugs | Nov 2024 | `pull_request_target` ran fork code |
| Ultralytics | Dec 2024 | cache poisoning → **PyPI** |
| tj-actions / reviewdog | Mar 2025 | tags force-pushed, 23k repos |
| Trivy ×2 | Mar 2026 | 75/76 tags force-pushed, CI token harvested |
| LiteLLM | Mar 2026 | stolen PyPI token via Trivy chain → **PyPI** |
| Telnyx | Mar 2026 | stolen PyPI token via Trivy chain → **PyPI** |
| elementary-data | Apr 2026 | template injection → **PyPI** |
| lightning | Apr 2026 | stale long-lived token, no OIDC → **PyPI** |
| Mini Shai-Hulud | May 2026 | cache poison + OIDC theft → **PyPI** (mistralai, guardrails-ai) |

<!--
Six malicious wheels on PyPI in the last eight weeks.
TeamPCP chain: Trivy → LiteLLM → Telnyx. Poison CI tool, harvest its PyPI tokens, upload.
Lightning: counter-example. Long-lived token, no OIDC. Trusted publishing would have stopped it, GHA hardening wouldn't.
Mini Shai-Hulud: same chain as TanStack on npm, mistralai + guardrails-ai dropper on PyPI side.
Ultralytics next as the PyPI worked example.
-->

---

## Ultralytics, Dec 2024

```
fork PR → format.yml runs fork code (pull_request_target)
       → branch name interpolates into shell
       → poisons GitHub Actions cache
publish workflow → restores poisoned cache
                → wheel built with Crypto miner
                → uploaded to PyPI as 8.3.41, 8.3.42
phase 2 → stolen PYPI_TOKEN, direct upload of 8.3.45, 8.3.46
```

- `dangerous-triggers`, `template-injection`, `cache-poisoning`
- Template-injection bug reported and patched in August 2024, regression reintroduced ten days after the advisory
- **1,348 PyPI repos** have the same `dangerous-triggers` + `cache-poisoning`

<!--
Ultralytics ships YOLO. ~60M downloads/month at the time.
Phase 1: fork PR, crafted branch name, pull_request_target runs fork code with cache write, branch name interpolates into shell, build cache poisoned. Publish run restores it, miner in wheel, token uploads it.
Phase 2: token already stolen from phase 1 runner. Direct upload, two more versions.
Bug reported by Adnan Khan in August 2024. Regression 10 days post-patch.
blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis
-->


---

<!-- _class: lead invert -->

# How bad is it?

Using zizmor to find common misconfigurations

---

<!-- _class: lead invert -->

<style scoped>
section { text-align: center; }
</style>

# :rainbow: zizmor :rainbow:

---


## zizmor

```
$ uvx zizmor .github/workflows/
```

- Static analyser for Actions workflows
- Named audits, severity + confidence
- Runs locally or in CI
- _[zizmor.sh](https://zizmor.sh)_

![](images/zizmor-output.png)

<!--
By William Woodruff, who is probably in this room (wave).
I didn't build this, I just pointed it at everything.
-->

---

## PyPI packages with workflows

- Every PyPI package with a linked GitHub repo, via ecosyste.ms
- Dependents + download counts for ranking
- **152,318** packages with `.github/workflows/`
- ~20% of linked repos fail to clone: package still installable, source gone

<!--
A chunk of PyPI links to repos that are deleted, renamed, or private.
You can pip install. You can't read the source.
that's a whole separate talk
-->

---

## Running zizmor on everything

- Shallow clone each repo
- `zizmor --format=json .github/workflows/`
- Also extract every `uses:` line for an actions inventory
- Put everything into SQLite

_[github.com/andrew/pycon](https://github.com/andrew/pycon)_

<!--
9-11 May 2026, zizmor 1.24.1. Resumable.
-->

---

## Limits of static YAML analysis

- Workflow files only
- Each file considered seperately
- Repo settings are out of scope: default token permissions, branch protection, etc
- A finding means the YAML permits the pattern, not always exploitable

<!--
Precision caveats before the big numbers in the next chapter.
A finding means the YAML permits the pattern.
Exploitability depends on repo settings zizmor can't see.
-->

---

<!-- _class: lead invert -->

# Findings

Common misconfigurations across Python packages

<!--
One slide per audit.
Pattern, why it's exploitable, PyPI repos affected, published CVEs.
-->

---

## Six audits

| audit | PyPI repos | GHSA advisories |
|---|---:|---:|
| `excessive-permissions` | 102,235 | 6 |
| `unpinned-uses`* | 85,774 | 4 |
| `use-trusted-publishing` | 44,181 | n/a |
| `template-injection` | 21,166 | **27** |
| `cache-poisoning` | 15,371 | 2 |
| `dangerous-triggers` | 7,025 | 8 |

\* <small> _`unpinned-uses` only for third-party actions_ </small>

<!--
n = 152,318. 49 advisories in GHSA ecosystem=actions. Overlap allowed.
27/49 published advisories are injection.
The 4 unpinned-uses are the four real tag-hijack compromises:
Trivy, xygeni, reviewdog, tj-actions.
bucket_cves.py regenerates this.
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
- For repos created before Feb 2023: `contents: write`, `actions: write`, …
- Any compromised step can push commits and dispatch workflows
- **102,235** pypi repos have at least one workflow without `permissions: {}`

<!--
Used as the pivot step.
Combine with any other audit and the attacker owns the repo.
Fix: permissions: {} at top of file.
-->

---

## `unpinned-uses`

```yaml
- uses: tj-actions/changed-files@v41
```

- `@v41` is a git tag; the owner (or attacker) can move it
- Next run executes whatever the tag now points at
- **85,774** repos use a third-party action by tag
- **4** published compromises via this: tj-actions, reviewdog, Trivy, xygeni

<!--
91% of repos that use any third-party action.
Trivy: 75/76 tags force-pushed.
403 PyPI packages still on Trivy by tag.
Fix: pin to 40-char SHA.
zizmor --fix=all rewrites tags to SHAs in place. Needs GH_TOKEN.
Most people don't know there's a one-liner (Seth).
-->

---

## `template-injection`

```yaml
- run: echo "PR title: ${{ github.event.pull_request.title }}"
```

- `${{ }}` expands before bash sees the script
- Attacker-controlled fields (PR title, branch name, issue body) become shell
- **21,166** PyPI repositories interpolate attacker-controlled fields into `run:`
- **27** of 49 published Actions CVEs are template-injection

<!--
elementary-data (Apr 2026): comment.body on issue_comment trigger.
Malicious wheel on PyPI in 10 min. Was in the dataset.
1,396 repos interpolate attacker-controlled fields.
99 on issue/issue_comment triggers. Secrets always in scope.
Biggest in the chain-of-10: sqlglot, 11.6M/month, disclosed.
Other 9 still in coordinated disclosure. Don't name them.
Fix: pass through env:, reference $VAR.
-->

---

## `use-trusted-publishing`

```yaml
- run: twine upload dist/*
  env:
    TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

- Long-lived token stored in GitHub secrets
- The most valuable target for other vectors
- **44,181** repos still on tokens (~78% of `gh-action-pypi-publish` users)
- Including `six` (896M/mo), `fsspec` (616M), `sqlalchemy` (335M)

<!--
Fix: OIDC trusted publishing with an environment.
Caveat (Seth): PyPI TP doesn't support reusable workflows yet.
Some packages have a legitimate excuse.
six, fsspec, sqlalchemy verified: plain twine + token, fair to name.
zizmor misses token-via-reusable-workflow callers entirely.
mistralai case, see zizmor_issue.md.
44,181 is an undercount.
Bridge into chapter 5.
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
- **15,371** PyPI repositories use a cache action in a way that could get poisoned
- **2** public CVE advisories

<!--
Ultralytics (Dec 2024): fork PR poisoned cache, release workflow restored it.
Crypto miner shipped to PyPI.
TanStack (11 May 2026): pnpm store cache poisoned across PR boundary.
Publish workflow restored it. Cached code extracted OIDC from runner memory.
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
- **7,025** PyPI repositories use `pull_request_target`
- **8** public CVE advisories

<!--
spotbugs (Nov 2024): stole the maintainer's PAT.
PAT sat unused for 4 months.
Used Mar 2025 to push the reviewdog and tj-actions tag-hijack chain.
Ultralytics (Dec 2024): entry point.
TanStack (11 May 2026): bundle-size.yml pull_request_target ran fork code.
Fix: use pull_request, or never check out PR head under _target.
-->

---

## `archived-uses`

```yaml
- uses: actions/create-release@v1
```

- Uses an action that has been archived on GitHub, i.e. deprecated
- No future updates, no security patches
- Might break if the action's runtime changes (e.g. deprecates Node 16)
- Might break if GitHub changes the API the action relies on
- **3,625** PyPI repos depend on an archived `archived-uses`

---

## Most popular third-party actions

| action | PyPI repos | unpinned |
|---|---:|---:|
| `pypa/gh-action-pypi-publish` | 56,490 | 84.0% |
| `codecov/codecov-action` | 20,651 | 91.8% |
| `astral-sh/setup-uv` | 17,047 | 85.6% |
| `softprops/action-gh-release` | 9,327 | 91.3% |
| `pypa/cibuildwheel` | 2,650 | 91.7% |

<!--
These are the dependencies of the Python ecosystem's CI.
actions/create-release is the Bernie: GitHub archived it five years
ago, ~2k PyPI repos still on it. upload-release-asset same story, 619.
Status data in data/top_action_repos_status.tsv.
-->

---

## What goes on inside an action?

`pypa/cibuildwheel`

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
- Runtime fetches: CPython, PyPy, GraalPy, virtualenv, Node.js, nuget 

<!--
zizmor stops at the workflow YAML.
What an action does at runtime is a separate problem.
cibuildwheel self-audits via zizmor issue #2770. Clean.
python-build-standalone. 7 hosts. No hash pinning.
Other top composites pin or only use actions/* (gh-action-pypi-publish,
codecov-action, pre-commit, snok/install-poetry).
aio-libs/create-release is the counterexample.
Pulls aio-libs/get-releasenote@v1.4.5, pypa/gh-action-pypi-publish@v1.5.0,
ncipollo/release-action@v1.
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
step-security/harden-runner: 144 publish jobs, 2.4% unpinned.
An order of magnitude better than everything else in the table.
The audience that would benefit most from pinning is the one
without the tooling that would tell them.
-->

---

<!-- _class: lead invert -->

# GitHub's Actions 2026 Security Roadmap

Lockfiles, hashes, verification

<!--
GitHub's own response to all this.
Acknowledge it directly.
-->

---

![](images/roadmap.png)

---

## GitHub's Actions 2026 Security Roadmap

- Published March 2026
- Workflow dependency locking, transitive SHAs
- Policy controls on triggers (ban `pull_request_target`)
- Scoped secrets
- Egress firewall for runners
- 3-9 month timelines
- _No committed ship dates yet_

[github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/](https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/)

<!--
Roadmap = aspirations, not commitments.
Lockfile = the big one. Maps to "missing PM features" slide.
None of this helps you today.
-->

---

## What's missing?

- Malware detection
- Yanking and recalling
- CVE alerts
- Enforcement of policies

<!--
Things a real package manager has.
Even after roadmap ships, these gaps remain.
PyPI has yank, recall, malware checks. Actions has none.
-->

---

<!-- _class: lead invert -->

# Practical hardening

Checklist and zizmor integration

<!--
Six rules, then how to wire zizmor into CI.
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
- Bind the publisher on PyPI to the environment name

<!--
intercom-client: id-token:write without environment is bypassable.
TanStack (11 May 2026): even with the environment, code that lands
in the publish workflow can mint OIDC from runner memory.
Runtime extraction needs rule 5: minimal publish job.
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
zizmorcore/zizmor-action is the official wrapper.
SARIF upload to the Security tab needs security-events: write.
Runs on every PR. Fails the check by default.
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

PyPI critical set: ~15% drop in three weeks after Trivy and elementary-data security events.

<!--
Deduped by repo. apispec, awscli, babel went to zero entirely.
-->

---

# Take aways

- :foot: GitHub Actions is full of footguns
- :rainbow: Review your workflows with zizmor
- :detective: Be cautious of 3rd party actions
- :lock: Set up Trusted Publishing
- :fire: Kill `pull_request_target` with :fire:

<!--
Five things to do Monday.
Each maps back to an audit + incident from the talk.
-->

---

<!-- _class: lead invert -->

# Thanks

Andrew Nesbitt
_nesbitt.io · @andrewnez · ecosyste.ms_

Data + scan tooling: _[github.com/andrew/pycon](https://github.com/andrew/pycon)_

<!--
Thanks.
Code, data, scan scripts at github.com/andrew/pycon.
Questions.

-->

---

# :rainbow: Support zizmor :rainbow:

If you find zizmor useful, please consider supporting it:
- [Contributing.md](https://github.com/zizmorcore/zizmor/blob/main/CONTRIBUTING.md)
- [GitHub Sponsors](https://github.com/sponsors/woodruffw)
- [Thanks.dev](https://thanks.dev/u/gh/woodruffw)
- [ko-fi](https://ko-fi.com/woodruffw)

<!--
zizmor is one maintainer.
If the talk just saved your team an incident, fund the tool.
-->

---

![](images/dogs.gif)

<!--
Closing dog. Mirrors slide 3.
-->
