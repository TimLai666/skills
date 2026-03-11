---
name: customer-journey-mapper
description: Use when a customer journey map, CJM, or touchpoint-based purchase journey must be designed from a customer persona and product or service, especially when the user mentions 顧客旅程地圖, Customer Journey Map, CJM, 顧客輪廓, 接觸點, or 關鍵時刻.
---

# Customer Journey Mapper

## Overview

Create a complete customer journey map in Traditional Chinese from the customer's point of view.

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

- the user wants a customer journey map or CJM
- the task starts from a customer persona and a product or service
- the user wants stages, touchpoints, emotions, key moments, marketing methods, or service ideas arranged into one journey
- the output should be practical for proposals, workshops, internal strategy, or coursework

Do not use this skill when:

- the task is only a persona profile with no journey
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

Default assumptions:

- produce one core persona journey, not multiple persona versions
- if the user provides custom stages, use them
- otherwise use the fixed five stages in this skill

## Data Sufficiency Gate

If both required inputs are clear enough, generate the table directly.

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

1. Read the persona and the product or service.
2. Infer or confirm the purchase and use context.
3. Build the journey from the customer's point of view, not the brand's point of view.
4. Fill the five stages in order unless the user supplied different stages.
5. Write `動機` before `行動` in every stage.
6. Make `科技服務`, `行銷方法`, and `目標` logically connected.
7. Do a final check for format, language, and customer viewpoint.

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

Use `$customer-journey-mapper` to create a complete customer journey map in Traditional Chinese from `顧客輪廓` and `產品或服務`, using a transposed Markdown table where `動機` appears before `行動`.
