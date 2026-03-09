---
name: customer-review-mining
description: Use when analyzing customer reviews, survey comments, support tickets, app store feedback, or social replies to identify pain points, compare segments, generate corpus-level scoring items, or summarize customer perception for product, service, and messaging decisions.
---

# Customer Review Mining

## Overview

把大量評論轉成可行動洞察。預設輸出以商業決策可讀性為主，但理論分析是每次都必經的分析步驟，不是選配。動態評分題項由當次語料萃取，避免被固定 rubric 綁死。

核心原則：
- 先做資料充分性檢查，再做分析
- 先逐條語意解析與理論映射，再做主題整合
- 每次都必須套用四個理論視角
- 馬斯洛映射預設引導 agent 使用 `$maslow-five-needs-marketing`
- 評分題項必須從整批評論中萃取，不可預設寫死
- 其他 skill 或 agent 只能補充理論深挖，不可取代本技能主分析骨架

## When to Use

Use when:
- 需要從評論找出主要痛點、滿意驅動因子與優先改善方向
- 需要比較不同產品、版本、渠道、地區或客群的評論差異
- 需要把質性回饋整理成產品、客服、營運或行銷可執行建議
- 需要從整批評論中提煉一組共用評分題項，再回頭對每則評論做一致化評分
- 需要把評論分析建立在明確理論框架上

Do not use:
- 沒有實際評論文本，只想憑空推論顧客感受
- 需要嚴格因果推論、統計檢定或正式學術方法論
- 只想做單句情緒分類，不需要主題、優先級或題項生成

Handoff:
- 若要把洞察改寫成訊息策略或文案 brief，可交給 `$copywriting`
- 若要把洞察轉成追蹤與 KPI 設計，可交給 `$analytics-tracking`
- 若要把洞察轉成實驗假設與測試設計，可交給 `$ab-test-setup`
- 馬斯洛理論映射預設交給 `$maslow-five-needs-marketing` 產出，再回填到本技能報告
- 若需要更深理論詮釋，可視需求讓 agent 使用其他相關 skill 補充，但主分析流程仍需完整由本技能執行

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

### Per-Review Semantic Parsing

每則評論先做逐條語意解析，至少標記以下四類訊號：
- 產品屬性與描述一致性
- 使用感受與功能表現
- 消費者需求與利益感知
- 服務體驗與互動脈絡

這一步是理論映射的前置輸入，不可省略。

### Mandatory Theory Mapping

每次分析都必須套用四個理論視角，並提供證據追溯：
- Product Positioning Theory
- Purchase Motivation Theory
- Maslow's Hierarchy of Needs
- Word-of-Mouth Motivation Theory

理論規則：
- 四個理論在每次分析都要出現映射結果
- 可用「逐條評論」或「聚類後評論群」映射，但必須可追溯原始證據
- 某理論若證據弱，只能標示低信心與限制，不可跳過
- 理論名稱不可替代引文與證據

Maslow Skill Route（必跑）：
- 先完成逐條語意解析，再引導 agent 使用 `$maslow-five-needs-marketing`
- 路由策略固定為 `預設呼叫 + 可回退`
- 若 `$maslow-five-needs-marketing` 不可用，才可回退本技能內建馬斯洛映射
- 回退時必須在 `Theory Coding Summary` 與 `Risks / Bias / Confidence Notes` 標示：
  - `attempted: true`
  - `used: false`
  - `fallback_reason`
  - 對應理論映射 `confidence: low`（除非有充分直接證據）
- 不可因外部 skill 不可用就跳過馬斯洛映射

詳見 [references/03-theory-overlay-map.md](./references/03-theory-overlay-map.md)

### Theme Synthesis And Prioritization

完成必經理論映射後，才可進行三大主題整合、子主題歸納與優先級排序。

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

4. 逐條語意解析（必經）
- 逐條標記產品屬性、使用感受、需求訊號、服務互動
- 建立可回溯的評論語意標註

5. 理論映射（必經）
- 對每則評論或每個評論群套用四個理論視角
- 每個理論至少提供映射證據與信心標記
- 馬斯洛映射先引導 `$maslow-five-needs-marketing`
- 若外部 skill 不可用，啟用 fallback 並標示 `fallback_reason`
- 若理論證據不足，回報低信心與限制，不可跳過
- 交叉參考：見 [Example A/B](./references/06-end-to-end-examples.md)

