---
name: ultrathink
description: Use whenever the agent thinks at all — writing copy or reports, proposals, planning products or features, coding, debugging, or any other task — running ALL curated thinking frameworks in sequence (currently 邏輯推導 logical reasoning: MECE, 空雨傘, 魚骨圖; 創意發想 creative ideation: 六頂思考帽, 腳本圖, 心智圖; 市場分析 market analysis: 3C 分析, SWOT 分析, 4P與4C; 進度管理 progress management: 惠特默模型, KPI 樹狀圖, PDCA; 權衡得失 weighing trade-offs: 決策矩陣, PMI 表, 力場分析; 預測未來 predicting the future: S 型曲線, 鴻溝理論, 長尾模型; 思維模型 mental models: 第一性原理, 反向思考法, 二階思考, 能力圈, 奧坎剃刀) to lock direction and key points before acting. Theme grouping is navigation only — work through every theme, not just the ones that look relevant. Trigger on ultrathink, 深度思考, 想清楚再做, 思考框架, 抓重點, 言之有物, 沒抓到重點, any framework or tool name above, or whenever a task involves thinking, planning, writing, building, or debugging.
---

# Ultrathink 動手前思考層

## Overview

只要在思考，就使用本 skill——想文案、寫報告、做提案、規劃新商品或新功能、寫程式、debug，任何需要動腦的時刻，都先依序跑過內建的思考框架，把方向和重點想清楚，再動手。

本 skill 只負責思考層，不規定交付物的最終格式，可與負責產出的其他 skill 疊加使用。使用時，所有框架與其內含工具全部依序跑過一遍，不挑選、不跳過。大主題的分組只是幫忙快速定位內容的索引，不是取用範圍——不能只看跟當前任務相關的主題，整個 skill 的內容都要看過、想過。

輸出包含：

- 各框架套用後的思考筆記（工作用）
- 方向摘要：核心結論、支撐結構、關鍵取捨
- 之後才進入交付物產出

## Input Contract

必填：

- `task` — 這次要完成什麼：交付物或要解決的問題，與其目的

可選：

- `audience` — 交付對象是誰、他們在意什麼
- `context` — 背景、素材、既有內容
- `constraints` — 限制（篇幅／時間／技術／資源）
- `show_thinking` — 是否完整輸出思考筆記（預設只輸出方向摘要）

資訊不足時，列出假設後繼續，並在方向摘要標明哪些判斷建立在假設上。

## Workflow

1. **界定任務** — 用一兩句話寫下：交付物或要解的問題是什麼、給誰、要造成什麼效果、怎樣算成功。這是後續所有框架共用的邊界。
2. **依序套用思考框架** — 按下表順序逐一執行：讀取該框架的 reference，把裡面每一個工具依序套用到當前任務，留下針對這個任務的具體思考筆記，不是框架定義的複述。每用完一個工具，立刻跑該工具的自檢清單，發現漏想的補完再往下。

| 順序 | 框架 | 內含工具 | 作用 |
| --- | --- | --- | --- |
| 1 | [邏輯推導](./references/01-logical-reasoning.md) | MECE、空雨傘、魚骨圖 | 依事物的道理思考：MECE 列舉不重不漏、空雨傘從事實推到行動、魚骨圖拆解成因對症下藥 |
| 2 | [創意發想](./references/02-creative-ideation.md) | 六頂思考帽、腳本圖、心智圖 | 先發散再收斂：六頂思考帽多觀點集結點子、腳本圖把想法具體化成故事、心智圖窮盡選項拓寬廣度 |
| 3 | [市場分析](./references/03-market-analysis.md) | 3C 分析、SWOT 分析、4P與4C | 看清環境再定位：3C 收斂定位、SWOT 盤點內外優劣導出方向、4P×4C 交叉比對賣方設計與買方感受 |
| 4 | [進度管理](./references/04-progress-management.md) | 惠特默模型、KPI 樹狀圖、PDCA | 把目標立正確、拆得動、滾得動：惠特默 14 項檢核目標、KPI 樹拆成可監控的子目標、PDCA 形成持續改善循環 |
| 5 | [權衡得失](./references/05-weighing-tradeoffs.md) | 決策矩陣、PMI 表、力場分析 | 用最優原則取代滿意原則：決策矩陣加權比較選項、PMI 表納入有趣點、力場分析衡量改變的推力與拉力 |
| 6 | [預測未來](./references/06-predicting-future.md) | S 型曲線、鴻溝理論、長尾模型 | 用模型推估接下來會怎樣：S 曲線判斷生命週期階段、鴻溝理論檢視能否跨進主流、長尾模型評估利基集結的價值 |
| 7 | [思維模型](./references/07-mental-models.md) | 第一性原理、反向思考法、二階思考、能力圈、奧坎剃刀 | 跨領域思考紀律，兼作前面所有結論的總體檢：拆到本質重建、反向排雷、推演連鎖反應、認清能力邊界、假設最少者優先 |

