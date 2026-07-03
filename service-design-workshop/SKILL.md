---
name: service-design-workshop
description: Use when turning a service design problem into a structured workshop output, especially for 服務設計, 服務藍圖, 服務流程, 接觸點, 前台後台, 服務實證, 顧客體驗, 利害關係人, 服務概念, or 服務架構. Trigger when the task asks for a practical service design brief, blueprint-ready structure, touchpoint analysis, or prototype and validation next steps rather than only theory review.
---

# Service Design Workshop

## Overview

把服務設計題目整理成可執行的工作坊輸出，先定義問題與場域，再整理利害關係人、服務概念、架構、接觸點與驗證步驟。
如果需求其實是 persona 或 customer journey map 本身，停止並改用 `customer-persona-framer` 或 `customer-journey-mapper`。

## Skill Boundaries

用「最終要交出的東西」判斷該用哪個 skill，不要用主題關鍵字判斷：

| 使用者要的最終產物 | 改用 |
|---|---|
| 正式服務藍圖表格、生態系地圖、前後台泳道圖 | `ecosystem-map-and-blueprint` |
| CJM 表格、情緒分數、情緒曲線、touchpoint 旅程表 | `customer-journey-mapper` |
| persona、顧客輪廓、5W1H 前置分析 | `customer-persona-framer` |
| 新服務概念發散、概念比較與淘汰 | `service-innovation-workshop` |
| 從模糊題目到可進原型的完整工作坊 brief | 本 skill |

補充判斷規則：

- 使用者說「畫藍圖」且旅程已明確：直接用 `ecosystem-map-and-blueprint`，不必先過本 skill。
- 「現有服務哪裡壞掉、怎麼修」用本 skill；「想做一個現在沒有的服務」用 `service-innovation-workshop`。一句話測試：修現有的用 design，做新的用 innovation。
- 本 skill 的輸出可直接餵下游：要精細旅程交 `customer-journey-mapper`，要正式藍圖交 `ecosystem-map-and-blueprint`，下游不必重做問題定義。
- 使用者只要求單一段落（例如只要利害關係人表）時，只輸出該段落，不硬塞六段。

## Input Contract

至少要有以下其中兩項：

- `service_problem`
- `target_users_or_customers`
- `service_context`
- `pain_points_or_failure_points`

可選：

- `business_goal`
- `constraints`
- `existing_touchpoints`
- `known_stakeholders`
- `requested_format`

資訊不足但使用者要快速草稿時，先列出 `3-5` 個假設，再繼續輸出。

## Workflow

1. 定義 `problem_and_context`，說清楚現況、場域、限制與設計目標。
2. 整理 `stakeholders_and_needs`，區分顧客、第一線、後台、合作方。
3. 形成 `service_concept_and_architecture`，明確說明價值、階段、接口與關鍵體驗。
4. 展開 `frontstage_backstage_touchpoints`，至少區分前台、後台、支援系統、服務實證。
5. 產出 `prototype_and_validation_next_steps`，把雛型、測試方式、觀察指標寫清楚。

## Workshop Formats

實際帶工作坊或使用者要求議程時套用以下版型；促進話術與人員處理讀 [references/service-design-facilitation-guide.md](./references/service-design-facilitation-guide.md)。

### 4 小時版：單一服務、單一場域、參與者 6-12 人

| 時間盒 | 階段 | 目的 | 促進手法 | 產出 |
|---|---|---|---|---|
| 0:00-0:25 | 開場與題目對焦 | 對齊題目、範圍、成功樣貌 | 開場定調＋題目一句話改寫 | `problem_and_context` 草稿 |
| 0:25-1:00 | 利害關係人盤點 | 找出所有被影響的人與其需求 | 角色默寫＋影響力×需求矩陣 | `stakeholders_and_needs` |
| 1:00-1:50 | 現況走查與痛點 | 把服務攤開找斷點 | 旅程走查＋便利貼＋親和圖 | 分階段痛點清單 |
| 1:50-2:00 | 休息 | — | — | — |
| 2:00-2:50 | 概念與架構 | 收斂成一個服務概念 | HMW 發散＋dot voting＋概念卡 | `service_concept_and_architecture` |
| 2:50-3:30 | 前後台接觸點展開 | 讓概念可營運 | 前台／後台／支援／實證四列牆面 | `frontstage_backstage_touchpoints` |
| 3:30-4:00 | 驗證計畫與收尾 | 決定下一步與 owner | 假設卡＋owner 認領制 | `prototype_and_validation_next_steps` |

### 整日版（7 小時）：跨部門、多利害關係人、或有現場觀察資料要消化

| 時間盒 | 階段 | 目的 | 促進手法 | 產出 |
|---|---|---|---|---|
| 0:00-0:30 | 開場定調 | 建立安全感與規則 | 開場話術＋working agreement | 共識規則、停車場 |
| 0:30-1:30 | 場域資料走讀 | 用證據取代印象 | 觀察資料 gallery walk | 證據牆 |
| 1:30-2:30 | 利害關係人與衝突盤點 | 揭露觀點矛盾 | 角色地圖＋衝突配對 | `stakeholders_and_needs` |
| 2:30-3:30 | 問題定義 | 收斂設計命題 | 命題句型改寫＋dot voting | `problem_and_context` |
| 3:30-4:30 | 午休 | — | — | — |
| 4:30-5:30 | 概念發散與收斂 | 產出 2-3 個概念再選一 | HMW＋概念卡＋三條件評估 | `service_concept_and_architecture` |
| 5:30-6:20 | 前後台接觸點展開 | 概念落到營運 | 四列牆面＋風險標記 | `frontstage_backstage_touchpoints` |
| 6:20-7:00 | 驗證計畫與收尾 | 綁定行動、owner 與時程 | 假設卡＋認領＋checkout | `prototype_and_validation_next_steps` |

