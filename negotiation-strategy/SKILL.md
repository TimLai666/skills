---
name: negotiation-strategy
description: Use when planning or executing a negotiation with structured strategy based on Harvard Negotiation Project (seven elements, BATNA/ZOPA), anchoring research, MESO, concession pacing, and tactical empathy. Trigger on 談判、議價、薪資談判、談薪水、供應商議價、合作條件、合約談判、開價、還價、BATNA, or salary negotiation, vendor pricing, B2B partnership terms, client contracts, cross-department resource bargaining, lease negotiation.
---

# 談判策略（Negotiation Strategy）

## Overview

把一場談判從「臨場發揮」變成「有準備、有規則、有紀錄」的結構化流程。理論基礎：哈佛談判專案七要素、BATNA/ZOPA、MESO 多方案等值提案、錨定研究、讓步節奏設計、Chris Voss 戰術同理心。

輸出不是理論講解，而是：七要素盤點表、開價數字與依據、讓步腳本、僵局應對方案、收尾承諾清單。

適用場景：薪資談判、供應商議價、B2B 合作、客戶合約、跨部門資源談判、租約。

## Trigger Map

Use：
- 使用者要準備一場具體談判（談薪水、跟供應商議價、談合作條件、談租金）。
- 使用者在談判進行中求救（「對方開了極端價」「對方說要回去請示」「卡住了」）。
- 使用者要複盤一場已結束的談判，找出下次可改的點。
- 使用者提到 BATNA、ZOPA、錨定、讓步策略、開價策略等概念並要求應用。

Do not use：
- 純合約條款法律風險審查，沒有談判策略需求。
- 純文書成稿（談判信、報價單），不需要策略設計。
- 衝突調解、家庭或人際糾紛（本 skill 的框架針對商務利益交換設計）。

Handoff：
- 合約文本的風險條款掃描 → 建議轉 `$red-flag-contract-scanner`，本 skill 只處理「哪些條款要談、怎麼談」。
- 談判 email 或信件成稿 → 先輸出訊息要點與句型，成稿建議轉 `$human-writing`。

## Mode Selection

依使用者所處階段選模式，不要一律跑全流程：

- `full_prep` — 談判前有準備時間：跑完整 Workflow 1-6，輸出全套 Output Contract。
- `live_counsel` — 談判進行中、要立刻回應：跳過完整盤點，先問兩個最小必要問題（你的 BATNA 現況？對方剛做了什麼？），直接給對應戰術與話術，事後補建議完整準備。
- `debrief` — 談判已結束：用七要素當檢核表逐項比對「準備了什麼 vs 實際發生什麼」，輸出下次改進清單與關係修復建議（如需要）。

## Input Contract

必要欄位：

- `subject_and_goal` — 談判標的與我方目標（要什麼、量化到數字或條款）
- `bottom_line_and_alternatives` — 我方底線與替代方案現況（BATNA 有沒有、有幾個、強不強）

重要可選欄位：

- `counterpart_intel` — 對方情報：需求、壓力來源、替代選項、決策者是誰
- `relationship_type` — 一次性 vs 長期關係（決定可用戰術的邊界）
- `time_pressure` — 時間壓力在哪邊、deadline 是真是假
- `history` — 過去往來、上次談判結果、既有承諾
- `constraints` — 不可退讓的紅線、授權範圍

缺 `bottom_line_and_alternatives` 時，不直接給開價建議，先帶使用者跑 BATNA 盤點（見 Workflow 第 2 步）。其他欄位缺漏可列假設後推進，但要標明哪些判斷建立在假設上。

## Workflow

1. **準備：七要素盤點** — 用 [references/01-preparation-seven-elements.md](./references/01-preparation-seven-elements.md) 的盤點表逐項填：Interests / Options / Alternatives / Legitimacy / Communication / Relationship / Commitment。雙方都要填，對方那欄用情報加推估，標明信心程度。
2. **BATNA 強化與 reservation point 設定** — 列出所有替代方案、評估可行性、挑最佳者做強化行動；再從 BATNA 換算 reservation point（換算方法見 reference 01）。同步推估對方 BATNA 與 ZOPA。
3. **開局：開價決策與錨定設計** — 依決策規則判斷誰先開價（資訊優勢在我方＝先開；完全不明＝誘導對方先開），設計錨點幅度與支撐依據。規則與幅度設計見 [references/02-tactics-and-counters.md](./references/02-tactics-and-counters.md)。
4. **交換：MESO 與讓步節奏** — 準備 3 個對我方等值的打包方案同時提出，從對方選擇讀偏好；讓步遵守遞減幅度、放慢頻率、每次標價交換，絕不無償讓步。
5. **僵局處理** — 先用戰術同理心（labeling / mirroring / 校準型問題）探真實障礙，再依僵局類型換招：換議題打包、換人、換時間、引入客觀標準、或明示 BATNA。骯髒戰術辨識與反制見 reference 02。
6. **收尾與承諾固定** — 確認決策者在場、逐條複述共識、當場約定書面化時程與負責人，防 nibbling 與事後翻盤。場景化收尾與紅線要點見 [references/03-scenario-playbooks.md](./references/03-scenario-playbooks.md) 各場景的「紅線清單」段。

