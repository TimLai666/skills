---
name: ultrathink
description: >-
  MUST run whenever the agent thinks at all — writing, planning, building,
  coding, debugging, or deciding. For each decision unit, MUST select one or
  two relevant task categories from 邏輯推導, 創意發想, 市場分析, 進度管理,
  權衡得失, 預測未來, and 辯論思考, then run every tool and self-check in each
  selected category. MUST NOT run every task category merely for completeness.
  After routing, MUST run isolated analyses in English, Spanish, German, Modern
  Standard Arabic, Korean, and Turkish, then synthesize in Traditional Chinese.
  MUST NOT choose thinking languages by country, market, jurisdiction, source,
  or audience. MUST then run the common layer in full:
  第一性原理, 反向思考法, 二階思考, 能力圈, 奧坎剃刀, the fallacy checks, and
  subtraction review. Trigger on ultrathink, 深度思考, 想清楚再做, 思考框架,
  抓重點, 言之有物, 沒抓到重點, any included framework name, or any task that
  involves thinking.
metadata:
  version: "1.4.0"
---

# Ultrathink 動手前思考層

## Overview

只要在思考，就使用本 skill。先把任務切成需要各自下結論的「決策單元」，每個決策單元選擇 1～2 個相關的任務類別。選中的類別要把全部工具與自檢依序跑完，不選的類別不讀、不硬套。

任務類別跑完後，固定執行六條多語言思考路徑：英文、西班牙文、德文、現代標準阿拉伯文、韓文與土耳其文。每條路徑都要完整回答任務，再執行該語言負責的注意力檢查。繁體中文保留使用者原意，並把六條路徑整理成共同結論、衝突、獨有發現與待查證事實，不在這一層下最終判斷。之後由共用層整合這些結果，跑完五個思維模型、謬誤檢核與減法審查，再形成最終判斷。繁體中文不算第七條思考路徑。多語言思考層與共用層都不占 1～2 個任務類別的名額，也不能因為任務看起來簡單而省略。

本 skill 只負責思考層，不規定交付物的最終格式，可與負責產出的其他 skill 疊加使用。

思考流程內部保留：

- 路由紀錄：決策單元、選中的任務類別、選擇依據
- 選中類別、多語言思考層與共用層的思考筆記（工作用）
- 方向摘要：核心結論、支撐結構、關鍵取捨

## Input Contract

必填：

- `task` — 這次要完成什麼：交付物或要解決的問題，與其目的

可選：

- `audience` — 交付對象是誰、他們在意什麼
- `context` — 背景、素材、既有內容
- `constraints` — 限制（篇幅／時間／技術／資源）
- `show_thinking` — 是否完整輸出思考筆記（預設只輸出方向摘要）

資訊不足但不影響核心結論時，列出假設後繼續，並在方向摘要標明假設。缺少的資料會影響核心結論時，該決策單元標成 `blocked`，只列資料缺口與查證方式，不得進入裁決與行動。

## Workflow

1. **界定決策單元** — 用一兩句話寫下：這次要下什麼結論、給誰、要造成什麼效果、怎樣算成功。複合任務若包含多個彼此獨立的結論，先拆成多個決策單元。每個單元各自執行步驟 2～4，所有單元完成後再進入任務層級的步驟 5～7。
2. **選擇 1～2 個任務類別** — 依下表選擇最直接影響這個結論的 1～2 類，留下選擇依據。即使三類以上看起來都相關，單一決策單元仍只選最相關的兩類；只有任務本來就包含多個可獨立下結論的決策時，才依步驟 1 拆分。

| 任務類別 | 內含工具 | 選擇線索 |
| --- | --- | --- |
| [邏輯推導](./references/01-logical-reasoning.md) | MECE、空雨傘、魚骨圖 | 要拆結構、解讀現象、追查成因或從事實導出行動 |
| [創意發想](./references/02-creative-ideation.md) | 六頂思考帽、腳本圖、心智圖 | 要產生替代方案、拓寬選項或具體化使用情境 |
| [市場分析](./references/03-market-analysis.md) | 3C 分析、SWOT 分析、4P與4C | 結論取決於對象、競爭、定位、通路或市場環境 |
| [進度管理](./references/04-progress-management.md) | 惠特默模型、KPI 樹狀圖、PDCA | 要設定目標、拆指標、安排執行或建立改善循環 |
| [權衡得失](./references/05-weighing-tradeoffs.md) | 決策矩陣、PMI 表、力場分析 | 要比較選項、判斷是否改變或分配資源 |
| [預測未來](./references/06-predicting-future.md) | S 型曲線、鴻溝理論、長尾模型 | 結論取決於生命週期、採用擴散、時間變化或頭尾配置 |
| [辯論思考](./references/07-debate-thinking.md) | 需根解損、判定立駁 | 要裁決變更提案或價值主張是否成立 |

路由時同步記下「最可能推翻目前方向、但沒有選的類別」及不選理由，避免先有答案再挑支持答案的框架。任務目標改變、關鍵假設被推翻或進入新階段時，重新界定決策單元並路由。

