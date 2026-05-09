# GitHub Actions Security in Python Packages

## Metadata

- **Description word count:** ~200
- **Session type:** Talk - 30 Minutes
- **Track:** Talks
- **Category:** Trailblazing Python Security
- **Audience level:** Some experience

---

## Description

GitHub Actions is the dominant CI system for Python open source, used for testing and publishing including trusted publishing to PyPI via OIDC. That means the security properties of Actions directly affect the Python supply chain.

But Actions is a package manager without the security features we expect from package managers: no lockfiles, mutable version tags, implicit transitive dependencies. Prior research shows 97% of workflows use actions from unverified creators. If a workflow can be compromised before the package is signed, downstream protections don't help.

I scanned GitHub Actions workflows across thousands of Python packages on PyPI using zizmor, a static analysis tool for Actions security. I found unpinned third-party actions, overly permissive GITHUB_TOKEN scopes, artifact poisoning risks, and pull request vulnerabilities that could let attackers hijack releases.

This talk presents findings at ecosystem scale and explores what the Python community can learn from how we've solved similar problems in pip.

What we'll cover:

- Why GitHub Actions is a supply chain risk
- What's missing compared to pip, npm, and other package managers
- Findings from scanning Python package workflows at scale
- What we can learn from pip's security model
- A checklist for hardening Python package release workflows
- How to integrate zizmor into CI pipelines

---

## Outline

- Introduction: GitHub Actions as the dominant CI for Python, trusted publishing implications (5 min)
- The problem: Actions as a package manager without security features (5 min)
- Methodology: ecosyste.ms dataset and zizmor scanning (3 min)
- Findings: common misconfigurations across Python packages (8 min)
- What pip got right: lockfiles, hashes, verification (4 min)
- Practical hardening: checklist and zizmor integration (5 min)

### Revised structure (post-incident)

The elementary-data compromise on 24 April changes the shape of the talk. Instead of opening with "Actions is a package manager without package manager features" and building up to data, open with the incident and work backwards.

- Cold open: the elementary-data attack, told in 90 seconds. A GitHub comment, ten minutes later a malicious wheel on PyPI. Show the workflow YAML, show the comment, show the PyPI page. (3 min)
- We had already scanned this package. Show the zizmor finding with the exact line highlighted. Three separate audits each would have stopped it. (2 min)
- So how many more are sitting in the dataset? Walk the funnel: 150,274 → 1,396 → 99 → 12 → 10. Explain why each step drops: trigger semantics, permissions, publishing method. Show the pandas-stubs false positive to be honest about precision. (5 min)
- That's one attack pattern. There have been five major Actions compromises in eighteen months and each maps to a different audit. Trivy and tj-actions → unpinned-uses. Ultralytics → dangerous-triggers + cache-poisoning. spotbugs → dangerous-triggers. Show the audit-to-repo-count table. (4 min)
- Concentration risk. `astral-sh/setup-uv` runs in 3,454 PyPI publish jobs, 92% unpinned. One tag-hijack on that repo is a tj-actions for Python. Show the top-10 actions-in-publish-job table. (3 min)
- Why this keeps happening: Actions has no lockfile, mutable tags, invisible transitive deps. pip solved these problems years ago. GitHub's 2026 roadmap finally adds workflow dependency locking. (4 min)
- What you can do today. The hardening checklist, and adding zizmor to CI. (5 min)
- The 43,758 packages still on stored PyPI tokens, with six and sqlalchemy at the top. If the audience does one thing, it's moving to trusted publishing with an environment. (3 min)

29 minutes. Cuts if running long: drop the pip comparison to two sentences inside the "why this keeps happening" section, or drop the pandas-stubs false positive.

---

## Notes

I run ecosyste.ms, which indexes package metadata, repository data, and CI configurations across all major ecosystems. This gives me access to GitHub Actions workflows for the vast majority of PyPI packages with public repositories.

For this talk, I'm pairing the ecosyste.ms dataset with zizmor (https://woodruffw.github.io/zizmor/), a static analyser for GitHub Actions security.

