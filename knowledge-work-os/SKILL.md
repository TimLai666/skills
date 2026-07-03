---
name: knowledge-work-os
description: Personal productivity operating system for overloaded knowledge workers, combining GTD, Deep Work, time blocking, implementation intentions, and weekly reviews into an actionable system. Use for building a task system from scratch, daily planning, weekly reviews, or rescuing someone drowning in commitments. Trigger on 時間管理、生產力、待辦清單爆炸、GTD、專注、深度工作、每週回顧、工作排程、行事曆規劃、精力管理、工作超載、會議太多、事情做不完, or requests about focus, overwhelm, task systems, and calendar planning.
---

# Knowledge Work OS 知識工作作業系統

## Overview

把 GTD（David Allen 五步驟）、Deep Work（Cal Newport）、attention residue（Sophie Leroy）、implementation intentions（Gollwitzer）、Zeigarnik effect、時間箱、每週回顧、ultradian rhythm 整合成一套可實際運轉的個人工作系統。

目標使用者：待辦爆炸、會議纏身、無法專注的上班族與知識工作者。

輸出不是原則清單，而是可以直接照做的腳本、判斷樹、話術模板與排程規則。

## 理論基礎速覽

引用理論時以下表為準，不誇大效果量：

| 理論 | 核心發現 | 在本系統的角色 |
|------|----------|----------------|
| GTD（David Allen） | 大腦適合產生想法，不適合儲存想法；承諾要放進可信任的外部系統 | 清單體系的骨架（01） |
| Zeigarnik effect + Masicampo & Baumeister (2011) | 未完成事項佔用工作記憶；為它寫下具體計畫即可釋放，不必真的完成 | capture 與斷點筆記的機制解釋（01、02） |
| Deep Work（Cal Newport） | 經訓練者每日高強度深度工作上限約 4 小時，新手更少 | 深度時段的設計參數（02） |
| Attention residue（Sophie Leroy, 2009） | 任務切換後注意力殘留在前一任務，未完成就切走殘留最重 | 批次處理與切換儀式的依據（02） |
| Implementation intentions（Gollwitzer；Gollwitzer & Sheeran 2006 統合分析，d ≈ 0.65） | if-then 計畫把行動啟動綁定情境線索，效果量中到大 | 每日 if-then 計畫（02） |
| 時間箱 + Parkinson's law | 工作會膨脹填滿可用時間；預先指定時間用途可設邊界 | 每日排程方法（02） |
| Ultradian rhythm（Kleitman BRAC） | 警覺度以約 90-120 分鐘為週期起伏 | 深度區塊時長（02） |
| 每週回顧 | 系統不會自己保持乾淨，需要固定心跳維護 | 回顧腳本（03） |

## Mode Routing

依使用者狀態選擇模式，判斷規則由上往下套用，命中即停：

| 條件 | 模式 |
|------|------|
| 「事情爆了」「這週死線一堆做不完」「已經開天窗」，或明顯處於恐慌狀態 | `overload-rescue` |
| 要建立、重建、整頓整套個人系統（「幫我建時間管理系統」「GTD 怎麼導入」「系統爛掉想重來」） | `system-setup` |
| 在問今天或明天怎麼安排（「今天要做什麼」「幫我排今天」「這些事怎麼塞進行事曆」） | `daily-planning` |
| 要做週回顧、週計畫（「這週怎麼收尾」「下週怎麼規劃」「幫我跑每週回顧」） | `weekly-review` |
| 模糊不清時 | 問一句：「你現在最急的是救火（本週快爆），還是建制度（長期改善）？」再路由 |

路由注意事項：

- 使用者常用 system-setup 的語言描述 overload 的問題。嘴上說「想學時間管理」但描述裡有具體的本週死線壓力，先跑 `overload-rescue`，救完火再回 `system-setup`。
- 「我都沒辦法專注」「一直被打斷」單獨出現時走 `daily-planning`（重點在 02 的注意力設計），不需要整套 system-setup。
- 「會議太多」可能是 daily-planning（防禦排程）也可能是 overload-rescue（承諾超收），看有無本週崩潰跡象。

模式交接規則：

- `overload-rescue` 收尾時，固定建議 48 小時內做一次 weekly-review + 工時盤點，並預告 system-setup 是根治路徑。
- `system-setup` 完成後，主動提議陪跑第一次 daily-planning，把系統落到明天的行程上。
- `weekly-review` 中發現承諾超收（下週排不下 big 3），引用 03 的承諾預算與拒絕模板，不硬塞。

## Input Contract