3. **收斂成方向摘要** — 整合各框架的筆記，寫出：核心結論或主張、支撐它的結構、考慮過但排除的方向與原因。
4. **產出與行動** — 帶著方向摘要動手：寫出交付物、執行方案或修正問題。完成後回頭對照思考筆記，確認沒有偏離結論、沒有漏掉筆記裡的重點。

## Output Contract

- `direction_summary` — 方向摘要（必有）：核心結論、支撐結構、關鍵取捨與假設
- `thinking_notes` — 各框架的套用筆記（`show_thinking` 為真時完整輸出，否則作為工作筆記支撐產出）
- 交付物本身依任務性質產出，格式不由本 skill 規定

預設使用繁體中文。

## Quality Rules

- 每個框架都要實際套用到當前任務並產出具體內容，只複述框架定義等於沒做。
- 思考筆記裡的每個關鍵判斷，要能在最終交付物中指認得到，不能思考歸思考、產出歸產出。
- 先思考後產出，不要先寫完再回頭補筆記。
- 所有框架與工具全部依序跑過，不挑選、不跳過；每個工具做完都要跑完它的自檢清單，漏想的補完才能往下。
- 大主題分組只是快速定位的索引，不是取用範圍。每次使用都要把全部主題與工具看過、想過，不能只讀與當前任務相關的部分。
- 團隊型思考工具在環境支援時，每個角色開一個獨立 context 的 subagent 扮演，各角色互不看彼此的產出，避免觀點互相污染；不支援 subagent 時才由自己依序分飾。
- 假設要標明，不要把假設寫成結論。

## Common Mistakes

- 把框架當表格填空，填出來的內容換一個任務也通用，代表沒有真的套用。
- 思考做完，產出卻自顧自地寫，方向摘要完全沒有進到交付物。
- 在交付物裡大量鋪陳思考過程，淹沒真正的內容（除非使用者要求展示）。
- 跳過任務界定直接套框架，連要窮盡的「整體」都沒定義。
- 只挑「看起來適合」的框架跑，其他默默略過。本 skill 的設計是全部跑過一遍。
- 把主題分組當篩選器，只讀跟當前任務「相關」的主題。分組是索引，內容是全集。

## Quick Reference

- 邏輯推導（MECE、空雨傘、魚骨圖：操作步驟、對照範例與自檢清單）：讀 [references/01-logical-reasoning.md](./references/01-logical-reasoning.md)
- 創意發想（六頂思考帽、腳本圖、心智圖：操作步驟、對照範例與自檢清單）：讀 [references/02-creative-ideation.md](./references/02-creative-ideation.md)
- 市場分析（3C 分析、SWOT 分析、4P與4C：檢視面向、操作步驟與自檢清單）：讀 [references/03-market-analysis.md](./references/03-market-analysis.md)
- 進度管理（惠特默模型、KPI 樹狀圖、PDCA：操作步驟、對照範例與自檢清單）：讀 [references/04-progress-management.md](./references/04-progress-management.md)
- 權衡得失（決策矩陣、PMI 表、力場分析：操作步驟、對照範例與自檢清單）：讀 [references/05-weighing-tradeoffs.md](./references/05-weighing-tradeoffs.md)
- 預測未來（S 型曲線、鴻溝理論、長尾模型：判斷表、操作步驟與自檢清單）：讀 [references/06-predicting-future.md](./references/06-predicting-future.md)
- 思維模型（第一性原理、反向思考法、二階思考、能力圈、奧坎剃刀：操作步驟、對照範例與自檢清單）：讀 [references/07-mental-models.md](./references/07-mental-models.md)

## Suggested Prompt

Use `$ultrathink` whenever you think through any task to run the full built-in thinking framework sequence, lock direction and key points first, then produce a substantive, well-aimed result.
