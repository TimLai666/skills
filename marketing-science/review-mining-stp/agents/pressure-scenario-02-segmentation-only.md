# Pressure Scenario 02: Segmentation Only

## Purpose

驗證 segmentation-only 模式是否維持輸出邊界。

## Scenario

輸入條件：

- 任務僅要求市場區隔與消費者畫像
- 不要求定位與知覺圖

## Failure Modes Under Test

- segmentation only 卻輸出完整 STP
- 缺少區隔變數 taxonomy
- 缺少人／貨／場
- 缺少 `System 1 / System 2`
- 缺少 Maslow keywords

## Pass Criteria

- 僅輸出 `Segmentation Summary`
- 含群體占比表
- 含 `<5%` rerun 規則
- 每群含清楚輪廓與敘事

## Fail Signs

- 提前輸出 targeting / positioning
- 缺少 cluster threshold
- 缺少 Maslow 關鍵字
