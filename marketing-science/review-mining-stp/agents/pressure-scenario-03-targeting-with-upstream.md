# Pressure Scenario 03: Targeting With Upstream

## Purpose

驗證 targeting 模式是否正確使用 upstream artifacts。

## Scenario

輸入條件：

- `run_mode=targeting`
- 已提供 `segment_profiles`
- 已提供 `comparison_axes`
- 無原始評論

## Failure Modes Under Test

- 忽略 upstream artifacts
- 因無評論而誤判無法執行 targeting
- 僅做比較表，不做 target selection

## Pass Criteria

- 正確使用 `segment_profiles`
- 不強迫回到 segmentation
- 產出 `Current Target Market Summary`、`Potential Target Market Summary`、`Target Selection Decision`

## Fail Signs

- 回 `MissingDataOutput`
- 忽略 artifacts
- 缺少 selection decision
