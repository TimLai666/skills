---
name: agent-delegation
description: >-
  Fixed rules for handing work to subagents or external coding CLIs, usable from
  any host (Claude Code, Codex, Antigravity, OpenCode). This skill MUST be loaded
  when the user mentions subagent、分工、派工、antigravity、agy、opencode、codex,
  or the Claude Code Agent tool, and MUST be loaded before the main agent
  dispatches any task to another agent, even when the task looks small. It
  SHOULD be loaded when the user asks who should write the code or which model
  to use. Before dispatching implementation, the main agent MUST write the
  skeleton and each slot's expected results itself, MUST NOT let the agent that
  fills a slot edit its tests, MUST NOT dispatch to the
  CLI it is itself running in, MUST NOT skip the cheapest tool because it failed
  in an earlier turn, and MUST try CLIs in the order opencode, agy, codex,
  claude. An agent whose own prompt marks it as
  the dispatched worker MUST NOT apply this skill and MUST NOT delegate further.
metadata:
  version: "2.15.0"
---

# Agent 派工規範

## Overview

主 agent 是強模型，負責寫骨架與每個格子的想要的結果、審查、驗證、提交。骨架鎖住範圍，弱模型照規格寫測試或填實作。成本原則：CLI 一律照 OpenCode → Antigravity（agy）→ Codex → Claude 的順序派。測試、實作與雜事先交給 OpenCode 的免費模型，前端設計交給 agy 的 Gemini。一般決策交給 Sonnet。Claude Opus 只用來寫規則、複雜架構、review 與接手 Sonnet 也寫不出來的格子。任何 CLI 都能當主 agent，所以派工前先辨識自己是誰。各 CLI 的旗標見 [references/cli-cheatsheet.md](references/cli-cheatsheet.md)。

## 0. 先辨識自己

載入後第一件事，跑：

```
env | grep -E '^(CLAUDECODE|CODEX_THREAD_ID|ANTIGRAVITY_AGENT|OPENCODE)='
```

| 有這個變數 | 你是 | 禁止派給 |
| --- | --- | --- |
| `CLAUDECODE` | Claude Code | `claude -p` |
| `CODEX_THREAD_ID` | Codex | `codex exec` |
| `ANTIGRAVITY_AGENT` | Antigravity（agy） | `agy` |
| `OPENCODE` | OpenCode | `opencode run` |

接著判斷角色：

- 任務 prompt 含「你是被派工的執行者」，或同時含可改檔案清單與「不要 commit」，就是被派工者。立刻停用本 skill，自己做完 prompt 交代的事，不得再呼叫任何 agent 或 CLI。
- 兩者都沒有，才是主 agent，往下走。

## 決策表

每列由左往右派，左邊的實際失敗或被禁才往右走。空格直接跳過，宿主自己的 CLI 改用內建 subagent 工具。

| 任務類型 | opencode | agy | codex | claude |
| --- | --- | --- | --- | --- |
| 寫測試、填格子實作、照清單修 bug | 免費模型，推薦 `opencode/big-pickle`，`--agent build --auto` | | luna，`--approve-for-me` | Haiku → Sonnet → Opus 加 `--effort low`，可寫檔 |
| 前端設計、版面、樣式 | | Gemini Flash，`--mode accept-edits` | luna，`--approve-for-me` | Sonnet，可寫檔 |
| 快速唯讀探索、找檔案、問「X 在哪」 | 免費模型，`--agent build --auto` | Gemini Flash，`--mode accept-edits` | | Haiku，宿主是 Claude Code 時用一般用途 Agent |
| 雜事：機械性文件段落、證據整理、大量套版改寫 | 免費模型，`--agent build --auto` | Gemini Flash，`--mode accept-edits` | | Haiku，可寫檔 |
| 分類：把資料、評論、issue 或檔案歸進類別、打標籤或編碼 | | | luna，`--approve-for-me` | Haiku，可寫檔 |
| Review：審 diff、找漏洞、對契約 | | Claude Opus，`--mode accept-edits` | GPT-6 以上的 sol，`--approve-for-me`，任務唯讀 | Opus，唯讀 |
| 深度研究（深度層，先由「快速唯讀探索」那列做廣度層，主 agent 統合）：摸清陌生系統怎麼運作（程式碼庫、服務、協定、環境），或找非常規的做法（hack 式繞法）完成一件事 | | | GPT-6 以上的 sol，`--approve-for-me` | Opus，可寫檔 |
| 決策：方案取捨、技術選型、只影響單一模組的設計 | | | | Sonnet，唯讀 |
| 寫規則與複雜架構：skill、prompt 與規則檔條文，以及跨多個模組、改資料模型或 API 契約的架構決策 | | Claude Opus，`--mode accept-edits` | | Opus，可寫檔 |

