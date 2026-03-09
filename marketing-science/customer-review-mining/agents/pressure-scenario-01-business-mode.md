# Pressure Scenario 01: Business Mode

## Purpose

測試 skill 在商業摘要模式下，是否能維持三大主題、證據紀律與可執行建議。

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
- 忽略比較維度
- 建議太空泛，沒有對應證據
- Executive Summary 過度理論化

## Pass Criteria

- 先重述分析目標與比較維度
- 第一層輸出維持三大主題
- 每個高優先建議都對應痛點與證據
- 理論只在次要層補充，不搶主輸出

## Fail Signs

- 沒有 `Theme Analysis Table`
- 沒有明確 iOS vs Android 比較
- 建議沒有衡量方式
- 只講理論，不講具體問題