6. 主題整合與優先級
- 以三大主題整合前述語意與理論結果
- 整理子主題、代表性引文與大致佔比

7. 生成共用評分題項
- 從整批評論抽候選題項
- 做動態正規化與命名
- 標出核心題項與 `exploratory` 題項
- 交叉參考：見 [Example D](./references/06-end-to-end-examples.md)

8. 回頭評分每則評論
- 使用同一組題項做 `0-7` 分評分
- 匯總成題項層級的統計摘要
- 交叉參考：見 [Example D](./references/06-end-to-end-examples.md)

9. 理論深挖（選配增強）
- 若需要更深解釋，可條件式請 agent 使用其他 skill 補充理論分析
- 增強分析需標註來源與限制，且不得覆蓋必經理論結果或 Maslow 必跑路由紀錄

10. 產出建議
- 先寫管理摘要
- 再列理論摘要、主題表、動態題項摘要與優先行動
- 只有在使用者要求結構化輸出時，才展開完整 JSON 附錄

## Output Contract

預設輸出順序：
1. `Executive Summary`
2. `Theory Coding Summary`
3. `Theme Analysis Table`
4. `Dynamic Item Set Summary`
5. `Dynamic Scorecard Summary`
6. `Priority Actions`
7. `Risks / Bias / Confidence Notes`
8. `Appendix (JSON)`

### Primary Output Rules

`Executive Summary`
- 2-5 點結論
- 每點都要可回溯到評論證據
- 不要用理論名詞塞滿摘要

`Theory Coding Summary`（必填）
- 四個理論都要有映射結果
- 每個理論都要附代表性證據
- 每個理論都要標示信心（`high|medium|low`）
- 若證據不足，明確寫出限制，不可留白
- 必填 Maslow 協作狀態：
  - `attempted`（是否嘗試呼叫 `$maslow-five-needs-marketing`）
  - `used`（是否成功採用其輸出）
  - `fallback_reason`（未採用時必填）

`Theme Analysis Table`
- 至少包含：`theme`, `subtheme`, `count`, `share`, `sample_quote`
- 若資料足夠，可加：`negative_rate`, `avg_severity`, `impact_score`

`Dynamic Item Set Summary`
- 列出本次分析產生的共用題項
- 每個題項至少附：`label`, `definition`, `evidence_cues`, `status`
- `status` 僅能是 `core` 或 `exploratory`

`Dynamic Scorecard Summary`
- 呈現高分與低分題項
- 標示題項覆蓋率、平均分與低信心題項

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

`Appendix (JSON)`
- 只有使用者要求結構化輸出時附上
- JSON 最小欄位不得缺少理論相關欄位

```json
{
  "analysis_scope": {},
  "theme_analysis": [],
  "theory_application_summary": [
    {
      "theory": "",
      "confidence": "high|medium|low",
      "maslow_collaboration_status": {
        "attempted": true,
        "used": true,
        "fallback_reason": ""
      }
    }
  ],
  "theory_evidence_trace": [],
  "generated_items": [],
  "scorecard_summary": [],
  "priority_actions": [],
  "evidence": []
}
```

詳見 [references/05-output-template-and-quality-checklist.md](./references/05-output-template-and-quality-checklist.md)

## Hard Rules

- 不可臆測不存在的欄位、分數或比較維度
- 不可用單一評論宣稱整體趨勢
- 不可做無證據支撐的因果推論
- 不可因為套了理論標籤，就跳過引文或證據
- 不可跳過理論映射步驟
- 不可只使用 1-2 個理論而不說明理由
- 不可跳過 `$maslow-five-needs-marketing` 引導步驟（除非已明確記錄 fallback）
- 不可把 fallback 說成成功協作
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
- [references/06-end-to-end-examples.md](./references/06-end-to-end-examples.md)

## Validation Assets

- [agents/pressure-scenario-01-business-mode.md](./agents/pressure-scenario-01-business-mode.md)
- [agents/pressure-scenario-02-theory-mode.md](./agents/pressure-scenario-02-theory-mode.md)
- [agents/pressure-scenario-03-missing-data-and-overclaim.md](./agents/pressure-scenario-03-missing-data-and-overclaim.md)
- [agents/validation-checklist.md](./agents/validation-checklist.md)
