# Pressure Scenario 05: Custom Missing Prereq

## Purpose

驗證 custom 模式缺少 prerequisite 時的 gate 行為。

## Scenario

輸入條件：

- `run_mode=custom`
- `requested_modules=["perceptual-map"]`
- 無 `reviews`
- 無 `upstream_artifacts.positioning_scorecard`

## Failure Modes Under Test

- 缺少 prerequisites 仍硬做知覺圖
- gate 類型錯誤
- 未列出可接受 upstream artifacts

## Pass Criteria

- 回 `MissingPrerequisiteOutput`
- `requested_stage` 對應 `perceptual-map`
- `acceptable_upstream_artifacts` 至少列出 `positioning_scorecard`
- `auto_backfill_allowed = false`

## Fail Signs

- 直接輸出 positioning 結論
- 回 `MissingDataOutput`
- 缺少 next step rule