I wrote about this topic recently: https://nesbitt.io/2025/12/06/github-actions-package-manager.html

I'll coordinate responsible disclosure for any significant findings before the conference. The goal is to present aggregate patterns and anonymised examples, not to name and shame.

I've spoken at FOSDEM, PackagingCon, Open Source Summit, and Ruby conferences. I'm co-organising the Package Management devroom at FOSDEM 2026.

---

## TODO

- [ ] Expand npm indexing beyond the critical subset so `report_token_risk.py` can validate the OIDC tier against intercom-client and the SAP CAP packages
- [ ] Fold the 29-30 April Mini Shai-Hulud chain into the incident section: SAP CAP → lightning (PyPI) → intercom-client (npm), same ~11 MB JS payload, cross-registry worm
- [ ] Add the intercom-client OIDC bypass to the trusted-publishing caveats: `id-token: write` on tag push with no environment protection, attacker pushed a tag and deleted the run
- [ ] Disclose to sqlglot now (11.6M/month, write-scoped injection), don't wait for the conference batch
- [ ] Disclose to airbyte-cdk and the rest of the 10 write-scoped issue_comment repos
- [ ] Hands-on verify the aio-libs `bot-conditions` auto-merge actually grants merge-without-review and whether the actor spoof works
- [ ] Re-scan the critical set once more closer to the conference, zizmor pinned to 1.24.1, for the "do incidents move the needle" closer
- [ ] Check for a zizmor 1.24.2 with the #1904 panic fix before the next full re-scan
- [ ] Separate the 1.23.1→1.24.1 delta from repo drift properly: extend workflows_export to all 456 critical repos and replay both versions
- [ ] Self-hosted runners on `pull_request`: needs `runs-on:` extraction from raw workflow YAML, not in zizmor output
- [ ] Transitive action dependency tree for the top 20 actions in publish jobs (`action.yml` → composite `uses:` → recurse)
- [ ] Propose a zizmor audit upstream for `id-token: write` without an `environment:` on the job — nothing currently flags it

---

## Research notes

### GitHub Actions 2026 security roadmap

https://github.blog/news-insights/product-news/whats-coming-to-our-github-actions-2026-security-roadmap/

GitHub announced a security roadmap that directly addresses several of the problems in this talk:

- **Workflow dependency locking**: A `dependencies:` section in workflow YAML that locks all direct and transitive dependencies with commit SHAs. Creates deterministic workflows and makes dependency updates visible as PR diffs. Public preview in 3-6 months.
- **Policy-driven workflow execution**: Central policies controlling who can trigger workflows and which events are permitted. Built on rulesets. Can prohibit `pull_request_target` entirely. 3-6 months.
- **Scoped secrets**: Secrets bound to specific repos, branches, environments, or trusted reusable workflows. Repository write access no longer grants secret management. 3-6 months.
- **Egress firewall for hosted runners**: Layer 7 firewall with monitor and enforce modes. Allowlists for domains, IP ranges, HTTP methods. 6-9 months.
- **Actions data stream**: Near real-time execution telemetry to S3 or Azure. 3-6 months preview, 6-9 months GA.

The dependency locking feature is essentially the lockfile solution from the blog post. Worth discussing in the talk as evidence that GitHub recognises these problems, and comparing the timeline against the data showing how widespread the issues are today.

### Case study: elementary-data

elementary-data is a dbt observability package on PyPI. It was in the scan dataset and zizmor reported 203 findings against its workflows. One of those findings was a High severity, High confidence template-injection in `update_pylon_issue.yml`, a workflow that syncs GitHub issue comments to a support ticketing system. The offending step:

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  handle_comment:
    runs-on: ubuntu-latest
    steps:
      - name: Extract Issue or Pull Request Details
        run: |
          echo "Comment Body: ${{ github.event.comment.body }}"
          ...
