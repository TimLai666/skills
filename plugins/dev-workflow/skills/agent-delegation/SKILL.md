---
name: agent-delegation
description: >-
  This skill MUST be loaded when the user mentions subagent、分工、派工、
  antigravity、agy、opencode、copilot、codex or Claude Code Agent, before dispatching
  work even on small tasks, and when proposing
  changes to existing API names, signatures, usage or behavior（介面變更）.
  It MUST also be loaded before delivering specifications, articles, or reports（規格、文章、報告）for fresh-context review.
  It SHOULD be loaded for questions about who should code or which model to use.
  Existing API changes MUST follow the conditional consultation rule before
  implementation. Ordinary delegation MUST use scripts/dispatch.py and its task-local levels,
  and MUST NOT skip tools based on earlier turns. Main agents MUST define skeletons
  and expected results before implementation, protect tests, and avoid their own CLI.
  Dispatched workers MUST NOT apply this skill or delegate. Ordinary prompts MUST
  carry project lessons; workers MUST report lessons for verification and recording.
metadata:
  version: "2.20.2"
---

# Agent 派工規範

## Overview

主 agent 是強模型，負責寫骨架與每個格子的想要的結果、審查、驗證、提交。骨架鎖住範圍，弱模型照規格寫測試或填實作。一般派工的成本原則：依任務列的可用工具，照 OpenCode → Antigravity（agy）→ GitHub Copilot CLI → Codex → Claude 的順序派。測試、實作與雜事先交給 OpenCode 的免費模型，前端設計交給 agy 的 Gemini。Copilot 固定用 Auto，排在 agy 之後。方案取捨、技術選型與單一模組設計依序交給 agy 的 Opus、Codex 的 GPT-6 以上 sol、Claude 的 Opus。其他任務的模型與接手順序依下方決策表。任何 CLI 都能當主 agent，所以派工前先辨識自己是誰。原生 CLI 的說明入口見 [references/cli-cheatsheet.md](references/cli-cheatsheet.md)。

## Input Contract

一般派工使用 [scripts/dispatch.py](scripts/dispatch.py)，先執行無參數總覽或 `--help`，再讀相關子指令的 `--help`。使用 `list-types` 選擇任務類型，使用 `list-levels` 核對該類型的層級與宿主交接方式；混合任務先拆開，分類與雜事或探索重疊時選分類。

主 agent 提供宿主、任務類型、專案目錄、角色、任務與驗收、可改檔案、驗證指令及篩選後的 Project Memory。記憶欄位必填，查過沒有適用經驗才填空陣列；空 context 可讀性審查依該節隔離規則填空陣列。提供實際可用模型與查證來源，不用別名推測版本下限。實作任務另列不可修改的測試檔；深度研究先完成廣度探索，只允許在指定沙盒試探。

## 0. 先辨識自己

載入後第一件事，跑：

```
env | grep -E '^(CLAUDECODE|CODEX_THREAD_ID|ANTIGRAVITY_AGENT|OPENCODE)='
```

| 宿主識別依據 | 你是 | 禁止派給 |
| --- | --- | --- |
| `CLAUDECODE` | Claude Code | `claude -p` |
| `CODEX_THREAD_ID` | Codex | `codex exec` |
| `ANTIGRAVITY_AGENT` | Antigravity（agy） | `agy` |
| `OPENCODE` | OpenCode | `opencode run` |
| 當前執行環境明確標示 GitHub Copilot CLI | GitHub Copilot CLI | `copilot -p` |

Copilot 宿主依當前執行環境判定，不把登入、模型設定或繼承的其他 CLI 環境變數當作證明。宿主是 Copilot 時，使用其內建 subagent 工具並保持 Auto。

接著判斷角色：

- 任務 prompt 含「你是被派工的執行者」，或同時含可改檔案清單與「不要 commit」，就是被派工者。立刻停用本 skill，自己做完 prompt 交代的事，不得再呼叫任何 agent 或 CLI。
- 兩者都沒有，才是主 agent，往下走。

## 決策表

