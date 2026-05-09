# GitHub Actions findings in crates.io critical packages

Andrew Nesbitt, 28 April 2026

This is a scan of the 813 most-downloaded crates.io packages with public GitHub repositories, run with zizmor 1.24.1 on 28 April 2026. The prompt was the elementary-data PyPI compromise on 24 April, where a `${{ github.event.comment.body }}` interpolation in an `issue_comment` workflow let an attacker post a comment that executed as shell, pivot to a write-scoped `GITHUB_TOKEN`, and push a malicious release. I ran the same queries against the crates.io critical set to see whether any Rust packages have the same shape.

## Template injection on attacker-controllable input

Two crates interpolate an externally-controllable expression into a `run:` block:

| crate | workflow | expression | trigger |
|---|---|---|---|
| [codespan-reporting](https://github.com/brendanzab/codespan) | [ci.yml](https://github.com/brendanzab/codespan/blob/HEAD/.github/workflows/ci.yml) | `github.head_ref` | pull_request |
| [petgraph](https://github.com/petgraph/petgraph) | [semver-checks.yml](https://github.com/petgraph/petgraph/blob/HEAD/.github/workflows/semver-checks.yml) | `github.event.pull_request.title` | pull_request |

Both fire on `pull_request`, which for fork PRs runs without repository secrets and with a read-capped token, so an attacker gets code execution on an empty runner and nothing else. Neither uses `issue_comment` or `issues`, the triggers that run with secrets in scope, and no other crate in the 813 does either.

## pull_request_target and workflow_run

zizmor flags six distinct repositories for `dangerous-triggers`. Most are labelling workflows that use `pull_request_target` only to apply labels and never check out fork code, which is the documented safe use:

| repo | workflow | trigger |
|---|---|---|
| [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | [labeler.yml](https://github.com/tokio-rs/tokio/blob/HEAD/.github/workflows/labeler.yml) | pull_request_target |
| [actix/actix-web](https://github.com/actix/actix-web) | [labeler.yml](https://github.com/actix/actix-web/blob/HEAD/.github/workflows/labeler.yml) | pull_request_target |
| [PyO3/pyo3](https://github.com/PyO3/pyo3) | [cache-cleanup.yml](https://github.com/PyO3/pyo3/blob/HEAD/.github/workflows/cache-cleanup.yml) | pull_request_target (closed only) |
| [PyO3/pyo3](https://github.com/PyO3/pyo3) | [coverage-pr-base.yml](https://github.com/PyO3/pyo3/blob/HEAD/.github/workflows/coverage-pr-base.yml) | pull_request_target (file has a safety comment) |
| [PyO3/pyo3](https://github.com/PyO3/pyo3) | [netlify-deploy.yml](https://github.com/PyO3/pyo3/blob/HEAD/.github/workflows/netlify-deploy.yml) | workflow_run |
| [rustwasm/gloo](https://github.com/rustwasm/gloo) | [publish-website.yml](https://github.com/rustwasm/gloo/blob/HEAD/.github/workflows/publish-website.yml) | workflow_run |
| [allan2/dotenvy](https://github.com/allan2/dotenvy) | [codecov-comment.yml](https://github.com/allan2/dotenvy/blob/HEAD/.github/workflows/codecov-comment.yml) | workflow_run |
| [rust-lang/rust-bindgen](https://github.com/rust-lang/rust-bindgen) | [publish.yml](https://github.com/rust-lang/rust-bindgen/blob/HEAD/.github/workflows/publish.yml) | workflow_run |

I have not verified each of these by hand. The pyo3 `coverage-pr-base.yml` file has an inline comment referencing a safety note, which suggests the maintainers have thought about it. The tokio and actix labellers look like the standard `actions/labeler` pattern.

The one I'd look at first is [rust-lang/rust-bindgen](https://github.com/rust-lang/rust-bindgen). Its [publish.yml](https://github.com/rust-lang/rust-bindgen/blob/HEAD/.github/workflows/publish.yml) triggers on `workflow_run` completion of a workflow named "Release" and runs `cargo publish --token ${CARGO_REGISTRY_TOKEN}`. If the upstream "Release" workflow can be reached from a fork PR, the `workflow_run` event fires in the base repository with secrets available. Whether that chain is actually reachable depends on what triggers "Release" and whether `publish.yml` checks `github.event.workflow_run.head_repository` before publishing. I haven't confirmed either way.

## Stored crates.io tokens

Eleven repositories publish to crates.io from CI using a stored `CARGO_REGISTRY_TOKEN` rather than OIDC trusted publishing. crates.io has supported trusted publishing since July 2025.

| crate | downloads | dependents | repo | workflow |
|---|---|---|---|---|
| jobserver | 338,129,256 | 31 | [rust-lang/jobserver-rs](https://github.com/rust-lang/jobserver-rs) | [publish.yml](https://github.com/rust-lang/jobserver-rs/blob/HEAD/.github/workflows/publish.yml) |
| textwrap | 325,179,579 | 375 | [mgeisler/textwrap](https://github.com/mgeisler/textwrap) | [publish-crate.yml](https://github.com/mgeisler/textwrap/blob/HEAD/.github/workflows/publish-crate.yml) |
| bindgen | 239,669,736 | 2,062 | [rust-lang/rust-bindgen](https://github.com/rust-lang/rust-bindgen) | [publish.yml](https://github.com/rust-lang/rust-bindgen/blob/HEAD/.github/workflows/publish.yml) |
| libz-sys | 172,709,287 | 97 | [rust-lang/libz-sys](https://github.com/rust-lang/libz-sys) | [ci.yml](https://github.com/rust-lang/libz-sys/blob/HEAD/.github/workflows/ci.yml) |
| cargo_metadata | 148,873,199 | 582 | [oli-obk/cargo_metadata](https://github.com/oli-obk/cargo_metadata) | [release.yml](https://github.com/oli-obk/cargo_metadata/blob/HEAD/.github/workflows/release.yml) |
| colored | 148,776,091 | 2,847 | [mackwic/colored](https://github.com/mackwic/colored) | [publish.yml](https://github.com/mackwic/colored/blob/HEAD/.github/workflows/publish.yml) |
| atoi | 103,571,080 | 90 | [pacman82/atoi-rs](https://github.com/pacman82/atoi-rs) | [release.yml](https://github.com/pacman82/atoi-rs/blob/HEAD/.github/workflows/release.yml) |
| outref | 92,542,263 | 4 | [Nugine/outref](https://github.com/Nugine/outref) | [publish.yml](https://github.com/Nugine/outref/blob/HEAD/.github/workflows/publish.yml) |
| infer | 79,959,735 | 110 | [bojand/infer](https://github.com/bojand/infer) | [release.yml](https://github.com/bojand/infer/blob/HEAD/.github/workflows/release.yml) |
| thrift | 67,875,388 | 39 | [apache/thrift](https://github.com/apache/thrift) | [release_rust.yml](https://github.com/apache/thrift/blob/HEAD/.github/workflows/release_rust.yml) |
| smawk | 62,254,932 | 1 | [mgeisler/smawk](https://github.com/mgeisler/smawk) | [publish-crate.yml](https://github.com/mgeisler/smawk/blob/HEAD/.github/workflows/publish-crate.yml) |

Three of these are in the rust-lang org. The libz-sys finding is on `cargo run -p maint -- publish` in `ci.yml`, which may be a packaging test rather than a real publish; the others are unambiguous `cargo publish` calls with a token.

zizmor also flags [microsoft/windows-rs](https://github.com/microsoft/windows-rs) here, but the step is `cargo publish --workspace --dry-run` with no token, so that's a false positive.

If I were prioritising, I'd verify the bindgen `workflow_run` chain first since it's the only place a privileged trigger and a stored publishing token sit in the same workflow, then work through the stored-token list as an OIDC migration nudge. The labellers are almost certainly fine but cheap to confirm.

This is the critical set only, not the full registry, and the `dangerous-triggers` rows are zizmor's static heuristic rather than confirmed exposures. Repository-level settings like the default `GITHUB_TOKEN` scope and environment protection rules aren't visible from workflow YAML and would change the picture for individual repos. Raw zizmor output for all 813 crates available on request.
