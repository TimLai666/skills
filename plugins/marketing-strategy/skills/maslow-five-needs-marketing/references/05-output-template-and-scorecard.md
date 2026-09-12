# Output Template and Scorecard

## Output Skeleton

完整策略可用以下模板。五層分析必須完整呈現；通路、排程、指標與文案選項依需求展開。訊息方向不強制交付完整計畫。

1. `executive_summary`
2. `five_layer_plan`
3. `campaign_architecture`
4. `kpi_ladder`
5. `risk_and_mitigation`
6. `action_plan`
7. `strategy_review`
8. `copy_message_briefs`

## StrategyOutput Template

```json
{
  "executive_summary": "2-5 個策略重點與決策理由",
  "five_layer_plan": [
    {
      "layer": "生理/安全/社交/尊重/自我實現",
      "audience_need": "",
      "product_response": "",
      "evidence_or_gaps": [],
      "relevance_to_goal": "",
      "investment_decision_and_reason": "",
      "objective": "",
      "message_core": "",
      "channels": [],
      "actions": [],
      "kpi": []
    }
  ],
  "campaign_architecture": [
    {
      "phase": "P1/P2/P3",
      "goal": "",
      "channel_focus": [],
      "handoff_logic": ""
    }
  ],
  "kpi_ladder": [
    {
      "leading_indicator": "",
      "result_indicator": "",
      "target": "",
      "window": ""
    }
  ],
  "risk_and_mitigation": [
    {
      "risk": "",
      "impact": "",
      "mitigation": "",
      "owner": ""
    }
  ],
  "action_plan": [
    {
      "period": "依實際期間",
      "action": "",
      "owner": "",
      "deliverable": ""
    }
  ],
  "strategy_review": [
    {
      "核心假設": "",
      "反證風險": "",
      "最小可行實驗": "",
      "依實際期間設定的檢核指標": ""
    }
  ],
  "copy_message_briefs": [
    {
      "layer": "",
      "message_core": "",
      "headline_angles": [],
      "cta_options": [],
      "proof_points": []
    }
  ]
}
```

`five_layer_plan` 必須有五筆，分別涵蓋全部五層；模板只示範一筆結構。關聯弱與資料不足都要填寫理由或缺口。

`copy_message_briefs` 是選定訊息的骨架，標題與 CTA 數量依需求。要完整成稿時，配合可用且適用的寫作 skill 完成。

`action_plan` 配合實際期間；若使用者指定 30 天，就排 30 天。舊格式的 `first_30_day_actions` 與 `strategic_iq_check` 可在需相容既有資料時沿用，分別對應行動計畫與策略檢核。

## 交付檢核

| 項目 | 通過條件 |
| --- | --- |
| 五層完整性 | 五層都有需求、產品回應、證據或缺口、目標關聯，沒有只填名稱或直接略過 |
| 決策依據 | 投入順序根據完整分析，弱關聯與未投入都有理由 |
| 可驗證性 | 已知事實與推論分開，待驗證內容有補證據的方法 |
| 可執行性 | 要求執行方案時，行動、角色、節奏與資源足以落地 |
| 可衡量性 | 要求衡量時，指標連回目標，期間與資料取得方式清楚 |
| 文案可用性 | 訊息能連回需求與證據，要求成稿時已交付成品 |
| 事實與承諾 | 數據、評價、限量與產品承諾有依據 |

修正未符合本次交付要求的項目，不用總分抵銷某一層漏分析或不實承諾。
