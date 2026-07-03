---
name: minto-pyramid-communication
description: Use when structuring workplace communication with the Minto Pyramid Principle, SCQA, and BLUF so the conclusion leads and the ask is explicit, especially for upward reporting, status reports, business emails, presentation outlines, and cross-team persuasion. Trigger on 向上匯報、工作報告、週報、商務 email、簡報大綱、說服提案、結論先行、金字塔原理、SCQA、跨部門溝通, or when raw findings must be turned into a decision-driving message.
---

# Minto 金字塔商務溝通

## Overview

把零散的發現、數據、事件，重組成「結論先行、以上統下」的溝通成品。理論基礎：Barbara Minto 金字塔原理 + SCQA 開場 + BLUF（Bottom Line Up Front）。

適用場景：向上匯報、工作報告、週報、商務 email、簡報大綱、跨部門說服、要預算要資源、壞消息回報。

輸出不是理論解說，是可直接寄出、可直接上台的成稿或骨架。

Do not use：

- 使用者只要潤飾文字、不需要重組結構（轉 `$human-writing`）。
- 對外行銷文案或社群貼文（受眾是大眾不是決策者，說服邏輯不同）。
- 法律、合約類文件（結構由法定格式決定，不適用結論先行）。

Handoff：

- 使用者要 .pptx 成品時，先用本 skill 產出 `deck_outline`（storyline 與每頁主張），再轉交 pptx 類 skill 製作檔案（外部依賴，非本 repo 提供；環境中沒有時，交付 `deck_outline` 純文字即為完成）。
- 結構定稿後要語氣潤飾、去 AI 腔，轉交 `$human-writing`，但不得動結論位置與標題主張句。
- 提案涉及完整商業計畫（市場、財務、ask 設計）時，結構層用本 skill，內容深度轉 `$commercial-proposal-writing`。

## Input Contract

必填：

- `audience` — 受眾是誰、職級、對此議題的既有立場（支持 / 中立 / 抗拒 / 未意識到問題）
- `purpose` — 溝通目的：讀完後要對方做什麼決定或行動，一句話
- `raw_material` — 原始素材：發現、數據、事件、分析結果、進度事實

可選：

- `format` — `email` / `one_pager`（一頁報告）/ `deck_outline`（簡報骨架）/ `verbal`（口頭匯報），預設 `email`
- `length_limit` — 篇幅限制（字數、頁數或秒數）
- `sensitivity` — 是否含壞消息、跨部門利害衝突
- `output_language` — 預設繁體中文

缺件處理：

- 缺 `purpose` 必須先問。沒有 ask 就無法決定 governing thought，不得硬產。
- 缺 `audience` 立場時，假設中立並在輸出標明此假設。
- `raw_material` 太少時列出假設後繼續，並標出哪些論點需要補證據。
- 使用者只丟一段流水帳而沒有任何欄位時，先從文中推斷 `audience` 與 `purpose`，回報推斷結果再產出。

## Workflow

1. **受眾決策分析**
   - 回答一個問題：對方讀完後要做什麼（核准 / 選 A 或 B / 給資源 / 知悉並放行）。
   - 這個答案決定金字塔頂點的措辭。不是你想講什麼，是對方需要聽什麼才能行動。
   - 產出：一句 ask 描述（誰、決定什麼、何時之前）。
2. **提煉 governing thought**
   - 用 [references/01-pyramid-core.md](./references/01-pyramid-core.md) 的五步法：素材倒出 → 分組 → 每組結論 → 組間結論 → 頂點改寫。
   - 必須是「有立場的主張」，不是主題。測試：句尾加「我不同意」，語意通順才算主張。
   - 產出：一句主張句，內含或緊連 ask。
3. **SCQA 開場設計**
   - 依受眾狀態從四變體選一：標準式 SCA、開門見山式 ASC、突出憂慮式 CSA、突出信心式 QSCA。
   - 選擇規則與 12 組中文範例見 [references/02-scqa-openings.md](./references/02-scqa-openings.md)。
   - 產出：開場段成稿 + 一行選擇理由。
4. **關鍵線 MECE 分組**
   - 支撐點 3±2 個。跑兩兩重疊測試與集體窮盡測試。
   - 出現「其他」桶代表分類軸錯了，換軸重分（時間 / 流程 / 對象 / 內外部）。
   - 產出：每點一句主張句 + 所屬證據清單。
5. **縱向 Q&A 檢查**
   - 對每個節點寫下「這句會讓讀者問什麼」（why / how / so what）。
   - 確認下一層第一句直接回答該疑問，不是回答別的問題。
   - 沒有引出任何疑問的節點是廢話，刪除。
