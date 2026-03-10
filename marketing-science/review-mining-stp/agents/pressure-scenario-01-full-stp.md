# Pressure Scenario 01: Business Mode

## Purpose

測試 skill 在商業摘要模式下，是否同時滿足：
- 三大主題分析
- 理論必經映射
- 研究級統計驗證
- 評分後顧客分群
- 動態題項生成與可執行建議

## Scenario

使用者提供 350 則跨 App Store 與客服工單評論，要求：
- 找出最近 30 天最嚴重的 3 個痛點
- 比較 iOS 與 Android 差異
- 給產品與客服團隊下週可執行建議

資料包含：
- `review_text`
- `created_at`
- `channel`
- `version`
- 部分 `rating`

## What This Scenario Tries To Break

- 跳過理論階段，只做主題表
- 把理論當選配，省略 `Theory Coding Summary`
- 沒有先引導 `$maslow-five-needs-marketing` 就直接做馬斯洛映射
- 跳過動態題項生成，改用固定 rubric
- 跳過統計檢定，直接下差異結論
- 未完成評分就直接分群
- 只報群名，沒有分群穩定度
- 建議沒有證據回溯

## Pass Criteria

- 有完整 `Theory Coding Summary` 且含四理論映射
- 有 Maslow 協作狀態欄位（`attempted`, `used`, `fallback_reason`）
- 若 `used: false`，有明確 fallback 理由與低信心標記
- 第一層輸出維持三大主題
- 題項由語料生成且跨評論共用
- 有 `Statistical Validation Summary`（含 FDR、effect size、CI）
- 有 `Customer Cluster Summary` 與 `Cluster-Specific Priority Actions`
- 分群依據為 core 題項分數矩陣，不是主題文字
- 建議具體且可追溯到評論證據

## Fail Signs

- 缺少 `Theory Coding Summary`
- 四理論中有理論被省略且未說明限制
- 未引導 `$maslow-five-needs-marketing`，也沒有 fallback 理由
- 把 fallback 寫成成功協作
- 直接列固定題項
- 統計結果只有 p-value，沒有 effect size/CI/FDR
- 先分群再評分（反序）
- 未回報 cluster stability（ARI/NMI 或同級指標）
- 建議沒有量測指標或證據
