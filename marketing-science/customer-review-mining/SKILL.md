---
name: customer-review-mining
description: Use when analyzing customer reviews, survey comments, support tickets, app store feedback, or social replies to identify pain points, compare segments, or summarize customer perception for product, service, and messaging decisions.
---

# Customer Review Mining

## Overview

將大量評論轉成可行動洞察。預設輸出以商業決策可讀性為主，理論編碼與 14 題項評分作為第二層分析框架，只有在需要時才展開完整附錄。

核心原則：
- 先有證據，再有結論
- 先做資料充分性檢查，再做分析
- 先給管理可用摘要，再補理論與結構化細節

## When to Use

Use when:
- 需要從評論找出主要痛點、抱怨原因、滿意驅動因子
- 需要比較不同產品、版本、渠道、地區或客群的評論差異
- 需要把質性回饋整理成產品、客服、營運或行銷可執行建議
- 需要在商業摘要之外，補上理論編碼、需求層次或口碑動機視角

Do not use:
- 沒有實際評論文本，只想憑空推論顧客感受
- 需要嚴格因果推論、統計檢定或學術研究設計
- 只需要單純情緒分類，不需要主題、優先級或行動建議

Handoff:
- 若需要把洞察改寫成文案方向或訊息測試 brief，交給 `$copywriting`
- 若需要追蹤方案、事件命名或 KPI 實作，交給 `$analytics-tracking`
- 若需要實驗設計或變體假設，交給 `$ab-test-setup`

## Input Contract

最低需求：
- `review_text`: `string`

建議欄位：
- `created_at`: `string`
- `rating`: `number`
- `product`: `string`
- `channel`: `string`
- `locale`: `string`
- `segment`: `string`
- `version`: `string`

可接受格式：
- `CSV`
- `JSON`
- 純文字清單

規模建議：
- `20` 到 `20,000` 則評論可直接分析
- 超過 `20,000` 則先分批、抽樣或分群

## Data Sufficiency Gate

