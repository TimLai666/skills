---
name: customer-discovery-interview
description: Use when designing, conducting, or analyzing customer discovery interviews with The Mom Test, JTBD forces and timeline, and laddering — from research question to recruiting, interview guide, live probing, and transcript-to-insight analysis. Trigger on 顧客訪談、用戶訪談、使用者訪談、需求訪談、痛點探索、idea 驗證、訪談大綱、訪談問題設計、訪談逐字稿分析、JTBD、Mom Test、switch interview, or when persona or journey work needs real interview evidence first.
---

# Customer Discovery Interview

## Overview

用 Mom Test、JTBD 四力與 timeline 訪談、laddering 手段目的鏈，把「怎麼問、怎麼挖、怎麼分析」做成可執行的訪談工作流。

本 skill 是本 repo 顧客研究鏈的最上游：

- `customer-persona-framer` 與 `customer-journey-mapper` 負責下游產出（persona、CJM），但它們預設輸入已存在。沒有訪談證據時，persona 只是假設。本 skill 補的就是這個缺口：產出有引文出處的顧客事實，再 handoff 給下游。
- `review-mining-stp` 處理大量評論文本的量化分析；本 skill 的訪談洞察可作為其屬性探索的種子假設。

預設繁體中文（台灣用語），訪談話術要像真人口語。

## Mode Policy

`mode: design | conduct | analyze`，未指定時依 auto 規則判斷：

- 使用者要 `訪談大綱`、`問題設計`、`招募`、`想驗證 idea 但還沒訪`，選 `design`。
- 使用者說 `正在訪談`、`等下要訪`、`幫我看這題怎麼追問`、貼上進行中的對話片段，選 `conduct`。
- 使用者提供 `逐字稿`、`訪談筆記`、`錄音轉文字`，或要 `編碼`、`洞察`、`分析`，選 `analyze`。
- 同時要多個階段時依序執行，一次只完成一個 mode 的產出再確認。

## Input Contract

### design

必填至少一項：

- `產品或服務或 idea` — 想驗證的東西
- `研究問題` — 想搞清楚的事（例：目標用戶現在怎麼解決 X）

可選：`階段`（problem discovery / solution validation，預設前者）、`客群線索`、`B2B 或 B2C`、`場次或時程限制`、`既有假設清單`。

### conduct

必填：`訪談大綱或研究問題`。
可選：`受訪者背景`、`即時對話片段`（訪談中逐段貼上，skill 回追問建議）。

### analyze

必填：`逐字稿或訪談筆記`（一份以上，附受訪者編號）。
可選：`研究問題`、`既有編碼表`、`下游用途`（persona / journey / STP）、`已訪場次與 segment 分佈`。

資訊不足但可推進時，先列 3-5 個假設再產出；缺研究問題就先幫使用者收斂研究問題，不要直接生一份泛用大綱。

## Workflow

### design

1. 收斂研究問題：把「想驗證 idea」翻成 2-4 個可透過過去行為回答的問題。
2. 定義招募篩選器：篩行為不篩人口屬性，設計篩題（讀 references/03）。
3. 產出訪談大綱：開場定位 → 暖場 → timeline 主體 → 四力補問 → laddering 深挖 → 收尾 commitment 測試（讀 references/01、02）。
4. 每題標註「這題在測什麼」與追問分支。
5. B2B 加開角色矩陣：用戶、買家、決策者各要訪誰、問什麼。

### conduct

1. 對照大綱與當前對話，判斷受訪者剛說的是事實、意見、還是假訊號。
2. 偵測到讚美、空泛承諾、突然給點子時，給出現場轉化話術（讀 references/01）。
3. 建議下一句追問：優先具體化（上一次是什麼時候）、laddering（那對你差在哪）、四力補位（哪一力還沒有證據）。
4. 收尾前提醒 commitment 測試：這場要拿到什麼推進。

### analyze

1. Open coding 逐句貼標，標籤附 [P編號:段落] 出處。
2. Affinity mapping 由下往上分組，跨受訪者才算 pattern。
3. 命名主題、做反例檢查（讀 references/03）。
4. 每個洞察套句式模板，標證據等級與支持人數。
5. 判斷理論飽和：連續 2-3 場無新編碼即建議停止或換 segment。
6. 依 `下游用途` 產出對應 handoff block。

## Output Contract

一律繁體中文。

### design 輸出段落

1. `研究問題與假設` — 每個假設標注要用什麼行為證據才算驗證
2. `招募篩選器` — 篩選條件 + 篩題（含誘餌題）+ 排除條件 + 誘因建議
3. `訪談大綱` — 固定格式，每題三欄：`問題（口語）｜這題在測什麼｜追問分支`
4. `執行注意` — 時長配置、B2B 角色矩陣（如適用）