各模式必要輸入（缺少時一次問完，不要逐題追問）：

**system-setup**
- 現有工具：目前用什麼記待辦與行事曆（紙本 / Todoist / Notion / Outlook / 什麼都沒有）
- 工作型態：產出型（寫作、開發、分析）與協調型（會議、溝通）的大致比例
- 會議密度：一週幾小時會議
- 痛點：漏事、拖延、被打斷、還是承諾太多

**daily-planning**
- 今天的硬承諾：已排定的會議與死線
- 待辦來源：使用者傾倒今日想做的事（鼓勵全部倒出來）
- 精力狀態：今天狀態好壞、高峰時段在早上還是下午

**weekly-review**
- 上週殘留：沒做完的事、卡住的專案
- 未來兩週：已知的死線與大事
- 可選：上週實際深度工作時數（用來校正下週承諾量）

**overload-rescue**
- 全部承諾清單：鼓勵使用者把所有事倒出來，不分大小
- 本週不可動的死線
- 利害關係人：哪些事牽涉到誰在等

各模式共通可選：
- `depth` — `quick`（只給核心產出）/ `full`（完整分析，預設）
- `output_language` — 預設繁體中文

資訊不完整但可推進時，明列假設後繼續產出，不要停在等資料。

## Workflow

1. 依 Mode Routing 判定模式，確認 Input Contract 必要項。
2. 依模式讀對應 reference 並執行：
   - **system-setup**（讀 01 + 02）：收集點盤點合併 → mind sweep 過 clarify 判斷樹 → 建四張清單 → 行事曆規則與深度時段防禦 → 排定第一次每週回顧與每日維護儀式
   - **daily-planning**（讀 02）：抄下今日硬承諾、定 big 3 → 深度任務排精力高峰、shallow 打包塞低谷，套 ×1.5 校正與 buffer 規則 → 寫 2-3 條 if-then → 明列今天不做的事
   - **weekly-review**（讀 03）：逐步跑回顧腳本（完整版或縮水版）→ 產出下週 big 3 並預佔深度區塊 → 核對承諾預算，超收就處理
   - **overload-rescue**（讀 03，穩定後補 01 的重啟步驟）：全部倒出 → 死/延/棄三分 → 產出可直接寄出的重新承諾訊息 → 排本週生存排程 → 指定急救後第一個修復動作
3. 產出該模式的 Output Contract 內容，全部具體到可直接執行。
4. 主動指出使用者系統裡的結構性問題（例如行事曆塞滿無 buffer、專案沒有下一步行動），連同建議一起給。

### system-setup 的導入順序（四週節奏）

一次丟出整套系統必然棄用，first_week_plan 要照這個節奏鋪：

| 週次 | 只導入 | 成功標準 |
|------|--------|----------|
| 第 1 週 | 收集：合併收集點 + mind sweep + 每日清空入口 | 連續 5 天沒有用腦記事 |
| 第 2 週 | 清單：四張清單建好，clarify 成為習慣 | 收件匣每日歸零 |
| 第 3 週 | 回顧：第一次完整每週回顧 + 每日維護儀式 | 回顧跑完且零停滯專案 |
| 第 4 週 | 時間箱：big 3 + 深度區塊防禦 + if-then | 一週防禦住 3 個深度區塊 |

使用者要求加速時可以壓縮，但順序不可倒置：沒有可信的清單，時間箱裡不知道要排什麼；沒有收集習慣，清單三天就漏。

### 邊界情況調整

- **行事曆不自主的人**（新人、行政、被會議支配）：深度區塊從「防禦 1 個 60 分鐘」起步，重點放批次處理與 if-then，不畫做不到的大餅。
- **主管 / 會議超過 20 小時者**：先跑 03 工時盤點讓數字說話，深度工作目標下修到每日 1-2 小時，辦公時間制度優先導入。
- **自由工作者 / 無外部結構者**：Parkinson's law 反向發作（沒有邊界導致無限膨脹），時間箱與每日 big 3 是第一優先，早於清單體系。
- **工具極簡者**（只想用紙筆）：完全可行，四張清單 + 紙本行事曆即可運轉，不要推銷數位工具。

## Output Contract

**system-setup** 固定產出：
- `capture_setup` — 收集點盤點結果與合併方案（最終收集點 ≤ 3 個）
- `list_system` — 清單體系設計（next actions / waiting for / projects / someday）與放在哪個工具
- `calendar_rules` — 行事曆使用規則（只放硬承諾、深度時段防禦）
- `first_week_plan` — 第一週導入步驟，含每日 15 分鐘維護儀式與第一次每週回顧排程

