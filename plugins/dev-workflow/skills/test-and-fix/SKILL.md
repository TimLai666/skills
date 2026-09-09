---
name: test-and-fix
description: "Run tests, find failures, fix them, verify. Diff-aware: tests affected behavior in web apps, APIs, CLIs, and libraries. This skill MUST be invoked on the triggers below, and SHOULD be invoked after any code change the user has not yet verified. Triggers on: 跑測試, 測一下, 有沒有壞掉, run tests, test this, 跑一下 tests, 測試, check if broken"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
metadata:
  version: "1.4.0"
---

## Preamble

Read the user's requested test scope and commands, project instructions, test configuration, and relevant source files. Use the project's existing delivery or task records when they help establish the expected behavior.

Identify the target: web UI, API, command-line tool, library, or another artifact. Testing can run on the current branch, including the base branch. Inspect existing changes before editing.

## Phase 1 — Analyze what changed

Use the supplied scope first. When testing changes, inspect the relevant staged, unstaged, or committed diff and trace its callers and consumers. Determine the comparison ref from the task or repository configuration; fetch only when the comparison needs updated remote information.

Map the affected behavior:
- Web UI: pages, components, interactions, and rendered states.
- API: endpoints, authentication, inputs, responses, and errors.
- CLI: arguments, input/output, exit codes, and file effects.
- Library: public functions, callers, return values, and edge cases.

For tests requiring a running service, find the startup command and address in project configuration, documentation, or existing process output. Start the required local service within the task's authorization. Ask only for essential information that cannot be established from available evidence.

---

## Phase 2 — Build test plan

For each affected behavior, identify the expected result, test method, and priority. Include relevant normal, invalid-input, empty, and failure cases. Use the project's existing test commands and verification requirements, following the testing strategy in **software-engineering-guidelines**.

Cross-check the plan against the request and relevant task records. A mismatch is a reason to clarify the expected behavior, not to silently change the test scope.

---

## Phase 3 — Execute tests

Execute the Phase 2 plan using the selected tests. For web UI changes, inspect the affected rendering and interactions in the running application. Run the full suite according to project rules.

For each test:
- **Pass** — describe what was verified
- **Fail** — exact symptom and evidence
- **Unexpected** — anything unplanned

---

## Phase 4 — Fix loop

For each failure, locate the root cause first. If it cannot be established from the tested changes and evidence, invoke **investigate**.

1. Add or update a regression test that fails without the fix and passes with it. Follow **software-engineering-guidelines** for timing: major or high-risk changes are test-first; small, local, low-risk fixes may add the test before or immediately after implementation.
2. Make the minimal fix, then rerun the failing case and relevant regression checks.
3. Commit according to the user's instructions and project conventions. If no commit arrangement is specified, retain the original default: commit the fix on its own, then commit its regression test separately. Writing a test first and committing it later are separate decisions. Stage only the intended changes, preserving unrelated work.

Every fixed bug needs regression coverage. Report verification gaps explicitly.

---

## Report

```text
## Test Report [feature/branch] [date]

### Summary
Tests run: N | Passed: N | Failed: N | Fixed: N (with regression tests)

### Changes tested
- [target/behavior] — [result]

### Bugs found & fixed
1. [description] — file:line — regression test: [test name]

### Issues found (not yet fixed)
1. [P0/P1/P2] [description] — blocking: [yes/no]

### Regression tests added
- [test file]: [test names]

### Recommendation
[SHIP / FIX FIRST / INVESTIGATE]
```

---

## Test framework bootstrap (if no tests exist)

Check whether built-in language tools, existing scripts, or a small reproducible test can verify the behavior. Use a test framework when it adds necessary capability; explain the dependency and setup implications before introducing it, following the task's authorization.

A reproducible check must exercise the actual behavior and expose the bug without the fix. If verification remains blocked, report the missing capability rather than treating an unverified fix as complete. Follow the commit arrangement above; commit framework setup separately when using the default arrangement.
