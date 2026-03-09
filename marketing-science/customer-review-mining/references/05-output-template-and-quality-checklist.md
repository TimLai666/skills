# Output Template And Quality Checklist

## Default Output Shape

以下段落皆為預設必填，`Theory Coding Summary` 不可省略。

### 1. Executive Summary

- 2-5 點最高價值結論
- 每點都要連到具體評論證據
- 不要把理論名詞堆成摘要

### 2. Theory Coding Summary (Required)

- 四個理論都要有映射結果
- 每個理論都要附證據或證據索引
- 每個理論都要附信心等級
- 證據不足時要寫限制，不可空白
- 馬斯洛協作狀態必填：
  - `attempted`
  - `used`
  - `fallback_reason`（`used: false` 時必填）

### 3. Theme Analysis Table

建議欄位：

| theme | subtheme | count | share | sample_quote |
| --- | --- | ---: | ---: | --- |

若資料足夠可加：

| negative_rate | avg_severity | impact_score |
| ---: | ---: | ---: |

### 4. Dynamic Item Set Summary

- 列出本次生成的共用題項
- 標示 `core` 與 `exploratory`
- 需附簡短定義與證據線索

### 5. Dynamic Scorecard Summary

- 顯示高分與低分題項
- 顯示覆蓋率與低信心題項

### 6. Priority Actions

建議欄位：

| priority | action | rationale | expected_outcome | metric |
| ---: | --- | --- | --- | --- |

### 7. Risks / Bias / Confidence Notes

至少檢查：
- 樣本量與代表性
- 來源偏差
- 語言偏差
- 時間切片問題
- 推論信心邊界

### 8. Appendix (JSON)

使用者要求結構化輸出時附上。最小欄位：

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
  "theory_evidence_trace": [
    {
      "theory": "",
      "mapping_unit": "review|cluster",
      "evidence_refs": [],
      "source_skill": "maslow-five-needs-marketing|customer-review-mining:fallback|customer-review-mining",
      "confidence": "high|medium|low",
      "limitations": []
    }
  ],
  "generated_items": [],
  "scorecard_summary": [],
  "priority_actions": [],
  "evidence": []
}
```

## Business-Readable Report Sample

```markdown
## Executive Summary
- 近期負評主要集中在 `service_experience` 的回覆延遲與問題未閉環，影響續購意願。
- `product_performance` 整體評價中性偏正，但「安裝便利性」在新手客群明顯偏低。
- `value_perception` 呈現分化：高分評論強調 CP 值，低分評論集中在期望落差與描述一致性。

## Theory Coding Summary
- Product Positioning Theory：`medium`
  - 映射：尺寸適配、安裝便利性、描述一致性
  - 證據：R12, R37, R88
- Purchase Motivation Theory：`high`
  - 映射：功能性動機、保障性動機、關係性動機
  - 證據：R08, R21, R63, R91
- Maslow's Hierarchy of Needs：`medium`
  - 映射：安全需求、尊重需求最明顯
  - 證據：R15, R46, R102
  - maslow_collaboration_status: `attempted=true`, `used=true`, `fallback_reason=""`
- Word-of-Mouth Motivation Theory：`medium`
  - 映射：助人利他、情緒表達
  - 證據：R04, R29, R54

## Theme Analysis Table
| theme | subtheme | count | share | sample_quote |
| --- | --- | ---: | ---: | --- |
| service_experience | response_speed | 28 | 28% | 「客服三天才回，錯過安裝時程」 |
| product_performance | installability | 24 | 24% | 「功能有到位，但安裝說明不清楚」 |
| value_perception | value_for_money | 20 | 20% | 「價格合理，但實際表現沒有預期高」 |

## Dynamic Item Set Summary
- `response_speed`：回覆與處理速度（core）
- `issue_resolution`：問題是否一次解決（core）
- `installability`：安裝便利性與教學清楚度（core）
- `value_for_money`：價格與體驗是否匹配（core）
- `pro_installation_tip`：進階安裝技巧分享（exploratory）

## Dynamic Scorecard Summary
- 高分題項：`product_fit`(5.9), `value_for_money`(5.4)
- 低分題項：`response_speed`(3.1), `issue_resolution`(2.9)
- 低信心題項：`pro_installation_tip`（覆蓋率 4%）

## Priority Actions
| priority | action | rationale | expected_outcome | metric |
| ---: | --- | --- | --- | --- |
| 1 | 設定客服首回 SLA 24h | 回覆延遲為最大負評來源 | 降低服務負評占比 | response_speed avg_score |
| 2 | 重寫安裝教學內容 | 新手客群安裝困難高頻出現 | 降低安裝相關客服單 | installability avg_score |
| 3 | 補強商品頁描述一致性 | 期望落差影響價值感知 | 降低退貨與負評率 | value_perception negative_rate |