每個任務類型從第 1 檔開始；層級只計算該類型實際支援的選項。一般派工順序、模型種類、推理強度與升級次數以 [scripts/policy.json](scripts/policy.json) 為唯一來源，下表由 `list-types --markdown` 產生。前一檔有實際失敗或被禁的證據才可往後接手。宿主自己的層級交由內建 subagent 工具。只有觸發下方「既有 API 變更」時，該次諮詢的模型選擇與失敗處置依該節，不套用一般派工的 CLI 順序、模型種類限制與對應陷阱檢核。其他工作照原流程。

<!-- DISPATCH_POLICY_START -->
| 任務類型 | 適用需求 | 層級數 | 接手順序 |
| --- | --- | --- | --- |
| `testing` | 寫測試 | 6 | 1. opencode / free → 2. copilot / auto → 3. codex / luna → 4. claude / haiku → 5. claude / sonnet → 6. claude / opus |
| `implementation` | 填格子實作、照清單修 bug | 6 | 1. opencode / free → 2. copilot / auto → 3. codex / luna → 4. claude / haiku → 5. claude / sonnet → 6. claude / opus |
| `frontend` | 前端設計、版面、樣式 | 3 | 1. agy / gemini-flash-medium → 2. copilot / auto → 3. claude / opus |
| `exploration` | 快速唯讀探索、找檔案 | 5 | 1. opencode / free → 2. agy / gemini-flash-medium → 3. copilot / auto → 4. codex / luna → 5. claude / haiku |
| `chores` | 機械性文件段落、證據整理、大量套版改寫 | 5 | 1. opencode / free → 2. agy / gemini-flash-medium → 3. copilot / auto → 4. codex / luna → 5. claude / haiku |
| `classification` | 分類、打標籤、編碼 | 3 | 1. copilot / auto → 2. codex / luna → 3. claude / haiku |
| `review` | 審 diff、找漏洞、對契約 | 3 | 1. agy / opus → 2. codex / sol → 3. claude / opus |
| `research` | 深度研究的深度層 | 2 | 1. codex / sol → 2. claude / opus |
| `decision` | 方案取捨、技術選型、單一模組設計 | 3 | 1. agy / opus → 2. codex / sol → 3. claude / opus |
| `rules` | 寫 skill、prompt、規則與複雜架構 | 2 | 1. agy / opus → 2. claude / opus |
<!-- DISPATCH_POLICY_END -->

主 agent 自己做：寫骨架與想要的結果、審測試、派出去不划算的格子、讀 diff、跑測試、commit，以及統合深度研究的全部結果、做整體判斷。

### Script 執行與內建工具交接

- 主 agent 必須透過 script 發起與接續一般派工，不自行重排工具或拼接派工指令。操作與參數查詢使用 CLI 的總覽及子指令 `--help`；原生工具說明入口見 [CLI 速查表](references/cli-cheatsheet.md)。
- 外部 CLI 的已知啟動、模型或額度錯誤，只有確認沒有專案檔案變動時才自動接手。正常回報、部分改檔、未知錯誤與逾時先交回主 agent 審查，不把 CLI 成功當成驗收通過。
- 結果為 `native_required` 時，主 agent 使用輸出指定的內建工具、合規模型與完整 prompt。禁止改用宿主自己的 CLI。內建工具不可用或派工失敗時，帶原派工識別碼、實際錯誤與下一層級接續；不可跳級。
- 結果為 `awaiting_review` 時，主 agent 讀 diff、核對範圍並親自驗證。回報已完成驗收、派工失敗或驗證失敗時，依 CLI 的條件接續。寫程式同級連續兩次驗證失敗才升級，不能把成果不合格冒充為未派出。
- 每次接續讀取原派工狀態，保留原 prompt、失敗證據與補充教訓。逾時或中斷先由主 agent 確認程序及半成品，再依「工具失敗」的接續與停止條件處理。
- 狀態與原始輸出存於專案外的使用者狀態目錄，由 script 接續與主 agent 審查時讀取；不在使用者專案根目錄新增協調檔。script 只追蹤自身管理的併行派工，其他 agent 與未納管寫入仍由主 agent 查證。
- 每次外部 CLI 結束，script 先停止其工作程序群，再檢查所有專案檔案（含忽略檔）與授權沙盒。掃描無法完成或有變動就先審查。需要持續執行的服務由主 agent 管理。

