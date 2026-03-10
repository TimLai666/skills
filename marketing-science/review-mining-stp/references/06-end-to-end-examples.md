# End-To-End Examples

## Example A: Full STP

### Input

```json
{
  "run_mode": "full",
  "analysis_goal": "根據評論完成 STP 並提出優先策略",
  "reviews": [
    {
      "id": "R01",
      "customer_id": "C001",
      "review_text": "包裝質感好，適合和朋友分享，但價格有點高",
      "channel": "app_store",
      "rating": 3
    },
    {
      "id": "R02",
      "customer_id": "C002",
      "review_text": "提神效果不錯，會回購，但希望價格再合理一點",
      "channel": "app_store",
      "rating": 5
    }
  ]
}
```

### Expected Output Requirements

- 輸出完整 `Segmentation Summary`、`Targeting Summary`、`Positioning Summary`、`Integrated STP Actions`
- `Segmentation Summary` 內含人／貨／場、`System 1 / System 2`、Maslow 關鍵字
- `Positioning Summary` 內含理想點與四象限策略
- `Positioning Summary` 內含真實散佈圖、品牌點、理想點、由原點出發的屬性向量、座標表與向量表

## Example B: Segmentation Only

### Input

```json
{
  "run_mode": "segmentation",
  "analysis_goal": "只建立市場區隔與畫像",
  "reviews": [
    { "id": "R11", "review_text": "跟同事一起喝很有氣氛，包裝也很體面" },
    { "id": "R12", "review_text": "CP 值普通，但提神效果夠" }
  ]
}
```

### Expected Output Requirements

- 僅輸出 segmentation 相關段落
- 不輸出完整 targeting / positioning
- 若分群初跑出現 `<5%` 小群，`Execution Scope Summary` 必須記錄重跑

## Example C: Targeting With Upstream Artifacts

### Input

```json
{
  "run_mode": "targeting",
  "analysis_goal": "界定現有與潛在目標市場",
  "upstream_artifacts": {
    "segment_profiles": [
      { "segment_id": "S1", "share": 0.38, "traits": ["重視提神", "對價格敏感"] },
      { "segment_id": "S2", "share": 0.27, "traits": ["重視分享情境", "偏好包裝質感"] }
    ]
  },
  "comparison_axes": ["loyalty", "purchased_or_not"]
}
```

### Expected Output Requirements

- 直接使用 `segment_profiles`
- 執行 `current-target-market` 與 `potential-target-market`
- 依反應變數型態切分方法
- 最終輸出必含 `Target Selection Decision`

## Example D: Positioning Only

### Input

```json
{
  "run_mode": "positioning",
  "analysis_goal": "只做定位評分表與知覺圖",
  "brands": ["品牌A", "品牌B", "品牌C"],
  "ideal_point_definition": "消費者心中最理想的即飲咖啡",
  "reviews": [
    { "id": "R21", "review_text": "品牌A包裝有質感，但價格偏高" },
    { "id": "R22", "review_text": "品牌B價格合理，但形象普通" }
  ]
}
```

### Expected Output Requirements

- 先建立 `Positioning Scorecard`
- 預設 `positioning_method_used = factor_analysis`
- 輸出 `POD / POP`、理想點分析與四象限策略矩陣
- 輸出 `Perceptual Map Figure`
- 圖面保留品牌點與理想點
- 圖面疊加由原點 `(0,0)` 出發的屬性向量
- 輸出 `Perceptual Map Coordinate Table` 與 `Perceptual Map Vector Table`

## Example E: Custom Missing Prerequisite

### Input

```json
{
  "run_mode": "custom",
  "analysis_goal": "只畫知覺圖",
  "requested_modules": ["perceptual-map"]
}
```

### Expected Output Requirements

- 回傳 `MissingPrerequisiteOutput`
- `acceptable_upstream_artifacts` 至少列出 `positioning_scorecard`
- `auto_backfill_allowed=false`

## Example G: MDS Without Attribute Vectors

### Input

```json
{
  "run_mode": "positioning",
  "analysis_goal": "使用品牌相似性資料建立知覺圖",
  "positioning_method": "mds",
  "upstream_artifacts": {
    "brand_similarity_matrix": [
      [0, 2, 5],
      [2, 0, 3],
      [5, 3, 0]
    ]
  },
  "brands": ["品牌A", "品牌B", "品牌C"]
}
```

### Expected Output Requirements

- 輸出品牌點 / 理想點散佈圖
- 明示 `attribute_vectors_not_defined`
- 不輸出假的向量表

## Example F: Cluster Share Guardrail

```json
{
  "initial_k": 4,
  "initial_cluster_shares": [0.51, 0.29, 0.14, 0.04],
  "rerun_trigger": "lowest_share_below_threshold",
  "threshold": 0.05
}
```

### Expected Output Requirements

- 若最低 share `< 0.05`，降低 `k`
- `Execution Scope Summary` 必須記錄 `cluster_threshold`、`reruns_performed`、`final_k`