各步驟的通過條件（沒過就不進下一步）：

| 步驟 | 通過條件 |
|------|---------|
| 1 準備 | 七要素表填完，對方欄至少「中」信心 3 項以上；否則第一輪目標改為蒐集情報 |
| 2 BATNA | 有一個經過可行性評估的最佳替代方案 + 換算出的 reservation point 數字 |
| 3 開局 | 開價數字、支撐標準、被追問時的說法，三者都備妥 |
| 4 交換 | 讓步階梯寫好且每階有交換條件；MESO 三包對我方分數相等 |
| 5 僵局 | 至少預判 2 個最可能僵局情境並寫好對應動作 |
| 6 收尾 | 共識全部逐條書面化，含時程與負責人 |

## Output Contract

依任務階段輸出對應段落，全程繁體中文：

- `preparation_sheet` — 七要素盤點表（含對方推估與信心標記）
- `batna_plan` — 替代方案清單、最佳 BATNA 強化行動、reservation point、推估 ZOPA
- `opening_design` — 誰先開、開價數字、錨點依據、備用說法
- `concession_script` — MESO 三方案、讓步階梯（每階的交換條件）
- `deadlock_playbook` — 預判的僵局情境與對應動作
- `closing_checklist` — 承諾固定清單與書面化步驟

單一問題（例如「對方開了極端價怎麼回」）可只輸出對應段落，不必全套。

## Quick Reference

- 七要素盤點表、BATNA/reservation point/ZOPA/aspiration 設定：讀 [references/01-preparation-seven-elements.md](./references/01-preparation-seven-elements.md)
- 錨定、MESO、讓步節奏、戰術同理心、骯髒戰術反制：讀 [references/02-tactics-and-counters.md](./references/02-tactics-and-counters.md)
- 薪資／供應商／B2B／跨部門／租約五場景 playbook：讀 [references/03-scenario-playbooks.md](./references/03-scenario-playbooks.md)

場景路由（辨識到場景時直接載入 reference 03 對應段落）：

| 使用者情境 | Playbook | 該場景最容易踩的坑 |
|-----------|----------|------------------|
| 談薪水、offer、調薪 | 03 (a) | 先報前薪被錨死、offer 前就開始談 |
| 供應商報價、漲價、採購 | 03 (b) | 只比單價不算 TCO、沒有第二家報價就上桌 |
| 合作案、分潤、通路、聯名 | 03 (c) | 沒寫 pilot 轉正條件、退出條款留白 |
| 要別部門的人力／排期 | 03 (d) | 用急迫感取代交換物、偷襲式升級 |
| 租金、續約、店面 | 03 (e) | 空手議價（沒有行情舉證與備選物件） |

## Quality Rules

- BATNA 未盤點前不出價。使用者急著要開價數字時，先用最短路徑補 BATNA 與 reservation point，再給數字。
- 每個讓步必須換到東西。輸出的讓步腳本中，任何一階讓步都要附「交換條件」欄位，不能留空。
- 先探利益後談立場。對方任何立場宣告（「就是這個價」）都先轉成利益假設再回應，不直接在立場上攻防。
- Aspiration 要高但可辯護。開價與目標必須附客觀標準（行情、前例、第三方鑑價），不能只憑膽量喊高。
- 談判紀錄要留書面。每輪結束輸出共識摘要與待辦，重要承諾建議以 email 複述確認。

## Common Mistakes

- 把立場當利益：只記對方「要 8 折」，沒挖出背後是預算週期、比價壓力還是內部 KPI。
- 單議題來回拉鋸：只在價格上推擠，應打包交期、付款條件、數量、年限等多議題交換。
- 透露底線：把 reservation point 說出口或用語氣暗示，等於放棄整個 ZOPA 上緣。
- 對極端錨定直接還價：一還價就被錨住，應先不還價、要求依據、再重新錨定（三步反制見 reference 02）。
- 贏了條款輸了關係：長期關係場景用一次性榨取戰術，省下的價差賠在後續合作品質與續約。

## Ethics Boundary

- 不教欺騙：不產出假 BATNA、假競品報價、假時限等虛構事實的話術。
- 骯髒戰術章節僅供辨識與防守，不得改寫成進攻腳本。
- 可以策略性地選擇「揭露什麼、何時揭露」，但不可陳述不實資訊。

## Suggested Prompts

- `我下週要談薪水，目前 offer 是 X，請用 $negotiation-strategy 幫我做完整準備。`
- `供應商漲價 15%，我們有兩家備選，請用 $negotiation-strategy 設計議價方案。`
- `對方一開口就砍五折，我該怎麼回？`