- 外部 CLI 派工一律明確指定自動核准：OpenCode 加 `--auto`，Copilot 加 `--allow-all-tools`，Codex 加 `--approve-for-me`，Claude Code 加 `--permission-mode auto`，Claude Code 不改用 bypass。Claude Code 與 agy 從目標專案目錄啟動。
- 自動核准不擴大任務可改檔案清單。表中的「唯讀」只表示 prompt 必須明寫「不得修改任何檔案」；探索、審查與實作沿用相同執行模式，不另設 plan、read-only 沙盒或唯讀工具清單，也不選唯讀專用 agent。宿主內建 subagent 不套用外部 CLI 旗標，可改範圍同樣寫在 prompt。

- 表中只寫模型種類。派工前先跑 `agy models` 或 `opencode models`，挑該種類最新版填進佔位符。
- Copilot 依本專案的免費版使用方式固定設 `--model auto`，不指定具體模型、推理強度或付費替代方案。`--allow-all-tools` 允許自動執行包含改檔在內的工具，`--trust-folder` 僅信任本次 prompt 模式的工作目錄設定。prompt 的可改範圍不變。Copilot 只用於決策表中明列 Auto 的任務，手動指定模型的種類限制不套用 Auto 的內部選擇，但 Auto 不作為 Fable、Opus 或 Astra 的指定模型諮詢。
- opencode 只能用免費模型：`opencode models | grep opencode/` 查得到才算。
- Codex 照表主動派。Review、深度研究與決策只用 GPT-6 以上、名稱含 sol 的模型。名稱含 luna 的模型只用於寫測試、填格子實作、照清單修 bug、快速唯讀探索、雜事與分類。
- 深度研究分三層：
  1. 廣度層：照「快速唯讀探索」那列派（OpenCode、Gemini Flash、Copilot Auto、luna、Haiku），每條負責一個範圍，掃描並回報發現與線索，附出處。回報當成線索，不當成事實。
  2. 深度層：主 agent 從線索挑出值得深挖的項目，每個項目依深度研究那列先派 sol，失敗後才派 Opus，一次只專研一件事，prompt 只放那一件。回報系統結構、可行做法與每個結論的依據（檔案路徑、指令輸出、文件出處）。
  3. 統合層：主 agent 合併廣度與深度的全部結果，核對關鍵依據、前後對照、做出整體判斷，決定採用哪個做法並親自執行。執行者的結論不直接當成定論。
  廣度層沒挑出值得深挖的項目時，不派深度研究。
- 深度研究的 agent 可實際試探系統，但可改檔案只列暫存目錄或沙盒，專案檔一律不可改。試探造成的副作用（建立的檔案、啟動的程序、改過的設定）一併寫進回報，由主 agent 決定保留或清掉。
- 非免費模型的 effort 預設 `medium`，主 agent 判斷任務需要時才調高，最高 `xhigh`。agy 的 Gemini 選模型名結尾是 `-medium` 的版本，agy 的 Claude 加 `--effort medium`，agy 最高只到 `high`。Agent 工具沒有 effort 參數，不用設。
- Haiku 與 Sonnet 只用 5.5 以上版本，所以 agy 的 Sonnet 4.6 不派。
- Haiku 用在唯讀探索、雜事、分類與簡單的寫程式任務。
- 任務同時符合分類與雜事或探索時，照分類那一列派。
- 輪到 Claude 時，Sonnet 用在 Haiku 寫不出來的寫程式任務。
- Opus 只用在前端設計、決策、寫規則、複雜架構、review、深度研究，以及 Sonnet 也沒過驗證的寫程式格子。派工順序依決策表，接手寫程式格子時 `claude -p` 改用 `--effort low`。
- 寫程式那一列，同一個格子在同一級連續兩次沒過驗證才往下一級，claude 那欄依 Haiku、Sonnet、Opus 的順序升級。
- 同一個 CLI 同時最多跑三條，Copilot 也計入，Claude Code 的 Agent 工具也算 claude。
- 不用宿主自己的 CLI 指令派工（`claude -p`、`codex exec` 等），改用宿主內建的 subagent 工具。同一個模型不同 CLI 可以。
- 每輪都照表從最左邊派起。上一輪額度耗盡、逾時或失敗，不代表這一輪還是，實際失敗了才往右走。
- 一般派工的唯一例外：主 agent 判斷很難的寫程式格子，若這次任務裡 opencode 已在同類型的格子交出不完整或沒過驗證的結果，可以跳過 OpenCode，從 Copilot Auto 派起，失敗後再派 luna，其餘往下升級的規則不變。

