# 串接 review-mining-stp（選用）

只有在要把編碼結果帶進 `review-mining-stp` 時才需要讀這一份。本 skill 可以完全獨立使用。

## 先搞清楚：兩邊的 `theory_annotations` 不是同一個東西

| | 掛在哪 | 回答什麼 | 結構 |
| --- | --- | --- | --- |
| 本 skill | 每一則證據（item-level） | 這句話屬於哪個構面 | 陣列，每筆有 `item_id` / `family` / `subtheory` / `quote` |
| `review-mining-stp` | `dimension_catalog` 的每個屬性欄位（attribute-level） | 這個屬性對應哪些理論構面 | 字典 `{family: [subtheory, ...]}` |

同名但層級不同。**不能把本 skill 的 JSON 直接餵給下游腳本**，會被 `io.py` 的契約檢查擋下。

`review-mining-stp` 的屬性探索階段本來就會自己走一遍理論標註，不依賴上游。本 skill 的價值是提供有引文可追溯的 item-level 證據基礎，讓那一步不必從零判斷。

## 轉換步驟（人工）

1. **先做屬性聚類。** 把 `theory_annotations` 的 quote 依「同一個客戶關注點」分組，每組成為一個候選屬性。這一步是本 skill 的輸出到 `dimension_catalog` 之間唯一需要判斷的地方。
2. **聚合標籤。** 每個屬性收集所有被分進來的 quote 的 `family` + `subtheory`，去重後寫成字典：

   ```json
   "theory_annotations": {
     "product_positioning": ["attributes", "functions"],
     "purchase_motivation": ["functional"]
   }
   ```

3. **填 `attribute_group`。** 取本 skill `stp_mapping.attribute_group_recommendation` 的建議值，合法值只有 `attribute_function` / `benefit_use` / `brand_personality` / `brand_image`。
4. **填 `stat_roles`。** 取 `stp_mapping.suggested_stat_roles`。
5. **補齊 `dimension_catalog` 其餘必填欄位**：`column`、`label`、`theme`、`salience_column`、`valence_column`、`plain_language_definition`。這些本 skill 不產出，要在下游自行定義。

## 常見錯誤

- 直接把 `theory_annotations` 陣列貼進 `dimension_catalog` — 結構不符，會 fail contract。
- 漏掉 `valence_column` — 那是下游必填欄位，本 skill 不產出。
- 使用 `theories` 以外的 family — 下游 taxonomy 只認 `product_positioning` / `maslow` / `purchase_motivation` / `wom_motivation` / `dual_process`。本 skill 只涵蓋其中三個，`maslow` 與 `dual_process` 需在下游自行判斷。