### conduct 輸出

每回合輸出：`判讀`（事實/意見/假訊號）→ `建議追問`（1-2 句口語話術）→ `還缺的證據`（哪一力、哪一層 job 還沒問到）。

### analyze 輸出段落

1. `編碼摘要` — 標籤數、主要編碼類別（行為/情緒/四力/job）
2. `主題` — affinity groups，每組附代表引文
3. `洞察清單` — 句式：`[某類人] 在 [情境] 時想要 [動機]，但 [阻礙]，所以 [現行解法與代價]`，每條附證據等級（S/A/B/C）、支持人數 n、引文出處
4. `飽和判斷與下一步` — 還缺哪個 segment 或角色
5. handoff blocks（依下游用途，見下）

### Handoff blocks

以下 block 名稱僅供本 skill 標示產出用途；block 內的欄位即對應下游 skill 的 Input Contract 欄位，下游不需要認得 block 名稱，直接把欄位內容當一般輸入餵入即可。

給 `customer-persona-framer`（persona 尚未存在時的預設下游）：

```md
### handoff_to_customer_persona_framer
- 產品或服務: ...
- 目標客群: （用行為定義，不用人口屬性）
- 初步 persona 線索: （每條附 [P編號] 出處與證據等級）
- 使用情境: ...
- 決策線索: push / pull / anxiety / habit 各一句摘要
- 輸出用途: ...
```

給 `customer-journey-mapper`（證據補充，不可取代 persona；最終 CJM 前仍須先經 `customer-persona-framer` 產出 persona）：

```md
### interview_evidence_for_journey_mapper
- 階段對映: first thought→認知；passive/active looking→考慮/研究；deciding→決策/購買；consuming→使用；satisfaction→關係建立
- 各階段證據: 動機引文、行動引文、情緒引文、關鍵時刻（各附出處）
```

給 `review-mining-stp`（僅作為其 attribute discovery pass 的種子，不得跳過該 skill 自身的 corpus 探索與凍結流程）：

```md
### handoff_to_review_mining_stp
- 候選屬性: attribute_key 候選 + 訪談引文 + 建議 theory family
- 待量化假設: 需要大量評論驗證的訪談洞察
```

## Quality Rules

- 禁提案式問題：大綱與追問中不得出現「你會不會用/買/喜歡/付多少」句型。
- 問過去不問未來：每題錨定在已發生的具體事件，「通常」「未來」「如果」開頭的題目要改寫。
- 每個洞察必須可追溯到引文出處 [P編號:段落]；無引文的判斷一律標記為假設。
- C 級口頭證據不得單獨支撐任何結論，至少要一條 A 級以上證據（分級見 references/03）。
- 訪談大綱每題附「這題在測什麼」，答不出來的題目刪掉。
- 話術用台灣口語，不用書面語照念（「你上次遇到這狀況是什麼時候？」而非「請描述您最近一次遭遇此問題之情境」）。
- handoff block 裡的每個欄位都要有訪談證據支撐，訪談沒問到的欄位寧可留空並註明，不要腦補。

## Common Mistakes

- 大綱塞滿功能偏好題與滿意度題，沒有一題在重建具體事件。
- 把「他說會買」當驗證通過，沒做 commitment 測試就結案。
- 訪完全部場次才開始分析，錯過調整大綱與判斷飽和的時機（第 3 場後就該邊訪邊編碼）。
- 用人口屬性篩受訪者，找來一群沒有目標行為的人。
- Affinity mapping 先設好類別再往裡塞標籤，變成驗證而不是探索。
- 單一受訪者的說法被寫成 pattern。
- 跳過本 skill 直接讓 `customer-persona-framer` 憑空生 persona，把假設包裝成研究結果。

## Quick Reference

- Mom Test 三規則、好壞問題對照、假訊號轉化、commitment 測試、B2B 多角色：讀 [references/01-mom-test-rules.md](./references/01-mom-test-rules.md)
- JTBD 四力問法、timeline 逐段腳本、switch interview、三層 job 追問：讀 [references/02-jtbd-forces-timeline.md](./references/02-jtbd-forces-timeline.md)
- Laddering、逐字稿編碼與 affinity mapping、洞察句式、證據分級、飽和與招募：讀 [references/03-analysis-and-sampling.md](./references/03-analysis-and-sampling.md)

## Suggested Prompts

- `Use $customer-discovery-interview in design mode to turn an idea into research questions, a recruiting screener, and a Mom Test compliant interview guide in Traditional Chinese.`
- `Use $customer-discovery-interview in analyze mode to code transcripts into themes and evidence-graded insights, then emit a handoff block for customer-persona-framer.`
