---
name: plan-grilling
description: "Grill a plan before anyone commits to it — a feature, a campaign, a proposal, a process change, a personal decision. Reframes the problem, challenges the scope, and locks decisions one at a time. This skill MUST be invoked on the triggers below, and SHOULD be invoked whenever the user thinks aloud about something they want to build, launch, or decide. MUST NOT be skipped because the plan already sounds settled — a plan that sounds settled is exactly where unexamined decisions hide. Triggers on: 幫我規劃, 規劃一下, 幫我想一下, 這個怎麼做, 逼問我, 壓力測試這個計畫, 幫我想這個功能, grill me, planning mode, 動手之前先想清楚"
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
  version: "2.0.0"
---

## What this covers

Any plan that someone is about to commit resources to. A feature, a marketing
campaign, a proposal, a process change, a hiring decision, a personal call.
The interview is the same in every case: find the real pain, reframe it,
challenge the scope, and force every implicit decision into the open.

Nothing here is specific to writing code. The one part that is — handing off to
`eng-architect` at the end — is marked as conditional and skipped for
everything else.

## Auto-trigger

When the user describes something they want to build, launch, change, or
decide, or says anything that implies "I need to think this through before I
start", activate this skill automatically. Do not wait for an explicit command.

---

## Core rules

### Ask about decisions, look up facts

If an answer can be found by reading the files, the config, the git history, or
by running a command, go and find it. Do not spend the user's turn on something
you could have looked up yourself.

The decisions are theirs. Put every one of those to them and wait.

### One question at a time

Never batch multiple questions. Ask one question, wait for the answer, record it, then move to the next.

### Multiple choice with recommendation

Every question must be:
1. A clear question in plain language
2. 2-4 concrete options (A, B, C...)
3. One option marked as **RECOMMENDED** with a one-line reason
4. The agent's recommendation is based on the context gathered so far

### Record every decision immediately

After each answer, append the decision to the plan document before asking the next question. Format:

```markdown
## Decision: [question topic]
- **Chose:** [selected option]
- **Rejected:** [other options with one-line reason why]
- **Timestamp:** [ISO-8601]
```

### Where the plan document goes

Wherever the user says. They may already have a home for this kind of document —
a `planning/` folder, an existing docs tree, a vault outside the repo. If they
name one, use it and do not talk them out of it.

Only when they have not said anything, default to `docs/plans/` inside the repo.
Resolve the directory once at the start and reuse it for the rest of the session.

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
_BRANCH=$(git branch --show-current 2>/dev/null | tr '/' '-')
[ -z "$_BRANCH" ] && _BRANCH="no-branch"
if [ -n "$_ROOT" ]; then
  mkdir -p "$_ROOT/docs/plans"
  echo "PLAN: $_ROOT/docs/plans/$(date +%Y-%m-%d)-$_BRANCH-<slug>-plan.md"
else
  echo "PLAN: none"
fi
```

The directory is negotiable, the filename is not. Keep the
`<date>-<branch>-<slug>-plan.md` shape wherever the file lands — `eng-architect`
locates the plan by globbing that shape, so a file named any other way is a file
it will not find.

`PLAN: none` means this is not a git repo — a standalone campaign or a personal
decision, for instance. Ask the user where the plan should go. Do not pick a
location yourself and do not write outside their project.

---

## Phase 1 — Understand the pain

Ask at most 3 of these, one at a time:

1. **Pain sharpness** — 「你上次遇到這個問題是什麼時候？給我一個具體的例子，不要假設情境。」
2. **Who suffers** — 「誰有這個問題？能不能說出具體的人，而不是一個類型？」
3. **Current workaround** — 「他們現在怎麼做？為什麼不夠好？」

After these answers, reframe:
- State 2-3 things the user did not realize they were describing
- State 1-2 assumptions that might be wrong and what breaks if they are
- State 1 completely different frame for the problem

Record the reframe. Get agreement before continuing.

---

## Phase 2 — Scope challenge (CEO review)

Ask the user to pick a scope mode — **this is the only batch question allowed**:

> 我讀完你的想法了。在進入細節之前，我想先確認 scope。
>
> **RECOMMENDED: C** — 你的描述聽起來 pain 是確認過的，先把核心功能做對最重要。
>
> A) **擴大 scope** — 找出隱藏的 10 星版本，每個擴大都是一次獨立確認
> B) **選擇性擴大** — 保持 baseline，但列出值得考慮的擴展
> C) **hold scope** — 把現有 plan 做到滴水不漏，不加不減
> D) **縮減 scope** — 砍到最小可學習版本

Record the mode selection.

Then go through these 10 sections **one at a time**, asking one question per section only when the answer is not already clear from context:

| # | Section | What to check | Ask only if... |
|---|---------|---------------|----------------|
| 1 | Problem clarity | 痛點具體嗎？ | pain 還是模糊的 |
| 2 | Who it's for | 是真的人嗎？ | 還沒有具體對象 |
| 3 | Scope in | 每個項目都直接解決問題嗎？ | scope 需要調整 |
| 4 | Scope out | 有「不做」清單嗎？ | 還沒有明確排除 |
| 5 | Success metric | 兩週內能量嗎？ | 還沒定義成功 |
| 6 | Assumptions | 最關鍵的假設是什麼？ | 有未驗證的高風險假設 |
| 7 | 10-star version | 做到極致長什麼樣？ | user 想知道上限 |
| 8 | Minimum version | 最小能學到東西的版本？ | scope 太大需要縮 |
| 9 | Failure modes | 最可能殺掉這件事的是什麼？ | 還沒盤點風險 |
| 10 | Recommendation | SHIP / REVISE / RECONSIDER | — (always ask) |

For each section:
- If the answer is already clear from context, skip silently and record `[already addressed]`
- If not clear, ask one question with options and a recommendation
- Record the decision immediately

---

## Phase 3 — Write plan document

After all decisions are recorded, write the final plan document:

```markdown
# Plan: [what is being planned]
_Created: [date] - plan-grilling - [repo]:[branch]_

## Problem
[2-3 sentences: the real pain, who has it, why now]

## Reframe
[What the user said vs. what they were actually describing]

## Scope decisions
### Chosen scope
- [item] - reason

### Explicitly out
- [item] - reason

### Deferred
- [item] - reason

## Assumptions to validate
- [assumption] - risk if wrong: [consequence]

## Success metric
[Measurable, 2-week horizon]

## Failure modes
- [risk] - mitigation: [what to do]

## Decisions log
[All recorded decisions from Phase 1-2]

## Next step
[One action, and only one.]
```

For development work, that next step is `eng-architect` — it reads this file to
lock architecture and build the convergence artifacts. It ships in the
`dev-workflow` plugin, so only name it once you have confirmed the user has that
plugin installed. For everything else, write the single action that moves this
plan forward.
