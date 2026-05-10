# TODO

## Slides

- [ ] Actions adoption % across PyPI packages with GitHub repos (chapter 1, pull from actions_pypi_org.db)
- [ ] % of PyPI-linked repos that 404 (chapter 3, filter failed.json to pypi + not-found/auth errors)
- [ ] % of packages that publish from Actions (chapter 1)
- [ ] `images/zizmor-output.png`: terminal screenshot of zizmor on a sample workflow
- [ ] `images/elementary-zizmor.png`: the actual finding with the line highlighted
- [ ] Screenshot of zizmor-action failing a PR check (chapter 6)
- [ ] Fill top-10 third-party actions in publish jobs from `slice_actions_in_publish_job.tsv`, including `softprops/action-gh-release` unpinned %
- [ ] Refresh ecosyste.ms scale numbers
- [ ] Refresh closing "maintainers are responding" table after the full re-scan

## Data

- [ ] Full `pypi.org` re-scan (weekend run, writes `.sha` sidecars for incremental refresh)
- [ ] One more critical-set re-scan closer to the conference, zizmor pinned
- [ ] Check for zizmor 1.24.2 with the #1904 panic fix before the next full scan
- [ ] Self-hosted runners on `pull_request`: extract `runs-on:` from raw workflow YAML
- [ ] Transitive action dependency tree for top-20 actions in publish jobs
- [ ] Expand npm indexing beyond critical so `report_token_risk.py` can validate the OIDC tier
- [ ] Separate the 1.23.1→1.24.1 delta from repo drift: extend workflows_export to all critical repos and replay both versions

## Disclosures

- [ ] sqlglot (11.6M/month, write-scoped issue_comment injection)
- [ ] airbyte-cdk and the rest of the 10 write-scoped issue_comment repos
- [ ] Hands-on verify aio-libs `bot-conditions` auto-merge actor spoof before mentioning on stage

## Content

- [ ] Fold the 29-30 April Mini Shai-Hulud chain into chapter 2 incidents (SAP CAP → lightning → intercom-client, cross-registry worm)
- [ ] Add intercom-client OIDC bypass to trusted-publishing caveats: `id-token: write` on tag push, no environment, attacker pushed tag and deleted the run
- [ ] Propose a zizmor audit upstream for `id-token: write` without `environment:` (mention to William)
