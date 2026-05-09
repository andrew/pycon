# Zizmor scan report

- Packages fetched from crates.io: 813
  - No repo URL: 2
  - github.com: 802
  - gitlab.redox-os.org: 3
  - gitlab.com: 3
  - hg.sr.ht: 1
  - codeberg.org: 1
  - fuchsia.googlesource.com: 1
- Packages with GitHub repos: 802 (572 unique repos)
- Repos scanned: 492
- Repos without workflows: 13 (2.6%)
- Repos with findings: 482 (98.0%)
- Total findings: 16932
  - High: 474 repos (96.3%)
  - Medium: 445 repos (90.4%)
  - Low: 281 repos (57.1%)
  - Informational: 59 repos (12.0%)

## Shared repositories

| Repository | Packages |
| --- | ---: |
| https://github.com/microsoft/windows-rs | 11 |
| https://github.com/RustCrypto/utils | 11 |
| https://github.com/smithy-lang/smithy-rs | 9 |
| https://github.com/rust-lang/futures-rs | 9 |
| https://github.com/actix/actix-net | 9 |
| https://github.com/RustCrypto/traits | 9 |
| https://github.com/RustCrypto/formats | 9 |
| https://github.com/wasm-bindgen/wasm-bindgen | 8 |
| https://github.com/tokio-rs/tracing | 7 |
| https://github.com/tokio-rs/tokio | 7 |
| https://github.com/rust-random/rngs | 6 |
| https://github.com/rust-cli/anstyle | 6 |
| https://github.com/crossbeam-rs/crossbeam | 6 |
| https://github.com/RustCrypto/hashes | 6 |
| https://github.com/Alexhuszagh/rust-lexical | 6 |
| https://github.com/rust-phf/rust-phf | 5 |
| https://github.com/retep998/winapi-rs | 5 |
| https://github.com/pyo3/pyo3 | 5 |
| https://github.com/open-telemetry/opentelemetry-rust | 5 |
| https://github.com/clap-rs/clap | 5 |

## Findings by audit type

| Audit | Severity | Repos | % scanned | Findings |
| --- | --- | ---: | ---: | ---: |
| unpinned-uses | High | 471 | 95.7% | 8130 |
| artipacked | Medium | 464 | 94.3% | 3068 |
| excessive-permissions | Medium | 378 | 76.8% | 2816 |
| superfluous-actions | Low | 261 | 53.0% | 1845 |
| archived-uses | Medium | 95 | 19.3% | 589 |
| template-injection | Informational | 78 | 15.9% | 231 |
| secrets-outside-env | Medium | 74 | 15.0% | 145 |
| cache-poisoning | High | 18 | 3.7% | 43 |
| use-trusted-publishing | Informational | 18 | 3.7% | 19 |
| secrets-inherit | Medium | 17 | 3.5% | 18 |
| dangerous-triggers | High | 7 | 1.4% | 10 |
| unpinned-images | High | 4 | 0.8% | 6 |
| misfeature | Low | 2 | 0.4% | 5 |
| unsound-condition | High | 2 | 0.4% | 2 |
| bot-conditions | High | 1 | 0.2% | 1 |
| github-env | High | 1 | 0.2% | 4 |

## Findings by severity

| Severity | Repos | % scanned | Findings |
| --- | ---: | ---: | ---: |
| High | 474 | 96.3% | 8276 |
| Medium | 445 | 90.4% | 5395 |
| Low | 281 | 57.1% | 3112 |
| Informational | 59 | 12.0% | 149 |

## Top 20 repos by distinct audit types

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/pyo3/pyo3 | 9 | 195 | 666 |
| https://github.com/rustwasm/gloo | 8 | 74 | 63 |
| https://github.com/rust-lang/rust-bindgen | 7 | 102 | 2062 |
| https://github.com/mgeisler/textwrap | 7 | 94 | 375 |
| https://github.com/time-rs/time | 7 | 87 | 3349 |
| https://github.com/sgodwincs/dlv-list-rs | 7 | 53 | 6 |
| https://github.com/sgodwincs/ordered-multimap-rs | 7 | 53 | 6 |
| https://github.com/mgeisler/smawk | 7 | 49 | 1 |
| https://github.com/mackwic/colored | 7 | 31 | 2847 |
| https://github.com/bojand/infer | 7 | 24 | 110 |
| https://github.com/oli-obk/cargo_metadata | 7 | 21 | 582 |
| https://github.com/smithy-lang/smithy-rs | 6 | 247 | 638 |
| https://github.com/RustCrypto/block-modes | 6 | 169 | 107 |
| https://github.com/RustCrypto/sponges | 6 | 103 | 24 |
| https://github.com/clap-rs/clap | 6 | 99 | 17139 |
| https://github.com/winnow-rs/winnow | 6 | 83 | 87 |
| https://github.com/petgraph/petgraph | 6 | 52 | 615 |
| https://github.com/microsoft/windows-rs | 6 | 50 | 665 |
| https://github.com/eyre-rs/eyre | 6 | 49 | 716 |
| https://github.com/criterion-rs/criterion.rs | 6 | 48 | 5450 |

## High severity (excluding unpinned-uses)

