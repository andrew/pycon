# Zizmor scan report: rubygems.org

- Packages fetched from rubygems.org: 974
  - No repo URL: 25
  - github.com: 947
  - gitlab.com: 2
- Packages with GitHub repos: 947 (682 unique repos)
- Repos scanned: 538
- Repos without workflows: 30 (5.6%)
- Repos with findings: 529 (98.3%)
- Total findings: 7297
  - High: 513 repos (95.4%)
  - Medium: 501 repos (93.1%)
  - Low: 165 repos (30.7%)
  - Informational: 35 repos (6.5%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/aws/aws-sdk-ruby | 225 |
| https://github.com/rails/rails | 13 |
| https://github.com/rspec/rspec | 5 |
| https://github.com/googleapis/google-api-ruby-client | 5 |
| https://github.com/kaminari/kaminari | 4 |
| https://github.com/googleapis/common-protos-ruby | 3 |
| https://github.com/getsentry/sentry-ruby | 3 |
| https://github.com/elastic/elasticsearch-ruby | 3 |
| https://github.com/sorbet/sorbet | 2 |
| https://github.com/sinatra/sinatra | 2 |
| https://github.com/ruby/rubygems | 2 |
| https://github.com/ruby/json | 2 |
| https://github.com/googlecloudplatform/google-cloud-ruby | 2 |
| https://github.com/flippercloud/flipper | 2 |
| https://github.com/flavorjones/mini_portile | 2 |
| https://github.com/bkeepers/dotenv | 2 |
| https://github.com/babel/ruby-babel-transpiler | 2 |
| https://github.com/ManageIQ/optimist | 2 |
| https://github.com/DatabaseCleaner/database_cleaner | 2 |
| https://github.com/CocoaPods/CocoaPods | 2 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| unpinned-uses | High | 510 | 94.8% | 3537 |
| artipacked | Medium | 506 | 94.1% | 1556 |
| excessive-permissions | Medium | 438 | 81.4% | 1417 |
| secrets-outside-env | Medium | 91 | 16.9% | 284 |
| cache-poisoning | High | 82 | 15.2% | 145 |
| template-injection | Informational | 48 | 8.9% | 138 |
| dangerous-triggers | High | 26 | 4.8% | 36 |
| unpinned-images | High | 25 | 4.6% | 72 |
| secrets-inherit | Medium | 17 | 3.2% | 36 |
| superfluous-actions | Low | 15 | 2.8% | 22 |
| use-trusted-publishing | Informational | 15 | 2.8% | 16 |
| archived-uses | Medium | 8 | 1.5% | 12 |
| bot-conditions | High | 3 | 0.6% | 4 |
| github-env | High | 3 | 0.6% | 4 |
| obfuscation | Low | 3 | 0.6% | 3 |
| insecure-commands | High | 2 | 0.4% | 8 |
| misfeature | Low | 2 | 0.4% | 3 |
| overprovisioned-secrets | Medium | 1 | 0.2% | 3 |
| unsound-condition | High | 1 | 0.2% | 1 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 513 | 95.4% | 3897 |
| Medium | 501 | 93.1% | 2637 |
| Low | 165 | 30.7% | 681 |
| Informational | 35 | 6.5% | 82 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/newrelic/newrelic-ruby-agent | 10 | 145 | 132 |
| https://github.com/SeleniumHQ/selenium | 9 | 153 | 1044 |
| https://github.com/googlecloudplatform/google-cloud-ruby | 8 | 338 | 179 |
| https://github.com/chef/chef | 8 | 71 | 11 |
| https://github.com/icalendar/icalendar | 8 | 45 | 79 |
| https://github.com/twilio/twilio-ruby | 8 | 41 | 101 |
| https://github.com/sass/ruby-sass | 7 | 137 | 1140 |
| https://github.com/fastlane/fastlane | 7 | 40 | 782 |
| https://github.com/ruby/rdoc | 7 | 35 | 5167 |
| https://github.com/bcrypt-ruby/bcrypt-ruby | 7 | 32 | 351 |
| https://github.com/redis/hiredis-rb | 7 | 32 | 136 |
| https://github.com/defunkt/colored | 7 | 31 | 429 |
| https://github.com/mtsmfm/language_server-protocol-ruby | 7 | 31 | 11 |
| https://github.com/slack-ruby/slack-ruby-client | 7 | 28 | 82 |
| https://github.com/DataDog/dd-trace-rb | 7 | 27 | 26 |
| https://github.com/sendgrid/sendgrid-ruby | 7 | 27 | 23 |
| https://github.com/jodosha/redis-store | 7 | 21 | 23 |
| https://github.com/redis-store/redis-actionpack | 7 | 13 | 2 |
| https://github.com/googleapis/google-cloud-ruby | 6 | 56 | 243 |
| https://github.com/redis/redis-rb | 6 | 53 | 1960 |

## High severity (excluding unpinned-uses)

360 findings across 152 repos (28.3%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| cache-poisoning | 82 | 145 |
| template-injection | 31 | 57 |
| dangerous-triggers | 26 | 36 |
| unpinned-images | 25 | 72 |
| excessive-permissions | 17 | 33 |
| github-env | 3 | 4 |
| bot-conditions | 3 | 4 |
| insecure-commands | 2 | 8 |
| unsound-condition | 1 | 1 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/newrelic/newrelic-ruby-agent | 5 | 18 | 132 |
| https://github.com/ruby/rdoc | 4 | 8 | 5167 |
| https://github.com/SeleniumHQ/selenium | 3 | 9 | 1044 |
| https://github.com/fastlane/fastlane | 3 | 9 | 782 |
| https://github.com/freerange/mocha | 3 | 7 | 4378 |
| https://github.com/bcrypt-ruby/bcrypt-ruby | 3 | 6 | 351 |
| https://github.com/DataDog/dd-trace-rb | 3 | 4 | 26 |
| https://github.com/icalendar/icalendar | 3 | 4 | 79 |
| https://github.com/mtsmfm/language_server-protocol-ruby | 3 | 3 | 11 |
| https://github.com/googlecloudplatform/google-cloud-ruby | 2 | 26 | 179 |
| https://github.com/jodosha/redis-store | 2 | 6 | 23 |
| https://github.com/chef/chef | 2 | 5 | 11 |
| https://github.com/puma/puma | 2 | 5 | 653 |
| https://github.com/NARKOZ/gitlab | 2 | 3 | 105 |
| https://github.com/collectiveidea/delayed_job_active_record | 2 | 3 | 136 |
| https://github.com/googleapis/google-cloud-ruby | 2 | 3 | 243 |
| https://github.com/redis-store/redis-actionpack | 2 | 3 | 2 |
| https://github.com/ruby/irb | 2 | 3 | 155 |
| https://github.com/ruby/net-imap | 2 | 3 | 22 |
| https://github.com/ruby/racc | 2 | 3 | 151 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/googlecloudplatform/google-cloud-ruby | 2838 | 8 | 338 | 179 |
| https://github.com/SeleniumHQ/selenium | 1463 | 9 | 153 | 1044 |
| https://github.com/sparklemotion/nokogiri | 1390 | 5 | 183 | 8056 |
| https://github.com/ruby-oauth/version_gem | 1176 | 5 | 147 | 33 |
| https://github.com/sass/ruby-sass | 1028 | 7 | 137 | 1140 |
| https://github.com/newrelic/newrelic-ruby-agent | 890 | 10 | 145 | 132 |
| https://github.com/ruby-oauth/oauth | 639 | 5 | 72 | 610 |
| https://github.com/chef/chef | 636 | 8 | 71 | 11 |
| https://github.com/ruby-oauth/oauth2 | 619 | 4 | 68 | 533 |
| https://github.com/RubyCrypto/ed25519 | 516 | 4 | 51 | 105 |
| https://github.com/googleapis/google-cloud-ruby | 493 | 6 | 56 | 243 |
| https://github.com/rmosolgo/graphql-ruby | 489 | 4 | 50 | 186 |
| https://github.com/activerecord-hackery/ransack | 486 | 4 | 56 | 156 |
| https://github.com/oauth-xx/snaky_hash | 483 | 3 | 53 | 2 |
| https://github.com/redis/redis-rb | 472 | 6 | 53 | 1960 |
| https://github.com/faker-ruby/faker | 471 | 4 | 49 | 1074 |
| https://github.com/googleapis/gax-ruby | 426 | 5 | 48 | 38 |
| https://github.com/javan/whenever | 420 | 3 | 47 | 96 |
| https://github.com/icalendar/icalendar | 379 | 8 | 45 | 79 |
| https://github.com/rubocop/rubocop-rspec | 374 | 4 | 47 | 2513 |
| https://github.com/rubocop/rubocop-capybara | 368 | 4 | 46 | 24 |
| https://github.com/fastlane/fastlane | 362 | 7 | 40 | 782 |
| https://github.com/twilio/twilio-ruby | 355 | 8 | 41 | 101 |
| https://github.com/zenchild/gssapi | 354 | 4 | 39 | 14 |
| https://github.com/ruby/reline | 353 | 4 | 43 | 20 |
| https://github.com/benbalter/licensee | 341 | 6 | 42 | 6 |
| https://github.com/flippercloud/flipper | 333 | 6 | 35 | 26 |
| https://github.com/rubocop/rubocop | 322 | 4 | 38 | 12291 |
| https://github.com/redis/hiredis-rb | 311 | 7 | 32 | 136 |
| https://github.com/getsentry/sentry-ruby | 300 | 6 | 49 | 46 |
