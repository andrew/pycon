<!-- spec_version: 1 -->

Audit GitHub Actions workflow files for security vulnerabilities. The target is the workflow YAML files in `.github/workflows/`. Findings are valid only if the vulnerable logic lives in these workflow files. Do not report that an action used by the workflow has a CVE unless the workflow's usage of that action creates the exposure.

The audit has two phases. Phase 1 produces an inventory of every sink in the workflows. Phase 2 works through the inventory and decides on each entry.

## Context

You will receive:
- The workflow YAML files for a single repository
- The zizmor findings for the same repository (static analysis results)
- The actions dependency data (what actions are used and whether they are pinned)

The zizmor findings flag known patterns. Your job is to go deeper: confirm or dismiss the zizmor findings with context, find issues zizmor misses, and assess the actual exploitability of each sink given the workflow's trigger configuration, permissions, and branching logic.

## Phase 1: Inventory

Before listing sinks, name the trust boundaries these workflows have. For GitHub Actions, boundaries are defined by who can trigger or influence a workflow run:

- **Repository maintainers**: can push to protected branches, merge PRs, create releases, modify workflow files. Trusted.
- **Collaborators with write access**: can push to non-protected branches, approve PRs, create tags. Trusted unless the repo has a wide collaborator set.
- **Fork contributors**: can open PRs, which triggers `pull_request` (safe, runs fork code in fork context) or `pull_request_target` (dangerous, runs base code with base secrets but fork-controlled inputs). Untrusted.
- **Issue/PR commenters**: can create issue titles, PR titles, commit messages, branch names, comment bodies. These values reach `github.event.*` context expressions. Untrusted.
- **Tag/release creators**: depends on branch protection. If anyone with write access can create a tag, the tag name is semi-trusted. If tags are unprotected, they are untrusted.
- **External triggers**: `repository_dispatch`, `workflow_dispatch` inputs, `schedule`. Trust depends on who can invoke them.

Write down which of these boundaries exist in these workflows, based on the trigger events configured. Every `on:` key establishes at least one boundary.

Then list every sink. A sink is any place where the workflow does something that would be dangerous if the input were hostile.

For each sink, record: file, line number or step identifier, sink class, what it consumes. Nothing else yet.

Sink classes for GitHub Actions workflows:

- **Expression injection**: any `${{ }}` expression inside a `run:` block, `with:` value, or `env:` value where the expression resolves to attacker-controllable data. The dangerous expressions are `github.event.issue.title`, `github.event.issue.body`, `github.event.pull_request.title`, `github.event.pull_request.body`, `github.event.comment.body`, `github.event.review.body`, `github.event.pages.*.page_name`, `github.event.commits.*.message`, `github.event.head_commit.message`, `github.head_ref`, `github.event.workflow_run.head_branch`, `github.event.inputs.*` (when workflow_dispatch). Also `github.ref_name` when tags are not protected.
- **Dangerous triggers**: `pull_request_target`, `workflow_run`, `issue_comment`, `issues` with a `run:` step that uses event data. These run with base repo permissions but can be influenced by untrusted actors.
- **Permission escalation**: workflows or jobs with `permissions: write-all` or broad write permissions (`contents: write`, `packages: write`, `id-token: write`) combined with code that runs on untrusted input. Also: `GITHUB_TOKEN` used in steps that process PR data.
- **Secret exposure**: secrets passed to steps that process untrusted input, secrets in `env:` at workflow level (available to all steps including untrusted ones), secrets passed via `with:` to actions that log or transmit them. Secrets inherited in reusable workflows via `secrets: inherit`.
- **Artifact poisoning**: `actions/upload-artifact` followed by `actions/download-artifact` across workflow runs, especially when the downloading workflow has elevated permissions. Artifacts are not signed; any workflow run can upload an artifact with any name.
- **Cache poisoning**: `actions/cache` with keys derived from untrusted input, or caches shared between trusted and untrusted workflow runs. A PR can poison a cache entry that a subsequent push workflow uses.
- **Unpinned actions**: `uses:` with a mutable tag (`v1`, `main`, `latest`) rather than a SHA. The action maintainer or anyone who compromises the action repo can change what code runs. Particularly dangerous for actions that receive secrets or have write permissions.
- **Script injection via environment**: values written to `$GITHUB_ENV` or `$GITHUB_OUTPUT` from untrusted input, which are then consumed by subsequent steps. Also `$GITHUB_PATH` manipulation.
- **Conditional bypass**: `if:` conditions on jobs or steps that can be circumvented. Common pattern: checking `github.actor` against a list (accounts can be renamed), checking labels (collaborators can add labels to external PRs), checking `github.event.pull_request.head.repo.full_name` (can be spoofed in some edge cases).
- **Self-hosted runner exposure**: workflows that run on `self-hosted` runners and process untrusted PRs. Self-hosted runners persist state between runs; a malicious PR can install backdoors.

