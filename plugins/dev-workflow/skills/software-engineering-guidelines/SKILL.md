---
name: software-engineering-guidelines
description: "Software engineering guidelines for any software change. This skill MUST be loaded before requirement clarification, architecture/design, implementation, refactoring, code review, testing, shipping, or creating Git commits (including standalone commit requests), and MUST NOT be skipped because the change is a one-liner. Covers simplicity, surgical changes, testing-first for high-impact changes with TDD (Test-Driven Development), and verifiable success criteria. Triggers on: 任何軟體規劃, 需求釐清, 架構設計, 寫 code, 改 code, 做功能, 修 bug, refactor, 開發, coding, development, 實作, 實現, 寫程式, 改程式, 加功能, 修問題, code review, 測試, 重構, init, 初始化專案, 建立 CLAUDE.md, 建立 AGENTS.md"
metadata:
  version: "1.4.3"
---

## Core Principles

### 1. Think Before Coding

**Verify what you can. Make material assumptions and tradeoffs clear.**

Before implementing:

- Check available information first. Ask the user when an unresolved gap would materially affect the result, scope, authorization, or an important tradeoff. Continue independent work while that decision is pending.
- Otherwise proceed with a reasonable assumption, explaining it when it helps the user assess the result. When interpretations differ materially, explain the relevant difference and recommend an approach for confirmation.
- If a simpler approach exists, say so. Push back when warranted.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting; don't refactor things that aren't broken; don't delete pre-existing dead code. Mention what you spot and suggest how to handle it — see the recording rule below.
- Match existing style, even if you'd do it differently.
- Remove imports/variables/functions that YOUR changes made unused.

**Recording rule:** Mention discovered out-of-scope issues to the user and record them using the project's existing follow-up location and conventions. If none are established, use `## Follow-ups` in the project's `AGENTS.md`, creating the section or file if needed. Preserve existing content and avoid duplicate records. When an issue is resolved, follow the project's completion convention; under the default `Follow-ups` arrangement, remove the resolved entry. See [references/follow-ups-example.md](references/follow-ups-example.md) for the default format and examples.

**Agent context files:** Inspect and follow the project's existing arrangement for agent instructions. When initializing project docs (e.g. `/init`) or asked to create or update agent context files, use this default if no arrangement exists: put the operating instructions in `AGENTS.md` and make `CLAUDE.md` a one-line pointer: "Read `AGENTS.md` before doing any project work." Create missing files as needed. Existing substantive instructions in either file count as an arrangement to preserve; a missing counterpart alone is not a reason to reorganize them.

The test: Every changed line should trace directly to the user's request.

### 4. Testing Strategy (Test-First + scoped TDD)

**Choose verification that demonstrates the change works and matches its impact.**

Baseline rule:

- Every behavior-changing change needs test coverage.
- For text, formatting, or documentation changes, use checks suited to the affected content.
- Run the full test suite according to the project's rules.
- Run the project's linter and type checker when provided, and report their results alongside the tests. Unresolved failures mean verification is incomplete.
- For small, local, low-risk fixes, add/update tests around the change (before or immediately after implementation is acceptable if justified).
- For large changes, broad-scope changes, or major new features, you MUST apply TDD: write the failing test first, then implement — don't write code and backfill tests.

判斷大改動的指標（任一符合即可）：

1. 觸及多個模組或層級（例如 UI、API、資料層同時調整）。
2. 變更公開行為邊界，如 API 契約、資料模型、存取規則、核心流程。
3. 新增核心新功能，或重構高風險路徑（付款、認證、權限、資料遷移、狀態轉換）。

Rules:

- **Bug fixes need a test that reproduces the bug; use the test-first requirements above to determine timing.**
- **Before refactoring, establish the result of relevant tests; rerun them after the change.**
- **Don't weaken a test just to make it pass.** Unless the test itself is wrong.

### 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals — e.g. "Add validation" → "Write tests for invalid inputs, then make them pass".

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

## Workflow

### A. Before Writing Code

1. Establish the requirement and approach (Principle 1).
2. Define success criteria (Principle 5).
3. Select verification and establish required pre-change results (Principle 4).

### B. While Writing Code

Implement using Principles 2–4.

### C. After Completion

1. Complete and report verification (Principle 4).
2. Review the Pre-Ship Checklist.

---

## Commit Messages

Follow the user's explicit instructions first, then the project's commit-message
rules. When neither specifies a format, use Conventional Commits:

```text
<type>(<optional-scope>): <summary>
```

Use an appropriate type such as `feat`, `fix`, `docs`, `refactor`, `test`, `build`,
`ci`, `perf`, `style`, `chore`, or `revert`. Omit the scope when it adds no useful
context. Write a concise, imperative summary of the actual change; add a body
when the reason or consequences need explanation. Mark breaking changes with
`!` or a `BREAKING CHANGE:` footer when applicable.

Default to English for the subject and body unless the user or project specifies
another language. Resolve format and language independently: a project-specific
format does not change the default language unless it also specifies one.

Examples:

```text
fix(auth): handle expired sessions
docs: clarify installation steps
```

## Pre-Ship Checklist

- [ ] Scope and simplicity reviewed against Principles 2–3.
- [ ] Verification completed under Principle 4.
- [ ] Results demonstrate the agreed success criteria; any remaining gaps are reported.
