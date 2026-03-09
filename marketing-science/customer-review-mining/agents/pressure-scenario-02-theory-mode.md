# Pressure Scenario 02: Theory Mode

## Purpose

測試 skill 在研究型需求下，是否仍保留商業主題骨架，同時正確使用條件式理論協作與動態題項。

## Scenario

使用者提供 120 則商品評論，要求：
- 用理論架構整理評論
- 顯示三大主題
- 附上動態題項摘要
- 如有必要可請 agent 用其他 skill 輔助理論解釋

## What This Scenario Tries To Break

- 直接把理論當第一層分類
- 沒有引文就硬做理論判讀
- 不做語料級題項生成
- 無條件調用外部 skill

## Pass Criteria

- 第一層仍是 `service_experience`、`product_performance`、`value_perception`
- 題項先由整批評論生成，再回頭評分
- 理論視角有證據，不是純推測
- 只有在需求真的更深時才啟用 agent 協作

## Fail Signs

- 沒有三大主題
- 題項逐篇漂移
- 理論標籤沒有代表性評論
- 每次都強制呼叫其他 skill