版型選擇規則：

- 參與者跨三個以上部門、或有現場觀察資料要消化，用整日版；單一團隊且題目已聚焦，用 4 小時版。
- 時間不足 4 小時：砍概念發散的廣度，不砍前後台展開，否則輸出會退化成旅程圖。
- 只有線上時段可用：先讀促進指南的線上調整節，所有時間盒加 20%。

## Output Contract

固定輸出以下段落：

- `service_design_brief`
- `problem_and_context`
- `stakeholders_and_needs`
- `service_concept_and_architecture`
- `frontstage_backstage_touchpoints`
- `prototype_and_validation_next_steps`

優先使用繁體中文 Markdown。若使用者要求簡報或課堂作業格式，保留同樣資訊架構，只改成較適合投影片或報告的表述。

## Output Quality Checklist

交付前逐段檢查，任何一項不過就回頭補，不要帶著缺口交付：

- `service_design_brief`：30 秒內能讀懂題目、對象、場域、目標；沒有未定義的縮寫或內部術語。
- `problem_and_context`：每個痛點有標注發生在服務前期／中期／後期；限制與假設分開列；假設有標示「未驗證」。
- `stakeholders_and_needs`：至少含顧客與第一線；每個角色都有痛點或阻力欄，不是只有需求；有標影響力高低。
- `service_concept_and_architecture`：概念能用一句話講完；每個服務階段都有對應的接口或資源；看得出「誰做什麼」而不只是「發生什麼」。
- `frontstage_backstage_touchpoints`：每個階段至少一個後台支援；全表至少三個具體服務實證（可被拍照的物件）；每列風險欄有內容且不是空話。
- `prototype_and_validation_next_steps`：原型形式具體（流程腳本、線框、情境模擬、實地試行擇一以上）；每個假設對應一個觀察指標；有測試對象與人數量級；沒有「持續優化」這種不可執行句。

## Quick Reference

- 定義與流程：讀 [references/service-design-principles-and-process.md](./references/service-design-principles-and-process.md)
- 方法與工具：讀 [references/service-design-methods.md](./references/service-design-methods.md)
- 輸出模板：讀 [references/service-design-output-templates.md](./references/service-design-output-templates.md)
- 工作坊促進：讀 [references/service-design-facilitation-guide.md](./references/service-design-facilitation-guide.md)

## Quality Rules

- 先定義問題，再提方案，不要直接跳結論。
- 用顧客體驗與服務運作雙視角，不只寫行銷話術。
- 接觸點必須對應到服務階段與前後台，不要只列通路名稱。
- 把服務實證寫成可觀察物件，例如空間、介面、通知、文件、制服、包裝。
- 驗證步驟要包含原型形式、測試對象、成功訊號。

## Common Mistakes

每條格式為「症狀 → 修法」：

- 寫成單純 customer journey。症狀：表格只有顧客行動與情緒，沒有後台與實證 → 修法：每個階段強制補「後台誰在支援」「顧客看得到什麼證據」兩欄。
- 方法名詞堆滿。症狀：AT-ONE、POEMS 都出現了，痛點仍然抽象 → 修法：刪掉方法名，直接寫「誰、在哪個階段、卡在什麼」。
- 只寫理想體驗。症狀：全文沒有限制、成本、人力等字眼 → 修法：每個概念補一行「要成立需要什麼」，寫不出來就降級該概念。
- 利害關係人只剩顧客。症狀：表裡沒有第一線與後台角色 → 修法：問「顧客體驗到的每件事是誰做出來的」，把答案列進表。
- 接觸點寫成通路清單。症狀：只有「LINE、官網、門市」，沒有階段對應 → 修法：每個接觸點綁一個服務階段與一個顧客任務。
- 服務實證缺席或抽象。症狀：實證欄寫「良好體驗」「專業形象」 → 修法：改成可拍照的東西：指示牌、通知訊息、收據、制服、包裝。
- 概念是功能清單。症狀：概念段落是功能堆疊，講不出一句話版本 → 修法：強制改寫成「為（誰）在（情境）提供（價值），靠（關鍵做法）」。
- 驗證計畫不可執行。症狀：只寫「先試營運看看」 → 修法：補齊原型形式、對象、方法、成功訊號四件套，缺一就不算完成。
- 假設混進事實。症狀：讀者分不出哪些是使用者提供、哪些是推測 → 修法：所有推測前綴「假設：」並集中列在 `problem_and_context`。

## Suggested Prompt

Use `$service-design-workshop` to turn a service design challenge into a Traditional Chinese workshop output with problem framing, stakeholders, service architecture, frontstage/backstage touchpoints, and prototype validation steps.
