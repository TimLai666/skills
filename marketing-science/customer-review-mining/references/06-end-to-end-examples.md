# End-To-End Examples

## Example A: 正常協作（Maslow 成功引導）

### Input（最小可執行）

```json
{
  "analysis_goal": "找出近 30 天痛點並提出優先行動",
  "reviews": [
    {
      "id": "R01",
      "review_text": "客服回覆快，但安裝說明不夠清楚",
      "channel": "app_store",
      "rating": 3
    },
    {
      "id": "R02",
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
- 產出三大主題與共用動態題項。

### Example Trace（節錄）

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

## Example B: Maslow fallback（不可用時回退）

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

## Example C: 小樣本限制（低信心 + exploratory 提升）

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

- 先輸出資料限制，不可宣稱跨市場趨勢。
- 仍執行四理論映射，但多數標記 `low confidence`。
- 動態題項可生成，但低頻題項應以 `exploratory` 為主。

### Example Item Summary（節錄）

```json
[
  { "label": "response_speed", "status": "core" },
  { "label": "installability", "status": "exploratory" },
  { "label": "value_for_money", "status": "exploratory" }
]
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
