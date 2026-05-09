# Zizmor scan report

- Packages fetched from npmjs.org: 2295
  - No repo URL: 19
  - github.com: 2274
  - git.coolaj86.com: 1
  - gitlab.com: 1
- Packages with GitHub repos: 2274 (1598 unique repos)
- Repos scanned: 1140
- Repos without workflows: 33 (2.9%)
- Repos with findings: 1135 (99.6%)
- Total findings: 18407
  - High: 1096 repos (96.1%)
  - Medium: 1085 repos (95.2%)
  - Low: 212 repos (18.6%)
  - Informational: 144 repos (12.6%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/babel/babel | 131 |
| https://github.com/DefinitelyTyped/DefinitelyTyped | 68 |
| https://github.com/smithy-lang/smithy-typescript | 50 |
| https://github.com/jestjs/jest | 48 |
| https://github.com/aws/aws-sdk-js-v3 | 34 |
| https://github.com/cssnano/cssnano | 30 |
| https://github.com/lodash/lodash | 29 |
| https://github.com/csstools/postcss-plugins | 25 |
| https://github.com/evanw/esbuild | 23 |
| https://github.com/micromark/micromark | 21 |
| https://github.com/storybookjs/storybook | 19 |
| https://github.com/radix-ui/primitives | 19 |
| https://github.com/blakeembrey/change-case | 16 |
| https://github.com/xtuc/webassemblyjs | 15 |
| https://github.com/gregberge/svgr | 14 |
| https://github.com/emotion-js/emotion | 13 |
| https://github.com/dcodeIO/protobuf.js | 10 |
| https://github.com/TooTallNate/proxy-agents | 10 |
| https://github.com/typescript-eslint/typescript-eslint | 9 |
| https://github.com/aws/aws-sdk-js-crypto-helpers | 8 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| unpinned-uses | High | 1070 | 93.9% | 8853 |
| artipacked | Medium | 1004 | 88.1% | 3271 |
| excessive-permissions | Medium | 940 | 82.5% | 3076 |
| secrets-outside-env | Medium | 295 | 25.9% | 994 |
| dangerous-triggers | High | 232 | 20.4% | 402 |
| template-injection | Informational | 119 | 10.4% | 964 |
| cache-poisoning | High | 80 | 7.0% | 257 |
| superfluous-actions | Low | 74 | 6.5% | 269 |
| use-trusted-publishing | Informational | 70 | 6.1% | 83 |
| bot-conditions | High | 58 | 5.1% | 59 |
| archived-uses | Medium | 18 | 1.6% | 45 |
| secrets-inherit | Medium | 11 | 1.0% | 74 |
| unsound-contains | High | 8 | 0.7% | 9 |
| unpinned-images | High | 6 | 0.5% | 14 |
| github-env | High | 3 | 0.3% | 11 |
| misfeature | Low | 3 | 0.3% | 9 |
| obfuscation | Low | 3 | 0.3% | 15 |
| unsound-condition | High | 2 | 0.2% | 2 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 1096 | 96.1% | 10062 |
| Medium | 1085 | 95.2% | 6700 |
| Low | 212 | 18.6% | 985 |
| Informational | 144 | 12.6% | 660 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/getsentry/sentry-javascript | 10 | 246 | 1423 |
| https://github.com/swc-project/swc | 10 | 196 | 7514 |
| https://github.com/cypress-io/cypress | 9 | 105 | 6559 |
| https://github.com/vercel/next.js | 8 | 378 | 8463 |
| https://github.com/facebook/watchman | 8 | 304 | 1100 |
| https://github.com/npm/cli | 8 | 263 | 9618 |
| https://github.com/npm/pacote | 8 | 75 | 590 |
| https://github.com/Azure/azure-sdk-for-js | 7 | 247 | 269 |
| https://github.com/babel/babel | 7 | 183 | 197540 |
| https://github.com/storybookjs/storybook | 7 | 176 | 41076 |
| https://github.com/microsoft/playwright | 7 | 157 | 2919 |
| https://github.com/sass/dart-sass | 7 | 137 | 45433 |
| https://github.com/remix-run/react-router | 7 | 102 | 23067 |
| https://github.com/npm/fs-minipass | 7 | 79 | 452 |
| https://github.com/npm/git | 7 | 78 | 10 |
| https://github.com/jsx-eslint/eslint-plugin-react | 7 | 72 | 105111 |
| https://github.com/npm/abbrev-js | 7 | 71 | 786 |
| https://github.com/npm/agent | 7 | 71 | 2 |
| https://github.com/npm/cacache | 7 | 71 | 750 |
| https://github.com/npm/fs | 7 | 71 | 24 |

## High severity (excluding unpinned-uses)

1210 findings across 373 repos (32.7%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| dangerous-triggers | 232 | 402 |
| template-injection | 86 | 303 |
| cache-poisoning | 80 | 257 |
| excessive-permissions | 68 | 152 |
| bot-conditions | 58 | 59 |
| unsound-contains | 8 | 9 |
| unpinned-images | 6 | 14 |
| github-env | 3 | 11 |
| unsound-condition | 2 | 2 |
| artipacked | 1 | 1 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/getsentry/sentry-javascript | 5 | 32 | 1423 |
| https://github.com/microsoft/playwright | 4 | 13 | 2919 |
| https://github.com/storybookjs/storybook | 4 | 10 | 41076 |
| https://github.com/npm/pacote | 4 | 9 | 590 |
| https://github.com/cypress-io/cypress | 4 | 7 | 6559 |
| https://github.com/webpack/webpack | 4 | 6 | 216244 |
| https://github.com/fb55/domhandler | 4 | 5 | 732 |
| https://github.com/fb55/domutils | 4 | 5 | 679 |
| https://github.com/facebook/react | 3 | 81 | 275174 |
| https://github.com/npm/cli | 3 | 55 | 9618 |
| https://github.com/Azure/azure-sdk-for-js | 3 | 26 | 269 |
| https://github.com/vercel/next.js | 3 | 18 | 8463 |
| https://github.com/swc-project/swc | 3 | 15 | 7514 |
| https://github.com/remix-run/react-router | 3 | 10 | 23067 |
| https://github.com/nodejs/undici | 3 | 9 | 1956 |
| https://github.com/mochajs/mocha | 3 | 7 | 261831 |
| https://github.com/typescript-eslint/typescript-eslint | 3 | 7 | 129460 |
| https://github.com/babel/babel | 3 | 6 | 197540 |
| https://github.com/npm/fs-minipass | 3 | 6 | 452 |
| https://github.com/npm/abbrev-js | 3 | 5 | 786 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/facebook/watchman | 3255 | 8 | 304 | 1100 |
| https://github.com/vercel/next.js | 3190 | 8 | 378 | 8463 |
| https://github.com/facebook/react | 3058 | 6 | 308 | 275174 |
| https://github.com/npm/cli | 2171 | 8 | 263 | 9618 |
| https://github.com/getsentry/sentry-javascript | 2066 | 10 | 246 | 1423 |
| https://github.com/Azure/azure-sdk-for-js | 2039 | 7 | 247 | 269 |
| https://github.com/swc-project/swc | 1795 | 10 | 196 | 7514 |
| https://github.com/babel/babel | 1613 | 7 | 183 | 197540 |
| https://github.com/browserify/pbkdf2 | 1512 | 4 | 183 | 840 |
| https://github.com/inspect-js/has-symbols | 1390 | 4 | 162 | 1561 |
| https://github.com/microsoft/playwright | 1249 | 7 | 157 | 2919 |
| https://github.com/storybookjs/storybook | 1161 | 7 | 176 | 41076 |
| https://github.com/inspect-js/has-tostringtag | 1090 | 4 | 112 | 894 |
| https://github.com/sass/dart-sass | 1028 | 7 | 137 | 45433 |
| https://github.com/facebook/flow | 959 | 6 | 109 | 468 |
| https://github.com/tailwindlabs/tailwindcss | 920 | 6 | 94 | 11727 |
| https://github.com/remix-run/react-router | 837 | 7 | 102 | 23067 |
| https://github.com/mongodb/node-mongodb-native | 805 | 6 | 84 | 11544 |
| https://github.com/cypress-io/cypress | 793 | 9 | 105 | 6559 |
| https://github.com/zloirock/core-js | 749 | 5 | 83 | 68956 |
| https://github.com/npm/fs-minipass | 662 | 7 | 79 | 452 |
| https://github.com/npm/git | 650 | 7 | 78 | 10 |
| https://github.com/npm/pacote | 627 | 8 | 75 | 590 |
| https://github.com/jsx-eslint/eslint-plugin-react | 617 | 7 | 72 | 105111 |
| https://github.com/npm/abbrev-js | 611 | 7 | 71 | 786 |
| https://github.com/npm/agent | 611 | 7 | 71 | 2 |
| https://github.com/npm/cacache | 611 | 7 | 71 | 750 |
| https://github.com/npm/fs | 611 | 7 | 71 | 24 |
| https://github.com/npm/hosted-git-info | 611 | 7 | 71 | 1640 |
| https://github.com/npm/ignore-walk | 611 | 7 | 71 | 291 |