### 既有 API 變更

只有準備變更既有 API，或函數、變數、結構體、Enum 等程式元素的命名、結構、用法或行為時，才啟動本節。不因任務涉及 API、一般設計、審查或派工就啟動。純內部實作調整若保持上述項目不變，或單純新增且不改變既有名稱、結構、用法或行為，照原流程。

- 變更包括函數／方法的名稱、簽名、參數、回傳值、錯誤與副作用，以及變數、欄位、結構體、Enum 的名稱、結構或使用方式。不以私有、內部使用、改動小或由主 agent 親自實作為豁免理由。
- 在修改受影響的骨架、測試或實作前，先查閱現有定義、呼叫處、測試與文件，整理初案、改動理由及相容性影響，再交給獨立模型諮詢。主 agent 自己的推理不算諮詢。

| 主 agent 環境 | 諮詢模型 |
| --- | --- |
| Claude | Fable 5.1 以上，沒有可用的合格 Fable 時，改用 Opus 5.5 以上 |
| GPT | Astra |

依主 agent 實際使用的模型系列選擇，不由 CLI 名稱猜測。在其他模型環境中，先請使用者指定諮詢模型。用目前工具實際提供的模型識別與版本，別名不足以證明版本下限時先查證。沿用宿主內建 subagent 或外部 CLI 的執行規則。指定模型無法使用時，僅能採用表中明列的替代模型。仍無可用模型就回報證據，暫停該介面變更並請使用者決定，其他獨立工作可繼續。

1. **諮詢**：提供現有程式與使用範例、初案、改動原因、限制及待決策事項。要求顧問檢查命名與用法、行為差異、相容性及替代方案，附依據並標明不確定處。諮詢任務不得修改任何檔案。
2. **修正初案**：主 agent 核對意見與原始內容，採納有依據的建議並修正方案。未採納的重要建議簡述理由，不直接轉貼模型回覆，也不為了顯示有修改而硬改合理的初案。
3. **交由使用者決定**：把修正後的方案與原本就需要使用者決定的事項合併提出。呈現現況與建議改法、最小使用範例、相容性與遷移影響、推薦選項及主要取捨。行為變更用相同輸入對照改前與改後的結果，不能只列函數簽名。範例格式見 [介面變更提案示例](references/api-change-examples.md)。
4. **依決定實作**：取得使用者對具體方案的確認後，接回原本的實作與驗證流程。已確認且未變動的部分不重問。諮詢後新增或改變的待決策事項須先確認。派工涉及這些介面時，在 prompt 列出核准範圍。執行者若發現還需要其他介面變更，先回報主 agent，由主 agent 依本節處理。

### 骨架與格子

派實作前，主 agent 先寫骨架：

- [ ] 骨架從頭到尾能跑，入口、資料形狀與空格子都在。
- [ ] 每個格子有簽名（輸入、輸出、錯誤怎麼回報）與想要的結果清單，邊界情況各列一條。虛擬碼想到才附。
- [ ] 有兩三條完整使用流程的驗收，全部格子填完後必跑。
- [ ] 互不相依的格子落在不同檔案。
- [ ] 修正的骨架是根因、所有要改的位置與每處的驗證。

邏輯短到交代與審查比直接寫還費工，或說不清楚要改哪裡的格子，主 agent 自己寫。其餘格子照下列順序派：