3. **跑完選中類別** — 讀取所選類別的 reference，把類別內每一個工具依序套用到當前決策單元，留下具體思考筆記。每用完一個工具，立刻跑當前階段可驗證的完整自檢。PDCA 等跨階段工具先完成目前能執行的階段，記下已完成階段、未完成階段與恢復條件，取得實際結果後再續跑；不得捏造尚未發生的執行結果。資料不足時仍要執行能完成的部分，若缺口會影響核心結論，該決策單元標成「資料不足，無法裁決」與 `blocked`，不得捏造資料補滿格式。
4. **跑完多語言思考層** — 讀取[多語言思考](./references/multilingual-thinking.md)，讓英文、西班牙文、德文、現代標準阿拉伯文、韓文與土耳其文六條固定路徑各自重新分析當前決策單元。每條路徑取得相同任務資料，在隔離 context 使用指定語言作答，不得翻譯或沿用其他路徑的答案。各路徑完成後，主 agent 用繁體中文整理共同結論、衝突、獨有發現與待查證事實，不得在這一步裁決衝突或形成最終判斷。
5. **跑完共用層** — 共用層不參與路由，也不占類別名額。每個任務執行一次，把選中類別的筆記與六語分析中會影響判斷的內容一起作為輸入，對所有決策單元逐一留下檢查結果，不得把任何單元合併略過：
   - 依序跑完[思維模型](./references/08-mental-models.md)的第一性原理、反向思考法、二階思考、能力圈、奧坎剃刀。
   - 全程以[謬誤檢核清單](./references/fallacy-checklist.md)輕量自檢；方向摘要收斂前與重要結論送出前，執行七組獨立 subagent 的完整檢核，命中後先修補再重檢。
   - 依 `subtraction-thinking` 檢查留下來的方案：哪些組成部分拿掉不影響核心目的，哪條路徑可以更短。
6. **逐單元收斂** — 決策單元為 `decidable` 時，依共用層對多語言紀錄與選中類別筆記的檢查結果形成最終判斷，再寫出核心結論或主張、支撐結構、關鍵取捨、假設、資料缺口與考慮過但排除的方向。決策單元為 `blocked` 時，改為輸出待查證計畫。任務狀態依各單元彙整：全部可裁決為 `decidable`，部分受阻為 `partially_blocked`，全部受阻為 `blocked`。
7. **產出與行動** — 只對 `decidable` 的決策單元依方向摘要行動；`blocked` 的決策單元只執行蒐集或查證缺失資料所需的動作。跨階段工具若尚未走完，交付時必須保留續跑紀錄；若任務成敗取決於尚未完成的階段，不得宣稱整個任務完成。最後回頭對照路由紀錄與思考筆記，確認六語分析中會影響判斷的內容已進入後續思考，產出沒有偏離結論，也沒有漏掉已確認的重點。

## Output Contract

- `status` — 任務裁決狀態（必有）：`decidable`、`partially_blocked` 或 `blocked`
- `routing_record` — 路由紀錄（必有）：每個決策單元各自的 `decidable`／`blocked` 狀態、選中的 1～2 個任務類別、選擇依據、最危險的未選類別與不選理由
- `direction_summary` — 方向摘要（每個 `decidable` 單元必有）：共用層形成的最終判斷、核心結論、支撐結構、關鍵取捨與假設
- `verification_plan` — 待查證計畫（每個 `blocked` 單元必有）：資料缺口、查證方式、恢復裁決的條件
- `continuation_record` — 續跑紀錄（有跨階段工具未完成時必有）：已完成階段、未完成階段、恢復條件與下一個檢查點
- `thinking_notes` — 選中類別、多語言思考層與共用層的套用筆記（`show_thinking` 為真時完整輸出，否則只作為內部工作筆記支撐產出）
- 交付物本身依任務性質產出，格式不由本 skill 規定

預設使用繁體中文。

## Quality Rules