146 findings across 68 repos (13.8%)

| Audit | Repos | Findings |
| --- | ---: | ---: |
| template-injection | 35 | 59 |
| cache-poisoning | 18 | 43 |
| excessive-permissions | 10 | 21 |
| dangerous-triggers | 7 | 10 |
| unpinned-images | 4 | 6 |
| unsound-condition | 2 | 2 |
| github-env | 1 | 4 |
| bot-conditions | 1 | 1 |

### Top 20 repos

| Repository | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: |
| https://github.com/rustwasm/gloo | 3 | 7 | 63 |
| https://github.com/rust-lang/rust-bindgen | 3 | 6 | 2062 |
| https://github.com/pyo3/pyo3 | 3 | 5 | 666 |
| https://github.com/smithy-lang/smithy-rs | 2 | 19 | 638 |
| https://github.com/BurntSushi/ripgrep | 2 | 2 | 403 |
| https://github.com/ia0/data-encoding | 2 | 2 | 469 |
| https://github.com/tokio-rs/tokio | 2 | 2 | 20254 |
| https://github.com/time-rs/time | 1 | 9 | 3349 |
| https://github.com/wasm-bindgen/wasm-bindgen | 1 | 9 | 2023 |
| https://github.com/bytecodealliance/wasm-tools | 1 | 5 | 177 |
| https://github.com/dtolnay/cxx | 1 | 3 | 185 |
| https://github.com/getsentry/rust-debugid | 1 | 3 | 15 |
| https://github.com/jhpratt/deranged | 1 | 3 | 3 |
| https://github.com/jhpratt/num_threads | 1 | 3 | 3 |
| https://github.com/utkarshkukreti/diff.rs | 1 | 3 | 135 |
| https://github.com/RustCrypto/crypto-bigint | 1 | 2 | 52 |
| https://github.com/actix/actix-web | 1 | 2 | 1049 |
| https://github.com/asomers/mockall | 1 | 2 | 430 |
| https://github.com/briansmith/ring | 1 | 2 | 996 |
| https://github.com/clap-rs/clap | 1 | 2 | 17139 |

## Zizscore

Score per finding = severity (High=4, Medium=3, Low=2, Info=1) x confidence (High=3, Medium=2, Low=1). Sum per repo.

| Repository | Zizscore | Audits | Findings | Max dependents |
| --- | ---: | ---: | ---: | ---: |
| https://github.com/RustCrypto/hashes | 5100 | 5 | 585 | 3390 |
| https://github.com/RustCrypto/formats | 3544 | 5 | 431 | 125 |
| https://github.com/RustCrypto/block-ciphers | 3174 | 4 | 384 | 467 |
| https://github.com/tokio-rs/tokio | 2423 | 5 | 261 | 20254 |
| https://github.com/smithy-lang/smithy-rs | 2276 | 6 | 247 | 638 |
| https://github.com/RustCrypto/elliptic-curves | 2110 | 4 | 275 | 197 |
| https://github.com/RustCrypto/utils | 1988 | 5 | 224 | 877 |
| https://github.com/RustCrypto/traits | 1748 | 5 | 212 | 801 |
| https://github.com/pyo3/pyo3 | 1745 | 9 | 195 | 666 |
| https://github.com/RustCrypto/password-hashes | 1512 | 4 | 183 | 229 |
| https://github.com/wasm-bindgen/wasm-bindgen | 1489 | 5 | 173 | 2023 |
| https://github.com/RustCrypto/block-modes | 1419 | 6 | 169 | 107 |
| https://github.com/rust-random/getrandom | 1380 | 4 | 160 | 1077 |
| https://github.com/RustCrypto/AEADs | 1300 | 4 | 173 | 302 |
| https://github.com/RustCrypto/stream-ciphers | 1244 | 5 | 148 | 99 |
| https://github.com/RustCrypto/MACs | 1056 | 5 | 126 | 911 |
| https://github.com/rustls/rustls | 1021 | 5 | 98 | 887 |
| https://github.com/bytecodealliance/rustix | 975 | 3 | 127 | 159 |
| https://github.com/apache/thrift | 883 | 5 | 91 | 39 |
| https://github.com/RustCrypto/sponges | 875 | 6 | 103 | 24 |
| https://github.com/clap-rs/clap | 871 | 6 | 99 | 17139 |
| https://github.com/dalek-cryptography/curve25519-dalek | 837 | 4 | 105 | 516 |
| https://github.com/vorner/arc-swap | 834 | 5 | 93 | 259 |
| https://github.com/RustCrypto/universal-hashes | 820 | 5 | 106 | 19 |
| https://github.com/iqlusioninc/crates | 820 | 4 | 99 | 203 |
| https://github.com/rust-lang/rust-bindgen | 813 | 7 | 102 | 2062 |
| https://github.com/chronotope/chrono | 782 | 4 | 94 | 11374 |
| https://github.com/RustCrypto/KDFs | 772 | 5 | 94 | 198 |
| https://github.com/hyperium/hyper | 756 | 4 | 84 | 3915 |
| https://github.com/winnow-rs/winnow | 748 | 6 | 83 | 87 |