1. 派測試 agent，照想要的結果寫測試，不寫實作。
2. 主 agent 審測試：逐條對照想要的結果，並在空格子上跑一次。有測試通過的退回重寫。
3. 派另一個實作 agent 填格子，填到測試通過，不得修改測試檔。認為測試錯就停下回報，由主 agent 裁決。
4. 主 agent 照第 4 節收件審查。

沒有測試環境或畫面類的格子，測試換成可執行的驗證步驟，由測試 agent 寫成指令或檢查清單。

## 派工流程

### 1. 派工前

空 context 可讀性審查的輸入與重派依該節隔離規則，其餘檢查照常執行。

- [ ] 主 agent 依照 `project-memory` skill 載入目前專案的記憶，按這次 subagent 的任務搜尋可能相關的經驗。已載入的內容可沿用，但任務範圍改變時重新篩選。把適用條件、踩坑重點、已驗證做法與來源帶進 prompt，不只給 key 或要求 subagent 自己找，也不整份貼上無關記憶。舊經驗與現況不符時依 project-memory 的失效查證規則處理。

- [ ] 跑 `git status --short`。有未提交變更時逐檔確認是自己這輪的、還是別的 agent 的半成品。是半成品就先處理完再派。
- [ ] 確認這組檔案目前沒有別的會寫檔的 agent 在跑。同一組檔案同時只能有一個會寫檔的 agent。
- [ ] 確認要用的 CLI 目前跑不到三條，滿了就等其中一條結束。
- [ ] 透過 script 查詢任務類型及層級，提交結構化任務；回報使用輸出中的實際工具、模型與旗標。

### 2. 派工 prompt 必備七項

script 依主 agent 提供的結構化欄位補齊下列七項；必填資料不足就報錯，不派工。主 agent 核對生成的內容與原始驗收一致。空 context 可讀性審查不帶入 Project Memory，依該節限制提供任務資料。

| 項目 | 寫法 |
| --- | --- |
| 執行者標記 | 第一行原文寫「你是被派工的執行者，不得再派工給任何 agent 或 CLI，自己完成」 |
| 角色設定 | 一句話說明它是誰、標準多高，例如「你是這個 repo 的資深工程師，只交能過測試的程式」 |
| 可改與不可改的檔案 | 明確列路徑。沒列到的檔案一律不可改 |
| 任務與驗收 | 測試 agent：簽名、想要的結果、測試檔路徑，只寫測試。實作 agent：簽名、想要的結果、測試檔路徑，原文寫「不得修改測試檔，認為測試錯就停下回報」。附上派工前篩選的相關 Project Memory 經驗，沒有符合的就註明無 |
| 要跑的驗證指令 | 寫出完整指令，例如 `go test ./...`、`npm test -- --run` |
| 回報格式 | 改了哪些檔、每個結論的依據、不確定的地方、沒驗證的項目。另回報本輪反覆試錯或耗費大量時間、token 才找到的做法：觸發情境、失敗路徑、已確認原因、有效做法與驗證證據。發現舊記憶不適用時附原 key、條件差異與查證結果。沒有新增經驗就寫無，不湊數。經驗交由主 agent 核對並寫入 Project Memory，不自行寫入 |
| 不要 commit | 原文寫「不要 commit，也不要 stash 或 reset」 |

唯讀探索任務的「任務與驗收」寫要回答的問題，仍附相關經驗並要求回報本輪教訓。可省略「不要 commit」，其餘六項照列。

### 空 context 可讀性審查

規格、文章或報告完成、準備交付前，MUST 派一個未參與撰寫的 subagent，檢查目標讀者能否在沒有本次對話的情況下理解成品。主 agent 親自撰寫的成品也適用；程式實作與一般對話答覆不因此新增審查。