主 agent 自己做：寫骨架與想要的結果、審測試、派出去不划算的格子、讀 diff、跑測試、commit，以及統合深度研究的全部結果、做整體判斷。

各 CLI 的指令：

```
opencode run --auto --dir <project-dir> --agent build -m <free-model> '<prompt>'
agy --model <model> --mode accept-edits -p='<prompt>'
codex exec --approve-for-me -C <project-dir> -m <luna-model|sol-model> -c model_reasoning_effort=medium '<prompt>'
claude -p --model <haiku|sonnet|opus> --effort medium --permission-mode auto '<prompt>'
```

claude 那欄在宿主是 Claude Code 時改用 Agent 工具（`model: haiku`／`sonnet`／`opus`）。codex 那欄在宿主是 Codex 時改用 Codex 內建的 subagent 功能，模型種類與任務可改範圍照該列填寫。

- 外部 CLI 派工一律明確指定自動核准：OpenCode 加 `--auto`，Codex 加 `--approve-for-me`，Claude Code 加 `--permission-mode auto`，不改用 bypass。Claude Code 與 agy 從目標專案目錄啟動。
- 自動核准不擴大任務可改檔案清單。表中的「唯讀」只表示 prompt 必須明寫「不得修改任何檔案」；探索、審查與實作沿用相同執行模式，不另設 plan、read-only 沙盒或唯讀工具清單，也不選唯讀專用 agent。宿主內建 subagent 不套用外部 CLI 旗標，可改範圍同樣寫在 prompt。

- 表中只寫模型種類。派工前先跑 `agy models` 或 `opencode models`，挑該種類最新版填進佔位符。
- opencode 只能用免費模型：`opencode models | grep opencode/` 查得到才算。
- Codex 照表主動派。Review 與深度研究只用 GPT-6 以上、名稱含 sol 的模型，其他任務只用名稱含 luna 的模型。
- 深度研究分三層：
  1. 廣度層：照「快速唯讀探索」那列派（opencode、Gemini Flash、Haiku），每條負責一個範圍，掃描並回報發現與線索，附出處。回報當成線索，不當成事實。
  2. 深度層：主 agent 從線索挑出值得深挖的項目，每個項目派一個 sol，一次只專研一件事，prompt 只放那一件。回報系統結構、可行做法與每個結論的依據（檔案路徑、指令輸出、文件出處）。
  3. 統合層：主 agent 合併廣度與深度的全部結果，核對關鍵依據、前後對照、做出整體判斷，決定採用哪個做法並親自執行。sol 的結論不直接當成定論。
  廣度層沒挑出值得深挖的項目時，不派 sol。
