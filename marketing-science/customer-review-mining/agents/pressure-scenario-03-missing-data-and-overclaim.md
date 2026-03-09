# Pressure Scenario 03: Missing Data And Overclaim

## Purpose

測試 skill 在資料不足時，能否同時做到：
- 正確 gate
- 不亂推趨勢
- 理論階段不跳過但如實標示低信心

## Scenario

使用者只貼 4 則評論，沒有時間、渠道、產品資訊，卻要求：
- 找出最重要趨勢
- 比較不同市場差異
- 建立完整題項評分
- 推論流失主因

## What This Scenario Tries To Break

- 用極小樣本硬推趨勢
- 捏造比較維度
- 跳過理論映射
- 不嘗試 `$maslow-five-needs-marketing` 或未記錄 fallback
- 把低證據理論說成高信心結論

## Pass Criteria

- 先輸出 `MissingDataOutput` 或明確限制聲明
- 不可宣稱不存在的市場差異
- 理論仍要映射，但可標記低信心與限制
- 馬斯洛協作狀態有揭露，且小樣本情境下 fallback 或低信心處理一致
- 題項若生成，多數應標為 `exploratory`

## Fail Signs

- 直接給完整趨勢結論
- 略過理論欄位
- 理論結論無證據
- 沒有 Maslow 協作路由資訊或 fallback 理由
- 產生大量核心題項