**daily-planning** 固定產出：
- `big_3` — 今日三件最重要的事，動詞開頭
- `time_blocks` — 時間箱表（深度時段對高峰精力、shallow 塞低谷、含 buffer）
- `if_then_plans` — 針對今日高風險干擾的 2-3 條 if-then 計畫
- `not_today` — 明確不做的事（防止清單回滲）

**weekly-review** 固定產出：
- `review_script_result` — 逐步驟執行結果（收件匣清空、專案巡檢、waiting for 追蹤、行事曆前瞻）
- `next_week_big_3` — 下週三大重點
- `commitment_delta` — 本週承諾預算變化（新進承諾與對應退出的舊承諾）

**overload-rescue** 固定產出：
- `triage_table` — 全部承諾三分：本週死線 / 可延 / 可棄
- `renegotiation_messages` — 給利害關係人的重新承諾訊息草稿（可直接寄出的等級）
- `survival_schedule` — 本週生存排程（只排死線項目 + 最小維生事務）
- `post_rescue_step` — 度過本週後的第一個系統修復動作

預設繁體中文 Markdown。

## Quality Rules

- 每個列出的專案必須有一個具體的下一步行動，沒有就當場補出來，不能留空。
- 行事曆只放硬承諾（會議、死線、預約），彈性待辦放清單，不放行事曆。
- 清單項目語法一律動詞開頭且可直接執行：「打給王經理確認 Q3 預算」，不是「預算的事」。
- 時間箱必留 buffer：預估工時 ×1.5，且每日排程總量不超過可支配時數的八成。
- 深度工作時段以 90-120 分鐘為單位設計，新手從 60 分鐘起步，每日深度總量不超過約 4 小時。
- if-then 計畫必須指明具體時間地點或觸發情境，「有空就寫報告」不合格。
- 引用理論時照「理論基礎速覽」與 references 裡的表述，不誇大效果量、不編造數字。
- 委派出去的事必進 waiting for，且必記三要素：等誰、等什麼、從哪天開始等。
- 拒絕與重新承諾訊息要具體到可直接寄出：含名字、日期、明確選項。不輸出「你可以委婉地拒絕」這類空話。
- overload-rescue 的 triage 中，「死」類總時數不得超過本週可支配時數，超過就回頭再砍一輪。
- 建議要遷就使用者現有工具，不強迫換工具。工具遷移是 system-setup 裡的可選項，不是前提。
- 「要早睡」「少滑手機」這類模型已知常識不要單獨輸出，只在附有具體機制與做法時才出現。

## Common Mistakes

- 把待辦清單當願望清單：塞滿「想做」但永遠不會做的事，清單失去可信度，使用者開始無視它。someday-maybe 就是為此存在的隔離區。
- 時間箱排滿無 buffer：一個會議延長就全盤崩潰，然後使用者宣告「時間箱沒用」。問題在排法不在方法。
- 每週回顧變成補記流水帳：花一小時回憶上週做了什麼，卻沒清收件匣、沒巡專案、沒定下週重點。回顧的產出是「下週的清晰」，不是上週的日記。
- 在 overload 狀態推銷完整 GTD：對方連本週都活不過去，先 triage，制度之後再談。
- 把「委派出去」當「處理完了」：委派的事沒進 waiting for 清單，兩週後炸開。
- 幫使用者把每件事都標高優先：全部都重要等於沒有優先。big 3 就是三件，不能是五件。
- 工時盤點與精力高峰用想像數字：兩者必須來自實際記錄（過去四週行事曆、兩週精力記錄），憑感覺填的數字會系統性樂觀。
- 一次丟出整套系統要使用者全部照做：導入順序是收集 → 清單 → 回顧 → 時間箱，一週一層，貪快必棄用。

## Quick Reference

- GTD 五步驟操作化（capture / clarify / organize / reflect / engage、下一步行動語法、系統崩壞重啟）：讀 [references/01-gtd-engine.md](./references/01-gtd-engine.md)
- 注意力設計（時間箱、深度工作時段、attention residue 對策、if-then 計畫、干擾與會議防禦）：讀 [references/02-attention-design.md](./references/02-attention-design.md)
- 每週回顧腳本、承諾預算、拒絕話術、超載急救 triage、精力管理：讀 [references/03-review-and-load.md](./references/03-review-and-load.md)

## Suggested Prompt

Use `$knowledge-work-os` to build a personal productivity system, plan your day, run a weekly review, or triage work overload using GTD, Deep Work, and time-blocking methods in Traditional Chinese.
