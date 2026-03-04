# Intake and Mode Selection

## 1) 先收斂任務背景

輸入前先蒐集以下資訊：

- 提案情境：`internal`、`fundraising`、`partnership`
- 決策對象：主管、投資人、合作夥伴
- 決策門檻：希望對方批准什麼（資源、預算、合作、投資）
- 時間壓力：何時要提案、何時要結果
- 可用證據：市場資料、客戶資料、財務資料、實驗資料

## 2) 模式選擇規則

- 使用者只有題目、方向、零散資料 -> `mode=generate`
- 使用者提供既有企劃或要求改稿 -> `mode=review`
- 使用者同時要「先寫再改」 -> 先 `generate` 後 `review`

## 3) 欄位標準化

| field | type | required | note |
| --- | --- | --- | --- |
| proposal_type | string | yes | internal/fundraising/partnership |
| industry | string | yes | 產業與市場邊界 |
| target_customer | string | yes | 決策單位與使用者角色 |
| problem_statement | string | yes | 一句話痛點定義 |
| available_data | object/list | yes | 來源、期間、樣本數 |
| budget | number/string | no | 沒有時需標示假設 |
| timeline | string | no | 例如 3、6、12 個月 |
| goal_kpi | list | yes | KPI + 門檻 |
| mode | string | no | generate/review |

## 4) 缺資料時的處理

- 不中止流程，但必須在輸出中標示：
  - `Assumption`：當前假設值
  - `Validation Needed`：需要補齊的資料與負責人
  - `Risk`：若假設錯誤的影響

## 5) 任務起始句模板

可用以下句型啟動：

- 生成模式：
  - 「以下依據既有資料建立假設版企劃，已標示需驗證欄位。」
- 審稿模式：
  - 「先給決策風險最高的缺陷，再提供逐段重寫版本。」
