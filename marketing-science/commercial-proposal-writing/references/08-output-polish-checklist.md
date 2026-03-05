# Output Polish Checklist

## 使用方式

本清單在 Generate / Review 輸出最後一階段執行。全部通過才可視為正式版輸出。

## 0) Data Sufficiency Gate（前置閘）

- [ ] 核心阻斷欄位已檢查：`proposal_type`, `target_customer`, `problem_statement`, `goal_kpi`, `available_data`。
- [ ] 若資料不足，已改輸出 `MissingDataQueryOutput`，未直接輸出完整正文。
- [ ] 若使用者回覆「沒有資料」，已提供 A/B/C/D 選單且等待使用者選擇。

## 1) 敘事完整性（新增）

- [ ] 最終輸出主體為 `narrative_body`，不是模板填空。
- [ ] 正文章節具連續敘事，非僅標題或條列。
- [ ] 未出現占位符（如 `{{...}}`）與空欄格式。

## 2) 內容保全（新增）

- [ ] 已輸出 `template_coverage_map`。
- [ ] STP/4P、財務推導、風險、里程碑、Ask 均有對應正文章節。
- [ ] `coverage_status=pass`；若 fail 已先補寫正文。

## 3) 結構完整性

- [ ] 已包含 `DraftOutput` 或 `ReviewOutput` 必要章節。
- [ ] 已包含 `style_metadata` 或 `語氣修正清單`。
- [ ] STP/4P 與財務風險段落未遺漏。

## 4) 語氣與正式度

- [ ] 口語詞與情緒詞已移除。
- [ ] 模糊形容詞已量化或加上條件。
- [ ] 未出現無證據保證句。
- [ ] 每段至少一個可核對元素（數字/條件/時間/責任人/驗證方法）。

## 5) 受眾一致性

- [ ] `tone_profile_final` 與受眾一致。
- [ ] 若發生語氣衝突，已附風險提示。
- [ ] 語氣檔位詞彙符合對應 style guide。

## 6) 可決策性與可追溯性

- [ ] Ask 明確、可執行、具時間點。
- [ ] 風險與對策成對出現。
- [ ] 關鍵數字可回溯到資料來源或顯式假設。
- [ ] 所有推估已標示 `Assumption` + `Validation Needed` + `Risk`（若為假設版）。

## 7) Review 模式專用

- [ ] 已確認原稿可審核；若缺原稿已先補件提問。
- [ ] 「口語句 -> 正式句」對照至少 8 條（短稿至少 5 條且有註記）。
- [ ] 每條對照都有修正理由。
- [ ] 已輸出 `missing_template_content` 與 `reintegrated_rewrite`。

## 8) 結尾確認句

輸出結尾附上：

- 「本版本已完成正式語體與內容保全檢核，可用於對外或決策審閱。」