若缺少最低分析條件，先回傳 `MissingDataOutput`，不要直接下結論。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "next_step_rule": "只有在 review_text 與分析目標足夠清楚時才進入評論探勘。"
}
```

Gate 規則：
- 沒有 `review_text`：停止分析
- 有評論但沒有分析目標：先要求界定要找痛點、比較對象或追蹤期間
- 樣本極少：可做觀察，不可宣稱趨勢
- 關鍵欄位缺失時可分析，但要明確標示侷限

詳見 [references/01-intake-and-scope-gate.md](./references/01-intake-and-scope-gate.md)

## Analysis Model

### Primary Business Taxonomy

第一層分類固定只用三大主題：
- `service_experience`
- `product_performance`
- `value_perception`

這一層決定預設報告與優先級排序。不要讓理論標籤取代這三個主題。

詳見 [references/02-theme-taxonomy.md](./references/02-theme-taxonomy.md)

### Theory Overlay

第二層是理論輔助視角，用來解釋評論，不用來取代證據：
- Product Positioning Theory
- Purchase Motivation Theory
- Maslow's Hierarchy of Needs
- Word-of-Mouth Motivation Theory

理論用途：
- 幫助整理評論在說哪一種價值、需求或分享動機
- 幫助補充研究型輸出或 appendix
- 不可直接把理論名稱當作結論

詳見 [references/03-theory-overlay-map.md](./references/03-theory-overlay-map.md)

### 14-Item Scorecard

第三層是結構化評分，只在有明確語意證據時使用。每題 `0-7` 分：
- `0`: 沒提到
- `1-3`: 間接或輕微提及
- `4`: 中立、模糊或有保留
- `5-6`: 明確提及
- `7`: 強烈且完整表達

14 題項：
- 運送快速
- 包裝品質
- 容易溝通
- 顧客支持
- 解決問題
- 信任賣家
- 再購意願
- 尺寸適配
- 容易安裝
- 外觀設計
- 品質良好
- 符合預期
- 高 CP 值
- 與描述一致

詳見 [references/04-scoring-rubric-14-items.md](./references/04-scoring-rubric-14-items.md)

## Workflow

1. 定義任務與比較範圍
- 重述分析目標
- 鎖定比較維度，例如時間、版本、地區、產品、渠道、客群

2. 執行資料充分性檢查
- 套用 Data Sufficiency Gate
- 缺欄位或樣本過小時先回報限制

3. 清理與標準化文本
- 去除空白、重複、廣告、無意義文字
- 保留 `raw_text` 與 `clean_text`
- 多語資料先分語言再整併

4. 進行三層分析
- 第一層：分類到三大主題
- 第二層：補充理論視角
- 第三層：必要時做 14 題項評分

5. 量化與排序
- 至少計算 `count`、`share`
- 若有情緒或嚴重度訊號，可補 `negative_rate`、`avg_severity`
- 若做優先級排序，可用 `impact_score = count * avg_severity * business_weight`
- 沒有足夠資訊時計算簡化版優先級，但要標示假設

6. 產出建議
- 先寫管理摘要
- 再列主題表與優先行動
- 只有在使用者要求研究型或結構化輸出時，才展開理論摘要與 JSON 附錄

## Output Contract

預設輸出順序：

1. `Executive Summary`
2. `Theme Analysis Table`
3. `Priority Actions`
4. `Risks / Bias / Confidence Notes`

選配輸出：

5. `Theory Coding Summary`
6. `14-Item Scorecard Summary`
7. `Appendix (JSON)`

### Primary Output Rules

`Executive Summary`
- 2-5 點結論
- 每點都要可回溯到評論證據

`Theme Analysis Table`
- 至少包含：`theme`, `subtheme`, `count`, `share`, `sample_quote`
- 若資料足夠，可加：`negative_rate`, `avg_severity`, `impact_score`

`Priority Actions`
- 只保留最值得做的 3-5 項
- 每項都要對應主題、原因、預期影響與衡量方式

`Risks / Bias / Confidence Notes`
- 樣本偏差
- 來源偏差
- 語言偏差
- 時間範圍限制
- 推論信心

### Secondary Output Rules

`Theory Coding Summary`
- 只總結最有解釋力的理論視角
- 每個視角至少附 1 句代表性評論或摘要證據

`14-Item Scorecard Summary`
- 呈現高分與低分題項
- 標示哪些題項因缺乏證據而未評分或低信心

`Appendix (JSON)`
- 只有使用者要求結構化輸出時附上

```json
{
  "analysis_scope": {},
  "theme_analysis": [],
  "priority_actions": [],
  "theory_coding_summary": [],
  "scorecard_summary": [],
  "evidence": []
}
```

詳見 [references/05-output-template-and-quality-checklist.md](./references/05-output-template-and-quality-checklist.md)

## Hard Rules

- 不可臆測不存在的欄位、分數或比較維度
- 不可用單一評論宣稱整體趨勢
- 不可做無證據支撐的因果推論
- 不可因為套了理論標籤，就跳過引文或證據
- 不可在證據不足時強行完成 14 題項評分
- 預設使用繁體中文，語氣專業、精簡、可執行

## References

- [references/01-intake-and-scope-gate.md](./references/01-intake-and-scope-gate.md)
- [references/02-theme-taxonomy.md](./references/02-theme-taxonomy.md)
- [references/03-theory-overlay-map.md](./references/03-theory-overlay-map.md)
- [references/04-scoring-rubric-14-items.md](./references/04-scoring-rubric-14-items.md)
- [references/05-output-template-and-quality-checklist.md](./references/05-output-template-and-quality-checklist.md)

## Validation Assets

- [agents/pressure-scenario-01-business-mode.md](./agents/pressure-scenario-01-business-mode.md)
- [agents/pressure-scenario-02-theory-mode.md](./agents/pressure-scenario-02-theory-mode.md)
- [agents/pressure-scenario-03-missing-data-and-overclaim.md](./agents/pressure-scenario-03-missing-data-and-overclaim.md)
- [agents/validation-checklist.md](./agents/validation-checklist.md)
