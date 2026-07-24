---
name: diff-inspector
description: "Inspect code diffs before opening a pull request or merging. This skill MUST be used when the user provides a code diff, pastes code changes, asks for a code or PR review, or when code is about to be submitted as a PR or merged. It MUST NOT be skipped solely because the diff is small. It SHOULD also be used before committing or handing back substantial or high-risk code changes. It MUST NOT be used when changes are limited to non-code content such as documentation, prose, images, or formatting. For small, low-risk self-changes, perform only a lightweight review without specialist dispatch. Checks requirement scope, correctness, security, compatibility, and test coverage. Triggers on: 幫我看程式 diff, 看一下程式改了什麼, review 程式碼, PR review, diff review, code review, 看看程式有沒有問題"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
metadata:
  version: "1.4.5"
---

## Review timing

Review before opening a pull request and before merging. Reuse the previous result if the relevant diff has not changed; otherwise review again.

---

## Establish review scope

Identify the relevant code diff from the user's input, current worktree, pull request, or merge target. Inspect the repository's existing Git state, conventions, and task context as needed. If the review scope or base remains unclear after inspection, ask the user.

---

## Review sequence

1. **Check scope:** Compare the diff with the stated request and report meaningful scope drift or missing requirements.
2. **Review code:** Review the full diff using the technical checks below.

---

## Technical review

Review the full diff. For each applicable area, verify:

- **SQL and data safety:** Queries handle untrusted values safely, remain bounded, and preserve data integrity.
- **Race conditions and state:** Concurrent operations, check-then-act flows, shared state, and asynchronous work remain atomic and consistent.
- **Authentication and trust boundaries:** Changed entry points enforce authentication, authorization, ownership, token validity, and input validation.
- **Error handling:** Failures are surfaced and handled, including partial failures, timeouts, cleanup, and recovery.
- **Performance and resources:** The change does not introduce unbounded work, resource leaks, unnecessary repeated work, or avoidable bottlenecks.
- **Completeness and compatibility:** For each changed shared contract, such as a state, field, path, identifier, schema, or configuration:
  1. Inventory relevant occurrences first: search the entire target tree using stable contract fragments such as path prefixes, filename patterns, field names, command names, or resolver functions.
  2. Trace each producer to all consumers and each consumer back to a concrete producer, including unchanged files outside the diff. A consumer has a concrete producer only when it computes the value or calls a named shared resolver. Prose placeholders, examples, and state expected from an earlier tool do not count.
  3. Compare the exact values or derivation logic used on both sides. Report unaccounted occurrences, missing implementations, and duplicated or divergent derivations.
- **Tests:** Tests demonstrate changed behavior, important edge and failure paths, and regression protection.

### Evidence and severity

Report a finding only when it is supported by relevant code and a concrete failure scenario.

- **P0:** Critical or blocking. Can cause a security breach, data loss, service outage, or another failure that must be fixed before merging.
- **P1:** Serious. Likely to cause incorrect behavior or a major regression and should normally be fixed before merging.
- **P2:** Moderate and localized. Actionable, but may be scheduled after merging when the risk is acceptable.

For each finding:

- cite the relevant file and line
- describe the trigger and impact
- assign P0, P1, or P2 based on impact
- label it `CONFIRMED` when the code proves the issue, or `NEEDS INVESTIGATION` when required facts are unavailable
- recommend a proportionate action

Do not report speculation or style preferences as defects.

Format: `[P0/P1/P2] [CONFIRMED/NEEDS INVESTIGATION] file:line - trigger, impact, description, and recommended action`

---

## Review perspectives

Select the perspectives relevant to the changed code and apply their checks:

- **Testing:** Missing negative and edge-case tests, weak regression coverage, isolation violations, flaky patterns, and changed public behavior without tests
- **Maintainability:** Unnecessary complexity, duplicated logic, unclear responsibilities, leaky abstractions, and changes that are difficult to understand, test, or extend
- **Security:** Missing validation at trust boundaries, authentication or authorization failures, insecure direct object references, privilege escalation, weak secret handling, XSS, command injection, SSRF, and path traversal
- **Performance:** N+1 queries, missing indexes, avoidable quadratic work, expensive loops, heavy dependencies, fetch waterfalls, and unbounded operations
- **Data migration:** Irreversible migrations, locking schema changes, missing foreign-key indexes, unsafe backfills, and removing old schemas before dependent code
- **API contract:** Incompatible response changes, new required inputs without defaults, changed error formats, and changed pagination behavior

Skip perspectives that are clearly unrelated to the diff. Deduplicate findings by path, line, and category; keep the highest-impact finding with the strongest evidence.

### Adversarial subagent

Run an adversarial subagent when the diff is large, spans multiple components, or affects high-impact behavior such as authentication, authorization, payments, sensitive data, migrations, concurrency, or critical user workflows.

```text
You are an adversarial reviewer. Review the established diff.

Think like an attacker and a chaos engineer. Find ways this code will fail in
production — not style issues, not missing tests, actual breakage or security holes.

Look specifically for:
- race conditions
- auth bypasses
- silent data corruption
- resource leaks
- swallowed failures
- trust boundary violations

For each finding: describe the exact failure scenario and classify as
FIXABLE or INVESTIGATE.
```

---

## Documentation and guidance consistency

Review documentation and distributable guidance affected by the diff, both at the repository root and within affected packages, modules, or subtrees. Include, where applicable:

- README files, architecture guides, contributing guides, API references, and other explanatory documentation
- Package- or module-specific documentation
- Changelogs and release notes when required by project convention or when the change affects users
- Repository operating contracts for agents working in the repository, such as `AGENTS.md` or `CLAUDE.md`
- Installable agent skills, prompts, templates, examples, plugin metadata, and other agent-facing artifacts distributed by the repository

Check whether changes to behavior, interfaces, setup, configuration, installation, migrations, required artifacts, workflows, handoff rules, tool usage, or deployment constraints are reflected in every affected document or artifact.

When the repository distributes installable skills or other agent-facing artifacts, treat them as product outputs. Verify that their instructions, examples, references, metadata, and packaging remain aligned with the changed behavior.

Report each mismatch with references to both the changed code and the affected document or artifact.

---

## Final output

Lead with actionable findings ordered from P0 to P2. Merge and deduplicate findings from the main review, review perspectives, documentation and guidance checks, and any adversarial review.

Use this structure:

```text
## Diff Inspector
Scope: [CLEAN / DRIFT / MISSING]
Reviewed: [diff source and scope]
Adversarial review: [RUN — Trigger: reason]

### Findings
- [P0/P1/P2] [CONFIRMED/NEEDS INVESTIGATION] file:line - trigger, impact, description, and recommended action

### Scope differences
- [include only when scope drift or missing requirements exist]
```

Include the `Adversarial review` line only when that review ran. If there are no findings, state `No findings.` Do not include empty sections.
