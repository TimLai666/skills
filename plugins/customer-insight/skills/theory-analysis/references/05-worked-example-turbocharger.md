# Worked Example (Turbocharger, 三理論同時套用)

同一批證據套用三個理論。注意 `i1`、`i2`、`i4` 各自被標到**兩個以上不同 family**——那不是重複標註，是不同問法的答案。

## Example Input

```json
{
  "analysis_goal": "理解消費者如何評價渦輪增壓器、為何購買、以及為何分享經驗",
  "theories": ["product_positioning", "purchase_motivation", "wom_motivation"],
  "evidence_items": [
    {
      "item_id": "i1",
      "content": "訪談摘錄：尺寸吻合，裝上去一次就成功，增壓反應比原廠件快。",
      "content_type": "text",
      "source_type": "interview_note",
      "source_ref": "intv-2026-01"
    },
    {
      "item_id": "i2",
      "content": "客服工單：包裝完整但物流有點慢，客服有回但要等一天。",
      "content_type": "text",
      "source_type": "support_ticket",
      "source_ref": "ticket-8890"
    },
    {
      "item_id": "i3",
      "content": "社群貼文：看了幾篇比較文才下單，怕買到不合規格；寫這段給想自己改裝的人參考。",
      "content_type": "text",
      "source_type": "social_post",
      "source_ref": "post-210"
    },
    {
      "item_id": "i4",
      "content": "社群貼文：我研究很久才找到這顆，裝完真的有差，分享給同好。",
      "content_type": "text",
      "source_type": "social_post",
      "source_ref": "post-233"
    },
    {
      "item_id": "i5",
      "content": "客服工單紀要：物流拖超久，真的很火大。",
      "content_type": "text",
      "source_type": "support_ticket",
      "source_ref": "ticket-8912"
    }
  ]
}
```

## Example JSON (theory_annotations 節錄)

```json
{
  "theories": ["product_positioning", "purchase_motivation", "wom_motivation"],
  "theory_annotations": [
    { "item_id": "i1", "family": "product_positioning", "subtheory": "attributes", "quote": "尺寸吻合" },
    { "item_id": "i1", "family": "product_positioning", "subtheory": "functions", "quote": "增壓反應比原廠件快" },
    { "item_id": "i1", "family": "purchase_motivation", "subtheory": "functional", "quote": "裝上去一次就成功" },

    { "item_id": "i2", "family": "product_positioning", "subtheory": "usage_context_service_experience", "quote": "客服有回但要等一天" },
    { "item_id": "i2", "family": "purchase_motivation", "subtheory": "security", "quote": "包裝完整但物流有點慢" },
    { "item_id": "i2", "family": "purchase_motivation", "subtheory": "relational", "quote": "客服有回但要等一天" },

    { "item_id": "i3", "family": "purchase_motivation", "subtheory": "security", "quote": "怕買到不合規格" },
    { "item_id": "i3", "family": "wom_motivation", "subtheory": "altruistic", "quote": "給想自己改裝的人參考" },

    { "item_id": "i4", "family": "product_positioning", "subtheory": "benefits", "quote": "裝完真的有差" },
    { "item_id": "i4", "family": "wom_motivation", "subtheory": "self_enhancement", "quote": "我研究很久才找到這顆" },
    { "item_id": "i4", "family": "wom_motivation", "subtheory": "social_identity", "quote": "分享給同好" },

    { "item_id": "i5", "family": "purchase_motivation", "subtheory": "security", "quote": "物流拖超久" },
    { "item_id": "i5", "family": "wom_motivation", "subtheory": "emotional_expression", "quote": "真的很火大" }
  ]
}
```

## 構面涵蓋檢查

| family | 已標到的 subtheory | 覆蓋 |
| --- | --- | --- |
| `product_positioning` | attributes, functions, benefits, usage_context_service_experience | 4/4 |
| `purchase_motivation` | functional, security, relational | 3/3 |
| `wom_motivation` | altruistic, social_identity, self_enhancement, emotional_expression | 4/4 |

實務上不必強求全覆蓋。某個構面沒有證據時標 `insufficient`，不要為了湊滿而硬標。

## Example Markdown (Section Names)

- 摘要
- 構面判讀（依理論分節）
- 證據引文
- STP 對接欄位
- 限制與假設
