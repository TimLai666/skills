# Validation Checklist

## 結構檢查

- SKILL.md frontmatter 符合 repo 規範，含 name、description 與 metadata.version。
- 主檔提供輸入判斷、觸發器選擇、通路寫法、交付要求與文件讀取入口。
- references/01-trigger-playbook.md 保留七種觸發器、雙軌命名及完整例句。
- references/02-application-matrix.md 保留通路與目標套用表。
- references/03-output-contracts.md 提供完整策略與缺資料的結構化格式。
- agents/openai.yaml 與主檔一致，三個既有情境保留。

## 行為檢查

- 依目標、受眾與證據選擇方法，說明作用，不按固定數量湊觸發器。
- 完整策略具備可用的主軸、心理驅動理由與所需文案方向，不限定必須 JSON。
- 單一 CTA／標題請求直接交付所需內容，不強出多個選項或完整策略包。
- 缺資料時先使用現有脈絡，只問會影響結果的關鍵問題，假設須明示。
- 使用繁體中文與台灣用語，CTA 清楚交代下一步。
- 文案實際使用的事實與承諾有依據，不把案例條件當成通用要求。
- 某個案例條件不成立時，能根據實際情境調整表達，不直接排除整種心理驅動。

## 驗收

- quick_validate.py 通過，修改的 YAML／JSON 能解析，引用有效。
- 逐一檢查三個 pressure scenario 的條件與通過標準是否和主檔一致。
- 對照檢查：同樣提供產品與優惠，若使用者只要一個 CTA，不能套用促銷頁整包交付。
- 若實際執行情境測試，保留輸出並依上述行為判斷。文件一致性檢查不等於實測通過。
