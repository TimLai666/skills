# Pressure Scenario 02: Theory Mode

## Purpose

測試 skill 在理論導向需求下，是否遵守理論必經規格並保留商業主題骨架。

## Scenario

使用者提供 120 則評論，要求：
- 用四個理論框架分析評論
- 顯示三大主題與優先項
- 附上動態題項摘要
- 必要時可請 agent 用其他 skill 補充深度詮釋

## What This Scenario Tries To Break

- 只套用 1-2 個理論
- 理論標籤沒有證據
- 題項不是語料級共用集合
- 跳過 `$maslow-five-needs-marketing` 協作路由
- 無條件把外部 skill 當主流程

## Pass Criteria

- 四理論全部出現映射結果
- 每個理論都有證據與信心等級
- 理論證據弱時有低信心與限制聲明
- 馬斯洛映射有協作狀態追蹤（`attempted`, `used`, `fallback_reason`）
- `theory_evidence_trace` 含 `source_skill`
- 題項先語料生成再回頭評分
- 外部 skill 僅作補充，不取代主流程

## Fail Signs

- 少於四理論且未解釋
- 理論結論沒有證據引用
- 沒有引導 `$maslow-five-needs-marketing` 且無 fallback 記錄
- `source_skill` 缺失或把 fallback 偽裝為外部成功協作
- 題項逐篇漂移
- 直接用外部 skill 替代本技能分析
