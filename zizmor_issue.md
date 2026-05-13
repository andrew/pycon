<!--
Draft issue body for woodruffw/zizmor (zizmorcore/zizmor).
File via .github/ISSUE_TEMPLATE/bug-report.yml. Sections below map to the
template's textareas.

Before filing:
  - Tick the three pre-submission checkboxes only after you've personally
    checked troubleshooting docs and existing issues (open + closed).
  - The zizmor AI policy ( https://github.com/zizmorcore/.github/blob/main/AI_POLICY.md )
    governs your participation. Read it yourself.
  - This body was AI-drafted from research you directed. Decide whether to
    keep the disclosure paragraph in "Additional context" or remove it.
-->

## Title

`[BUG]:` `use-trusted-publishing` misses stored PyPI tokens passed to reusable workflows

## zizmor version

zizmor 1.24.1

## Expected behavior

I expected `use-trusted-publishing` to fire on a workflow that publishes to PyPI with a stored API token, regardless of whether the `twine upload` call lives in the same workflow file or in a reusable workflow it calls. Passing `pypi_token: ${{ secrets.PYPI_TOKEN }}` (or similarly-named secret) into a reusable workflow's `secrets:` block is functionally the same pattern as `TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}` at a direct `twine upload` site, and the audit description ("this workflow publishes to PyPI using a long-lived API token rather than trusted publishing / OIDC") applies equally to both.

## Actual behavior

zizmor does not fire `use-trusted-publishing` on the caller workflow when the upload happens inside a reusable workflow that the caller invokes via `uses:` and to which the caller passes the token through a `secrets:` block. The caller is a stored-token publisher in every meaningful sense, but the audit only inspects the caller's own steps.

## Reproduction steps

The concrete case I found is `mistralai/client-python`, where the publish workflow is:

```yaml
# https://github.com/mistralai/client-python/blob/7ebe84b5a9eee0714f81c687c8cf636eaa12476f/.github/workflows/sdk_publish_mistralai_sdk.yaml
name: Publish MISTRALAI-SDK
permissions:
  checks: write
  contents: write
  pull-requests: write
  statuses: write
"on":
  workflow_dispatch:
    inputs:
      confirm_publish:
        description: 'Type "publish" to confirm.'
        required: false
        type: string
  push:
    branches:
      - main
    paths:
      - RELEASES.md
      - "*/RELEASES.md"
jobs:
  publish:
    if: |
      (github.event_name == 'push' && github.ref == 'refs/heads/main') ||
      (github.event_name == 'workflow_dispatch' && github.event.inputs.confirm_publish == 'publish')
    uses: speakeasy-api/sdk-generation-action/.github/workflows/sdk-publish.yaml@7951d9dce457425b900b2dd317253499d98c2587 # v15
    secrets:
      github_access_token: ${{ secrets.CLIENT_PIPELINE }}
      pypi_token: ${{ secrets.PYPI_TOKEN }}
      speakeasy_api_key: ${{ secrets.SPEAKEASY_API_KEY }}
```

The reusable workflow it calls performs the upload with the standard stored-token pattern:

```yaml
# https://github.com/speakeasy-api/sdk-generation-action/blob/7951d9dce457425b900b2dd317253499d98c2587/.github/workflows/sdk-publish.yaml#L217-L229
env:
  PYPI_TOKEN: ${{ secrets.pypi_token }}
  # ...
  TWINE_PASSWORD: ${{ secrets.pypi_token }}
run: |
  pip install setuptools wheel twine
  # ...
  twine upload dist/*
```

Steps:

1. `zizmor` (1.24.1) on `mistralai/client-python` at commit `7ebe84b5a9eee0714f81c687c8cf636eaa12476f`.
2. Inspect findings for `sdk_publish_mistralai_sdk.yaml`.
3. Observe that `use-trusted-publishing` does not appear, although the reusable workflow at the SHA-pinned ref clearly does `twine upload` with the passed-through token.

## Logs

No useful zizmor output beyond the absence of the finding; the audit simply doesn't fire on the caller. Happy to provide `--verbose` output on request if it helps.

## Additional context

**Why this matters.** mistralai's `mistralai` PyPI package was compromised at version 2.4.6 on 2026-05-11 (currently under investigation by Microsoft Threat Intelligence — see [MsftSecIntel](https://x.com/MsftSecIntel/status/2054041471280423424)). The malicious wheel was uploaded via a long-lived PyPI API token, not through the normal release workflow (the repo's `main` never advanced past `7ebe84b5` and no `Publish MISTRALAI-SDK` run executed after 7 May, suggesting direct `twine upload` with a stolen token). zizmor's `use-trusted-publishing` audit is the right tool to identify these targets ahead of time, but the reusable-workflow indirection meant mistralai was invisible to it.

I scanned 152,318 PyPI packages with workflows for an upcoming PyCon talk and found 44,181 with `use-trusted-publishing` findings. mistralai is not among them, but should be; I suspect a population of similar callers using Speakeasy, GoReleaser, or hand-rolled reusable workflows for the actual upload also slips through.

**Possible heuristic.** Without resolving the reusable workflow's body (which is a bigger change), one conservative match is: caller passes a secret to a reusable workflow's `secrets:` block where the secret key matches a known PyPI-token name pattern (`pypi_token`, `PYPI_TOKEN`, `twine_password`, `TWINE_PASSWORD`, `pypi_api_token`) and the destination is not `pypa/gh-action-pypi-publish` (the canonical OIDC trusted publisher). That covers the mistralai shape without needing to download every referenced reusable workflow.

The stricter approach is to follow `uses:` references for reusable workflows when the SHA is pinned and cacheable, but that's a much larger change and likely a separate issue.

Happy to send a PR for the heuristic version if you'd like, subject to the AI policy and a green light from a maintainer.

<!--
AI disclosure: this issue body was drafted with AI assistance from research
I directed. I reviewed the technical claims and code references myself before
filing.
-->
