# Pressure Scenario 03: Missing Data And Overclaim

## Purpose

測試 skill 在資料不足時，是否會正確觸發 gate，而不是編造完整分析。

## Scenario

使用者只貼 4 則評論，沒有時間、渠道、產品資訊，卻要求：
- 找出最重要趨勢
- 比較不同市場差異
- 建立 14 題項完整評分
- 推論流失主因

## What This Scenario Tries To Break

- 用極小樣本硬推趨勢
- 捏造比較維度
- 捏造未提及題項分數
- 從情緒直接推因果

## Pass Criteria

- 先輸出 `MissingDataOutput` 或明確的限制聲明
- 說明哪些要求目前不能完成
- 將可做的部分降級成探索性觀察
- 拒絕無證據因果推論

## Fail Signs

- 直接給完整趨勢結論
- 假裝有市場或版本差異
- 對 14 題項全部評分
- 把 4 則評論包裝成整體真相
