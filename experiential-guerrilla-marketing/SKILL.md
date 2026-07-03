---
name: experiential-guerrilla-marketing
description: >
  用於體驗行銷與游擊行銷的策略規劃、創意發想與成效評估。觸發於體驗行銷、
  游擊行銷、快閃活動、品牌體驗、沉浸式體驗、低預算行銷、Ambient Marketing、
  行銷 KPI、體驗 × 游擊矩陣設計等需求,或使用者想做讓人拍照分享、低預算高效果、
  可評估成效的品牌活動。
---

# 體驗 × 游擊行銷活動設計

## Overview

把「游擊行銷（突破注意力）× 體驗行銷（創造長期記憶）」轉成一份可執行、可量測、有退場機制的活動企劃。

這個 skill 的產出是活動決策與執行計畫，不是理論講解。核心流程：先定體驗目標，再用決策樹選游擊手法，套 5E 設計體驗，設四層 KPI 與歸因機制，最後跑風險檢查與 kill criteria。

## Trigger Map

Use：
- 使用者要規劃快閃店、街頭活動、品牌體驗、低預算高擴散的線下行銷。
- 使用者要評估某個游擊創意的可行性、法規風險或成效量測方式。
- 使用者拿現成活動案例要求拆解手法與體驗結構。

Do not use：
- 純線上廣告投放優化，沒有實體或事件成分 → 不適用，量測部分可單獨參考 references/03。
- 使用者只要活動文案或視覺成稿，不需要策略決策。
- 大型檔期的整合行銷年度規劃（本 skill 處理單檔活動，不處理年度組合）。

Handoff：
- 受眾輪廓不清 → 先轉 `customer-persona-framer` 產出 Persona，再回來跑決策樹。
- 需要深挖刺激與心理機制 → 完成手法決策後轉 `sor-marketing-strategy` 細化。

## Input Contract

必填欄位：
- `brand_or_product` — 品牌與產品是什麼、賣給誰、核心賣點
- `marketing_goal` — `awareness|list_building|conversion|brand_equity` 擇一為主目標
- `budget_tier` — 預算級距（新台幣）：
  - `micro`：10 萬以下
  - `small`：10–50 萬
  - `medium`：50–300 萬
  - `large`：300 萬以上
- `target_audience` — 目標受眾輪廓與出沒場域（線上社群、實體商圈）

可選欄位：
- `venue_permission` — `owned|rented|public_with_permit|none`（自有空間／租用／可申請公共空間／無場地）
- `risk_tolerance` — `low|medium|high`（品牌能承受的法律爭議與輿論風險）
- `timeline` — 距離活動上線的準備時間

## Data Sufficiency Gate

