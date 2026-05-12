# TODO

## Slides

- [x] Actions adoption: 362,899 with GH repo, 150,274 with workflows (chapter 1)
- [x] Publish from Actions: 53,747 use `pypa/gh-action-pypi-publish` (chapter 1)
- [x] Top third-party actions table (Findings)
- [x] Publish-job concentration table with unpinned % (Findings)
- [x] Transitive deps: top composites are clean, `aio-libs/create-release` is the counterexample (Findings)
- [x] % of PyPI-linked repos that fail to clone: ~20% (68,291 of 343,292 distinct GH URLs in failed.json). Upper bound, includes auth/timeout not just 404.
- [x] CVE counts per audit: 49 GHSA actions advisories, 27 template-injection / 8 dangerous-triggers / 4 unpinned-uses / 2 cache-poisoning (`bucket_cves.py`)
- [ ] zizmor findings on top-20 action repos' own workflows (Findings: auditing the actions)
- [ ] `images/zizmor-output.png`: terminal screenshot of zizmor on a sample workflow
- [ ] `images/elementary-zizmor.png`: the actual finding with the line highlighted
- [ ] Screenshot of zizmor-action failing a PR check (chapter 6)
- [ ] Refresh ecosyste.ms scale numbers

## Data

- [x] `bucket_cves.py`: fetches GHSA ecosystem=actions, regex-buckets by audit, writes `data/cve_buckets.json`. 10 unbucketed (mostly Harden-Runner egress, runner privesc) worth a manual pass
- [ ] Run scrutineer + zizmor on the rest of `top_action_repos.txt` (cibuildwheel done: 1 Low, self-audits with zizmor #2770; runtime fetches from 7 upstream hosts unpinned)
- [ ] Extend `resolve_actions.py` over the long tail (top-200) to find more unpinned third-party transitives than just aio-libs
- [ ] Full `pypi.org` re-scan (running, `--workers 3`)
- [ ] One more critical-set re-scan closer to the conference, zizmor pinned
- [ ] Check for zizmor 1.24.2 with the #1904 panic fix before the next full scan
- [ ] Self-hosted runners on `pull_request`: extract `runs-on:` from raw workflow YAML
- [ ] Expand npm indexing beyond critical so `report_token_risk.py` can validate the OIDC tier
- [ ] Separate the 1.23.1→1.24.1 delta from repo drift: extend workflows_export to all critical repos and replay both versions

## Disclosures

- [ ] sqlglot (11.6M/month, write-scoped issue_comment injection)
- [ ] airbyte-cdk and the rest of the 10 write-scoped issue_comment repos
- [ ] Hands-on verify aio-libs `bot-conditions` auto-merge actor spoof before mentioning on stage

## Content

- [ ] If the typomania-based typosquat audit lands in zizmor before the talk, add it to Findings; test corpus is `actions_pypi_org.db`. Real-world signal in HEAD is org-confusion (`actions/gh-action-pypi-publish`, `actions/setup-uv`); keyboard-typo variants show 0/9,230 but that's survivorship-biased since a 404ing typo self-corrects within a commit. The audit's value is catching it at PR time, which HEAD-only data can't measure. Would need workflow git history to estimate the true commit rate.

- [ ] Fold the 29-30 April Mini Shai-Hulud chain into chapter 2 incidents (SAP CAP → lightning → intercom-client, cross-registry worm)
- [ ] Add intercom-client OIDC bypass to trusted-publishing caveats: `id-token: write` on tag push, no environment, attacker pushed tag and deleted the run
- [ ] Propose a zizmor audit upstream for `id-token: write` without `environment:` (mention to William)

## Brief-derived stats

The May full scan runs `--no-brief`. Brief data exists for ~69k repos in `data/brief/pypi_org/` from earlier runs; `report_brief.py` reads from there. Report brief-derived stats as percentages, not counts, since it's a ~46% sample. If a full-coverage brief pass is needed later, run `scan.py pypi.org --force` without `--no-brief` once disk allows.

## Refresh after the full re-scan completes

Re-run `uv run slide_data.py` from `collect/` and update:

- [ ] Chapter 1: 362,899 / 150,274 / 53,747
- [ ] Six-audits overview table and the six per-audit repo counts
- [ ] Most-popular third-party actions table
- [x] Publish-job concentration table (`slice_publish_jobs.py` regenerates the TSV from the latest db)
- [ ] `use-trusted-publishing` package list (six, fsspec, sqlalchemy, ...)
- [ ] "Maintainers are responding" table (add the new data point)
- [ ] 404 rate
