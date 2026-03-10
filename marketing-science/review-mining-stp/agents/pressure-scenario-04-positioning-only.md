# Pressure Scenario 04: Positioning Only

## Purpose

驗證 positioning 模式是否正確建立定位評分表與知覺圖。

## Scenario

輸入條件：

- 任務僅要求 positioning
- 提供 `brands` 與 `ideal_point_definition`
- 輸出包含知覺圖與定位診斷

## Failure Modes Under Test

- 未先建評分表即直接輸出定位結論
- 缺少理想點
- 預設錯用 `MDS`
- 缺少 `POD / POP`
- 缺少四象限策略矩陣
- 只有知覺圖摘要，沒有真實散佈圖
- 圖上缺少品牌點
- 有向量但不是由原點出發
- 圖後製移除品牌點
- 圖像與座標 / 向量資料不一致

## Pass Criteria

- 含 `Positioning Scorecard`
- 含 `Dynamic Scorecard Summary` 且包含信度 / 效度分析
- `positioning_method_used = factor_analysis`，除非輸入明確為相似性資料
- 含理想點分析、競爭態勢、`POD / POP`
- 含 `Perceptual Map Figure`
- 圖面保留品牌點與理想點
- 含由原點 `(0,0)` 出發的屬性向量
- 含 `Perceptual Map Coordinate Table` 與 `Perceptual Map Vector Table`
- 含訴求 / 改善 / 改變 / 放棄

## Fail Signs

- 缺少理想點
- 缺少定位評分表
- 缺少四象限策略
- 缺少圖像輸出
- 缺少向量表
- 向量起點不是原點
