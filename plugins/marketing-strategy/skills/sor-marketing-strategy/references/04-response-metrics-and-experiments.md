# Response Metrics And Experiments

## Purpose

把 response 從「有沒有成交」擴大成可分階段觀察的指標系統，並把 S-O-R 假設轉成可測試的實驗。

## Response Ladder

| Response Level | 常見指標 | 前導訊號 | 典型風險 |
| --- | --- | --- | --- |
| attention | impression CTR, view rate, 停留 | 首屏停留、滑動、開信 | 只買到注意，沒買到意義 |
| engagement | click depth, add-to-cart, 收藏, 回覆 | 二次互動、內容展開 | 互動高但意圖弱 |
| conversion | signup, order, booking, lead | checkout start, form start | 壓榨短期轉換傷害信任 |
| repurchase | repeat order, renewal, upgrade | 回訪、再瀏覽、再開信 | 促銷依賴過高 |
| advocacy | referral, review, share, UGC | NPS、收藏、轉傳 | 聲量和推薦品質脫鉤 |

## KPI Ladder Rules

- 定義目標結果及能觀察作用路徑的前導訊號；有重要副作用時加入對應指標。數量依問題與資料決定。
- 若目標是 `conversion`，guardrail 常見是：
  - bounce rate
  - refund rate
  - lead quality
- 若目標是 `repurchase`，guardrail 常見是：
  - unsubscribe rate
  - notification mute
  - complaint/support rate

## Activity Participation Rate

活動參與率是衡量參與行為的一種例子，只有符合本次目標時才使用，欄位可命名為 `activity_participation_rate`。

定義：
- 在指定期間內，完成指定活動行為的人數占可參與人數的比例。

計算口徑：

```text
activity_participation_rate
= unique_users_completed_activity / unique_users_eligible_for_activity
```

適用場景：
- 品牌活動、直播互動、社群任務、會員任務、門市體驗活動。
- S-O-R 中常用來衡量 `engagement` 層級的 response。

使用注意：
- 需要明確定義 `eligible`，避免把無法參與的人算進分母。
- 若活動分多步驟，另補 step-level participation，避免只看總參與率。
- 依活動目標決定是否同時觀察後續行為，不固定搭配成交或回購指標。

## Experiment Mapping

把 S-O-R 假設寫成：

```text
Because [current organism problem],
we believe changing [stimulus]
will shift [desired organism state]
and increase [target response]
for [audience].
We'll measure this through [leading metrics] and [result metric].
```

## Good Experiment Targets

- 一次只驗證一個主要 stimulus change
- 先測最接近瓶頸的 stimulus
- 先選 impact 高、實作成本低、反效果與執行風險可控的測試

## Example Patterns

### 落地頁

- 問題：有流量，註冊低
- 假設：不是 CTA 顏色問題，而是 trust/risk 沒建好
- 可測 stimulus：
  - 將 social proof 與 guarantee 前移
  - 簡化 hero 訊息
- leading metrics：
  - CTA click-through rate
  - pricing section view
- result metric：
  - signup completed

### CRM / 回購

- 問題：推播有開，但回購低
- 假設：訊息有 attention，沒有 relevance 或 trust
- 可測 stimulus：
  - 促銷導向 vs 使用情境導向
  - generic offer vs 分群 offer
- leading metrics：
  - open rate
  - click-to-product rate
- result metric：
  - repeat purchase rate
- guardrail：
  - unsubscribe
  - block/mute rate

## Handoff Notes

- 需要正式樣本量、檢定方法與測試期間時，使用可用且適用的統計分析能力完成。
- 需要事件、參數、GA4/GTM 實作時，使用可用的追蹤與開發工具完成，不把規劃當成已實作。

## Minimum Output For Experiment Plan

使用者需要實驗計畫時列出：
- `hypothesis`
- `control`
- `variant`
- `primary_metric`
- `leading_metrics`
- `guardrails`
- `decision_rule`
