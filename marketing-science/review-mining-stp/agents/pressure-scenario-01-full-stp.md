# Pressure Scenario 01: Full STP

## Purpose

驗證完整模式是否覆蓋 STP 全鏈路。

## Scenario

輸入條件：

- 多品牌即飲咖啡評論
- 任務要求包含市場區隔、目標市場選擇、品牌定位、知覺圖、策略矩陣

資料欄位：

- `review_text`
- `created_at`
- `channel`
- `rating`
- `brands`

## Failure Modes Under Test

- 僅改名，未形成 STP 結構
- segmentation 跳過人／貨／場
- 缺少 `System 1 / System 2`
- cluster `<5%` 仍被保留
- targeting 僅列差異，不做 selection
- positioning 缺少理想點、`POD / POP`、四象限策略

## Pass Criteria

- 輸出完整 `Segmentation Summary`、`Targeting Summary`、`Positioning Summary`
- 含 Maslow keywords
- `貨` 類含 `System 1 / System 2`
- 群組占比均 `>5%`
- 含 `Target Selection Decision`
- 含品牌欄、理想點、知覺圖方法
- 含 `POD / POP`
- 含訴求 / 改善 / 改變 / 放棄

## Fail Signs

- 缺少 target selection
- 缺少理想點
- 缺少 cluster rerun 規則
- 缺少四象限策略
