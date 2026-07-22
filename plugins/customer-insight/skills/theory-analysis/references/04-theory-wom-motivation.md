# 口碑動機理論（`wom_motivation`）

## 理論概念

口碑動機理論（Word-of-Mouth Motivation Theory）用於解釋個體為何主動分享產品或服務經驗。
分析重點是分享行為背後的心理驅動，而不只是內容本身的正負面。

支援跨來源證據：訪談摘要、客服對話或工單紀要、社群貼文與留言、研究筆記、觀察紀錄。

## Allowed Taxonomy

- `family`: `wom_motivation`
- `subtheory`: `altruistic` / `social_identity` / `self_enhancement` / `emotional_expression`

## 構面定義與標註焦點

| subtheory | 理論意涵 | 標註焦點 |
| --- | --- | --- |
| `altruistic` | 助人利他動機 | 幫助他人降低搜尋成本與決策風險的分享 |
| `social_identity` | 社交認同動機 | 參與社群互動、取得認同、維持歸屬感 |
| `self_enhancement` | 專業展現動機 | 展現能力、專業、經驗或成就感 |
| `emotional_expression` | 情緒表達動機 | 情緒宣洩或態度表達，常伴隨強烈正負向語氣 |

## 判準補充

- `social_identity` vs `self_enhancement`：重點在「被社群看見／互動」優先 `social_identity`；重點在「展示我很懂／我做到了」優先 `self_enhancement`。
- `altruistic` 需有明確「幫助別人」語意，不可僅因內容詳細就標註。
- 沒有明顯分享意圖時標示 `insufficient`，不要從內容豐富度反推動機。

## 覆蓋率補充

- 本理論門檻為 70%，低於另外兩個理論。理由見 [00-input-and-gate.md](00-input-and-gate.md)。
- 若大量證據只有功能描述而無分享意圖，要在限制章節說明，不要把功能描述當成分享動機。

## STP 對接建議值

選用本理論時，`stp_mapping` 填：

- `attribute_group_recommendation`: `benefit_use|brand_image|brand_personality`
- `suggested_stat_roles`: `["segmentation", "targeting"]`

不含 `attribute_function`，因為口碑動機處理的是分享意圖，不是產品規格。

## 研究應用

- 判讀不同證據來源中，分享行為的主導動機是否一致
- 區分「為了幫助他人」與「為了展現自我」等常見混淆動機
- 評估情緒性訊號是否正在放大品牌風險或傳播擴散