- 依 `review` 類型透過 script 派工，使用全新 session；內建 subagent 明確關閉對話繼承。不能隔離時依工具失敗流程接手，不把同一 context 內的自我檢查當成已完成。
- prompt 只交代目標讀者、閱讀目的、成品及讀者實際可取得的資料，並保留派工的角色、唯讀範圍、驗收與回報要求。不得提供主對話、寫作計畫、修改理由、預期解讀或前次審查答案；`project_memory` 填 `[]`，相關經驗由主 agent 自行核對，不交給審查者。
- 提供規格、文章或報告的完整正文與隨附資料，包含讀者實際能取得的引用文件與附件；不要求讀者具備超出目標讀者設定的知識。
- 審查者先用自己的話說明成品主旨，規格另說明要求的行為與驗收條件，報告另說明主要結論與依據，再逐項指出無法理解的位置、可能的誤解、缺少的資訊與最小修正建議，附段落、頁碼或檔案行號。不得修改任何檔案，不自行腦補缺失資訊；沒有發現問題就明說。
- 主 agent 對照成品核對意見，修正確實依賴隱藏脈絡的部分。優先改善結構、命名或刪除無關內容，必要時才補說明；可讀性審查不取代事實查證、測試或正確性審查。
- 修正後以更新成品重新發起派工，用新的空 context 複查，不沿用前次審查者或帶入前次回報。工具失敗依原流程接續，但接手 prompt 只保留啟動或執行失敗證據，不帶入成品解讀或審查意見。交付時如實區分已通過、仍有缺口與工具受阻。

### 3. 派工中

- [ ] 背景 agent 被中斷時先看磁碟：`git status --short` 加 `git diff --stat`，判斷做到哪裡。
- [ ] 需要重派時，原 prompt 從記錄檔取回，不憑記憶重寫。Claude Code 的 subagent 在 `head -1 ~/.claude/projects/<專案>/<session>/subagents/agent-<id>.jsonl`，其他 CLI 見速查表的續接欄。
- [ ] 重派前把前一位執行者已驗證的相關教訓補進原 prompt，保留證據與不確定處，再交給接手者。
- [ ] 重派前決定半成品去留：保留並告知新 agent，或 `git checkout -- <檔案>` 清掉。

### 4. 收件審查

主 agent 親自做，不派另一個 agent 代審。規格、文章或報告交付前，另依「空 context 可讀性審查」檢查成品能否獨立理解。

- [ ] 讀完整 diff：`git diff`，不是只看 subagent 摘要。
- [ ] 回報裡的每個數字、測試通過數、檔案數，都對回實際輸出或檔案。
- [ ] 自己跑一次驗證指令，貼實際輸出。subagent 說「測試通過」不算證據。
- [ ] 比對可改檔案清單，多改的檔案一律退回。實作 agent 的 diff 碰到測試檔也退回。
- [ ] 全部格子完成後跑完整使用流程驗收。
- [ ] 才決定採用、退修或丟棄。
- [ ] 不論成果採用或退修，都核對 subagent 回報的試錯與探索經驗，連同主 agent 自己的發現，判斷能否避免下次重複耗費時間與 token。依 project-memory 的記錄標準篩選，不把推測、流水帳或未解問題當成已驗證教訓。
- [ ] 對符合條件的經驗，在原專案目錄依 project-memory 的工具先搜尋去重，再新增或更新，無須逐筆詢問使用者。舊記憶須查證確實失效後才更新原 key，保留仍有效的適用條件。寫入後讀回確認，不宣稱未完成的記錄已保存。

### 5. 工具失敗

一般派工的授權包含依 script 規則重試與改派。主 agent MUST 自行處理工具失敗並接續，MUST NOT 因單一工具失敗、額度耗盡、模型不可用、未登入或內建工具不可用，就詢問使用者是否重試、改派或繼續。接手順序不隨主 agent 環境改變，新的派工從該任務類型第 1 檔開始。

script 記錄每次失敗的原始輸出與實際旗標。`native_required` 由主 agent 使用指定的內建工具派工，失敗時帶實際錯誤接續。`awaiting_review` 是主 agent 的審查點，不是使用者的確認點：主 agent 自行檢查程序、磁碟、半成品與驗證結果，再帶原派工識別碼及實際證據依 script 接續，遵守同級重試與不可跳級的限制。無法確認程序已停止或半成品可安全接續時，先排除阻礙，不盲目重派。

