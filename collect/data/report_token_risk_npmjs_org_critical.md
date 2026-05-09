# Token-hygiene risk: npmjs.org

1119 of 1598 repos flagged (297 via token audits, 1118 via oidc audits).

Token audits (×3): secrets-outside-env, overprovisioned-secrets, secrets-inherit — stored publish credentials exposed in workflows.

OIDC audits (×1): excessive-permissions, artipacked — weak GitHub-side trust boundary; relevant when publishing via trusted-publisher OIDC where there is no token to leak.

Score = (3×token + 1×min(oidc, 20)) × (1 + downloads/1M).

| # | package | downloads | deps | out-env | overprov | inherit | ex-perm | artipack | token | oidc | score | hit |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | eslint-visitor-keys | 1,027,654,466 | 1,888 | 22 | 0 | 0 | 7 | 5 | 22 | 12 | 80235.0 |  |
| 2 | @azure/abort-controller | 77,850,980 | 269 | 184 | 0 | 0 | 0 | 3 | 184 | 3 | 43762.3 |  |
| 3 | debug | 2,393,108,233 | 46,672 | 0 | 0 | 0 | 13 | 5 | 0 | 18 | 43093.9 |  |
| 4 | @next/env | 126,573,162 | 8,463 | 50 | 0 | 53 | 101 | 34 | 103 | 135 | 41971.6 |  |
| 5 | typescript | 502,474,598 | 488,056 | 19 | 0 | 0 | 0 | 30 | 19 | 30 | 38767.5 |  |
| 6 | react-is | 814,091,899 | 275,174 | 7 | 0 | 0 | 0 | 43 | 7 | 43 | 33418.8 |  |
| 7 | @babel/parser | 647,225,603 | 197,540 | 10 | 0 | 0 | 0 | 37 | 10 | 37 | 32411.3 |  |
| 8 | ajv | 1,104,226,275 | 14,548 | 8 | 0 | 0 | 2 | 2 | 8 | 4 | 30946.3 |  |
| 9 | @rollup/rollup-linux-x64-musl | 516,094,268 | 130,345 | 14 | 0 | 0 | 1 | 10 | 14 | 11 | 27406.0 |  |
| 10 | @smithy/util-utf8 | 489,855,369 | 536 | 15 | 0 | 0 | 0 | 10 | 15 | 10 | 26997.0 |  |
| 11 | uuid | 1,025,879,189 | 41,299 | 0 | 0 | 0 | 13 | 12 | 0 | 25 | 20537.6 |  |
| 12 | core-js | 246,677,421 | 68,956 | 22 | 0 | 0 | 5 | 11 | 22 | 16 | 20309.5 |  |
| 13 | type-fest | 1,300,669,217 | 5,723 | 2 | 0 | 0 | 4 | 5 | 2 | 9 | 19525.0 |  |
| 14 | ms | 1,763,146,318 | 5,545 | 2 | 0 | 0 | 2 | 3 | 2 | 5 | 19405.6 |  |
| 15 | glob | 1,318,942,385 | 48,165 | 1 | 0 | 0 | 6 | 5 | 1 | 11 | 18479.2 |  |
| 16 | lru-cache | 1,594,120,234 | 6,362 | 0 | 0 | 0 | 6 | 5 | 0 | 11 | 17546.3 |  |
| 17 | zod | 328,954,222 | 6,111 | 13 | 0 | 0 | 4 | 7 | 13 | 11 | 16497.7 |  |
| 18 | @opentelemetry/core | 399,847,973 | 1,073 | 7 | 0 | 0 | 1 | 19 | 7 | 20 | 16434.8 |  |
| 19 | @swc/helpers | 219,758,677 | 7,514 | 15 | 0 | 2 | 21 | 32 | 17 | 53 | 15673.9 |  |
| 20 | undici-types | 844,669,727 | 1,956 | 1 | 0 | 4 | 1 | 0 | 5 | 1 | 13530.7 |  |

## Known compromises in this dataset

None found in dataset.
