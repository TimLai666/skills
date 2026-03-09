---
name: customer-review-mining
description: Use when analyzing customer reviews, survey comments, support tickets, app store feedback, or social replies to identify pain points, compare segments, generate corpus-level scoring items, or summarize customer perception for product, service, and messaging decisions.
---

# Customer Review Mining

## Overview

把大量評論轉成可行動洞察。預設輸出以商業決策可讀性為主，理論分析與動態評分題項作為第二層補充，只有在需要時才展開完整結構化附錄。

核心原則：
- 先做資料充分性檢查，再做分析
- 先用三大商業主題整理，再補理論與評分題項
- 評分題項必須從整批評論中萃取，不可預設寫死
- 理論可由其他 skill 或 agent 輔助，但只在需要時才啟用

## When to Use

Use when:
- 需要從評論找出主要痛點、滿意驅動因子與優先改善方向
- 需要比較不同產品、版本、渠道、地區或客群的評論差異
- 需要把質性回饋整理成產品、客服、營運或行銷可執行建議
- 需要從整批評論中提煉一組共用評分題項，再回頭對每則評論做一致化評分
- 需要在商業摘要之外，加上理論視角或請 agent 協助做更深的解釋

Do not use:
- 沒有實際評論文本，只想憑空推論顧客感受
- 需要嚴格因果推論、統計檢定或正式學術方法論
- 只想做單句情緒分類，不需要主題、優先級或題項生成

Handoff:
- 若要把洞察改寫成訊息策略或文案 brief，可交給 `$copywriting`
- 若要把洞察轉成追蹤與 KPI 設計，可交給 `$analytics-tracking`
- 若要把洞察轉成實驗假設與測試設計，可交給 `$ab-test-setup`
- 若需要更深的理論詮釋，可視需求讓 agent 使用其他相關 skill 輔助，但不可讓外部 skill 取代本 skill 的主分析骨架

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
- 有評論但沒有分析目標：先界定是找痛點、找滿意驅動因子、比較差異，或產出建議
- 樣本極少：可做探索性觀察，不可宣稱趨勢
- 關鍵欄位缺失時仍可分析，但要明確標示限制

詳見 [references/01-intake-and-scope-gate.md](./references/01-intake-and-scope-gate.md)

## Analysis Model

### Primary Business Taxonomy

第一層分類固定只用三大主題：
- `service_experience`
- `product_performance`
- `value_perception`

這一層決定預設報告與優先級排序。不要讓理論標籤或動態題項取代這三個主題。

詳見 [references/02-theme-taxonomy.md](./references/02-theme-taxonomy.md)

### Theory Overlay

第二層是理論輔助視角，用來補充解釋評論，不用來取代證據或主題表：
- Product Positioning Theory
- Purchase Motivation Theory
- Maslow's Hierarchy of Needs
- Word-of-Mouth Motivation Theory

理論使用規則：
- 預設先完成本 skill 的主分析
- 只有在使用者要求更深理論框架、跨模型對照或外部專業輔助時，才條件式請 agent 使用其他 skill
- 理論摘要必須附評論證據，不可只列概念名詞
- 不可讓理論部分壓過商業輸出

詳見 [references/03-theory-overlay-map.md](./references/03-theory-overlay-map.md)

### Corpus-Derived Scorecard

第三層是動態評分題項。題項必須先從整批評論中萃取，再以同一組題項回頭評分每則評論。

流程固定如下：
1. 從整批評論抽取候選題項
2. 合併同義詞、重複描述與近似概念
3. 為每個題項定義短標籤、定義與證據線索
4. 用同一組題項對每則評論做 `0-7` 分評分

評分規則：
- `0`: 沒提到或沒有足夠證據
- `1-3`: 間接、輕微、模糊提及
- `4`: 中立、保留或正反混雜
- `5-6`: 明確提及
- `7`: 強烈且完整表達

題項規則：
- 題項必須來自重複評論訊號，而不是單一句話
- 僅被單一孤立評論支持的題項，預設標成 `exploratory`，不納入核心分數集
- 題項名稱必須可比較、可聚合、可回溯
- 不可每個評論各自生成不同題項集合

