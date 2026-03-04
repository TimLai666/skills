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
| tone_profile | string | no | executive_formal/investor_formal/consulting_formal/gov_formal/auto |
| formality_level | string | no | standard/strict，預設 strict |
| audience | string | no | 受眾描述，用於覆寫語氣判斷 |

## 4) 核心阻斷欄位（Data Sufficiency Gate）

缺任一欄位即先問，不可直接生成正文：

- `proposal_type`
- `target_customer`
- `problem_statement`
- `goal_kpi`
- `available_data`

## 5) 缺資料時的回應格式

當核心欄位不足時，先輸出：

- `missing_fields`
- `why_needed`
- `questions_to_user`
- `no_data_options`（A/B/C/D）
- `next_step_rule`

不產生完整企劃正文。

## 6) 使用者明確表示無資料時（A/B/C/D 固定選單）

- **A. 最快假設版（當日）**：
  - 以通用假設建立草稿，所有假設必標註 `Assumption/Validation Needed/Risk`。
- **B. 輕量訪談驗證版（2-5 天）**：
  - 先盤點 3-5 位利害關係人訪談，再輸出。
- **C. 小規模數據蒐集後正式版（1-2 週）**：
  - 先取得最小可用數據，再產出對外版。
- **D. 客製方案**：
  - 由使用者指定時程/資料可得性/受眾後客製流程。

預設不自動替使用者選方案；未選擇前維持在提問狀態。

## 7) 語氣自動映射（混合策略）

若 `tone_profile=auto`：

1. 先依 `proposal_type` 預設：
   - `internal -> executive_formal`
   - `fundraising -> investor_formal`
   - `partnership -> consulting_formal`
2. 再以 `audience` 或 prompt 關鍵詞覆寫：
   - 政府、標案、審議、公部門、法遵 -> `gov_formal`
   - 董事會、管理層、經營會議 -> `executive_formal`
   - 投資人、VC、基金、IR -> `investor_formal`
   - 顧問、策略報告、MECE -> `consulting_formal`

若使用者明確指定 `tone_profile`，優先於自動映射。

## 8) 禁止幻想規則

- 不得臆測市場規模、轉換率、財務數字、KPI 基準。
- 不得把猜測當作事實句。
- 若採假設，需顯式標示 `Assumption` + `Validation Needed` + `Risk`。

## 9) 任務起始句模板

可用以下句型啟動：

- 缺資料提問模式：
  - 「目前缺少關鍵欄位，先補齊以下資訊後才能輸出正式版企劃。」
- 生成模式：
  - 「以下依據既有資料建立企劃；若屬假設已明確標註需驗證項。」
- 審稿模式：
  - 「先給決策風險最高的缺陷，再提供逐段重寫版本。」
- 正式版模式：
  - 「以下內容已依 `{{tone_profile_final}}` 語體與 `{{formality_level}}` 正式度規範完成潤飾。」