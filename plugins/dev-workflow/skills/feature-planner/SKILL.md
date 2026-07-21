---
name: feature-planner
description: "Plan a feature before building. Brainstorm the idea, challenge scope, and lock decisions one at a time. Triggers on: 幫我想這個功能, 幫我規劃, 這個怎麼做, 幫我想一下, feature planning, planning mode, 規劃一下, 做這個功能之前先想清楚"
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
  version: "1.0.0"
---

## Auto-trigger

When the user describes something they want to build, is thinking about a new feature, or says anything that implies "I need to plan this before coding", activate this skill automatically. Do not wait for an explicit command.

---

## Core rules

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

The plan document lives at `~/.mystack/projects/<slug>/<date>-<branch>-<feature>-plan.md`.

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
# Feature Plan: [feature name]
_Created: [date] - feature-planner - [repo]:[branch]_

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
Run eng-architect to lock architecture and build convergence artifacts.
```

---

## Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"feature-planner\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
