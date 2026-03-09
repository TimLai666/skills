# Intake And Scope Gate

## Goal

在任何評論分析前，先確認資料與任務是否足以支持結論。

## Minimum Inputs

- `review_text`
- 明確分析目標，至少一種：
  - 找痛點
  - 找滿意驅動因子
  - 比較兩組以上評論
  - 產出行動建議

## Recommended Inputs

- `created_at`
- `rating`
- `product`
- `channel`
- `locale`
- `segment`
- `version`

## Gate Decisions

### Proceed

可進入分析的條件：
- 有實際評論文本
- 任務目標清楚
- 樣本量足夠支持所要求的結論層級

### Proceed With Limits

資料不足但仍可做探索性分析：
- 樣本很小，但使用者只要初步觀察
- 缺少時間或渠道欄位，無法做比較，只能做整體摘要
- 缺少評分欄位，仍可做主題與證據整理

### Stop And Return MissingDataOutput

以下情況不要硬做：
- 沒有 `review_text`
- 不知道要分析什麼問題
- 使用者要求比較，但缺少可比較欄位或分組資訊
- 使用者要求趨勢判讀，但沒有時間資訊且樣本不足

## MissingDataOutput

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "next_step_rule": "補齊最低必要資訊後再進入評論探勘。"
}
```

## Example

```json
{
  "missing_fields": ["review_text", "analysis_goal"],
  "why_needed": {
    "review_text": "沒有原始評論就無法做任何主題或證據分析",
    "analysis_goal": "不知道是要找痛點、比較版本，還是整理行動建議"
  },
  "questions_to_user": [
    "請提供評論原文或檔案",
    "請指定本次分析要回答的主要問題"
  ],
  "temporary_assumptions": [],
  "next_step_rule": "補齊後再分析"
}
```
