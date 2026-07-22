# Output Contract (JSON + Markdown)

三個理論共用同一份輸出契約。多理論時**輸出一份 JSON**，用每筆標註自己的 `family` 區分，不要每個理論各出一份。

## JSON Contract

```json
{
  "theories": ["product_positioning", "purchase_motivation"],
  "dimension_results": [
    {
      "family": "product_positioning",
      "dimension": "attributes",
      "summary": "",
      "signal_direction": "positive|mixed|negative|insufficient",
      "evidence_count": 0,
      "evidence_item_ids": [],
      "confidence": "high|medium|low"
    }
  ],
  "evidence_quotes": [
    {
      "item_id": "",
      "family": "product_positioning",
      "dimension": "attributes",
      "quote": "",
      "reason": "",
      "sentiment": "positive|neutral|negative"
    }
  ],
  "theory_annotations": [
    {
      "item_id": "",
      "family": "product_positioning",
      "subtheory": "attributes",
      "quote": ""
    }
  ],
  "stp_mapping": {
    "attribute_group_recommendation": "見各理論參考檔的「STP 對接建議值」",
    "suggested_stat_roles": ["見各理論參考檔"],
    "dimension_catalog_notes": []
  },
  "quality_checks": {
    "input_valid": true,
    "missing_fields": [],
    "coverage": {
      "total_items": 0,
      "coded_items_by_theory": {}
    },
    "warnings": [],
    "assumptions": []
  }
}
```

## Markdown Contract

固定輸出以下章節：

1. `摘要`
2. `構面判讀` — 多理論時依理論分節
3. `證據引文`
4. `STP 對接欄位`
5. `限制與假設`

## Coding Procedure

1. 逐項證據切分關鍵語句。
2. 每句在**每個選用理論之下**可標註 0-2 個 subtheory，避免過度多標。同一句可以同時屬於不同理論的構面——那不是重複標註，是不同問法的答案。
3. 每筆標註都要綁定原文 quote 與簡短理由。
4. 不確定時標記 `insufficient`，不要補腦。

## Evidence Rules

- `quote` 必須是證據內容中的連續片段，可逐字對回原文，不可改寫成看似直接引述。
- `reason` 需指出為何對應該構面，不可只重述原句。
- `sentiment` 允許：`positive | neutral | negative`。

## Consistency Rules

- `theory_annotations.family` 只能是 `theories` 陣列裡出現過的值。
- `theory_annotations.subtheory` 必須屬於該 `family` 的 taxonomy，見各理論參考檔。不得自創 subtheory。
- `dimension_results.dimension` 與 `theory_annotations.subtheory` 必須對齊。
- `evidence_count` 必須等於該構面被引用的 `evidence_quotes` 筆數。
- 每個構面摘要至少要有一則證據，否則明確標示 `insufficient`。
- `quality_checks.input_valid = false` 時，先輸出 gate 結果，不輸出具體結論或強結論，只給缺資料說明與下一步。
- `stp_mapping` 的建議值依選用理論而定，見各理論參考檔的「STP 對接建議值」。多理論時取聯集，並在 `dimension_catalog_notes` 註明各值來自哪個理論。