- 深度研究的 agent 可實際試探系統，但可改檔案只列暫存目錄或沙盒，專案檔一律不可改。試探造成的副作用（建立的檔案、啟動的程序、改過的設定）一併寫進回報，由主 agent 決定保留或清掉。
- 非免費模型的 effort 預設 `medium`，主 agent 判斷任務需要時才調高，最高 `xhigh`。agy 的 Gemini 選模型名結尾是 `-medium` 的版本，agy 的 Claude 加 `--effort medium`，agy 最高只到 `high`。Agent 工具沒有 effort 參數，不用設。
- Haiku 與 Sonnet 只用 5.5 以上版本，所以 agy 的 Sonnet 4.6 不派。
- Haiku 用在唯讀探索、雜事、分類與簡單的寫程式任務。
- 任務同時符合分類與雜事或探索時，照分類那一列派。
- Sonnet 用在中等偏低算力的任務、一般決策與 Haiku 寫不出來的寫程式任務。其他中階算力任務也用 Sonnet。
- Opus 只用在寫規則、複雜架構、review，以及 Sonnet 也沒過驗證的寫程式格子，其他任務一律不派 Opus。接手寫程式格子時 `claude -p` 改用 `--effort low`。
- 寫程式那一列，同一個格子在同一級連續兩次沒過驗證才往下一級，claude 那欄依 Haiku、Sonnet、Opus 的順序升級。
- 同一個 CLI 同時最多跑三條，Claude Code 的 Agent 工具也算 claude。
- 不用宿主自己的 CLI 指令派工（`claude -p`、`codex exec` 等），改用宿主內建的 subagent 工具。同一個模型不同 CLI 可以。
- 每輪都照表從最左邊派起。上一輪額度耗盡、逾時或失敗，不代表這一輪還是，實際失敗了才往右走。
- 唯一例外：主 agent 判斷很難的寫程式格子，若這次任務裡 opencode 已在同類型的格子交出不完整或沒過驗證的結果，可以跳過免費模型直接從 luna 派起，其餘往下升級的規則不變。

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

- [ ] 跑 `git status --short`。有未提交變更時逐檔確認是自己這輪的、還是別的 agent 的半成品。是半成品就先處理完再派。
- [ ] 確認這組檔案目前沒有別的會寫檔的 agent 在跑。同一組檔案同時只能有一個會寫檔的 agent。
- [ ] 確認要用的 CLI 目前跑不到三條，滿了就等其中一條結束。
- [ ] 依決策表選好工具與模型，記下實際旗標，回報時要列。

### 2. 派工 prompt 必備七項

少一項就不送。

| 項目 | 寫法 |
| --- | --- |
| 執行者標記 | 第一行原文寫「你是被派工的執行者，不得再派工給任何 agent 或 CLI，自己完成」 |
| 角色設定 | 一句話說明它是誰、標準多高，例如「你是這個 repo 的資深工程師，只交能過測試的程式」 |
| 可改與不可改的檔案 | 明確列路徑。沒列到的檔案一律不可改 |
| 任務與驗收 | 測試 agent：簽名、想要的結果、測試檔路徑，只寫測試。實作 agent：簽名、想要的結果、測試檔路徑，原文寫「不得修改測試檔，認為測試錯就停下回報」 |
| 要跑的驗證指令 | 寫出完整指令，例如 `go test ./...`、`npm test -- --run` |
| 回報格式 | 改了哪些檔、每個結論的依據、不確定的地方、沒驗證的項目 |
| 不要 commit | 原文寫「不要 commit，也不要 stash 或 reset」 |

唯讀探索任務的「任務與驗收」寫要回答的問題，可省略「不要 commit」，其餘五項照列。

### 3. 派工中

- [ ] 背景 agent 被中斷時先看磁碟：`git status --short` 加 `git diff --stat`，判斷做到哪裡。
- [ ] 需要重派時，原 prompt 從記錄檔取回，不憑記憶重寫。Claude Code 的 subagent 在 `head -1 ~/.claude/projects/<專案>/<session>/subagents/agent-<id>.jsonl`，其他 CLI 見速查表的續接欄。
- [ ] 重派前決定半成品去留：保留並告知新 agent，或 `git checkout -- <檔案>` 清掉。

