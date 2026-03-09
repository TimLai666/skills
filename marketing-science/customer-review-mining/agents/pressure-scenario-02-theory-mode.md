# Pressure Scenario 02: Theory Mode

## Purpose

測試 skill 在研究型需求下，是否仍保留商業主題骨架，同時正確使用理論 overlay 與 14 題項評分。

## Scenario

使用者提供 120 則商品評論，要求：
- 用理論架構整理評論
- 顯示三大主題
- 加上 14 題項評分摘要
- 附上代表性引文

## What This Scenario Tries To Break

- 直接把理論當第一層分類
- 沒有引文就硬做理論判讀
- 對每個題項都評分，即使評論沒有提到
- 把研究型輸出寫得冗長失焦

## Pass Criteria

- 第一層仍是 `service_experience`、`product_performance`、`value_perception`
- 理論視角有證據，不是純推測
- 14 題項的 `0` 分被正確保留
- 研究型補充不破壞主輸出的可讀性

## Fail Signs

- 沒有三大主題
- 每題幾乎都有高分
- 理論標籤沒有代表性評論
- 研究附錄蓋過主要結論
