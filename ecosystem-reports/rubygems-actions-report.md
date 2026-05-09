# GitHub Actions findings in RubyGems critical packages

Andrew Nesbitt, 28 April 2026

This is a scan of the 947 most-downloaded RubyGems packages with public GitHub repositories (794 with workflows after deduplication), run with zizmor 1.24.1 on 28 April 2026. Same method as the PyPI, crates.io, and Packagist scans following the elementary-data compromise on 24 April. RubyGems has supported OIDC trusted publishing since December 2023, so the threat model matches PyPI: a stored `RUBYGEMS_API_KEY` is the credential of interest, and `pull_request_target` or `workflow_run` with a write-scoped token is the pivot.

## Template injection on attacker-controllable input

Two gems interpolate an externally-controllable expression into a `run:` block:

| gem | workflow | expression | trigger |
|---|---|---|---|
| [puma](https://github.com/puma/puma) | [release-checks.yml](https://github.com/puma/puma/blob/HEAD/.github/workflows/release-checks.yml) | `github.head_ref` | pull_request |
| [language_server-protocol](https://github.com/mtsmfm/language_server-protocol-ruby) | [generator.yml](https://github.com/mtsmfm/language_server-protocol-ruby/blob/HEAD/.github/workflows/generator.yml) | `github.head_ref` | pull_request |

Both fire on plain `pull_request`, so fork PRs run with no secrets and a read-capped token. Puma additionally gates on `startsWith(github.head_ref, 'release-v')`. None of the 947 gems interpolate `issue_comment` or `issues` event data.

## pull_request_target and workflow_run

zizmor reports 34 `dangerous-triggers` findings across roughly 20 distinct repositories. Most are labellers and PR-comment bots:

| repo | workflow | note |
|---|---|---|
| [rails/rails](https://github.com/rails/rails) | labeler.yml | covers 14 gems in the critical set |
| [hashie/hashie](https://github.com/hashie/hashie), [ruby-grape/grape](https://github.com/ruby-grape/grape), [slack-ruby/slack-ruby-client](https://github.com/slack-ruby/slack-ruby-client), [ruby-grape/grape-entity](https://github.com/ruby-grape/grape-entity) | danger-comment.yml | Danger CI commenting |
| [octokit/octokit.rb](https://github.com/octokit/octokit.rb) | add_to_octokit_project.yml, immediate-response.yml | |
| [SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) | label-commenter.yml, pr-labeler.yml | |
| [Shopify/liquid](https://github.com/Shopify/liquid), [shopify/bootboot](https://github.com/shopify/bootboot) | cla.yml | |
| [getsentry/sentry-ruby](https://github.com/getsentry/sentry-ruby) | validate-pr.yml | |
| [elastic/elasticsearch-ruby](https://github.com/elastic/elasticsearch-ruby) | docs-deploy.yml, docs-preview-cleanup.yml | |
| [chef/chef](https://github.com/chef/chef) | danger.yml, kitchen.yml, labeler.yml, windows-fips.yml | |

The ones I'd read first because they touch releases or merging:

- [gjtorikian/commonmarker](https://github.com/gjtorikian/commonmarker) (88M downloads). [automerge.yml](https://github.com/gjtorikian/commonmarker/blob/HEAD/.github/workflows/automerge.yml) runs on `pull_request_target` with `contents: write`. [tag_and_release.yml](https://github.com/gjtorikian/commonmarker/blob/HEAD/.github/workflows/tag_and_release.yml) also runs on `pull_request_target` and creates a tag, though it's gated on `merged == true` and a `release` label, so a maintainer has to merge first. The automerge half is the part to verify: if it can be made to merge a fork PR, the tag-and-release half follows.
- [newrelic/newrelic-ruby-agent](https://github.com/newrelic/newrelic-ruby-agent) (177M). [lambda_release.yml](https://github.com/newrelic/newrelic-ruby-agent/blob/HEAD/.github/workflows/lambda_release.yml) runs on `workflow_run` with `contents: write`. Whether the upstream workflow is fork-reachable needs checking.
- [fastlane/fastlane](https://github.com/fastlane/fastlane) (191M). [announce_release.yml](https://github.com/fastlane/fastlane/blob/HEAD/.github/workflows/announce_release.yml) on a privileged trigger, alongside two PR-handling workflows.
- [ruby/rdoc](https://github.com/ruby/rdoc) (290M). [fork-preview-deploy.yml](https://github.com/ruby/rdoc/blob/HEAD/.github/workflows/fork-preview-deploy.yml) on `workflow_run`; the name suggests it deliberately handles fork content.

## Stored RubyGems API keys

Ten repositories publish to RubyGems from CI using a stored API key rather than OIDC trusted publishing:

| gem | downloads | dependents | repo | workflow |
|---|---|---|---|---|
| faraday_middleware | 433,667,314 | 1,830 | [lostisland/faraday_middleware](https://github.com/lostisland/faraday_middleware) | [publish.yml](https://github.com/lostisland/faraday_middleware/blob/HEAD/.github/workflows/publish.yml) |
| faraday-excon | 360,789,073 | 16 | [excon/faraday-excon](https://github.com/excon/faraday-excon) | [publish.yml](https://github.com/excon/faraday-excon/blob/HEAD/.github/workflows/publish.yml) |
| colorize | 158,696,219 | 2,234 | [fazibear/colorize](https://github.com/fazibear/colorize) | [release.yml](https://github.com/fazibear/colorize/blob/HEAD/.github/workflows/release.yml) |
| faraday-http-cache | 129,604,142 | 296 | [plataformatec/faraday-http-cache](https://github.com/plataformatec/faraday-http-cache) | [release-please.yml](https://github.com/plataformatec/faraday-http-cache/blob/HEAD/.github/workflows/release-please.yml) |
| twilio-ruby | 120,678,017 | 101 | [twilio/twilio-ruby](https://github.com/twilio/twilio-ruby) | [test-and-deploy.yml](https://github.com/twilio/twilio-ruby/blob/HEAD/.github/workflows/test-and-deploy.yml) |
| stripe | 104,256,917 | 85 | [stripe/stripe-ruby](https://github.com/stripe/stripe-ruby) | [ci.yml](https://github.com/stripe/stripe-ruby/blob/HEAD/.github/workflows/ci.yml) |
| annotate | 84,987,366 | 73 | [ctran/annotate_models](https://github.com/ctran/annotate_models) | [release.yml](https://github.com/ctran/annotate_models/blob/HEAD/.github/workflows/release.yml) |
| ffaker | 70,528,177 | 528 | [ffaker/ffaker](https://github.com/ffaker/ffaker) | [publish.yml](https://github.com/ffaker/ffaker/blob/HEAD/.github/workflows/publish.yml) |
| sendgrid-ruby | 55,692,029 | 23 | [sendgrid/sendgrid-ruby](https://github.com/sendgrid/sendgrid-ruby) | [test-and-deploy.yml](https://github.com/sendgrid/sendgrid-ruby/blob/HEAD/.github/workflows/test-and-deploy.yml) |

faraday-http-cache uses `rubygems/release-gem@v1`, the official action that supports OIDC, but passes `GEM_HOST_API_KEY: ${{ secrets.RUBYGEMS_API_KEY }}` to it instead of letting it mint a token. The voxpupuli/json-schema finding is a `gem push` to GitHub Packages rather than rubygems.org, so it's a different registry's credential.

If I were prioritising: commonmarker's `automerge.yml` is the only place a `pull_request_target` trigger sits next to `contents: write` and a release workflow in the same repo, so that's the chain to verify or rule out first. The stored-token list is an OIDC migration nudge; faraday_middleware and colorize are the high-impact ones by dependent count.

This is the critical set only, not the full registry. The `dangerous-triggers` rows are zizmor's static heuristic and each needs reading to confirm whether fork code or fork-controlled input reaches anything privileged. Raw zizmor output for all 947 gems available on request.
