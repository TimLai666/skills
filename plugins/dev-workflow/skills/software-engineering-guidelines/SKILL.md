---
name: software-engineering-guidelines
description: "Software engineering guidelines for any software change. This skill MUST be loaded before requirement clarification, architecture/design, implementation, refactoring, code review, testing, or shipping, and MUST NOT be skipped because the change is a one-liner. Covers simplicity, surgical changes, testing-first for high-impact changes with TDD (Test-Driven Development), and verifiable success criteria. Triggers on: 任何軟體規劃, 需求釐清, 架構設計, 寫 code, 改 code, 做功能, 修 bug, refactor, 開發, coding, development, 實作, 實現, 寫程式, 改程式, 加功能, 修問題, code review, 測試, 重構, init, 初始化專案, 建立 CLAUDE.md, 建立 AGENTS.md"
metadata:
  version: "1.3.0"
---

## Core Principles

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If something is unclear, stop, name what's confusing, and ask.
- If multiple interpretations exist, present them — don't pick silently.
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

**Recording rule:** All discovered issues that are out of scope for the current task must be mentioned to the user and recorded in the project's `AGENTS.md` under `## Follow-ups`. Don't just mention them in chat and let them disappear — record them so the user can decide whether to act on them now or later. Once a follow-up is resolved, delete it from the list. See [references/follow-ups-example.md](references/follow-ups-example.md) for format and examples.

**Agent context files:** `AGENTS.md` is the project's operating contract; `CLAUDE.md` is a one-line pointer to it: "Read `AGENTS.md` before doing any project work." When initializing project docs (e.g. `/init`) or asked to create or update `CLAUDE.md`, write the actual content into `AGENTS.md` and keep `CLAUDE.md` as the pointer — create either file if missing.

The test: Every changed line should trace directly to the user's request.

### 4. Testing Strategy (Test-First + scoped TDD)

**All changes and features must have meaningful tests. No test = not done.**

Baseline rule:

- Every behavior-changing change needs test coverage.
- For small, local, low-risk fixes, add/update tests around the change (before or immediately after implementation is acceptable if justified).
- For large changes, broad-scope changes, or major new features, you MUST apply TDD: write the failing test first, then implement — don't write code and backfill tests.

判斷大改動的指標（任一符合即可）：

1. 觸及多個模組或層級（例如 UI、API、資料層同時調整）。
2. 變更公開行為邊界，如 API 契約、資料模型、存取規則、核心流程。
3. 新增核心新功能，或重構高風險路徑（付款、認證、權限、資料遷移、狀態轉換）。

Rules:

- **Every bug fix must start with a test that reproduces the bug.**
- **Before refactoring, confirm all tests pass. After refactoring, confirm again.**
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

1. Confirm the requirement, state assumptions, surface anything unclear (Principle 1).
2. List possible approaches, explain which you choose and why.
3. Define success criteria: what does "done" look like (Principle 5).
4. If tests exist, run them first to confirm they all pass.

### B. While Writing Code

Apply Principles 2–4: keep it simple, change only what the request requires, and use the TDD loop for TDD-scope work.

### C. After Completion

1. Run all tests, confirm they all pass.
2. Run linter / type checker (if the project has one).
3. Walk the Pre-Ship Checklist below.

---

## Pre-Ship Checklist

- [ ] Every changed line traces to the user's request — nothing was added that wasn't asked for.
- [ ] No abstractions for single-use code; code is simple, no more than required.
- [ ] All changes and features have corresponding tests; large or high-risk changes were implemented test-first (TDD).
- [ ] Bug fix has a test that reproduces the bug.
- [ ] All tests pass, and no test was weakened just to make it pass.
- [ ] Linter / type checker reports no errors.
