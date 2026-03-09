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

### 5. Theory Coding Summary

- 只保留 1-4 條最有用理論洞察
- 每條都附代表性證據

### 6. 14-Item Scorecard Summary

- 只列最值得看的高低分題項
- 指出未評分或低信心題項

### 7. Appendix (JSON)

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

## Quality Checklist

- 是否先做 Data Sufficiency Gate
- 是否保留三大主題作為第一層分類
- 是否用引文或摘要證據支撐每個高價值結論
- 是否避免從單一評論推出整體結論
- 是否避免不必要的理論堆疊
- 是否明確標示偏誤與信心限制
- 是否在沒有證據時讓題項維持 `0`
