# Output Template And Quality Checklist

## Default Output Shape

以下段落皆為預設必填：

1. `Executive Summary`
2. `Theory Coding Summary`
3. `Theme Analysis Table`
4. `Dynamic Item Set Summary`
5. `Dynamic Scorecard Summary`
6. `Statistical Validation Summary`
7. `Customer Cluster Summary`
8. `Cluster Archetype Cards`
9. `Cluster-Specific Priority Actions`
10. `Priority Actions`
11. `Risks / Bias / Confidence Notes`
12. `Appendix (JSON)`

## Required Section Specs

### Statistical Validation Summary (Required)

每個核心比較都要包含：

| comparison_id | metric | test_name | group_n | statistic | p_value | p_value_adj | effect_size | ci_95 | interpretation |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |

固定規格：
- `alpha = 0.05`
- 多重比較修正：`BH-FDR`
- `95% CI`
- 禁止只報 p-value

### Customer Cluster Summary (Required)

每群至少包含：

| cluster_id | size | share | unit | top_attention_items | low_attention_items | pain_points | value_drivers |
| --- | ---: | ---: | --- | --- | --- | --- | --- |

其中：
- `unit` 只能是 `customer` 或 `review_proxy`
- `review_proxy` 必須同時附限制說明

### Cluster Archetype Cards (Required)

每群應輸出：
- `who_they_are`
- `what_they_care_about`
- `what_blocks_them`
- `evidence_quotes`
- `action_focus`

### Cluster-Specific Priority Actions (Required)

每群 1-3 項行動：

| cluster_id | action | rationale | expected_outcome | metric |
| --- | --- | --- | --- | --- |

## Appendix (JSON) Minimum Schema

```json
{
  "analysis_scope": {},
  "theme_analysis": [],
  "theory_application_summary": [],
  "theory_evidence_trace": [],
  "generated_items": [],
  "scorecard_summary": [],
  "statistical_validation_summary": [],
  "statistical_test_results": [],
  "multiple_comparison_control": {
    "method": "BH-FDR",
    "alpha": 0.05
  },
  "cluster_configuration": {
    "primary_method": "k-medoids",
    "secondary_method": "hierarchical_ward",
    "k_search_range": [2, 8]
  },
  "cluster_profiles": [],
  "cluster_assignments": [],
  "cluster_stability": [],
  "cluster_action_map": [],
  "priority_actions": [],
  "evidence": []
}
```

## Business-Readable Report Sample

```markdown
## Executive Summary
- `service_experience` 的回覆延遲是最大痛點，且在高價值客群更明顯。
- 分群結果顯示「效率敏感群」與「價值敏感群」的關注面向明確分化。
- 統計檢定顯示 iOS 與 Android 在 `response_speed` 分數差異顯著，且效果量中等。

## Theory Coding Summary
- 四理論均有映射與證據；Maslow 協作狀態為 `attempted=true`, `used=true`。

## Theme Analysis Table
| theme | subtheme | count | share | sample_quote |
| --- | --- | ---: | ---: | --- |
| service_experience | response_speed | 42 | 0.30 | 「客服回覆要等兩天」 |
| product_performance | installability | 31 | 0.22 | 「功能有到位，但安裝門檻高」 |
| value_perception | value_for_money | 28 | 0.20 | 「價格可以，但期待更穩定」 |

## Dynamic Item Set Summary
- `response_speed` (core)
- `issue_resolution` (core)
- `installability` (core)
- `value_for_money` (core)
- `advanced_install_tip` (exploratory)

## Dynamic Scorecard Summary
- 低分題項：`response_speed`(3.0), `issue_resolution`(3.2)
- 高分題項：`value_for_money`(5.5)

## Statistical Validation Summary
| comparison_id | metric | test_name | group_n | statistic | p_value | p_value_adj | effect_size | ci_95 | interpretation |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| C1 | response_speed_score (iOS vs Android) | Mann-Whitney U | 160 vs 190 | 11234 | 0.004 | 0.011 | 0.29 (Cliff's delta) | [0.14, 0.42] | 差異顯著且具實務意義 |
| C2 | low_score_rate (iOS vs Android) | two-proportion z | 160 vs 190 | 2.66 | 0.008 | 0.016 | 0.13 (risk diff) | [0.03, 0.22] | Android 低分率較高 |

## Customer Cluster Summary
| cluster_id | size | share | unit | top_attention_items | low_attention_items | pain_points | value_drivers |
| --- | ---: | ---: | --- | --- | --- | --- | --- |
| CL1 | 118 | 0.34 | customer | response_speed, issue_resolution | appearance | 回覆慢、問題未閉環 | 快速回覆與一次解決 |
| CL2 | 142 | 0.40 | customer | value_for_money, product_fit | advanced_install_tip | 價值落差 | 價格與效能匹配 |
| CL3 | 90 | 0.26 | customer | installability | response_speed | 安裝門檻 | 教學清晰度 |

## Cluster Archetype Cards
- CL1 效率敏感群：重視回覆速度與解決效率，對等待高度不耐。
- CL2 價值敏感群：重視 CP 值與符合預期，對價格/效能落差敏感。
- CL3 上手門檻群：重視安裝與教學，容易被初期摩擦勸退。

## Cluster-Specific Priority Actions
| cluster_id | action | rationale | expected_outcome | metric |
| --- | --- | --- | --- | --- |
| CL1 | 客服首回 SLA 24h + 未結案追蹤 | 主要痛點集中在等待與未閉環 | 降低低分率 | response_speed avg_score |
| CL2 | 強化商品頁效能邊界說明 | 降低期望落差 | 提升 value_for_money | value_perception negative_rate |
| CL3 | 重寫安裝導引與影片 | 降低上手門檻 | 提升 installability | installability avg_score |

## Priority Actions
- 跨群通用優先項 3-5 條，需對應主題、量測與時程。

## Risks / Bias / Confidence Notes
- 若缺 `customer_id`，群組單位為 `review_proxy`，解讀需保守。
- 小樣本分群必標記 `exploratory=true` 與 `confidence=low`。
```

