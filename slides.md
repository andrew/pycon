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
- Actions adoption % across PyPI packages with public repos
- Trusted publishing: PyPI accepts OIDC tokens minted by Actions
- The workflow that builds the wheel is part of the supply chain
- If the workflow is compromised before signing, attestations sign the wrong thing
-->

---

<!-- _class: lead invert -->

# 2. The problem

Actions as a package manager without security features

<!--
5 min.
- uses: is a dependency declaration
- No lockfile, mutable tags, invisible transitive deps, no signature verification
- 97% of workflows use actions from unverified creators (USENIX 2022)
- Five compromises in eighteen months: spotbugs, Ultralytics, tj-actions, Trivy, elementary-data
- nesbitt.io/2025/12/06/github-actions-package-manager.html
-->

---

<!-- _class: lead invert -->

# 3. Methodology

ecosyste.ms dataset and zizmor scanning

<!--
3 min.
- ecosyste.ms: every PyPI package with a public repo
- zizmor: static analyser for Actions security
- 150,274 packages, 6-11 April 2026, zizmor 1.23.1
- Findings + actions inventory into SQLite
- github.com/andrew/pycon
-->

---

<!-- _class: lead invert -->

# 4. Findings

Common misconfigurations across Python packages

<!--
8 min. The longest section.
- Audit breakdown table across 150,274 packages
- Map each audit back to a real incident
- elementary-data case study: it was in the dataset, three audits would have caught it
- The funnel: 150,274 → 1,396 → 99 → 12 → 10
- pandas-stubs false positive for honesty
- Concentration: third-party actions in publish jobs (setup-uv 3,454)
- 43,758 packages still on stored PyPI tokens
-->

---

<!-- _class: lead invert -->

# 5. What pip got right

Lockfiles, hashes, verification

<!--
4 min.
- pip vs Actions feature comparison
- Transitive resolution vs invisible composite action deps
- PEP 592 yanking, PEP 740 attestations, PEP 751 lockfiles
- GitHub's 2026 roadmap: workflow dependency locking is the lockfile, finally
-->

---

<!-- _class: lead invert -->

# 6. Practical hardening

Checklist and zizmor integration

<!--
5 min.
- Move to trusted publishing with an environment
- permissions: {} on every workflow
- Pin third-party actions to SHA
- Never ${{ }} into run:, pass through env:
- Keep the publish job minimal
- Run zizmor in CI
- Re-scan delta: critical set hardened 19-31% in three weeks after Trivy/elementary-data
-->

---

# Thanks

Andrew Nesbitt
_nesbitt.io · @andrewnez · ecosyste.ms_

Data + scan tooling: _github.com/andrew/pycon_
zizmor: _woodruffw.github.io/zizmor_