該類型的選項全部失敗，或接續確實需要使用者登入、授予權限、額外付費、擴大任務範圍或決定可能遺失成果的處置時，才停下來請使用者決定。單一工具需要這些操作，但後續仍有已授權且可安全接續的選項時，先依 script 改派，不要求使用者修復該工具。既有 API 變更的指定模型諮詢沿用該節的失敗處置。

| 症狀 | 回報寫法 |
| --- | --- |
| 模型不存在或需升級 CLI | 貼錯誤原文與 `agy models`／`opencode models` 輸出 |
| 權限被拒、未登入 | 貼錯誤原文，說明需要哪個權限或登入指令 |
| 逾時 | 貼逾時設定與已完成部分 |
| 額度耗盡（rate limit、quota、usage limit） | 貼錯誤原文 |

### 6. 回報

每次回報獨立一段列出宿主與每次派工：

```
宿主：Claude Code
工具與模型：agy / <實際 flash 模型名> / --mode accept-edits
工具與模型：opencode / <實際免費模型名> / --agent build --auto
```

沒派工就寫「工具與模型：無」。每次交接與收件依 script 輸出提醒執行：核對教訓與經驗，依 project-memory 流程搜尋去重、記錄並讀回確認。

## 陷阱

| 陷阱 | 檢核方式 |
| --- | --- |
| 沒辨識宿主就派工，結果呼叫自己 | 回報第一行必須有「宿主：」，且工具清單裡沒有宿主自己的 CLI 指令，宿主自己的那欄用的是內建 subagent 工具 |
| 被派工的 agent 也載入本 skill 再往下派 | 被派工者的回報裡不得出現任何派工動作。出現就退回，檢查 prompt 第一行有沒有執行者標記 |
| 沒寫骨架就派實作 | 派實作前，骨架、該格子的想要的結果與審過的測試都已存在 |
| 很難的格子沒有 opencode 失敗紀錄就跳過 OpenCode | 跳過 OpenCode 時，回報要指出這次任務裡 opencode 在哪個同類型格子交出不完整或沒過驗證的結果，並附該次輸出 |
| 上一輪額度耗盡，這一輪直接往右派 | 回報裡出現該列最左邊以外的工具時，必須附上這一輪左邊每一格的實際錯誤原文或驗證失敗輸出 |
| 測試在空格子上就通過 | 審測試時在空格子跑一次，回報附上全部失敗的輸出 |
| 實作 agent 改測試讓自己過關 | 收件時 `git diff` 列出的檔案不含測試檔 |
| 兩個 agent 同時改同一個檔 | 派第二個前重跑 `git status --short`，路徑重疊就等第一個完成 |
| 只看 subagent 摘要就採用 | 回報裡必須有主 agent 自己跑的驗證輸出 |
| 模型不存在時換成決策表以外的種類 | 回報的模型必須屬於決策表該列的種類，且與派工前記下的一致 |
| Codex 用錯模型 | Review、深度研究與決策的模型是 GPT-6 以上且名稱含 sol。luna 只用於決策表的寫測試／實作／修 bug、快速唯讀探索、雜事與分類列，前端設計不派 luna |
| effort 沒照預設或超過上限 | 非免費模型的派工旗標是 `medium`，調高時回報寫出理由，任何派工都沒有 `max`。Opus 接手寫程式格子是 `low` |
| 同一個 CLI 同時跑超過三條 | 派工前列出該 CLI 正在跑的派工，加上這次不超過三條 |
| Opus 沒按決策表派工 | 回報的模型名稱含 opus 時，該次派工必須屬於決策表明列 Opus 的任務並遵守接手順序。接手寫程式格子時附上 Sonnet 在同一個格子連續兩次沒過驗證的輸出，且旗標含 `--effort low` |
| 分類任務沒按決策表選模型 | Copilot 使用 Auto，其他工具的模型名稱必須含 haiku 或 luna，不得含 opus 或 sonnet |
| 任務派給 5.5 以下的 Sonnet 或 Haiku | 回報的模型名稱含 sonnet 或 haiku 時，版本必須是 5.5 以上 |