```

The `${{ }}` expansion happens before bash sees the script, so whatever a commenter types becomes part of the shell source. Anyone with a GitHub account can comment on a public issue.

On 24 April 2026 an account created two days earlier posted a comment on an old pull request. The comment body closed the `echo` string and appended a `curl | bash` stager. The job ran it with the repository's default `GITHUB_TOKEN`, which had write permissions because the workflow never declared a `permissions:` block. The stager used that token to push an orphan commit with a forged `github-actions[bot]` author, bump `pyproject.toml` to 0.23.3, drop a malicious `.pth` file into the package root, and call the API to dispatch the existing release workflow against the new tag. Ten minutes after the comment was posted, `elementary-data==0.23.3` was on PyPI and a matching multi-arch image was on GHCR. The `.pth` payload ran on interpreter startup and exfiltrated SSH keys, cloud credentials, Kubernetes configs, and wallet files to an attacker domain.

Three separate zizmor audits in our scan results map onto this attack chain, and fixing any one of them would have stopped it. `template-injection` flagged the comment body interpolation that gave the attacker code execution. `excessive-permissions` flagged the missing `permissions:` block that let the injected code write to the repo and dispatch workflows. `use-trusted-publishing` flagged the long-lived PyPI API token in the release job; with OIDC trusted publishing the forged dispatch from an orphan commit would have failed the publisher identity check.

The talk proposal says I'll present aggregate patterns and anonymised examples rather than naming projects. This one is now a public incident with a published post-mortem from StepSecurity, so it's fair to use by name. It's a clean demonstration that the findings in the dataset are exploitable in practice and that the static analysis would have caught it.

References: https://www.stepsecurity.io/blog/elementary-data-compromised-on-pypi-and-ghcr-forged-release-pushed-via-github-actions-script-injection

### Other packages with the same pattern

After the incident I went back to the dataset and filtered the template-injection findings down to expressions an outsider can control: issue and comment bodies, issue and PR titles, branch names, commit messages. Out of 150,274 packages scanned, 1,396 (0.93%) interpolate at least one of these into a `run:` block.

Most of those are branch names (`github.head_ref`, `github.event.pull_request.head.ref`, 1,073 findings combined) and PR titles (280). Those need the attacker to open a PR from a fork, and on the default `pull_request` trigger a forked PR runs without repository secrets, which limits the blast radius unless the workflow uses `pull_request_target`.

The narrower set is workflows that interpolate `github.event.comment.body`, `github.event.issue.title`, or `github.event.issue.body`. Those fire on `issues` or `issue_comment` events, which always run in the base repository's context with full secret access, and anyone with a GitHub account can trigger them. There are 99 packages in that set.

Of those 99, 18 also have a `use-trusted-publishing` finding, meaning they push to PyPI from CI using a stored API token rather than OIDC. That's the complete elementary-data chain: zero-barrier code execution in a job that has, or can pivot to, a PyPI credential. The list includes elementary-data itself plus a cluster of sqlglot forks that share the same upstream workflow.

The package list is in `collect/data/template_injection_attacker_controlled.tsv`, now joined with download counts and sorted. These need coordinated disclosure before the talk; they're live vulnerabilities in named projects.

Seth Larson asked the right follow-up: are these injections actually in workflows with write access or publishing credentials? I went back and checked the `permissions:` block on each of the 18 at the job level. After dropping a tutorial repo and deduplicating the sqlglot forks, 12 distinct repos remain. 10 of those 12 give the injected code a write-scoped `GITHUB_TOKEN`: 5 because the workflow has no `permissions:` block and the repo predates the Feb 2023 default change, 5 because the job explicitly declares `contents: write`. The remaining 2 (cdp-scrapers, bidsmreye) restrict the token to `issues: write`, which blocks the push-and-dispatch pivot, though repo-level secrets are still in scope because of how `issue_comment` triggers work.

The static analysis blind spots worth being honest about on stage: we can't see the repo's "Workflow permissions" default setting from YAML, so the 5 no-permissions-block cases are write-scoped only if the owner hasn't flipped that toggle. And we can't see whether a `PYPI_API_TOKEN` is a repo secret or an environment-scoped secret with protection rules. elementary-data is the existence proof that the defaults are still dangerous in practice.

The biggest single target in the verified-write set is sqlglot at ~11.6M monthly downloads across `sqlglot` and `sqlglotrs`, with 104 dependent packages. Disclosure to that project should happen now rather than in the conference batch.

Widening from the 99 zero-barrier cases to the full 1,396 with any attacker-controlled injection, the top of the download-sorted list includes networkx (244M/month, `pull_request.head.label`), pandas-stubs (86M, `comment.body` used as a JSON lookup key), sglang (50M, `head_ref`), and browser-use (7.4M, `head.ref`).

I checked the trigger type on each of these and they all wash out. networkx, sglang, browser-use, pystache, and Open3D use the plain `pull_request` trigger, where fork PRs run with no secrets and a read-capped token regardless of what `permissions:` declares. The attacker gets code execution on an empty runner. dash-bootstrap-components gates on `if: github.event.pull_request.merged`, so a maintainer has to merge a PR with a hostile branch name first. pandas-stubs does use `issue_comment`, but the job condition is `if: contains(fromJSON('["/pandas_nightly", "/mypy_nightly"]'), github.event.comment.body)`, which means the body must exactly match one of two strings before the interpolation is reached. zizmor flags it because it can't reason about the `if:` constraint. Worth showing as an honest false positive.

So the triage funnel for the talk is roughly: 150,274 packages scanned, 1,396 with attacker-controlled template injection, 99 where the trigger is `issues` or `issue_comment` so secrets are in scope by construction, 12 distinct repos that also publish to PyPI with a stored token, 10 where the injection job has a write-scoped `GITHUB_TOKEN`. The 1,396 number is the headline for "this pattern is everywhere", the 10 is the number for "and here's how many are one comment away from an elementary-data". The gap between them is mostly the `pull_request` trigger doing its job.

Splitting the 99 by how they publish: 18 use a stored PyPI token, 17 use OIDC trusted publishing via `pypa/gh-action-pypi-publish`, and 64 have no detectable CI publishing at all (manual releases, or the package is effectively abandoned).

The 17 OIDC packages are worth a separate point in the hardening section. Trusted publishing means there's no long-lived credential to steal, but it doesn't stop the elementary-data pivot on its own. If the injection job has `actions: write` and the publish workflow accepts `workflow_dispatch`, the attacker dispatches the real publish workflow from inside the repo, the workflow gets a valid OIDC token because the claims (repo, workflow filename) are correct, and PyPI accepts the upload. The defence is configuring an environment on the publish job with required reviewers or branch restrictions, and binding the trusted publisher on the PyPI side to that environment name.

The largest package in the OIDC set is airbyte-cdk at 1.1M monthly downloads and 266 dependents. Its `slash_command_dispatch.yml` interpolates `github.event.comment.body` into a bash `[[ ]]` test with no author check and no `permissions:` block. A multiline comment closes the conditional and continues as shell. The publish workflow accepts `workflow_dispatch` and does declare `environment:` on the publish job, so whether the pivot completes depends on whether that environment has protection rules configured, which we can't see from the YAML. Goes on the disclosure list either way.

### Recent incidents and the audits that catch them

elementary-data is one entry in a run of GitHub Actions compromises over the last eighteen months. Each one maps to a zizmor audit, and each audit gives a number for how many PyPI packages have the same exposure today.

**Trivy, March 2026.** An attacker force-pushed 75 of 76 version tags in `aquasecurity/trivy-action`, so any workflow referencing `@0.x.y` ran a credential stealer before the legitimate scan. This was the second compromise in three weeks; the first gave the attacker the credentials for the second. The defence is SHA pinning, which zizmor reports as `unpinned-uses`. 403 PyPI packages currently use `aquasecurity/trivy-action` and 460 of those uses are by tag, a month after the incident. 83,751 packages in the dataset have at least one unpinned third-party action; that's 91% of the packages that use third-party actions at all.

**tj-actions/changed-files and reviewdog/action-setup, March 2025.** Same mechanism: tags force-pushed to point at malicious commits. tj-actions was used by 23,000+ repos at the time, and the payload dumped runner memory to public workflow logs. The attack chain went reviewdog → tj-actions/eslint-changed-files → tj-actions/changed-files, which is the transitive action dependency problem in the next section. CVE-2025-30066 and CVE-2025-30154, with a CISA advisory. A year on, 336 PyPI packages still reference tj-actions/changed-files by tag.

**spotbugs, November 2024.** Where the tj-actions chain started. A `pull_request_target` workflow in spotbugs checked out and ran code from a fork PR with repository secrets in scope, which let the attacker steal a maintainer's PAT. That PAT had access to reviewdog. zizmor reports this pattern as `dangerous-triggers`: 6,812 PyPI package repos have at least one.

**Ultralytics, December 2024.** Also `pull_request_target`, but the escalation went through GitHub's action cache. The fork PR poisoned a cache entry, and the release workflow later restored it and ran the payload while building wheels. Two malicious releases of `ultralytics` reached PyPI with a crypto miner. zizmor's `cache-poisoning` audit covers the restore-side of this: 14,280 repos in the dataset.

**Codecov, April 2021.** The bash uploader script that `codecov/codecov-action` downloaded was modified at the source to exfiltrate environment variables. Different mechanism from tag hijacking but the same lesson about trusting third-party code in CI. `codecov/codecov-action` is currently the most-used non-first-party action in Python CI: 20,182 packages, 92.7% of uses unpinned.

The full audit breakdown across 150,274 packages, by distinct repos with at least one finding:

| audit | repos |
|---|---|
| unpinned-uses (third-party only) | 83,751 |
| artipacked | 114,247 |
| excessive-permissions | 99,885 |
| secrets-outside-env | 64,213 |
| use-trusted-publishing | 43,758 |
| template-injection | 20,626 |
| cache-poisoning | 14,280 |
| dangerous-triggers | 6,812 |
| bot-conditions | 873 |
| github-env | 375 |

References:
- https://thehackernews.com/2026/03/trivy-security-scanner-github-actions.html
- https://www.stepsecurity.io/blog/trivy-compromised-a-second-time---malicious-v0-69-4-release
- https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066
- https://www.wiz.io/blog/new-github-action-supply-chain-attack-reviewdog-action-setup
- https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-tj-actionschanged-files-cve-2025-30066-and-reviewdogaction
- https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/
- https://words.filippo.io/compromise-survey/

### Data slices

Each incident above suggests a query to run against the dataset. Results saved as TSVs in `collect/data/`.

`dangerous-triggers` ∩ stored PyPI token (`slice_dangerous_triggers_pypi_token.tsv`): 1,934 repos. The Ultralytics shape: a `pull_request_target` or `workflow_run` trigger in the same repo as a token-based PyPI publish. Top of the list by downloads: huggingface-hub (205M), the opentelemetry-python-contrib family (163M), flatbuffers (93M), tokenizers (81M), pygithub (73M), safetensors (68M). Caveat: `dangerous-triggers` fires on any use of these triggers, including safe label-only workflows that never check out fork code. Each one needs the same per-workflow verification we did for the template-injection set before it can be called exploitable.

Third-party actions running in the same job as `pypa/gh-action-pypi-publish` (`slice_actions_in_publish_job.tsv`): if one of these gets tag-hijacked, it runs with the publish job's credentials and can tamper with the wheel before upload. `astral-sh/setup-uv` is in 3,454 publish jobs with 92% of uses unpinned. `softprops/action-gh-release` is in 2,306. `salsify/action-detect-and-tag-new-version` is in 260 with zero pinned uses. The Trivy attack against any one of these is a mass PyPI compromise.

`bot-conditions` (`slice_bot_conditions.tsv`): 873 repos gate something on `github.actor == 'dependabot[bot]'` or similar, which zizmor flags as spoofable under certain re-run and event conditions. The aio-libs family (aiohttp 326M, multidict 414M, yarl 413M, frozenlist 358M, aiosignal 344M, propcache 365M) all share an `auto-merge.yml` with this check, as does hatchling (287M). I haven't verified what the auto-merge actually grants; if it's "merge Dependabot PRs without review" the question is whether an attacker can get their own PR into a state where the actor reads as `dependabot[bot]`. zizmor's docs say yes in narrow cases. Needs hands-on confirmation before it goes in a slide.

`github-env` (`slice_github_env.tsv`): 375 repos write attacker-influenced data to `$GITHUB_ENV` or `$GITHUB_PATH`, which lets a value that looks inert in one step become code execution in a later step. scikit-learn (190M, 8,580 dependents) does this in `bot-lint-comment.yml`; azure-core and azure-identity (175M each) in `event-processor.yml`. Same verification caveat: depends on the trigger and what gets written.

`use-trusted-publishing` (`slice_use_trusted_publishing.tsv`): 43,758 repos still publish to PyPI with a long-lived API token. By downloads: six (896M), fsspec (616M), annotated-types (552M), pyasn1 (430M), tomli (377M), greenlet (337M), sqlalchemy (335M). This is the list to hand to the PSF if anyone wants a prioritised outreach campaign for trusted publishing adoption. Moving these to OIDC wouldn't fix every problem above but it removes the credential that makes most of them worth exploiting.

Self-hosted runners on public repos with `pull_request` triggers (the PyTorch 2023 pattern) needs the raw workflow corpus to detect `runs-on:` values; the zizmor output and actions inventory don't capture it. Skipped for now.

### Change over time

Re-scanned the PyPI critical set on 28 April with zizmor 1.24.1 and again on 9 May. The original scan was 6-11 April with 1.23.1. Old results saved in `data/zizmor_results_prev/`.

Findings counts below are deduped by repository; packages that share a repo (google-cloud-python ×13, azure-sdk-for-python ×12, opentelemetry ×8, etc.) are counted once. An earlier version of this table counted per package, which roughly doubled the numbers and overstated the deltas; the dedup was added to `load_db.py` on 28 April after that table was generated.

| audit | 6-11 Apr | 28 Apr | 9 May | Apr→Apr |
|---|---|---|---|---|
| unpinned-uses | 7,446 | 6,320 | 6,326 | -15% |
| artipacked | 2,755 | 2,337 | 2,329 | -15% |
| excessive-permissions | 2,186 | 1,887 | 1,873 | -14% |
| template-injection | 708 | 715 | 708 | +1% |
| use-trusted-publishing | | 93 | 93 | |

`secrets-outside-env` dropped to zero, but that's a zizmor persona change in 1.24.0, not a real fix. The rest is mostly repos hardening: unpinned-uses, artipacked, and excessive-permissions weren't touched in 1.24.0, so the ~15% drops are maintainers pinning and adding `permissions:` blocks in the three weeks after Trivy (19 March) and elementary-data (24 April). apispec, awscli, and babel went to zero findings entirely. 28 April to 9 May is essentially flat.

This conflates the zizmor upgrade with repo changes, so it's not usable for the main aggregate numbers. The talk should stay on the 6-11 April / 1.23.1 snapshot for everything in the funnel and the audit table. But re-running the critical set at intervals could make a good closing slide: "do publicised incidents move the needle." Would need at least one more data point closer to the conference, ideally with the zizmor version held constant (scan.py is now pinned to 1.24.1).

To do later: separate the zizmor delta from the repo delta by re-running 1.24.1 against the workflows as they were on 6 April (would need the workflows_export to cover all 456, currently only 31). Or just accept the conflation and present it as "net change."

Running both versions against the 31 frozen workflow exports gives the clean version delta with no repo drift: unpinned-uses, artipacked, excessive-permissions, dangerous-triggers, cache-poisoning, and use-trusted-publishing are identical between 1.23.1 and 1.24.1. template-injection drops about 3% from the `needs.*.result` false-positive fix. secrets-outside-env disappears because of a persona change. So the version bump barely moves anything the talk uses, and the 19-31% drops in the live re-scan are almost entirely repos hardening.

### Scan tooling notes

zizmor 1.24.1 panics on `${{ (a || b).prop }}` expressions (hit in cupy's `pr-updated.yml`). Already reported and fixed upstream as zizmorcore/zizmor#1903 / #1904, but not in a release yet. scan.py was silently recording crashed scans as `[]`; fixed to check stderr and route to `failed.json`. Keep an eye out for a 1.24.2 before the full re-scan; otherwise the crash detection will at least surface affected repos rather than zeroing them.

1,733 of the 150k April results are empty `[]` files. Spot-checked stamina, pytest, requests: all genuinely zero-finding. Those three are good "what right looks like" examples for the hardening section.

### Hardening checklist

Each item maps back to a real incident. Ordered roughly by effort versus payoff.

Move to trusted publishing. Replace the stored `PYPI_API_TOKEN` with OIDC via `pypa/gh-action-pypi-publish`. Configure the trusted publisher on PyPI with an environment name, then put that environment behind required reviewers or a branch restriction. OIDC alone removes the stealable credential; the environment is what stops the elementary-data dispatch pivot. 43,758 packages in the dataset still use a token.

Add a `permissions:` block to every workflow. `permissions: {}` at the top of the file, then grant only what each job needs. The elementary-data workflow had no block, so the injected code got `contents: write` and `actions: write` from the repo default. 99,885 packages have at least one workflow without a `permissions:` block.

Pin third-party actions to a commit SHA. `uses: owner/action@<40-char-sha>  # vX.Y.Z`. Tags are mutable; Trivy proved that twice in three weeks. There's no point pinning `actions/*`: if GitHub's own org is compromised the runner image and the platform are already gone, and zizmor can be told to allow first-party tags via `unpinned-uses` config. Everything else gets a SHA. 83,751 packages have at least one unpinned third-party action. Dependabot and Renovate both understand SHA pins and will update them.