Read every workflow file. For each `on:` trigger, trace what data from that trigger reaches `run:` blocks, `with:` parameters, and `env:` values. The trigger determines the trust level; the data flow determines the sink.

## Phase 2: Per-sink checklist

Work through the inventory in order. For each sink:

### Step 1: Trace the input

What value reaches the sink. Trace from the `${{ }}` expression or variable backwards to where it originates. For expressions, the origin is the event payload field. For environment variables, trace through `$GITHUB_ENV` writes or `env:` declarations. For action outputs, trace to the action that produced them and what that action consumed.

If the value is a hardcoded string, a repository secret set by a maintainer, or a value that only maintainers can influence, write "maintainer-controlled" and move to the next sink.

### Step 2: Trust boundary

Which trigger event fires this workflow, and who can cause it to fire with controlled input. Check it against the boundaries from Phase 1.

Key judgments:
- `pull_request` from a fork: the workflow runs in the fork's context with read-only access. Expression injection in a `run:` block is still dangerous (the attacker runs code) but secrets are not exposed. If the workflow has `pull_request_target`, the same expression injection gives access to secrets.
- `issues` / `issue_comment`: anyone with a GitHub account can create these. If the workflow uses event body/title in a `run:` block, it is attacker-controlled.
- `push` to a protected branch: only maintainers. But `push` to any branch including those created by bots: check branch protection rules.
- `workflow_run` triggered by a PR workflow: the workflow_run has the base repo's context and secrets, but the triggering PR was from a fork. Any data passed via artifacts or outputs from the PR workflow is untrusted.

If the boundary check rules the sink out, write the reason and move on.

### Step 3: Exploit scenario

Write a concrete exploit scenario. Not a script (there is no code to run locally) but a step-by-step description:

1. The attacker does X (opens a PR with title containing Y, creates an issue with body Z, pushes a tag named W)
2. This triggers workflow W which runs job J
3. The expression `${{ github.event.X.Y }}` expands to the attacker's payload in a `run:` block
4. The payload executes as shell commands with access to secrets A, B, C
5. The attacker exfiltrates secrets via (DNS, HTTP callback, modified artifact)

If the scenario requires preconditions that the workflow's configuration prevents (the trigger does not match, a condition gates it, permissions are restricted), write what stopped it and move on.

### Step 4: Zizmor cross-reference

Check whether zizmor flagged this sink. If it did, note the finding ID and whether the zizmor assessment matches your analysis. If zizmor missed it, note that. If zizmor flagged it but you believe it is not exploitable given the full workflow context, explain why.

### Step 5: Rate

Severity:

- **Critical**: exploitable by any GitHub user with no preconditions beyond creating an issue or opening a PR. Gives access to repository secrets or write permissions.
- **High**: exploitable by a fork contributor or issue author with realistic preconditions. Gives access to secrets, write permissions, or the ability to modify releases.
- **Medium**: requires specific conditions (a label to be applied, a branch to exist, a maintainer to trigger a workflow_dispatch with attacker-influenced input). Or: a supply chain risk via unpinned action in a security-sensitive workflow.
- **Low**: theoretical risk with significant mitigating factors, or a hygiene issue (excessive permissions not combined with an exploitable sink).

Confidence: what you verified from the YAML versus what depends on runtime configuration you cannot see (branch protection rules, environment protection rules, repository settings).

## Output

One report per repository at `reports/{repository-name}.md`.

```yaml
---
repository: [URL]
spec_version: 1
model: [name and version]
date: [YYYY-MM-DD]
workflow_files_reviewed: [count]

boundaries:
  - trigger: [on: event]
    actors: [who can cause this]
    trusted: [yes/no/conditional]
    data_controlled: [what event fields they influence]

findings:
  - id: F1
    sinks: [S1, S2]
    title: [short descriptive title]
    severity: [Critical/High/Medium/Low]
    confidence: [High/Medium/Low]
    cwe: [CWE-NNN]
    workflow: [filename]
    trigger: [event that enables this]
    zizmor: [matched/missed/false-positive]
    description: |
      [exploit scenario]
---
```

The body contains: the sink inventory table, a finding section per finding, and a ruled-out section listing each sink with the step that stopped it and why.

Build the full inventory before judging any sink. Multiple findings go in one file. If nothing survived to a finding, the report is the inventory and the ruled-out section.

Do not include process markers or evaluations of the project. Write what the workflows do and what an attacker can do with them.
