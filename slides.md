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

<!--
Adoption stat: % of PyPI packages with a public GitHub repo
that have .github/workflows/. Pull from actions_pypi_org.db.
Compare to Travis/CircleCI/Azure if the brief data has it.
-->

---

## It's also how packages reach PyPI

<!--
Not just tests. The release workflow builds the wheel and uploads it.
Stat: % of packages that publish from Actions
(pypa/gh-action-pypi-publish or twine in a workflow).
-->

---

## Trusted publishing

<!--
PyPI accepts short-lived OIDC tokens minted by Actions instead of
stored API tokens. The workflow's identity (repo, filename, ref,
environment) IS the credential.
This is good. It's also a statement of trust in Actions.
-->

---

## The workflow is part of your supply chain

<!--
PEP 740 attestations, Sigstore, SLSA all verify "this artifact
came from this workflow". They don't verify the workflow itself
wasn't compromised first. Signing happens last; everything
upstream of it is in scope.
-->

---

## zizmor

<!--
Static analyser for GitHub Actions workflows by William Woodruff,
who is probably in this room (wave). Runs locally or in CI,
reads .github/workflows/, reports findings as named audits with
severity and confidence.
Show a quick terminal screenshot here so the audit names in the
rest of the talk aren't abstract.
Make clear: I didn't build this, I just pointed it at everything.
woodruffw.github.io/zizmor
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

<!--
uses: owner/repo@ref pulls and executes someone else's code.
That's `pip install`. Except ref is a git ref, not an immutable version.
-->

---

## What's missing

<!--
No lockfile. Mutable version tags. Invisible transitive deps
(composite actions resolve their own uses:). No signature
verification. No --require-hashes equivalent.
97% of workflows use actions from unverified creators (USENIX 2022).
-->

---

## Tags are mutable

<!--
@v4 is a git tag. The owner can move it. force-push it.
You re-run last week's green build and get different code.
This is the mechanism behind tj-actions and Trivy.
-->

---

## Transitive dependencies are invisible

<!--
Composite actions have their own uses: lines you never see.
Pin your direct dep to a SHA, its action.yml still pulls @main.
There's no resolver, no tree, no `pip freeze`.
reviewdog -> tj-actions/eslint-changed-files -> tj-actions/changed-files
went through exactly this.
-->

---

## Five compromises in eighteen months

<!--
spotbugs (Nov 2024), Ultralytics (Dec 2024), tj-actions/reviewdog
(Mar 2025), Trivy x2 (Mar 2026), elementary-data (Apr 2026).
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

<!--
ecosyste.ms gives every PyPI package with a linked public repo,
plus dependents and download counts for ranking.
150,274 packages with .github/workflows/.
-->

---

## Running zizmor at scale

<!--
Shallow clone, zizmor --format=json on .github/workflows/,
also extract every uses: line for the actions inventory.
6-11 April 2026, zizmor 1.23.1. Resumable.
Everything lands in SQLite. github.com/andrew/pycon.
-->

---

## What zizmor can and can't see

<!--
Static analysis of YAML only. Can't see: repo "Workflow permissions"
default toggle, whether a secret is environment-scoped, branch
protection rules, environment reviewers. Findings are "the YAML
permits this", not "this is exploitable today".
Sets up the honesty about precision in chapter 4.
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

<!--
The big table. Repos-with-at-least-one-finding per audit.
artipacked 114k, excessive-permissions 99k, unpinned-uses 83k,
use-trusted-publishing 43k, template-injection 20k,
cache-poisoning 14k, dangerous-triggers 6.8k.
-->

---

## Each audit maps to a real incident

<!--
Trivy/tj-actions -> unpinned-uses (83,751).
spotbugs -> dangerous-triggers (6,812).
Ultralytics -> cache-poisoning (14,280).
elementary-data -> template-injection (20,626).
These aren't hypothetical patterns.
-->

---

## Case study: elementary-data

<!--
Show the workflow YAML: issue_comment trigger,
echo "${{ github.event.comment.body }}".
Then the comment payload, then the chain: write-scoped token,
orphan commit, dispatch release workflow, 0.23.3 on PyPI in 10 min.
-->

---

## We scanned it two weeks before the attack

<!--
Screenshot of the zizmor finding with the line highlighted.
Three audits each would have stopped it: template-injection,
excessive-permissions, use-trusted-publishing.
-->

---

## How many more look like elementary-data

<!--
The funnel: 150,274 -> 1,396 attacker-controlled injection ->
99 on issues/issue_comment -> 12 with stored PyPI token ->
10 with write-scoped GITHUB_TOKEN.
Explain why each step drops.
Biggest in the 10: sqlglot, 11.6M/month. Disclosed.
-->

---

## A false positive, for honesty

<!--
pandas-stubs: issue_comment + comment.body interpolation, but the
if: condition requires exact match to one of two strings.
zizmor can't reason about the constraint.
Cut this if running long.
-->

---

## Third-party actions in publish jobs

<!--
Concentration risk. astral-sh/setup-uv in 3,454 publish jobs,
92% unpinned. softprops/action-gh-release in 2,306.
A tag-hijack on any of these runs with the publish credentials.
-->

---

## 43,758 packages on stored PyPI tokens

<!--
six 896M, fsspec 616M, annotated-types 552M, sqlalchemy 335M.
The credential that makes most of the above worth exploiting.
This is the bridge into "what pip got right" and then hardening.
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

<!--
requirements.txt with --require-hashes, uv.lock, PEP 751.
The whole point: what you resolved yesterday is what you install
tomorrow. Actions has nothing equivalent; @v4 today is not @v4
next week.
-->

---

## Hash verification

<!--
pip --require-hashes refuses anything that doesn't match.
Actions: a SHA pin is the closest you get, and it's manual,
per-reference, and doesn't cover transitive.
-->

---

## Yanking and recall

<!--
PEP 592: a maintainer can yank a bad release and resolvers stop
picking it. Actions: a hijacked tag stays hijacked until someone
notices and force-pushes it back. tj-actions tags were malicious
for hours.
-->

---

## GitHub is catching up

<!--
2026 roadmap: workflow dependency locking with transitive SHAs,
policy controls on triggers, scoped secrets, egress firewall.
The lockfile feature is pip circa 2013. Better late.
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

<!--
One slide, six items, each maps to an audit and an incident:
1. Trusted publishing with an environment
2. permissions: {} on every workflow
3. Pin third-party actions to SHA
4. Never ${{ }} into run:
5. Keep the publish job minimal
6. Run zizmor in CI
-->

---

## Trusted publishing, properly

<!--
The one item worth its own slide. OIDC removes the credential;
the environment with required reviewers stops the dispatch pivot.
Show the YAML.
-->

---

## Adding zizmor to CI

<!--
The promised "how to integrate" bullet.
zizmorcore/zizmor-action in a pull_request workflow.
Show the YAML, show what a failing check looks like in a PR.
-->

---

## What clean looks like

<!--
stamina, pytest, requests all scan with zero findings.
It's achievable. Point at one of their workflow files.
-->

---

## Maintainers are responding

<!--
The re-scan delta: PyPI critical set, three data points
(6-11 Apr, 28 Apr, 9 May). unpinned-uses -19%,
excessive-permissions -31% after Trivy and elementary-data.
End on the upward note.
-->

---

# Thanks

Andrew Nesbitt
_nesbitt.io · @andrewnez · ecosyste.ms_

Data + scan tooling: _github.com/andrew/pycon_
zizmor: _woodruffw.github.io/zizmor_