## Risks / Bias / Confidence Notes
- 樣本以近 30 天評論為主，季節性波動未完全反映。
- Android 渠道樣本明顯高於 iOS，跨渠道比較需保守解讀。
- 理論映射依引文證據進行，低頻訊號僅作 exploratory。
```

## Appendix JSON Sample

```json
{
  "analysis_scope": {
    "goal": "Identify pain points, compare iOS vs Android, and prioritize actions",
    "time_window": "last_30_days",
    "channels": ["app_store", "support_ticket"],
    "sample_size": 100
  },
  "theme_analysis": [
    {
      "theme": "service_experience",
      "subtheme": "response_speed",
      "count": 28,
      "share": 0.28,
      "sample_quote": "客服三天才回，錯過安裝時程"
    },
    {
      "theme": "product_performance",
      "subtheme": "installability",
      "count": 24,
      "share": 0.24,
      "sample_quote": "功能有到位，但安裝說明不清楚"
    }
  ],
  "theory_application_summary": [
    {
      "theory": "Product Positioning Theory",
      "confidence": "medium",
      "maslow_collaboration_status": {
        "attempted": false,
        "used": false,
        "fallback_reason": "not_applicable_for_non_maslow_theory"
      }
    },
    {
      "theory": "Purchase Motivation Theory",
      "confidence": "high",
      "maslow_collaboration_status": {
        "attempted": false,
        "used": false,
        "fallback_reason": "not_applicable_for_non_maslow_theory"
      }
    },
    {
      "theory": "Maslow's Hierarchy of Needs",
      "confidence": "medium",
      "maslow_collaboration_status": {
        "attempted": true,
        "used": true,
        "fallback_reason": ""
      }
    },
    {
      "theory": "Word-of-Mouth Motivation Theory",
      "confidence": "medium",
      "maslow_collaboration_status": {
        "attempted": false,
        "used": false,
        "fallback_reason": "not_applicable_for_non_maslow_theory"
      }
    }
  ],
  "theory_evidence_trace": [
    {
      "theory": "Maslow's Hierarchy of Needs",
      "mapping_unit": "review",
      "evidence_refs": ["R15", "R46", "R102"],
      "source_skill": "maslow-five-needs-marketing",
      "confidence": "medium",
      "limitations": []
    },
    {
      "theory": "Word-of-Mouth Motivation Theory",
      "mapping_unit": "review",
      "evidence_refs": ["R04", "R29", "R54"],
      "source_skill": "customer-review-mining",
      "confidence": "medium",
      "limitations": []
    }
  ],
  "generated_items": [
    {
      "label": "response_speed",
      "definition": "顧客對回覆與處理速度的評價",
      "parent_theme": "service_experience",
      "evidence_cues": ["回很慢", "等三天", "很快回覆"],
      "status": "core"
    },
    {
      "label": "pro_installation_tip",
      "definition": "評論中提及進階安裝技巧與專業建議",
      "parent_theme": "product_performance",
      "evidence_cues": ["要先校正", "專業工具才好裝"],
      "status": "exploratory"
    }
  ],
  "scorecard_summary": [
    {
      "label": "response_speed",
      "coverage": 0.41,
      "avg_score": 3.1,
      "high_score_rate": 0.12,
      "low_score_rate": 0.48
    },
    {
      "label": "value_for_money",
      "coverage": 0.36,
      "avg_score": 5.4,
      "high_score_rate": 0.42,
      "low_score_rate": 0.11
    }
  ],
  "priority_actions": [
    {
      "priority": 1,
      "action": "設定客服首回 SLA 24h",
      "rationale": "回覆延遲是最大負評來源",
      "expected_outcome": "降低服務負評占比",
      "metric": "response_speed avg_score"
    }
  ],
  "evidence": [
    {
      "ref": "R12",
      "quote": "客服三天才回，錯過安裝時程"
    },
    {
      "ref": "R88",
      "quote": "價格合理，但實際表現沒有預期高"
    }
  ]
}
```

## Quality Checklist

- 是否先做 Data Sufficiency Gate
- 是否先做逐條語意解析
- 是否執行四理論必經映射
- 是否每個理論都有證據與信心等級
- 是否在證據不足時標示限制而非跳過理論
- 是否先嘗試 `$maslow-five-needs-marketing`，失敗時才 fallback
- 是否明確區分「成功協作」與「fallback」
- 是否先生成共用題項，再評分單篇評論
- 是否合併同義題項
- 是否避免低頻訊號被升格為核心題項
- 是否避免無證據因果推論
- 是否保持理論摘要精簡，不壓過商業結論
