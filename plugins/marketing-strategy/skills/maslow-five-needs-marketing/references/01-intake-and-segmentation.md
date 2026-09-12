# Intake and Segmentation

## 1) 核心資料與執行條件

| field | type | required | note |
| --- | --- | --- | --- |
| product_or_service | string | yes | 產品/服務描述與核心價值 |
| target_audience | string | yes | 受眾輪廓、購買場景與痛點 |
| offer | string | yes | 價值主張與成交主體 |
| goal_kpi | string[] | 執行／評估時 | 成功判準；數值目標依資料與需求設定 |
| time_horizon | string | 執行計畫時 | 執行期間與檢核節點 |

## 2) Optional Inputs

| field | type | required | note |
| --- | --- | --- | --- |
| budget | string | no | 預算區間與限制 |
| channels | string[] | no | 可用通路清單 |
| copy_goal | enum | no | 文案目的：awareness/consideration/conversion/retention |
| copy_channel | enum | no | 文案主通路：ad/landing-page/email/social/line |
| desired_emotion | enum | no | 情緒目標：trust/belonging/status/aspiration |
| copy_constraints | string[] | no | 文案限制：字數、禁用詞、法規、語氣邊界 |
| brand_tone | string | no | 品牌語氣限制 |
| constraints | string[] | no | 法規、素材、人力限制 |
| proof_assets | string[] | no | 案例、評價、數據證據 |
| market_context | string | no | 市場趨勢與季節性 |
| competition_context | string | no | 競品動態與定位 |

## 3) Segmentation Checklist

- 人口層：年齡、職業、收入、地區。
- 行為層：購買頻率、使用情境、替代方案。
- 心理層：動機、焦慮、身份訴求、價值觀。
- 風險層：價格敏感度、信任門檻、轉換阻力。

## 4) Copy Brief Minimum (Optional but Recommended)

- 文案方向需理解用途與通路；`desired_emotion` 可以是五層分析後的結論，不要求使用者先指定。
- 先從現有資料確認，只有缺口會改變方向或妨礙交付時才提問。
## 5) Data Sufficiency Gate

依[主檔的資料充分性規則](../SKILL.md#data-sufficiency-gate)判斷是否需要提問。只做訊息方向時，不要求數值 KPI 與期間；完整執行方案需確認影響可行性的條件。需要結構化回覆時，可用以下 `MissingDataOutput`，一般對話直接問關鍵問題。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "補齊影響決策的關鍵資訊，其他可獨立分析的部分繼續"
}
```

## 6) Non-Guessing Rule

- 不可自行捏造受眾特徵、成效數據、通路限制。
- 不確定資訊必須標記 `Assumption`，並附 `Validation Needed`。
