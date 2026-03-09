# End-To-End Examples

## Example A: 正常協作（Maslow 成功引導）

### Input（最小可執行）

```json
{
  "analysis_goal": "找出近 30 天痛點並提出優先行動",
  "reviews": [
    {
      "id": "R01",
      "customer_id": "C001",
      "review_text": "客服回覆快，但安裝說明不夠清楚",
      "channel": "app_store",
      "rating": 3
    },
    {
      "id": "R02",
      "customer_id": "C002",
      "review_text": "價格合理，功能有改善，會考慮再買",
      "channel": "app_store",
      "rating": 5
    }
  ]
}
```

### Expected Behavior

- 先做逐條語意解析，再做四理論映射。
- 馬斯洛映射先引導 `$maslow-five-needs-marketing`。
- 產出三大主題、共享動態題項、統計驗證與分群摘要。

### Theory Trace（節錄）

```json
{
  "theory": "Maslow's Hierarchy of Needs",
  "mapping_unit": "review",
  "evidence_refs": ["R01", "R02"],
  "source_skill": "maslow-five-needs-marketing",
  "confidence": "medium",
  "limitations": []
}
```

---

## Example B: Maslow Fallback（不可用時回退）

### Trigger

- 嘗試引導 `$maslow-five-needs-marketing` 失敗（不可用或回傳無效）。

### Required Output Markers

```json
{
  "theory": "Maslow's Hierarchy of Needs",
  "maslow_collaboration_status": {
    "attempted": true,
    "used": false,
    "fallback_reason": "skill_unavailable_or_invalid_response"
  },
  "confidence": "low"
}
```

### Evidence Trace（節錄）

```json
{
  "theory": "Maslow's Hierarchy of Needs",
  "mapping_unit": "cluster",
  "evidence_refs": ["R10", "R11", "R14"],
  "source_skill": "customer-review-mining:fallback",
  "confidence": "low",
  "limitations": ["maslow_external_skill_unavailable"]
}
```

---

## Example C: 小樣本限制（統計與分群照跑，但 exploratory）

### Input

```json
{
  "analysis_goal": "找出主要問題並比較市場差異",
  "reviews": [
    { "id": "R1", "review_text": "客服慢", "rating": 2 },
    { "id": "R2", "review_text": "裝起來有點難", "rating": 3 },
    { "id": "R3", "review_text": "價格還可以", "rating": 4 },
    { "id": "R4", "review_text": "功能普通", "rating": 3 }
  ]
}
```

### Expected Behavior

- 統計與分群仍執行，不可跳過。
- 全部推論標記 `exploratory=true`、`confidence=low`。
- 不可輸出高信心強決策語句。

### Example Statistical Output（節錄）

```json
{
  "comparison_id": "S1",
  "test_name": "Mann-Whitney U",
  "p_value": 0.19,
  "p_value_adj": 0.27,
  "effect_size": "0.18 (Cliff's delta)",
  "ci_95": [-0.12, 0.45],
  "exploratory": true,
  "confidence": "low",
  "limitations": ["small_sample_size"]
}
```

### Example Clustering Output（節錄）

```json
{
  "cluster_configuration": {
    "primary_method": "k-medoids",
    "selected_k": 2
  },
  "cluster_stability": {
    "ari_mean": 0.32,
    "nmi_mean": 0.37,
    "exploratory": true,
    "confidence": "low"
  },
  "decision_guardrail": "Do not use as high-confidence policy decision"
}
```

---

## Example D: 動態題項正規化（同義詞合併）

### Candidate Mentions（Before）

- 回覆快、客服秒回、溝通迅速、等待過久
- CP 值高、價格划算、值得買、價格合理

### Normalized Shared Items（After）

```json
[
  {
    "label": "response_speed",
    "definition": "顧客對客服回覆與處理速度的評價",
    "parent_theme": "service_experience",
    "evidence_cues": ["回覆快", "客服秒回", "等待過久"],
    "status": "core"
  },
  {
    "label": "value_for_money",
    "definition": "顧客對價格與整體體驗匹配度的評價",
    "parent_theme": "value_perception",
    "evidence_cues": ["CP 值高", "價格划算", "價格合理"],
    "status": "core"
  }
]
```

### Scoring Consistency Rule

- 同一分析範圍內，所有評論都使用同一組 shared items。
- 不可逐篇新建題項；低頻新訊號先標 `exploratory`。

---

## Example E: Scorecard -> Clustering（必經鏈路）

### Input

```json
{
  "analysis_goal": "依在意面向分群並制定群組策略",
  "reviews": [
    { "id": "R11", "customer_id": "U01", "review_text": "客服回覆慢，但價格還可以" },
    { "id": "R12", "customer_id": "U01", "review_text": "問題回覆要催很多次" },
    { "id": "R21", "customer_id": "U02", "review_text": "價格合理、性能符合預期" },
    { "id": "R22", "customer_id": "U03", "review_text": "安裝教學不清楚，但產品本身不錯" }
  ]
}
```

### Required Pipeline

1. 生成 `generated_items`（只用 `core` 題項進分群）
2. 逐則評分得到 score matrix
3. 先做統計驗證（含 FDR + effect size + CI）
4. 跑 `K-medoids`（k=2..8, silhouette 選 k）
5. 用 `Hierarchical (Ward)` 解讀群間關係
6. 產出 `cluster_action_map`

### Example Output（節錄）

```json
{
  "cluster_configuration": {
    "primary_method": "k-medoids",
    "secondary_method": "hierarchical_ward",
    "k_search_range": [2, 8],
    "selected_k": 3
  },
  "cluster_profiles": [
    {
      "cluster_id": "CL1",
      "size": 1,
      "share": 0.33,
      "top_attention_items": ["response_speed", "issue_resolution"],
      "low_attention_items": ["value_for_money"],
      "pain_points": ["slow_response"],
      "value_drivers": ["fast_resolution"],
      "recommended_actions": ["sla_24h", "ticket_follow_up"]
    },
    {
      "cluster_id": "CL2",
      "size": 1,
      "share": 0.33,
      "top_attention_items": ["value_for_money", "product_fit"],
      "low_attention_items": ["response_speed"],
      "pain_points": ["expectation_gap"],
      "value_drivers": ["stable_performance"],
      "recommended_actions": ["pricing_copy_alignment"]
    }
  ],
  "cluster_stability": [
    {
      "method": "bootstrap_200",
      "ari_mean": 0.71,
      "nmi_mean": 0.75,
      "min_cluster_share": 0.22
    }
  ],
  "cluster_action_map": [
    { "cluster_id": "CL1", "actions": ["sla_24h", "priority_response_queue"] },
    { "cluster_id": "CL2", "actions": ["value_message_rewrite"] }
  ]
}
```
