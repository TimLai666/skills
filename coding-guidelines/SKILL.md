---
name: coding-guidelines
version: 1.0.0
description: "Behavioral guidelines for writing code. Think before coding, simplicity first, surgical changes, TDD, verifiable success criteria. Triggers on: 寫 code, 改 code, 做功能, 修 bug, refactor, 開發, coding, development, 實作, 實現, 寫程式, 改程式, 加功能, 修問題"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
---

## Auto-trigger

**Any code writing or code changing work must load this skill first.** Whether it's a new feature, bug fix, refactor, or code review — if you're touching code, read this first.

---

## Core Principles

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

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
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. TDD (Test-Driven Development)

**All changes and features must have corresponding tests. No test = not done.**

Cycle:
```
1. Write a failing test (define expected behavior)
2. Write minimum code to make the test pass
3. Refactor, ensure tests still pass
4. Repeat
```

Rules:
- **Write the test first, then implement.** Don't write code and backfill tests.
- **Every bug fix must start with a test that reproduces the bug.** Test passes after fix.
- **Every new feature must have a corresponding test.** Feature without test coverage is not done.
- **Before refactoring, confirm all tests pass.** After refactoring, confirm again.
- **Don't weaken a test just to make it pass.** Unless the test itself is wrong.
- Tests must prove the change works, not just inflate coverage numbers.

### 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

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

1. Confirm you understand the requirement. Ask if unclear.
2. State assumptions and constraints.
3. List possible approaches, explain which you choose and why.
4. Define success criteria: what does "done" look like.
5. If existing tests exist, run them first to confirm they all pass.

### B. While Writing Code

1. **TDD loop**: red → green → refactor.
2. Every change must trace back to a requirement.
3. Don't touch what you shouldn't.
4. Keep code simple, no more than required.
5. Match existing code style.

### C. After Completion

1. Run all tests, confirm they all pass.
2. Run linter / type checker (if the project has one).
3. Check: can every changed line trace back to a requirement?
4. Check: did you accidentally touch something you shouldn't have?
5. Check: is the code simple enough? Would a senior engineer call it overcomplicated?

---

## Common Pitfalls

- **Gold plating**: adding features not asked for because it was "easy."
- **Premature abstraction**: extracting shared logic that only appears once.
- **Defensive coding for impossible scenarios**: error handling for errors that can't happen.
- **Refactoring unrelated code**: changing A while "cleaning up" B, breaking B.
- **Test-after**: writing code first then backfilling tests that only test the surface.
- **Making test pass by weakening assertion**: failing test → change test instead of changing code.

---

## Pre-Ship Checklist

- [ ] Every changed line traces to a user's request.
- [ ] Nothing was added that wasn't asked for.
- [ ] No abstractions for single-use code.
- [ ] All changes and features have corresponding tests.
- [ ] Test was written before implementation.
- [ ] Bug fix has a test that reproduces the bug.
- [ ] All tests pass.
- [ ] Linter / type checker reports no errors.
- [ ] Code is simple, no more than required.
