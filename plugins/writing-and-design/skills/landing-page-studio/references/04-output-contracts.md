# Output Contracts

這些欄位供結構化交付或工具整合使用；一般對話直接交付成品、來源與驗證摘要，不必把頁面 HTML 再塞進 JSON。

## LandingPageInput 範例

以下為假設旅宿頁面的輸入示例，實際文字與主張須依本案資料確認：

```json
{
  "brand_theme": "溫泉旅宿",
  "value_props": ["客房獨立湯池", "在地食材早餐", "車站接駁"],
  "primary_cta": "查詢空房",
  "style_direction": "暖單色編輯部極簡",
  "output_mode": "single-file-html",
  "variant_mode": "single",
  "autonomy_mode": "multi-iteration",
  "animation_level": "high",
  "motion_preference": "respect-reduced-motion"
}
```

## MissingDataOutput

缺少必要資料時提供 `missing_fields`、`why_needed`、`questions_to_user` 與 `next_step_rule`。問題使用自然語言，說明缺項如何影響頁面；不要要求重填已知資訊。

## GenerationOutput

| 欄位 | 實際交付內容 |
| --- | --- |
| artifact_type | single-html / react-tree |
| artifact_payload | 成品檔案／專案路徑；要求 inline 時才放原始碼 |
| asset_sources | 各素材的來源 URL、提供者與必要 attribution |
| animation_manifest | 實際效果的 id、category、library、target、trigger、fallback；規格見 03 |
| autonomy_report | 有進行迭代時記錄問題、修正與原因，不虛構候選稿或分數 |
| qa_report | 實際檢查方式、結果、效能數據與未驗證項目 |

`variant_mode=batch` 時加上 `batch_results` 與 `variant_diff_summary`，記錄各版實際的風格、節奏與微互動差異。版本比較保留相同主要行動與真實內容，避免用不同證據製造勝負。