### 4. 收件審查

主 agent 親自做，不派另一個 agent 代審。

- [ ] 讀完整 diff：`git diff`，不是只看 subagent 摘要。
- [ ] 回報裡的每個數字、測試通過數、檔案數，都對回實際輸出或檔案。
- [ ] 自己跑一次驗證指令，貼實際輸出。subagent 說「測試通過」不算證據。
- [ ] 比對可改檔案清單，多改的檔案一律退回。實作 agent 的 diff 碰到測試檔也退回。
- [ ] 全部格子完成後跑完整使用流程驗收。
- [ ] 才決定採用、退修或丟棄。

### 5. 工具失敗

wrapper 或 CLI 失敗時直接照決策表往右轉下一個，不停下來問使用者。錯誤原文在回報裡照實列出，不默默換工具。該列的選項全部失敗才停下來，讓使用者決定。下一輪仍從最左邊派起。

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

沒派工就寫「工具與模型：無」。派工 prompt 直接照第 2 節七項依序寫，每項一行。

## 陷阱

| 陷阱 | 檢核方式 |
| --- | --- |
| 沒辨識宿主就派工，結果呼叫自己 | 回報第一行必須有「宿主：」，且工具清單裡沒有宿主自己的 CLI 指令，宿主自己的那欄用的是內建 subagent 工具 |
| 被派工的 agent 也載入本 skill 再往下派 | 被派工者的回報裡不得出現任何派工動作。出現就退回，檢查 prompt 第一行有沒有執行者標記 |
| 沒寫骨架就派實作 | 派實作前，骨架、該格子的想要的結果與審過的測試都已存在 |
| 很難的格子沒有 opencode 失敗紀錄就直接派 luna | 跳過免費模型時，回報要指出這次任務裡 opencode 在哪個同類型格子交出不完整或沒過驗證的結果，並附該次輸出 |
| 上一輪額度耗盡，這一輪直接往右派 | 回報裡出現該列最左邊以外的工具時，必須附上這一輪左邊每一格的實際錯誤原文或驗證失敗輸出 |
| 測試在空格子上就通過 | 審測試時在空格子跑一次，回報附上全部失敗的輸出 |
| 實作 agent 改測試讓自己過關 | 收件時 `git diff` 列出的檔案不含測試檔 |
| 兩個 agent 同時改同一個檔 | 派第二個前重跑 `git status --short`，路徑重疊就等第一個完成 |
| 只看 subagent 摘要就採用 | 回報裡必須有主 agent 自己跑的驗證輸出 |
| 模型不存在時換成決策表以外的種類 | 回報的模型必須屬於決策表該列的種類，且與派工前記下的一致 |
| Codex 用錯模型 | 回報的工具清單裡有 codex 時，review 與深度研究的 `-m` 是 GPT-6 以上且名稱含 sol，其他任務的 `-m` 名稱含 luna |
| effort 沒照預設或超過上限 | 非免費模型的派工旗標是 `medium`，調高時回報寫出理由，任何派工都沒有 `max`。Opus 接手寫程式格子是 `low` |
| 同一個 CLI 同時跑超過三條 | 派工前列出該 CLI 正在跑的派工，加上這次不超過三條 |
| Opus 用在寫規則、複雜架構與 review 以外的任務 | 回報的模型名稱含 opus 時，該次派工必須屬於決策表「Review」或「寫規則與複雜架構」那一列，或是附上 Sonnet 在同一個格子連續兩次沒過驗證的輸出，且旗標含 `--effort low` |
| 分類任務派給 luna 與 Haiku 以外的模型 | 分類任務的派工，回報的模型名稱必須含 haiku 或 luna，不得含 opus 或 sonnet |
| 任務派給 5.5 以下的 Sonnet 或 Haiku | 回報的模型名稱含 sonnet 或 haiku 時，版本必須是 5.5 以上 |
