---
name: ab-experiment-design
description: Design and interpret online controlled experiments (A/B tests) for marketing campaigns, product features, landing pages, and pricing — hypothesis cards, sample size, SRM checks, guardrails, readout decision trees. Trigger on AB test、A/B 測試、實驗設計、對照實驗、轉換率優化、CRO、假設驗證、樣本數計算、MDE、實驗判讀、成效檢定、SRM、guardrail。
---

# A/B 實驗設計與判讀

## Overview

把「想測的改動」變成一份可執行、可判讀、可累積的對照實驗：假設卡 → 指標設計 → 樣本數與工期 → 執行健檢 → 判讀決策 → 實驗登記。

適用場景：行銷 campaign、產品功能、landing page、定價測試。

定位：本 repo 的 `data-analysis-workflow` 是通用資料分析流程；本 skill 只管「上線前後的對照實驗設計與判讀」。使用者要的是既有資料的探索式分析時，轉用 `$data-analysis-workflow`。

理論基礎：假設檢定、統計檢定力與 MDE、sequential testing 與 peeking 問題、SRM 檢查、novelty effect、Twyman's law、guardrail metrics（參考 Kohavi 等人的線上對照實驗實務）。

## Trigger Map

Use：

- 設計新的 A/B 測試：行銷 campaign、產品功能、landing page、定價測試。
- 計算樣本數、MDE、工期，或評估「流量夠不夠跑實驗」。
- 判讀已完成或進行中的實驗結果，包含 SRM、guardrail、segment 爭議。
- 建立實驗登記制度、假設排序（ICE / PXL）。

Do not use：

- 既有資料的探索式分析、EDA、建模 → 轉用 `$data-analysis-workflow`。
- 只要行銷策略與心理假設、還沒到實驗設計 → 轉用 `$sor-marketing-strategy`。
- 純 GA4 / GTM 事件實作細節，不涉及實驗設計。

Handoff：

- 行銷情境還沒有心理層假設時，先跑 `$sor-marketing-strategy` 產出 `experiment_plan` 骨架，再接回本 skill 寫假設卡與統計設計。
- 實驗結束後的資料要做深入清理、EDA 或建模，交給 `$data-analysis-workflow`。

## Scenario Notes

- **行銷 campaign**：分流單位常是受眾名單而非即時流量；一次性大檔期不可重來，先過 references/03「何時不該跑 AB」再設計。
- **產品功能**：novelty / primacy effect 風險最高（見 references/02），重大功能上線後留 holdback 驗證長期效果。
- **Landing page**：redirect 分流是 SRM 的高風險來源；頁面速度必進 guardrail。
- **定價測試**：倫理與法規風險最高。預設先建議 quasi-experiment（不同市場、時段或方案包裝，見 references/03），使用者明確確認風險後才做同時段差別定價。

## Input Contract

必要欄位：

- `change_description` — 要測什麼改動、對誰生效、控制組長什麼樣
- `baseline` — primary 指標目前基準值（轉換率，或平均值 ± 標準差）
- `traffic` — 可進實驗的流量（日或週不重複使用者數）
- `expected_effect` — 期望效果量或「最小值得做的效果」（MDE，相對或絕對）
- `risk_tolerance` — guardrail 可接受的惡化上限、實驗最長可跑多久

可選欄位：

- `randomization_unit` — user / session / device / 門市，預設 user
- `platform` — 實驗平台或自建分流
- `seasonality_notes` — 檔期、促銷、假日等干擾
- `prior_experiments` — 同區塊過去的實驗結果

缺必要欄位時先問，一次問完，並附上你建議的預設值。

## Data Sufficiency Gate

拿到 baseline、MDE、traffic 後，先跑 `scripts/sample_size.py` 估工期，再決定要不要設計實驗：

- 工期 ≤ 4 週：正常設計。
- 4–8 週：可跑，但要使用者確認願意等，且改動在期間不得再改版。
- 超過 8 週（或超過使用者給的工期上限）：不要硬跑。明確告知「此流量在合理工期內偵測不到這個 MDE」，並給替代路徑：
  - 放大 MDE：只測預期效果更大的改動（整頁改版，而非按鈕顏色）
  - 換更靈敏的 proxy 指標，並標明 proxy 風險（見 references/01）
  - 改用 pre-post + 控制組、quasi-experiment 或質化驗證（見 references/03）

## Workflow