## Appendix JSON Sample

```json
{
  "analysis_scope": {
    "goal": "Score -> statistical validation -> customer clustering",
    "sample_size": 350
  },
  "theory_application_summary": [
    {
      "theory": "Maslow's Hierarchy of Needs",
      "confidence": "medium",
      "maslow_collaboration_status": {
        "attempted": true,
        "used": true,
        "fallback_reason": ""
      }
    }
  ],
  "generated_items": [
    { "label": "response_speed", "status": "core" },
    { "label": "value_for_money", "status": "core" }
  ],
  "statistical_validation_summary": [
    {
      "comparison_id": "C1",
      "metric": "response_speed_score",
      "test_name": "Mann-Whitney U",
      "group_n": "160 vs 190",
      "statistic": 11234,
      "p_value": 0.004,
      "p_value_adj": 0.011,
      "effect_size": "0.29 (Cliff's delta)",
      "ci_95": [0.14, 0.42],
      "interpretation": "significant_with_practical_effect"
    }
  ],
  "statistical_test_results": [
    {
      "comparison_id": "C2",
      "metric": "low_score_rate",
      "test_name": "two-proportion z",
      "groups": ["ios", "android"],
      "group_n": [160, 190],
      "statistic": 2.66,
      "p_value": 0.008,
      "p_value_adj": 0.016,
      "effect_size": "0.13 (risk diff)",
      "ci_95": [0.03, 0.22],
      "assumption_checks": ["normal_approx_ok"],
      "conclusion": "android_higher_low_score_rate",
      "caveats": []
    }
  ],
  "multiple_comparison_control": {
    "method": "BH-FDR",
    "alpha": 0.05
  },
  "cluster_configuration": {
    "primary_method": "k-medoids",
    "secondary_method": "hierarchical_ward",
    "k_search_range": [2, 8],
    "selected_k": 3
  },
  "cluster_profiles": [
    {
      "cluster_id": "CL1",
      "size": 118,
      "share": 0.34,
      "unit": "customer",
      "top_attention_items": ["response_speed", "issue_resolution"],
      "low_attention_items": ["appearance"],
      "pain_points": ["slow_response"],
      "value_drivers": ["fast_issue_resolution"],
      "recommended_actions": ["sla_24h"]
    }
  ],
  "cluster_assignments": [],
  "cluster_stability": [
    {
      "method": "bootstrap_200",
      "ari_mean": 0.72,
      "nmi_mean": 0.76,
      "min_cluster_share": 0.26
    }
  ],
  "cluster_action_map": [
    {
      "cluster_id": "CL1",
      "actions": ["sla_24h", "ticket_follow_up"]
    }
  ],
  "priority_actions": [],
  "evidence": []
}
```

## Quality Checklist

- 是否先做 Data Sufficiency Gate
- 是否先做逐條語意解析與四理論映射
- 是否先生成共享題項並完成逐條評分
- 是否評分後才做統計與分群（不可反序）
- 是否完成統計檢定 + `BH-FDR` + effect size + CI
- 是否避免只報 p-value
- 是否以 `core` 題項分數矩陣做分群
- 是否同時輸出 `K-medoids` 主分群與 `Hierarchical (Ward)` 群間解讀
- 是否回報分群穩定度（bootstrap ARI/NMI）與最小群體占比
- 低樣本是否標記 `exploratory=true` 與 `confidence=low`
- 是否避免把關聯差異寫成因果結論
