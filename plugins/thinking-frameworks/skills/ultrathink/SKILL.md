---
name: ultrathink
description: Use before producing any deliverable — articles, reports, proposals, plans, business models, or code — to run a structured pre-work thinking pass through curated thinking frameworks in sequence (currently 邏輯推導 logical reasoning: MECE, 空雨傘, 魚骨圖; 創意發想 creative ideation: 六頂思考帽, 腳本圖), locking direction and key points so the output is substantive and well-aimed. Trigger on ultrathink, 深度思考, 想清楚再做, 思考框架, 抓重點, 言之有物, 沒抓到重點, 邏輯推導, MECE, 不重不漏, 空雨傘, 魚骨圖, fishbone, 創意發想, 六頂思考帽, six thinking hats, 腳本圖, storyboard, or when the user wants output that misses fewer points and has real depth.
---

# Ultrathink 動手前思考層

## Overview

在產出任何交付物之前，先依序套用內建的思考框架，把方向和重點想清楚，再動手。任務型態不限：文章、報告、提案、企劃、商業模式、程式，或其他任何要交付成果的工作。

本 skill 只負責思考層，不規定交付物的最終格式，可與負責產出的其他 skill 疊加使用。使用時，所有框架與其內含工具全部依序跑過一遍，不挑選、不跳過。

輸出包含：

- 各框架套用後的思考筆記（工作用）
- 方向摘要：核心結論、支撐結構、關鍵取捨
- 之後才進入交付物產出

## Input Contract

必填：

- `task` — 這次要完成什麼：交付物類型與目的

可選：

- `audience` — 交付對象是誰、他們在意什麼
- `context` — 背景、素材、既有內容
- `constraints` — 限制（篇幅／時間／技術／資源）
- `show_thinking` — 是否完整輸出思考筆記（預設只輸出方向摘要）

資訊不足時，列出假設後繼續，並在方向摘要標明哪些判斷建立在假設上。

## Workflow

1. **界定任務** — 用一兩句話寫下：交付物是什麼、給誰、要造成什麼效果、怎樣算成功。這是後續所有框架共用的邊界。
2. **依序套用思考框架** — 按下表順序逐一執行：讀取該框架的 reference，把裡面每一個工具依序套用到當前任務，留下針對這個任務的具體思考筆記，不是框架定義的複述。每用完一個工具，立刻跑該工具的自檢清單，發現漏想的補完再往下。

| 順序 | 框架 | 內含工具 | 作用 |
| --- | --- | --- | --- |
| 1 | [邏輯推導](./references/01-logical-reasoning.md) | MECE、空雨傘、魚骨圖 | 依事物的道理思考：MECE 列舉不重不漏、空雨傘從事實推到行動、魚骨圖拆解成因對症下藥 |
| 2 | [創意發想](./references/02-creative-ideation.md) | 六頂思考帽、腳本圖 | 先發散再收斂：六頂思考帽以多觀點集結點子，腳本圖把模糊想法具體化成可分享的故事 |

3. **收斂成方向摘要** — 整合各框架的筆記，寫出：核心結論或主張、支撐它的結構、考慮過但排除的方向與原因。
4. **產出交付物** — 帶著方向摘要動手。完成後回頭對照思考筆記，確認產出沒有偏離結論、沒有漏掉筆記裡的重點。

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
- 團隊型思考工具在環境支援時，每個角色開一個獨立 context 的 subagent 扮演，各角色互不看彼此的產出，避免觀點互相污染；不支援 subagent 時才由自己依序分飾。
- 假設要標明，不要把假設寫成結論。

## Common Mistakes

- 把框架當表格填空，填出來的內容換一個任務也通用，代表沒有真的套用。
- 思考做完，產出卻自顧自地寫，方向摘要完全沒有進到交付物。
- 在交付物裡大量鋪陳思考過程，淹沒真正的內容（除非使用者要求展示）。
- 跳過任務界定直接套框架，連要窮盡的「整體」都沒定義。
- 只挑「看起來適合」的框架跑，其他默默略過。本 skill 的設計是全部跑過一遍。

## Quick Reference

- 邏輯推導（MECE、空雨傘、魚骨圖：操作步驟、對照範例與自檢清單）：讀 [references/01-logical-reasoning.md](./references/01-logical-reasoning.md)
- 創意發想（六頂思考帽、腳本圖：操作步驟、對照範例與自檢清單）：讀 [references/02-creative-ideation.md](./references/02-creative-ideation.md)

## Suggested Prompt

Use `$ultrathink` before producing any deliverable to run the built-in thinking framework sequence, lock direction and key points first, then produce a substantive, well-aimed result.