6. **橫向邏輯選擇**
   - 每組決定歸納或演繹：受眾抗拒用演繹鋪路，受眾趕時間用歸納直給，判斷不出來預設歸納。
   - 歸納組必須通過複數名詞測試；演繹鏈不超過三步。
7. **依格式輸出**
   - 套用 [references/03-formats-playbook.md](./references/03-formats-playbook.md) 對應模板成稿。
   - 交付前跑 [references/04-review-checklist.md](./references/04-review-checklist.md) 自檢，任一項不過就回修。

## Output Contract

固定輸出以下段落：

- `governing_thought` — 一句話主答案（主張句，含 ask 方向）
- `scqa_opening` — 選用的變體與開場成稿，附一行選擇理由
- `pyramid_outline` — 頂點 + 關鍵線（每點一句主張）+ 各點支撐證據，標明每組用歸納或演繹
- `final_output` — 依 `format` 完成的成稿或骨架
- `delivery_notes`（可選）— 預期追問與應答、口頭補充要點、哪些證據建議備而不發

格式特化：

- `email`：主旨行必須輸出，行動項置底加粗。
- `one_pager`：標題即 governing thought，附篇幅分配。
- `deck_outline`：附標題列連讀檢查結果（storyline test）。
- `verbal`：額外附 30 秒電梯版。

## Quality Rules

- **第一段測試**：只讀第一段（或 email 主旨+首句），受眾必須已知道結論與你要他做什麼。做不到就重寫第一段。
- **標題行動化**：一頁報告的節標題、簡報的每頁標題必須是主張句。測試：把所有標題依序連讀，要等於一段完整論證；連不起來就改標題。
- **無「其他」分組**：關鍵線與任何分組不得出現「其他 / 雜項 / 補充」。出現即代表分類軸錯誤，必須換軸。
- **每個主張下必有支撐**：任何主張句下面至少一條具體證據（數據、事件、引述）。沒有證據的主張要嘛補證據、要嘛降級為假設並標明。
- **activity vs findings 檢查**：逐條掃描內容，「我做了 X」是 activity，「做了 X 之後發現 Y、所以 Z」才是 finding。報告主體只留 findings，activities 移附錄或刪除。
- **量化優先**：影響一律用數字表達（錢 / 天 / 人 / %）。「有點延遲」「影響不小」不得出現在成稿。

## Common Mistakes

- **埋結論（buried lede）**：先鋪背景、方法、過程，結論放最後一段。修法：把最後一段搬到最前面，背景壓縮進 SCQA 的 S。
- **流水帳式活動報告**：週報寫成「週一開會、週二寫文件」。修法：改以結論分組（進度結論 / 風險 / 需要的支援），活動只當證據。
- **資料倒灌**：把所有分析都放進正文證明自己努力。修法：正文只留直接支撐關鍵線的證據，其餘全進 appendix。
- **主題句不是主張句**：標題寫「關於 Q3 供應鏈風險」而非「Q3 供應鏈風險已需啟用第二供應商」。修法：改寫成可以被反對的完整句子。
- **向上匯報不給選項與建議**：只丟問題等主管想辦法。修法：永遠附選項 A/B、你的推薦與理由、需要對方決定什麼與期限。
- **開場變體選錯**：對抗拒的受眾用 ASC 開門見山，結論還沒鋪路就被打槍。修法：先回受眾決策分析，重選變體。

## Quick Reference

- 四規則操作化、governing thought 五步提煉、縱向問答、歸納 vs 演繹、MECE 檢查：讀 [references/01-pyramid-core.md](./references/01-pyramid-core.md)
- SCQA 心理機制、四變體選擇規則、12 組中文商務開場範例：讀 [references/02-scqa-openings.md](./references/02-scqa-openings.md)
- Email / 一頁報告 / 簡報骨架 / 30 秒口頭版 / 向上管理與壞消息結構（含 before/after）：讀 [references/03-formats-playbook.md](./references/03-formats-playbook.md)
- 交付前自檢清單與病徵診斷表：讀 [references/04-review-checklist.md](./references/04-review-checklist.md)

## Suggested Prompt

Use `$minto-pyramid-communication` to restructure raw findings into a conclusion-first email, one-page report, deck outline, or verbal briefing with the Minto Pyramid Principle and SCQA, in Traditional Chinese.

範例：

- `用 $minto-pyramid-communication 幫我把這份專案進度整理成給總經理的一頁報告，我要爭取延長兩週時程。`
- `這是我這週做的事，幫我用金字塔原理改寫成結論先行的週報。`
- `我要跨部門跟 IT 要兩個人力支援，幫我寫說服 email，對方立場偏抗拒。`
- `明天要跟 CEO 匯報一個壞消息，給我 30 秒口頭版和一封後續 email。`
