# Pressure Scenario 01: Business Mode

## Purpose

測試 skill 在商業摘要模式下，是否能維持三大主題、證據紀律、動態題項生成與可執行建議。

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

- 直接用情緒分類取代主題分析
- 跳過動態題項生成，改用固定 rubric
- 忽略比較維度
- 建議太空泛，沒有對應證據

## Pass Criteria

- 先重述分析目標與比較維度
- 第一層輸出維持三大主題
- 題項是從語料生成且跨評論共用
- 每個高優先建議都對應痛點與證據

## Fail Signs

- 沒有 `Theme Analysis Table`
- 直接列固定題項
- 沒有明確 iOS vs Android 比較
- 建議沒有衡量方式