Never interpolate `${{ github.event.* }}` into `run:`. Pass it through `env:` and reference the shell variable instead. `env: BODY: ${{ github.event.comment.body }}` then `echo "$BODY"`. Same data, no expansion before bash sees it. 20,626 packages have at least one template-injection finding.

Avoid `pull_request_target` and `workflow_run` unless you have a specific reason. If you must use `pull_request_target`, never check out the PR head and never restore caches in that job. 6,812 packages use one of these triggers.

Keep the publish job minimal. `actions/checkout`, `actions/download-artifact`, `pypa/gh-action-pypi-publish`, nothing else. Build the wheel in a separate job, upload it as an artifact, download it in the publish job. Every third-party action in the publish job is a tag-hijack target with your release credentials. 3,454 packages run `astral-sh/setup-uv` in the same job as the upload.

Run zizmor in CI. `zizmor .github/workflows/` as a step in a `pull_request` workflow. It catches every pattern above before merge.

### Transitive action dependencies

Even when a workflow pins its direct action dependencies to a SHA, the actions themselves may pull in unpinned transitive dependencies. Composite actions resolve their own `uses:` directives invisibly. A workflow author pins `actions/checkout@sha` but has no visibility into what that action depends on internally.

Prior research (USENIX Security 2022) found 54% of JavaScript actions contain at least one security weakness, with most coming from indirect dependencies.

To analyse this:
1. Take the most popular actions from our dataset
2. Fetch their `action.yml` files from GitHub
3. For composite actions, extract the `uses:` directives and check pinning
4. Recurse into transitive deps
5. Build a dependency tree showing where the unpinned links are

This would show that even "properly pinned" workflows still have unpinned transitive dependencies they can't control, reinforcing the argument for a lockfile that covers the full dependency tree.
