# End-To-End Examples

## How To Read These Examples

每個案例都分成兩層：

- `Agent Request`: 使用者 / agent 對 skill 的請求長相
- `Runnable Artifacts`: 真正可直接給 scripts 跑的 scored artifacts

## Example A: Full STP From Raw Reviews

### Agent Request

```json
{
  "run_mode": "full",
  "analysis_goal": "根據評論完成 STP 並提出優先策略",
  "reviews": [
    {
      "id": "R01",
      "review_text": "包裝質感好，適合和朋友分享，但價格有點高",
      "channel": "app_store",
      "rating": 3
    },
    {
      "id": "R02",
      "review_text": "提神效果不錯，會回購，但希望價格再合理一點",
      "channel": "app_store",
      "rating": 5
    }
  ]
}
```

### Runnable Artifacts

- `review_scoring_table.csv`
- `review_foundation.json`
- `analysis_context.json`
- `brands.json`
- `ideal_point.json`

### Expected Output Requirements

- scripts 會先產出 `segmentation_variables.csv`、`targeting_dataset.csv`、`positioning_scorecard.csv`
- 完整 `Segmentation Summary`、`Targeting Summary`、`Positioning Summary`
- `Execution Scope Summary` 要列出 canonical inputs 與 emitted intermediates
- `Positioning Summary` 要有真實知覺圖、ideal point、pairwise competition landscape

## Example B: 14 項案例 Schema

### Agent Request

```json
{
  "run_mode": "full",
  "analysis_goal": "沿用既有 14 項案例維度，但不要把它當固定契約",
  "reviews": "..."
}
```

### Runnable Artifacts

- `review_scoring_table.csv`
  - 含 `review_id`, `unit_id`, `brand`
  - 另含 14 個 score columns，例如 `fast_shipping`, `quality_good`, `value_for_money`
- `review_foundation.json`
  - `dimension_catalog` 把 14 項欄位標上 `theme`, `theory_tags`, `stat_roles`
  - `theme_mapping` 至少涵蓋 `service_experience`, `product_performance`, `value_perception`

### Expected Output Requirements

- scripts 可以完整跑通
- validator 不得因為不是固定欄位順序或未來擴充欄位而失敗
- traceability 要把這個案例標為 example schema，而不是 canonical schema

## Example C: Full STP With Custom Schema

### Agent Request

```json
{
  "run_mode": "full",
  "analysis_goal": "讓 AI 自動抽出新維度，不沿用既有 14 項名稱",
  "reviews": "..."
}
```

### Runnable Artifacts

- `review_scoring_table.csv`
  - 含自定義數值欄位，例如 `delivery_confidence`, `setup_clarity`, `premium_feel`
- `review_foundation.json`
  - `dimension_catalog` 每列至少有 `column`, `label`, `theme`, `theory_tags`, `stat_roles`
- `analysis_context.json`
  - 可帶入 `comparison_axes`

### Expected Output Requirements

- scripts / validator 不依賴固定 14 欄
- targeting 預設從 `stat_roles` 取 `current_target` / `potential_target`
- `comparison_axes` 可覆蓋預設排序軸

## Example D: Segmentation Only With Direct Intermediate Artifact

### Agent Request

```json
{
  "run_mode": "segmentation",
  "analysis_goal": "只建立市場區隔與畫像"
}
```

### Runnable Artifacts

- `review_foundation.json`
- `segmentation_variables.csv`
- `analysis_context.json`

### Expected Output Requirements

- 只輸出 segmentation 相關段落
- 若分群過程出現 `< 5%` 小群，必須在 `Execution Scope Summary` 記錄 `reruns_performed`

## Example E: Targeting Partial Run With Upstream Segment Profiles

### Agent Request

```json
{
  "run_mode": "targeting",
  "analysis_goal": "界定現有與潛在目標市場",
  "comparison_axes": ["seller_trust", "repurchase_intent", "problem_resolution"]
}
```

### Runnable Artifacts

- `targeting_dataset.csv`
- `segment_profiles.json`
- `review_foundation.json` 或含同等 role 資訊的上游輸出
- `analysis_context.json`

### Expected Output Requirements

- 直接使用 `segment_profiles`
- 輸出 `priority_segments / secondary_segments / deprioritized_segments`
- `target_selection_rationale` 必須引用 `comparison_axes_used`

## Example F: Positioning Only

### Agent Request

```json
{
  "run_mode": "positioning",
  "analysis_goal": "只做定位評分表與知覺圖",
  "ideal_point_definition": "消費者心中最理想的品牌形象"
}
```

### Runnable Artifacts

- `positioning_scorecard.csv`
- `brands.json`
- `ideal_point.json`
- `analysis_context.json`

### Expected Output Requirements

- `positioning_method_used` 預設為 `factor_analysis`
- `positioning_scorecard` 輸出要含理想點
- `Dynamic Scorecard Summary` 必須有距離、落差、信度、效度
- `competition_landscape` 必須是品牌 pairwise 距離

## Example G: Custom Missing Prerequisite

### Agent Request

```json
{
  "run_mode": "custom",
  "analysis_goal": "只畫知覺圖",
  "requested_modules": ["perceptual-map"]
}
```

### Runnable Artifacts

- `brands.json`
- `ideal_point.json`

### Expected Output Requirements

- 回傳 `MissingPrerequisiteOutput`
- `missing_prerequisites` 只列真正缺少的檔案，例如 `positioning_scorecard.csv`
- `auto_backfill_allowed=false`

## Example H: Raw Reviews Sent Directly To Scripts

### Runnable Artifacts

- `reviews.json`

### Expected Output Requirements

- scripts 不直接處理 raw reviews
- `MissingPrerequisiteOutput` 必須指向 `review_scoring_table.csv` 與 `review_foundation.json`
- `next_step_rule` 必須把責任明確指回 agent-layer preprocessing
