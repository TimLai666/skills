# Input And Gate

三個理論共用同一套輸入契約與資料充足性判定。

## Required Input

- `analysis_goal: string`
- `theories: string[]` — 本次要套用的理論，至少一個。合法值：`product_positioning` / `purchase_motivation` / `wom_motivation`
- `evidence_items: array<object>`
  - `item_id: string`
  - `content: string`
  - `content_type: string`

Optional:

- `source_type: string`
- `source_ref: string`
- `context_tags: string[]`

若使用者沒有指定 `theories`，依 `analysis_goal` 判斷：問「產品被怎麼看」用 `product_positioning`，問「為什麼買」用 `purchase_motivation`，問「為什麼分享」用 `wom_motivation`。判斷不出來就直接問使用者，不要預設全跑。

## Validation Rules

- `analysis_goal` 不可為空字串。
- `theories` 至少要有 1 個合法值，出現未定義的理論名稱時直接報錯，不要自創 taxonomy。
- `evidence_items` 至少要有 1 筆，且每筆至少要有可用的 `content`。
- `content` 應為可分析文字（原文、逐字稿、摘要皆可）。全為空白或只有符號視為不可用。
- 若證據僅有評分而無可分析內容，回傳缺資料，不要猜測。
- 若 `item_id` 重複，保留原值但在 `quality_checks.warnings` 註記重複風險。
- 若證據內容過短或只有單字評價，在 `quality_checks.warnings` 註記低訊號。

## Missing Data Output

缺資料時，輸出：

```json
{
  "missing_fields": ["analysis_goal", "evidence_items.content"],
  "why_needed": {
    "analysis_goal": "Needed to bound coding focus and prevent random interpretation.",
    "evidence_items.content": "Needed to produce auditable evidence quotes."
  },
  "questions_to_user": [
    "What decision should this coding support?",
    "Can you provide evidence items with stable item_id values and analyzable content?"
  ],
  "next_step_rule": "Do not code until required input is complete."
}
```

## Coverage Rule

覆蓋率**逐理論分別計算**，門檻也不同：

| family | 門檻 | 判定方式 |
| --- | --- | --- |
| `product_positioning` | 80% | 證據項目被任一定位構面標註 |
| `purchase_motivation` | 80% | 證據項目被 `functional` / `security` / `relational` 其中之一標註 |
| `wom_motivation` | 70% | 證據項目有可辨識動機，或有明確 `insufficient` 判斷 |

`wom_motivation` 門檻較低是理論特性——不是每則證據都帶分享意圖，硬要標滿反而是過度詮釋。

- 未達門檻時，`quality_checks.warnings` 必須說明原因，例如語料太短或噪音過高，並在摘要明確說出資料限制，不輸出過度結論。
- 某個理論覆蓋不足，不影響其他理論的結論，但要分開說明。
