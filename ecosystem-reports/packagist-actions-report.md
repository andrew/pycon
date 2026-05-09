# GitHub Actions findings in Packagist critical packages

Andrew Nesbitt, 28 April 2026

This is a scan of the 547 most-downloaded Packagist packages with public GitHub repositories, run with zizmor 1.24.1 on 28 April 2026. It follows the same method as the PyPI and crates.io scans prompted by the elementary-data compromise on 24 April.

The Packagist threat model differs from PyPI and crates.io. Composer packages are git tags; Packagist polls the repository via webhook and serves whatever is tagged. There is no upload step and no registry token stored in CI. The equivalent of a forged release is just pushing a tag with a write-scoped `GITHUB_TOKEN`, which means the attack chain is shorter but also that the `use-trusted-publishing` audit doesn't apply. zizmor reports zero findings for it across all 547 packages.

## Template injection on attacker-controllable input

One package interpolates an externally-controllable expression into a `run:` block:

| package | workflow | expression | trigger |
|---|---|---|---|
| [pusher/pusher-php-server](https://github.com/pusher/pusher-http-php) | [release.yml](https://github.com/pusher/pusher-http-php/blob/HEAD/.github/workflows/release.yml) | `github.event.pull_request.body`, `github.event.pull_request.head.ref` | pull_request |

The trigger is plain `pull_request`, so fork PRs run with no secrets and a read-capped token. None of the 547 packages interpolate `issue_comment` or `issues` event data, which is the zero-barrier pattern from elementary-data.

## pull_request_target and workflow_run

zizmor reports 138 `dangerous-triggers` findings. 81 of those are the Laravel `illuminate/*` subtree-split mirrors, which all carry a `close-pull-request.yml` that fires on `pull_request_target: [opened]` to post a comment and close the PR. Another 15 are a similar `pull-requests.yml` in other read-only mirrors. After removing those, around 30 distinct repositories remain:

| package | downloads | workflow | repo |
|---|---|---|---|
| ramsey/uuid | 713,790,439 | merge-me.yml | [ramsey/uuid](https://github.com/ramsey/uuid) |
| egulias/email-validator | 704,569,680 | upload-to-codacy.yml | [egulias/EmailValidator](https://github.com/egulias/EmailValidator) |
| ramsey/collection | 498,372,937 | merge-me.yml | [ramsey/collection](https://github.com/ramsey/collection) |
| squizlabs/php_codesniffer | 371,338,886 | label-\*.yml (3 files) | [PHPCSStandards/PHP_CodeSniffer](https://github.com/PHPCSStandards/PHP_CodeSniffer) |
| ezyang/htmlpurifier | 335,134,486 | lint-pr.yml | [ezyang/htmlpurifier](https://github.com/ezyang/htmlpurifier) |
| justinrainbow/json-schema | 321,940,700 | welcome.yml | [jsonrainbow/json-schema](https://github.com/jsonrainbow/json-schema) |
| friendsofphp/php-cs-fixer | 239,357,900 | maint_self-approval.yml, maint_add-milestone.yml | [PHP-CS-Fixer/PHP-CS-Fixer](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer) |
| sentry/sentry | 218,708,487 | validate-pr.yml | [getsentry/sentry-php](https://github.com/getsentry/sentry-php) |
| composer/composer | 189,912,590 | api-surface-comment.yml | [composer/composer](https://github.com/composer/composer) |
| elasticsearch/elasticsearch | 180,929,188 | backport.yml, docs-\*.yml | [elastic/elasticsearch-php](https://github.com/elastic/elasticsearch-php) |
| spatie/\* (9 packages) | 56M–173M | dependabot-auto-merge.yml | [spatie](https://github.com/spatie) |
| cweagans/composer-patches | 96,466,976 | automerge.yml | [cweagans/composer-patches](https://github.com/cweagans/composer-patches) |

I have not verified each of these. By filename most are labellers, PR linters, and welcome bots, which typically use `pull_request_target` for write access to labels and never check out fork code. The ones I'd read first:

- [composer/composer api-surface-comment.yml](https://github.com/composer/composer/blob/HEAD/.github/workflows/api-surface-comment.yml), since it's the package manager itself.
- [PHP-CS-Fixer maint_self-approval.yml](https://github.com/PHP-CS-Fixer/PHP-CS-Fixer/blob/HEAD/.github/workflows/maint_self-approval.yml), because a self-approval workflow on `pull_request_target` is unusual.
- [ramsey/uuid merge-me.yml](https://github.com/ramsey/uuid/blob/HEAD/.github/workflows/merge-me.yml) and [cweagans/composer-patches automerge.yml](https://github.com/cweagans/composer-patches/blob/HEAD/.github/workflows/automerge.yml), since auto-merge on a privileged trigger is the pattern that produces a tag without review.

## Spoofable bot checks

All nine `bot-conditions` findings are in [spatie](https://github.com/spatie) packages, each with the same `dependabot-auto-merge.yml` gated on `${{ github.actor == 'dependabot[bot]' }}` under `pull_request_target`. zizmor flags this check as bypassable in some re-run scenarios. The same pattern shows up in the aio-libs packages on PyPI. Whether it's practically exploitable depends on what the workflow does after the check passes; for spatie it enables auto-merge on the PR, which combined with Packagist's tag-polling model would be a path to a release if an attacker could get a PR into a state where the actor reads as Dependabot.

## What this means for Packagist

There is no elementary-data-shaped finding in the critical set and no registry credential to steal. The exposure that matters for PHP is any workflow that gives an outsider a write-scoped `GITHUB_TOKEN`, because that token can push a tag and Packagist will serve it. The `dangerous-triggers` and `bot-conditions` lists above are where that token is in scope alongside attacker-influenced input, and the auto-merge workflows are where it could turn into a tag without a human approving anything.

This is the critical set only (547 packages), not the full registry. The `dangerous-triggers` rows are zizmor's static heuristic and each needs reading to confirm whether fork code or fork-controlled input actually reaches anything privileged. Raw zizmor output for all 547 packages available on request.
