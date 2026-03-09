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
  "theory_application_summary": [],
  "theory_evidence_trace": [],
  "generated_items": [],
  "scorecard_summary": [],
  "priority_actions": [],
  "evidence": []
}
```

## Quality Checklist

- 是否先做 Data Sufficiency Gate
- 是否先做逐條語意解析
- 是否執行四理論必經映射
- 是否每個理論都有證據與信心等級
- 是否在證據不足時標示限制而非跳過理論
- 是否先生成共用題項，再評分單篇評論
- 是否合併同義題項
- 是否避免低頻訊號被升格為核心題項
- 是否避免無證據因果推論
- 是否保持理論摘要精簡，不壓過商業結論