- 每個決策單元只選 1～2 個任務類別；不得為了顯得完整而全選，也不得把複合任務塞成一個單元來規避上限。
- 選中的類別要把所有工具與自檢完整跑完；未選類別不讀、不套用。
- 選中類別的 reference 若提到其他類別或工具，不得因此擴張本次路由。只有另一類也已選中時才能接用；否則只記成後續重新路由的候選。
- 多語言思考層固定執行英文、西班牙文、德文、現代標準阿拉伯文、韓文與土耳其文六條實際語言路徑。不得用繁體中文角色扮演、同一語言的視角提示或前一路徑的翻譯取代。
- 固定語言路徑在 subagent 可用時各自使用隔離 context；工具不存在、啟動失敗、執行名額已滿或其他原因導致 subagent 當下不可用時，立即改由主 agent 依序執行，不得停在未完成狀態。每條路徑只能取得共同任務資料，不得取得其他路徑的輸出。
- 語言差異只用來增加分析路徑，不當作正確性證據。多數路徑同意的事實仍要查證，少數路徑提出的觀點也不能因票數少而直接丟棄。
- 多語言思考層只能整理共同結論、衝突、獨有發現與待查證事實。最終判斷必須等共用層檢查完這些內容後才能形成。
- 題目涉及的國家、市場、法域、資料來源與受眾，不得改變六條思考語言。查閱原文與製作交付物時可以使用其他語言，但不得把它算成多語言思考路徑。
- 共用層每次都要完整執行，不得算進 1～2 個任務類別，也不得依相關性跳過其中任何思維模型。
- 跨階段工具要建立完整循環並按階段續跑；尚未取得實際結果前，不得宣稱後續階段或整個循環已完成。
- 跨階段工具尚未完成時，必須留下 `continuation_record`；任務成敗依賴未完成階段時，不得把任務標成完成。
- 每個已執行的工具都要實際套用到當前決策單元並產出具體內容，只複述框架定義等於沒做。
- 思考筆記裡的每個關鍵判斷，要能在最終交付物中指認得到，不能思考歸思考、產出歸產出。
- 先思考後產出，不要先寫完再回頭補筆記。
- 團隊型思考工具在環境支援時，每個角色開一個獨立 context 的 subagent 扮演，各角色互不看彼此的產出，避免觀點互相污染；不支援 subagent 時才由自己依序分飾。
- 謬誤檢核貫穿全程，不限辯論思考：任何階段寫下的推理都以[謬誤檢核清單](./references/fallacy-checklist.md)為標準隨時輕量自檢；方向摘要收斂前與重要結論端出去前，執行完整的七組獨立 subagent 地毯式檢核，組間互不相見。
- 工具需要的資料不足時，要列出缺口與不能下的結論，不得為了完成格式而捏造數據、案例或評分。
- 假設要標明，不要把假設寫成結論。

## Common Mistakes

- 把框架當表格填空，填出來的內容換一個任務也通用，代表沒有真的套用。
- 沒拆決策單元，直接替一整包複合任務選兩類，導致後半段目標沒有重新路由。
- 先決定答案，再挑只會支持答案的類別，刻意避開最可能推翻方向的類別。
- 把「只選 1～2 類」誤解成類內工具也能挑著跑。選類是減少不相干類別，不是降低所選類別的完整度。
- 把共用層當成第 1 或第 2 個類別，因而少選一個真正處理任務的類別。
- 六條固定路徑只做逐句翻譯，答案的假設、因果鏈與反例完全相同，形成假多樣性。
- 多語言思考層整理完六條路徑後直接裁決，導致後續共用層只能替既定答案背書。
- 因為題目談日本市場、德國法規或法文資料，就改掉固定思考語言或把資料語言冒充成認知路徑。
- 思考做完，產出卻自顧自地寫，方向摘要完全沒有進到交付物。
- 在交付物裡大量鋪陳思考過程，淹沒真正的內容（除非使用者要求展示）。
- 跳過任務界定直接套框架，連要窮盡的「整體」都沒定義。

## Quick Reference

- 任務類別只讀選中的 1～2 份：
  - 邏輯推導（MECE、空雨傘、魚骨圖）：讀 [references/01-logical-reasoning.md](./references/01-logical-reasoning.md)
  - 創意發想（六頂思考帽、腳本圖、心智圖）：讀 [references/02-creative-ideation.md](./references/02-creative-ideation.md)
  - 市場分析（3C 分析、SWOT 分析、4P與4C）：讀 [references/03-market-analysis.md](./references/03-market-analysis.md)
  - 進度管理（惠特默模型、KPI 樹狀圖、PDCA）：讀 [references/04-progress-management.md](./references/04-progress-management.md)
  - 權衡得失（決策矩陣、PMI 表、力場分析）：讀 [references/05-weighing-tradeoffs.md](./references/05-weighing-tradeoffs.md)
  - 預測未來（S 型曲線、鴻溝理論、長尾模型）：讀 [references/06-predicting-future.md](./references/06-predicting-future.md)
  - 辯論思考（論點三要素、質詢拆解、需根解損、判定立駁）：讀 [references/07-debate-thinking.md](./references/07-debate-thinking.md)
- 多語言思考層每次都讀：
  - 多語言思考（固定六語認知路徑與繁中彙整）：讀 [references/multilingual-thinking.md](./references/multilingual-thinking.md)
- 共用層每次都讀：
  - 謬誤檢核清單（全程輕量自檢與關鍵時刻七組完整檢核）：讀 [references/fallacy-checklist.md](./references/fallacy-checklist.md)
  - 思維模型（第一性原理、反向思考法、二階思考、能力圈、奧坎剃刀）：讀 [references/08-mental-models.md](./references/08-mental-models.md)
  - 減法審查：載入並執行 `subtraction-thinking`

## Suggested Prompt

Use `$ultrathink` to route each decision unit, run isolated English, Spanish, German, Modern Standard Arabic, Korean, and Turkish analyses, synthesize them in Traditional Chinese, then complete the common thinking layer before acting.
