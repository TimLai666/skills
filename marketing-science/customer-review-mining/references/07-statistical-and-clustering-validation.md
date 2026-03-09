# Statistical And Clustering Validation

## Purpose

固定「評分後」的統計與分群驗證規格，確保結果可比較、可審計、可落地。

## Global Settings

- `alpha = 0.05`
- 多重比較修正：`BH-FDR`
- 信賴區間：`95% CI`
- 所有推論都需回報樣本數、效應量與限制
- 禁止把關聯差異寫成因果結論

## Statistical Test Selection Matrix

| Metric Type | Groups | Primary Test | Small-Sample Fallback | Effect Size |
| --- | --- | --- | --- | --- |
| Item score (0-7, ordinal) | 2 | Mann-Whitney U | Permutation rank test | Cliff's delta |
| Item score (0-7, ordinal) | >=3 | Kruskal-Wallis | Permutation Kruskal | epsilon-squared |
| Proportion (coverage/high/low rate) | 2 | two-proportion z | Fisher's exact | risk difference / odds ratio |
| Proportion (coverage/high/low rate) | >=3 | chi-square | exact/permutation chi-square | Cramer's V |

## Minimum Statistical Result Fields

每個 comparison 必含：

- `comparison_id`
- `metric`
- `test_name`
- `groups`
- `group_n`
- `statistic`
- `p_value`
- `p_value_adj`
- `effect_size`
- `ci_95`
- `assumption_checks`
- `conclusion`
- `caveats`

## Effect Size Interpretation Guide

### Cliff's Delta

- `< 0.147`: negligible
- `0.147-0.33`: small
- `0.33-0.474`: medium
- `>= 0.474`: large

### Epsilon-Squared

- `< 0.01`: negligible
- `0.01-0.08`: small
- `0.08-0.26`: medium
- `>= 0.26`: large

## Clustering Protocol

### Feature Matrix

- 僅使用 `generated_items` 的 `core` 題項分數
- `0` = 未關注，`1-7` = 關注強度
- 有 `customer_id` 時先聚合到顧客層（每題項中位數）
- 無 `customer_id` 時使用 `review_proxy` 並強制標記限制

### Model Pipeline

1. `K-medoids` for k=2..8（silhouette 選最佳 k）
2. `Hierarchical (Ward)` on cluster centroids（群間關係解讀）
3. bootstrap 穩定度評估（建議 >= 200 次）

### Minimum Clustering Result Fields

- `cluster_configuration`
- `cluster_profiles`
- `cluster_assignments`
- `cluster_stability`
- `cluster_action_map`

## Cluster Stability Threshold Guidance

- `ARI mean >= 0.70`: 穩定
- `0.50 <= ARI mean < 0.70`: 中等，需保守解讀
- `ARI mean < 0.50`: 不穩定，僅 exploratory

## Low-Sample Guardrail

低樣本仍要跑統計與分群，但必須：

- `exploratory = true`
- `confidence = low`
- 回報 `limitations` 與 `decision_guardrail`
- 禁止輸出高信心政策決策語句

## Fail Conditions

- 缺少 `BH-FDR` 校正
- 只報 p-value 不報 effect size/CI
- 未先評分即直接分群
- 使用主題文字而非 score matrix 分群
- 小樣本輸出高信心強結論