1. **假設卡撰寫** — 依 [references/01-hypothesis-and-metrics.md](./references/01-hypothesis-and-metrics.md) 的格式寫出證據、改動、行為改變、驗證指標。多個候選時用 ICE 或 PXL 排序。
2. **指標設計** — primary 唯一且離改動最近；secondary 輔助解讀機制；guardrail 必設（營收、退訂、速度、客訴至少檢查一輪）。
3. **樣本數與工期計算** — 跑 [scripts/sample_size.py](./scripts/sample_size.py)，過 Data Sufficiency Gate。工期取「樣本數需求」與「至少 1–2 個完整週」的較大者。公式與速查表見 [references/02-statistics-gates.md](./references/02-statistics-gates.md)。
4. **執行健檢** — 上線後第一天內檢查 SRM（chi-square，p < 0.001 即警報）；平台第一次使用或分流邏輯改過，先跑 AA test。
5. **判讀決策** — 跑滿預定樣本與工期後才判讀，依 [references/03-interpretation-and-pitfalls.md](./references/03-interpretation-and-pitfalls.md) 的決策樹走：健檢 → 顯著性 → guardrail → segment 一致性 → 實務顯著性 → 決策。
6. **實驗登記與知識累積** — 不論結果，用 references/03 的登記模板記錄假設、設計、結果、決策、學習。

## Output Contract

### 實驗計畫書（設計階段輸出）

- `hypothesis_card` — 完整假設卡
- `metrics` — primary（唯一）/ secondary / guardrail，各含定義、資料來源、方向
- `design` — 分流單位、分組比例、觸發條件、排除規則
- `sample_and_duration` — 每組樣本數、預估工期、計算參數（baseline、MDE、alpha、power）
- `health_checks` — SRM 檢查排程、AA test 需求
- `analysis_plan` — 判讀時間點、事前聲明的 segment、多重比較處理方式
- `risks` — novelty 風險、季節性干擾、guardrail 停損條件

### 判讀報告（結束階段輸出）

- `health_status` — SRM 結果、資料品質檢查
- `primary_result` — 效果量、信賴區間、p 值（sequential / Bayesian 設計則給對應輸出）
- `guardrail_results` — 每個 guardrail 的變化量與是否越線
- `decision` — ship / no-ship / 延長 / 重測，附理由
- `segments_observed` — 事後觀察到的 segment 差異，一律標記「待驗證假設」
- `learnings` — 寫入實驗登記的內容

## Quick Reference

- 假設卡格式、ICE / PXL 排序、指標層級與 guardrail 必設清單、proxy 陷阱、OEC：讀 [references/01-hypothesis-and-metrics.md](./references/01-hypothesis-and-metrics.md)
- 樣本數公式與速查表、alpha/power 慣例、工期規則、peeking 與 sequential、SRM、AA test、novelty、多重比較：讀 [references/02-statistics-gates.md](./references/02-statistics-gates.md)
- 判讀決策樹、Twyman's law、Simpson's paradox、HARKing 禁令、何時不該跑 AB 與替代方案、登記模板：讀 [references/03-interpretation-and-pitfalls.md](./references/03-interpretation-and-pitfalls.md)
- 樣本數計算器：`python scripts/sample_size.py --help`（stdlib only，可直接執行）

## Quality Rules

- primary 指標只能有一個。想放兩個時，回頭修假設卡，而不是加指標。
- guardrail 沒設完不出計畫書。
- 不 peeking：固定樣本設計下，期中偷看且「顯著就停」會讓實際 false positive 遠超 5%。要邊跑邊看，就改用 sequential 設計（mSPRT / group sequential）或明示先驗的 Bayesian 設計。
- SRM p < 0.001 時整批資料作廢，先修分流再重跑；不可「修正權重後繼續用同批資料」。
- 事後 segment 只能當假設，不能當結論。要宣稱 segment 效果，開新實驗驗證。
- primary 顯著但任一 guardrail 惡化越線 → 不上線，量化 trade-off 讓使用者決策。
- underpowered 的不顯著結果不可宣稱「無效果」，只能標記 inconclusive。
- 分流單位與分析單位不一致（user 分流、session 指標）時，變異數會被低估，要用 references/02 的方式修正，不可直接套公式。
- 定價實驗在使用者確認倫理與法規風險前，不輸出同時段差別定價的設計。
- 所有數字可重算：報告附樣本數、期間、alpha、power、MDE 等計算參數。

## Common Mistakes

- 把「點擊率上升」當成功，沒看下游營收 guardrail（proxy metric 陷阱）。
- 用「跑到顯著為止」代替事前樣本數計算。
- 只跑 3 天就下結論，沒涵蓋完整的週間與週末循環。
- 多變體、多指標全部用 α = 0.05 各測一次，既不校正也不分層級判讀。
- 把 novelty effect 當長期效果，新功能首週高峰直接外推全年。
- 結果好到不像真的還直接慶祝，沒先過 Twyman's law 查 instrumentation。
- 實驗做完不登記，半年後同一個假設又測一次。

## Suggested Prompts

- `用 $ab-experiment-design 設計這個 landing page 改版的 A/B 測試，日流量約 6000。`
- `基準轉換率 3%，想偵測相對 8% 的提升，幫我算樣本數和工期。`
- `這是實驗結果，primary 顯著但退訂率上升，幫我用判讀決策樹判斷該不該上線。`
