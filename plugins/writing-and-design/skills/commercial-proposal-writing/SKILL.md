---
name: commercial-proposal-writing
description: >-
  This skill MUST be used when drafting or reviewing internal proposals,
  fundraising decks, partnership proposals, proposal rewrites, and
  decision-oriented business plans that must persuade a specific audience to
  approve resources, invest money, or commit to collaboration. MUST trigger on
  requests such as 商業企劃, 內部提案, 募資提案, 合作提案, 提案優化, 提案審稿, 董事會版本, 投資人版本, ask 撰寫,
  資料不足處理.
metadata:
  version: "1.2.1"
---

# 商業企劃寫作

## Overview

協助內部提案、募資及合作企劃，讓決策者理解問題、方案、證據與需要批准的資源。依請求產出完整提案、修改指定內容或審查原稿。

## Input Contract

沿用對話與原稿中的資料。完整提案先釐清決策對象、問題、決策請求、可用證據及資源與時程。局部修改只需要目標段落、修改目的及會影響判斷的脈絡。審查需要原稿與審查範圍。

資料不足時，先依 [輸入與受眾判斷](references/01-intake-and-audience-routing.md) 主動查找、核對並補齊本次需要的資料，再判斷是否需要補問。只有與任務無關的內容才能省略，不得因缺資料就刪掉必要章節或改用假設。不得編造市場、財務、團隊經歷或成效。

## Workflow

| 任務 | 做法與必讀文件 |
| --- | --- |
| 完整提案 `generate` | 讀 [企劃五問](references/02-strategy-thinking-engine.md) 與 [提案類型](references/03-proposal-structure-by-type.md)，確認決策邏輯。依既有或指定結構寫作，需要完整骨架時使用 [提案模板](assets/templates/proposal_full_template.md)，相關章節讀 [寫作手冊](references/04-section-writing-playbook.md)。 |
| 局部改稿 `rewrite` | 讀指定段落及相關上下文，保留原有事實、語氣與結構，只修改約定範圍。按內容讀寫作手冊中的相關章節。 |
| 純審查 `review` | 讀 [審稿規則](references/06-review-rubric-and-rewrite-rules.md)，列出有依據的問題、影響與修正建議。只有使用者要求改寫時才交付改稿，完整盤點可參考 [審稿模板](assets/templates/review_report_template.md)。 |

- 涉及財務、KPI 或風險時，讀 [數字與風險](references/05-financial-assumption-and-risk-guide.md)，檢查來源、公式與假設。
- 寫作時讀 [語氣指南](references/07-formal-tone-style-guide.md)，並搭配 human-writing。完成後按任務範圍使用 [交付檢查](references/08-output-polish-and-pitch-checklist.md)。
- 商業模式重設交由 business-model-architect。研究分析腳本 `scripts/*.py` 僅在明確要求研究分析時使用。

## Output Contract

- 完整提案：交付可閱讀的正文、具體決策請求，以及必要的數字推導、假設與待驗證事項。草案須標明尚缺哪些決策依據。
- 局部改稿：交付改好的指定內容。只有影響理解時才補充修改理由或資料缺口。
- 純審查：交付實際發現與建議，標出原稿位置及影響。資料不足以判斷的部分明示限制，不把局部審查當成整份企劃的送審判定。

## Quality Rules

- 以受眾要做的決策選擇內容。問題須交代受影響對象、代價及現有方案的不足，方案須連到具體成果。
- 關鍵結論須有證據或明示假設。數字保留來源、推導與適用條件，財務、KPI、資源及時程須一致。
- 競爭比較應說明選擇理由，市場資料應支持需求判斷。涉及行銷時才檢查通路、轉換與適用的單位經濟指標。
- 執行計畫交代能力、責任與繼續或停止的條件。揭露會影響決策的風險及因應，不為湊數新增風險。
- 完整提案必須明說要求批准什麼、需要多少資源、何時決策及下一步。使用者指定的完整結構須遵守，其他情況依任務選擇章節。
