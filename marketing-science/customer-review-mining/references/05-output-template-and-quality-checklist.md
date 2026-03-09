# Output Template And Quality Checklist

## Default Output Shape

### 1. Executive Summary

- 2-5 點最高價值結論
- 每點都要連到具體評論證據
- 不要把理論名詞塞滿摘要

### 2. Theme Analysis Table

建議欄位：

| theme | subtheme | count | share | sample_quote |
| --- | --- | ---: | ---: | --- |

若資料足夠可加：

| negative_rate | avg_severity | impact_score |
| ---: | ---: | ---: |

### 3. Priority Actions

建議欄位：

| priority | action | rationale | expected_outcome | metric |
| ---: | --- | --- | --- | --- |

### 4. Risks / Bias / Confidence Notes

至少檢查：
- 樣本量是否過小
- 資料來源是否偏單一渠道
- 是否有語言或地區偏差
- 是否存在時間切片問題
- 哪些推論屬於低信心

## Optional Sections

### 5. Dynamic Item Set Summary

- 列出本次生成的共用題項
- 說明哪些是 `core`，哪些是 `exploratory`

### 6. Dynamic Scorecard Summary

- 只列最值得看的高低分題項
- 指出覆蓋率低或低信心題項

### 7. Theory Coding Summary

- 只保留最有用理論洞察
- 若有其他 skill 協作，標示是條件式補充

### 8. Appendix (JSON)

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

## Quality Checklist

- 是否先做 Data Sufficiency Gate
- 是否保留三大主題作為第一層分類
- 是否先生成共用題項，再評分單篇評論
- 是否合併同義題項
- 是否避免單一低頻訊號被升格為核心題項
- 是否避免不必要的理論堆疊
- 是否明確標示偏誤與信心限制
- 是否在需要時才啟用 agent 協作理論分析