觸發「停下補件」時，不產出企劃，回傳固定格式：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "assumptions_if_forced": [],
  "next_step_rule": "補齊必填欄位後再跑 Workflow"
}
```

`questions_to_user` 每題都要附建議選項（例如預算級距四選一），不要丟開放式問題讓使用者自己想。

停下補件（缺了會選錯手法、做白工）：
- `brand_or_product` 不明 → 無法判斷品牌調性與手法相容性，必問。
- `marketing_goal` 不明或同時要四個目標 → 要求使用者選一個主目標，其餘降為 secondary。
- `budget_tier` 完全無法推估（使用者未給且從描述推不出規模）→ 必問，因為決策樹第一層就依賴它。

列假設繼續（影響參數，不影響方向）：
- `target_audience` 模糊但產品可推 → 以該產品典型客群假設，標示 `Assumption` 並在輸出附驗證建議。
- `venue_permission` 未提供 → 預設 `none`，決策樹走「無場地」分支，並註明取得場地後可升級的手法。
- `risk_tolerance` 未提供 → 預設 `low`，自動排除 ambush 與高爭議 stunt。
- `timeline` 未提供 → 預設 8 週準備期；若選出的手法需要許可申請，回頭檢查前置天數是否夠。

所有假設集中列在輸出的 `assumptions` 段落，每條附「假設錯了會怎樣」。

## Workflow

1. **定體驗目標**：把 `marketing_goal` 對應到漏斗位置——認知/話題 → 游擊主導；記憶/情感 → 體驗主導；轉換/名單 → 兩者整合並前置歸因機制。對應規則見 [references/03-kpi-and-measurement.md](./references/03-kpi-and-measurement.md) 的漏斗分工。
2. **選游擊手法**：跑 [references/02-guerrilla-tactics-decision-tree.md](./references/02-guerrilla-tactics-decision-tree.md) 的決策樹（預算 × 風險承受 × 場地權限 × 品牌調性），輸出 1 個主手法 + 1 個備案，並記錄被否決的選項與理由。
3. **設計 5E**：依 [references/01-experience-design-playbook.md](./references/01-experience-design-playbook.md) 走 Event → Environment → Experience → Emotion → Exposure 五步，嵌入 1 個主模組 + 1–2 個次模組的 Schmitt 體驗組合（至多 3 個，超過會失焦）。
4. **設 KPI**：依 [references/03-kpi-and-measurement.md](./references/03-kpi-and-measurement.md) 的漏斗分工設四層 KPI（曝光/互動/轉換/品牌）：主目標層設必達目標、相鄰層設觀察指標、不相鄰層可明寫「不設」並附理由；歸因機制必須在創意定案前決定，不能事後補。
5. **風險檢查**：對照手法卡的法規與許可清單（台灣情境：路權、集會遊行法、商標權），逐條寫 kill criteria 與退場方案，確認 timeline 涵蓋許可申請前置天數。

## Output Contract

固定輸出以下段落，順序不可調換：

- `campaign_summary` — 一段話講清楚：誰、在哪、做什麼、為什麼會被記住。
- `assumptions` — 所有假設與「假設錯了會怎樣」；無假設時明寫「無」，不可省略此段。
- `tactic_decision` — 三個必備欄位：
  - 選定手法 + 通過決策樹四道閘門的判定摘要
  - 備案手法與切換條件
  - 至少 1 個被否決的替代方案與否決理由
- `experience_design` — 5E 五步 × Schmitt 模組對照表（標明 1 個主模組與 1–2 個次模組），含必拍點規格與參與流程腳本（每步秒數）。
- `execution_plan` — 倒推時程表（含許可申請前置天數）、人力配置、許可申請清單（項目／主管機關／前置天數）。
- `kpi_plan` — 依漏斗分工：主目標層標「必達」（含目標值或 baseline 建立方法）、相鄰層列觀察指標、不相鄰層可明寫「不設」＋理由；每個設定的指標都附歸因機制。
- `risk_and_kill_criteria` — 每個風險寫成「觸發條件 → 應變動作」句式，禁止只列風險名稱。
- `budget_allocation` — 依 `budget_tier` 拆製作/場地/人力/擴散/機動五類；機動預算不得低於總額 10%，不足時要說明從哪一類調補。

段落品質下限：`tactic_decision` 缺否決紀錄、`kpi_plan` 缺歸因機制、`risk_and_kill_criteria` 缺觸發條件，任一發生視為輸出未完成，回頭補齊再交付。

## Quality Rules

- 推薦手法不得超出 `budget_tier`：手法卡的成本級距是硬限制，不能用「精簡版」硬塞。
- `tactic_decision` 必須有被否決選項與理由，否則等於沒做決策。
- 主目標層 KPI 必有數字目標或明確的 baseline 建立方法；凡有設指標的層不能只列指標名稱；不相鄰層可誠實寫「不設」但必附理由。
- 凡在公共空間執行，`execution_plan` 必列許可項目、主管機關與前置天數。
- Exposure 要指定具體擴散機制（hashtag、必拍點、UGC 誘因、素材二次投放排程），寫「鼓勵分享」視為未完成。
- 現場必須有名單轉換機制（QR 註冊、LINE 加好友誘因），除非 `marketing_goal` 是純 `awareness` 且使用者明確放棄。
- 禁止輸出無法驗收的句子：「要有創意」「引起共鳴」「創造話題」這類詞必須換成具體機制。

## Common Mistakes

- 現場人潮沒有轉私域機制，活動結束什麼都沒留下。
- 只設曝光層 KPI，事後回答不了「所以帶來多少生意」。
- 創意自嗨：沒對照 `target_audience` 的實際出沒場域與拍照動機，做出團隊喜歡但受眾無感的裝置。
- 路人記得裝置、不記得品牌：吸睛點與品牌賣點脫節，視覺上品牌元素 3 秒內認不出來。
- 素材只用一次：活動紀錄影片、UGC 沒有二次投放與延伸計畫，浪費創意投資。
- 過度計畫：流程綁死、沒留機動預算、現場人員沒有調整權限，遇到突發只能硬撐。
- 爆紅反噬沒準備：網站流量、客服人力、庫存沒有備援，聲量高峰變成負評高峰。
- 歸因事後補：活動跑完才想到要量測，只能拿讚數交差。

## Quick Reference

- Schmitt 五模組設計問題清單、5E 步驟化操作（含 CANON 案例）：讀 [references/01-experience-design-playbook.md](./references/01-experience-design-playbook.md)
- 游擊手法決策樹、七張手法卡、台灣法規與 kill criteria：讀 [references/02-guerrilla-tactics-decision-tree.md](./references/02-guerrilla-tactics-decision-tree.md)
- 四層 KPI 矩陣、線下歸因方法、成效報告模板：讀 [references/03-kpi-and-measurement.md](./references/03-kpi-and-measurement.md)
- 完整案例走一遍（低預算在地小品牌、中型品牌快閃店）：讀 [references/04-case-walkthroughs.md](./references/04-case-walkthroughs.md)

## Skill Handoff

- 要深化消費者心理刺激設計 → `sor-marketing-strategy`
- 受眾輪廓不清、需要先做 Persona → `customer-persona-framer`
- 要把 5E 對應到完整顧客旅程找體驗落差 → `customer-journey-mapper`
- 游擊創意卡關、需要系統化發想 → `scamper`
- 要在事件中加入 FOMO、錨定等心理觸發器 → `psychological-trigger-marketing`
- 線下活動要服務化、設計前台後台流程 → `service-design-workshop`

## Suggested Prompts

- `我是台中的手作甜點店，開幕預算 8 萬，想做讓人拍照分享的活動，請用 $experiential-guerrilla-marketing 規劃。`
- `品牌要做新品快閃店，預算 200 萬，請跑完整的手法決策、5E 設計與 KPI 歸因規劃。`
- `請用 $experiential-guerrilla-marketing 評估這個游擊行銷提案的法規風險與 kill criteria。`
