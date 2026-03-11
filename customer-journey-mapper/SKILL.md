---
name: customer-journey-mapper
description: Use when the final customer journey map, CJM, or touchpoint-based journey table must be produced from a completed persona, product or service, or a `handoff_to_customer_journey_mapper` block, especially when the user asks for 顧客旅程地圖, CJM, final journey table, or wants prior persona/framing work turned into the finished map.
---

# Customer Journey Mapper

## Overview

Create the final customer journey map in Traditional Chinese from the customer's point of view.
This skill is downstream of persona definition and journey-framing work.
If no completed persona is available yet, stop and use `customer-persona-framer` first.

Default output is one Markdown table in transposed vertical form:
`項目 | 認知 | 考慮/研究 | 決策/購買 | 使用 | 關係建立`

The row order is fixed:

1. `動機`
2. `行動`
3. `情緒`
4. `（服務）接觸點`
5. `感受/關鍵時刻`
6. `科技服務`
7. `行銷方法`
8. `目標`

`動機` must always appear before `行動`.

## When To Use

Use this skill when:

- the user wants the finished customer journey map or CJM table itself
- the task already has a clear persona and a product or service
- the task includes a `handoff_to_customer_journey_mapper` block from upstream framing work
- the user wants stages, touchpoints, emotions, key moments, marketing methods, or service ideas arranged into one final journey table
- the output should be practical for proposals, workshops, internal strategy, or coursework

Do not use this skill when:

- the task is only a persona profile, 人物誌, 顧客輪廓, or target audience definition with no final journey map
- the task is only 5W1H, touchpoint discovery, or journey pre-analysis; use `customer-persona-framer`
- no completed persona is provided yet; use `customer-persona-framer` first, then return with the persona or `handoff_to_customer_journey_mapper`
- the task is only a funnel KPI dashboard with no customer narrative
- the user wants a service blueprint with backstage operations; this skill is customer-facing only

## Input Contract

Required:

- `顧客輪廓`
- `產品或服務`

Optional:

- `品牌/產業背景`
- `目標市場`
- `目前接觸點`
- `輸出用途`
- `handoff_to_customer_journey_mapper`

If `handoff_to_customer_journey_mapper` is present:

- treat the block as authoritative input
- do not re-ask fields that are already present
- let explicit user overrides outside the block win over the handoff block

Default assumptions:

- produce one core persona journey, not multiple persona versions
- if the user provides custom stages, use them
- otherwise use the fixed five stages in this skill

## Data Sufficiency Gate

If both required inputs are clear enough, generate the table directly.
If no completed persona is available, do not draft the final map yet.
Route the work to `customer-persona-framer` first.

If a `handoff_to_customer_journey_mapper` block contains at least `顧客輪廓` and `產品或服務`, generate directly from the handoff.

If information is missing and the user did not ask for speed:

- ask concise follow-up questions first
- do not generate the final map yet

If information is missing and the user asks for a quick draft, for example:

- `先做一版`
- `快速版`
- `可先假設`
- `直接幫我生成`

Then:

1. list `3-5` assumptions first
2. generate the full table after the assumptions
3. keep the assumptions concrete and business-relevant

## Stage Policy

Default stages:

- `認知`
- `考慮/研究`
- `決策/購買`
- `使用`
- `關係建立`

If the user explicitly defines different stages, respect the user-defined stages and preserve the same row order.

## Output Contract

Always answer in Traditional Chinese.

Preferred format:

- one Markdown table
- transposed vertical layout
- stages as column headers
- fixed row order as below

```md
| 項目 | 認知 | 考慮/研究 | 決策/購買 | 使用 | 關係建立 |
|---|---|---|---|---|---|
| 動機 |  |  |  |  |  |
| 行動 |  |  |  |  |  |
| 情緒 |  |  |  |  |  |
| （服務）接觸點 |  |  |  |  |  |
| 感受/關鍵時刻 |  |  |  |  |  |
| 科技服務 |  |  |  |  |  |
| 行銷方法 |  |  |  |  |  |
| 目標 |  |  |  |  |  |
```

## Workflow

1. Read the direct inputs and any `handoff_to_customer_journey_mapper` block.
2. Normalize the effective inputs, using explicit user overrides over handoff values.
3. Read the persona and the product or service.
4. Infer or confirm the purchase and use context.
5. Build the journey from the customer's point of view, not the brand's point of view.
6. Fill the five stages in order unless the user supplied different stages.
7. Write `動機` before `行動` in every stage.
8. Make `科技服務`, `行銷方法`, and `目標` logically connected.
9. Do a final check for format, language, and customer viewpoint.

## Quality Rules

- use customer voice and customer logic
- avoid brand slogans or empty marketing claims
- make each cell specific enough to act on
- let `情緒` show a real state or state change
- let `感受/關鍵時刻` describe the moment that changes momentum
- make `科技服務` an enabler, not a vague buzzword
- make `行銷方法` match the stage and touchpoint
- make `目標` describe what the service or marketing action is trying to achieve
- do not fall back to a horizontal table where each stage is a row
- if the input is persona-only or framing-only, do not force a final table; route the work to `customer-persona-framer`

## Short Example

Input:

- `顧客輪廓`: 忙碌上班族，重視健康但沒時間準備午餐
- `產品或服務`: 健康便當訂閱服務

Output shape:

```md
| 項目 | 認知 | 考慮/研究 | 決策/購買 | 使用 | 關係建立 |
|---|---|---|---|---|---|
| 動機 | 想找省時又健康的午餐方案 | 想確認價格與口味是否值得 | 想低風險試用避免踩雷 | 想驗證是否真的方便好吃 | 想找到可長期依賴的午餐解法 |
| 行動 | 搜尋健康便當資訊 | 比較方案與評價 | 下單試吃 | 收餐並食用 | 回購與推薦 |
```

## Suggested Prompt

Use `$customer-journey-mapper` to create the final Traditional Chinese customer journey map from `顧客輪廓` and `產品或服務`, or from a `handoff_to_customer_journey_mapper` block, using a transposed Markdown table where `動機` appears before `行動`.
