---
name: theory-analysis
description: >-
  Code cross-source evidence — interview notes, support tickets, social posts,
  research notes, observations — into theory dimensions with auditable quotes.
  This skill MUST be used when the user names Product Positioning Theory,
  Purchase Motivation Theory, or Word-of-Mouth Motivation Theory, and SHOULD be
  used when classifying evidence into product attributes, functions, benefits,
  usage context, purchase drivers, or sharing motives. 觸發詞：產品定位理論、購買動機理論、
  口碑動機理論、證據編碼、質性編碼、理論標註、跨來源證據分析。One evidence item can carry
  annotations from several theories at once — they are different questions, not
  duplicates. This skill MUST NOT be used for generic sentiment tagging, and its
  output MUST NOT be pasted straight into a review-mining-stp dimension_catalog,
  which is attribute-level and needs the handoff steps in
  references/06-stp-handoff.md.
metadata:
  version: "1.0.0"
---

# Theory Analysis

把散落的文字證據逐句貼上理論標籤，變成可追溯、可統計的結構化資料。

## Overview

三個理論是**同一批證據的三種問法**，不是三種工具：

| 理論 | 問的問題 | 參考檔 |
| --- | --- | --- |
| `product_positioning` | 這段話在講產品的什麼 | [02](references/02-theory-product-positioning.md) |
| `purchase_motivation` | 這個人為什麼買 | [03](references/03-theory-purchase-motivation.md) |
| `wom_motivation` | 這個人為什麼分享 | [04](references/04-theory-wom-motivation.md) |

可以只用一個，也可以同時套用多個。同一則證據被標到多個理論是正常的。

來源不限於評論：訪談摘要、客服工單、社群貼文、研究筆記、觀察紀錄都可以。

## Input Contract

至少提供：

- `analysis_goal: string`
- `theories: string[]` — 至少一個，合法值見上表
- `evidence_items: array` — 每筆需有 `item_id`、`content`、`content_type`

建議可選：`source_type`、`source_ref`、`context_tags`。

完整規則見 [00-input-and-gate.md](references/00-input-and-gate.md)。

## Data Sufficiency Gate

缺必要欄位或沒有可用證據內容時，輸出 `MissingDataOutput`，不做硬判讀。格式見 [00-input-and-gate.md](references/00-input-and-gate.md)。

使用者沒指定 `theories` 時依 `analysis_goal` 判斷；判斷不出來就問，不要預設全跑。

## Workflow

1. 讀 [00-input-and-gate.md](references/00-input-and-gate.md)，完成輸入檢核與理論選擇。
2. 讀本次選用理論的參考檔（[02](references/02-theory-product-positioning.md) / [03](references/03-theory-purchase-motivation.md) / [04](references/04-theory-wom-motivation.md)），校準構面定義與判準。
3. 依 [01-output-contract.md](references/01-output-contract.md) 的 Coding Procedure 逐句標註。多理論時每句在每個理論之下各判一次。
4. 依 [01-output-contract.md](references/01-output-contract.md) 輸出 JSON 與 Markdown。
5. 需要對齊格式與深度時，看 [05-worked-example-turbocharger.md](references/05-worked-example-turbocharger.md)。
6. 要串接 `review-mining-stp` 才讀 [06-stp-handoff.md](references/06-stp-handoff.md)。

## Output Contract

一份 JSON 加一份 Markdown，多理論也只出一份，靠每筆標註自己的 `family` 區分。完整 schema 見 [01-output-contract.md](references/01-output-contract.md)。

## Quality Rules

- 每個構面結論至少要有一則可稽核引文，否則標記 `insufficient`。
- `quote` 必須是原文連續片段，可逐字對回，不可改寫成看似直接引述。
- `reason` 要說明為何對應該構面，不可只重述原句。
- 不得輸出各理論 taxonomy 之外的 subtheory。
- 每個選用理論分別計算覆蓋率，未達 80% 要在摘要說出資料限制。

## Common Mistakes

- 把同一句被標到不同理論當成重複標註而刪掉。那是三個問題的三個答案。
- 為了湊滿構面而硬標，該標 `insufficient` 的不標。
- 把運送、包裝、售後一律歸到 `purchase_motivation.functional`，沒依定義區分 `security` 與 `relational`。
- 只因內容詳細就標 `wom_motivation.altruistic`，沒有明確的幫助他人語意。
- 把本 skill 的 item-level 輸出直接當成 `review-mining-stp` 的 attribute-level `dimension_catalog`。

## Quick Reference

| 需求 | 讀哪一份 |
| --- | --- |
| 輸入檢核、缺資料處理、覆蓋率門檻 | [00-input-and-gate.md](references/00-input-and-gate.md) |
| JSON schema、標註程序、一致性規則 | [01-output-contract.md](references/01-output-contract.md) |
| 某個理論的構面定義與判準 | [02](references/02-theory-product-positioning.md) / [03](references/03-theory-purchase-motivation.md) / [04](references/04-theory-wom-motivation.md) |
| 完整範例（三理論同時套用） | [05-worked-example-turbocharger.md](references/05-worked-example-turbocharger.md) |
| 串接 review-mining-stp | [06-stp-handoff.md](references/06-stp-handoff.md) |

## Suggested Prompt

- `Use $theory-analysis to code these evidence items against purchase motivation theory and return JSON + Markdown in Traditional Chinese.`
- `請用 $theory-analysis 同時以產品定位理論與口碑動機理論分析這批證據，逐句標註並附原文引文。`