詳見 [references/04-dynamic-item-generation-and-scoring.md](./references/04-dynamic-item-generation-and-scoring.md)

## Workflow

1. 定義任務與比較範圍
- 重述分析目標
- 鎖定比較維度，例如時間、版本、地區、產品、渠道、客群

2. 執行資料充分性檢查
- 套用 Data Sufficiency Gate
- 缺欄位或樣本過小時先回報限制

3. 清理與標準化文本
- 去除空白、重複、廣告與無意義文字
- 保留 `raw_text` 與 `clean_text`
- 多語資料先分語言再整併

4. 進行第一層主題分析
- 先分類到三大主題
- 整理子主題、代表性引文與大致佔比

5. 生成共用評分題項
- 從整批評論抽候選題項
- 做動態正規化與命名
- 標出核心題項與 `exploratory` 題項

6. 回頭評分每則評論
- 使用同一組題項做 `0-7` 分評分
- 匯總成題項層級的統計摘要

7. 視需要補理論分析
- 預設只補最有用的 1-3 個理論視角
- 若使用者要更深研究型輸出，可條件式請 agent 使用其他 skill 輔助

8. 產出建議
- 先寫管理摘要
- 再列主題表、動態題項摘要與優先行動
- 只有在使用者要求結構化輸出時，才展開完整 JSON 附錄

## Output Contract

預設輸出順序：
1. `Executive Summary`
2. `Theme Analysis Table`
3. `Priority Actions`
4. `Risks / Bias / Confidence Notes`

選配輸出：
5. `Dynamic Item Set Summary`
6. `Dynamic Scorecard Summary`
7. `Theory Coding Summary`
8. `Appendix (JSON)`

### Primary Output Rules

`Executive Summary`
- 2-5 點結論
- 每點都要可回溯到評論證據
- 不要用理論名詞塞滿摘要

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

`Dynamic Item Set Summary`
- 列出本次分析產生的共用題項
- 每個題項至少附：`label`, `definition`, `evidence_cues`, `status`
- `status` 僅能是 `core` 或 `exploratory`

`Dynamic Scorecard Summary`
- 呈現高分與低分題項
- 標示題項覆蓋率、平均分與低信心題項

`Theory Coding Summary`
- 只總結最有解釋力的理論視角
- 每個視角至少附 1 句代表性評論或摘要證據
- 若本次有 agent 使用其他 skill 協助，需標示該協作是條件式加值，不是主分析來源

`Appendix (JSON)`
- 只有使用者要求結構化輸出時附上

```json
{
  "analysis_scope": {},
  "theme_analysis": [],
  "generated_items": [],
  "scorecard_summary": [],
  "priority_actions": [],
  "theory_coding_summary": [],
  "evidence": []
}
```

詳見 [references/05-output-template-and-quality-checklist.md](./references/05-output-template-and-quality-checklist.md)

## Hard Rules

- 不可臆測不存在的欄位、分數或比較維度
- 不可用單一評論宣稱整體趨勢
- 不可做無證據支撐的因果推論
- 不可因為套了理論標籤，就跳過引文或證據
- 不可使用寫死的固定題項集合
- 不可每個評論各自生成不同的評分題項集合
- 不可把低頻孤立訊號偽裝成核心題項
- 預設使用繁體中文，語氣專業、精簡、可執行

## References

- [references/01-intake-and-scope-gate.md](./references/01-intake-and-scope-gate.md)
- [references/02-theme-taxonomy.md](./references/02-theme-taxonomy.md)
- [references/03-theory-overlay-map.md](./references/03-theory-overlay-map.md)
- [references/04-dynamic-item-generation-and-scoring.md](./references/04-dynamic-item-generation-and-scoring.md)
- [references/05-output-template-and-quality-checklist.md](./references/05-output-template-and-quality-checklist.md)

## Validation Assets

- [agents/pressure-scenario-01-business-mode.md](./agents/pressure-scenario-01-business-mode.md)
- [agents/pressure-scenario-02-theory-mode.md](./agents/pressure-scenario-02-theory-mode.md)
- [agents/pressure-scenario-03-missing-data-and-overclaim.md](./agents/pressure-scenario-03-missing-data-and-overclaim.md)
- [agents/validation-checklist.md](./agents/validation-checklist.md)
