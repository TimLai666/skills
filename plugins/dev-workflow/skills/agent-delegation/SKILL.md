---
name: agent-delegation
description: >-
  Fixed rules for handing work to subagents or external coding CLIs, usable from
  any host (Claude Code, Codex, Antigravity, OpenCode). This skill MUST be loaded
  when the user mentions subagent、分工、派工、antigravity、agy、opencode、codex,
  or the Claude Code Agent tool, and MUST be loaded before the main agent
  dispatches any task to another agent, even when the task looks small. It
  SHOULD be loaded when the user asks who should write the code or which model
  to use. The main agent MUST NOT write production code itself while a
  delegation path in the decision table is available, MUST NOT dispatch to the
  CLI it is itself running in, MUST NOT skip the cheapest tool because it failed
  in an earlier turn, and MUST NOT use Codex as a worker unless the user asks
  for it in the current task. An agent whose own prompt marks it as
  the dispatched worker MUST NOT apply this skill and MUST NOT delegate further.
metadata:
  version: "1.3.0"
---

# Agent 派工規範

## Overview

主 agent 負責切任務、寫契約與 ticket、審查、驗證、提交，不自己寫程式。成本原則：Antigravity（agy）與 OpenCode 最便宜，是主力。實作交給 OpenCode 的免費模型，前端設計與探索交給 agy 的 Gemini，品質靠主 agent 把任務切細加親自審查來守，弱模型拿到的每張 ticket 都小到沒有跑歪的空間。Claude Opus 與 Codex 留給 review。任何 CLI 都能當主 agent，所以派工前先辨識自己是誰。各 CLI 的旗標見 [references/cli-cheatsheet.md](references/cli-cheatsheet.md)。

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

依成本由低到高排。第一選擇失敗或被禁才往右走。

| 任務類型 | 第一選擇 | 備案 | 模型種類 |
| --- | --- | --- | --- |
| 實作：寫程式、改程式、修 bug | `opencode run --agent build -m <free-model> '<prompt>'` | 同一張 ticket 連續兩次沒過驗證，改派 agy 的 Claude：`agy --model <opus-model> --mode accept-edits -p='<prompt>'` | 免費模型，推薦 `opencode/big-pickle` → Claude Opus 系列 |
| 前端設計、版面、樣式 | agy 的 Gemini：`agy --model <gemini-model> --mode accept-edits -p='<prompt>'` | OpenCode 免費模型 | Gemini 系列最新版 |
| 快速唯讀探索、找檔案、問「X 在哪」 | agy 的 Gemini Flash：`agy --model <flash-model> --mode plan -p='<prompt>'` | 宿主是 Claude Code 用 Agent 工具 `Explore`；其他宿主用 `opencode run --agent plan -m <free-model> '<prompt>'` | Gemini Flash 系列最新版 |
| 雜事：機械性文件段落、證據整理、大量套版改寫 | `opencode run --agent build -m <free-model> '<prompt>'` | agy 的 Gemini Flash | 免費模型 |
| Review：審 diff、找漏洞、對契約 | 使用者當次指定 Codex 時 `codex exec -s read-only -m <model> '<prompt>'`，否則 agy 的 Claude：`agy --model <opus-model> --mode plan -p='<prompt>'` | 宿主是 Claude Code 用 Agent 工具（`model: opus`）；其他宿主用 `claude -p --model opus '<prompt>'` | Codex 使用者指定 > Claude Opus 系列 |
| 主 agent 自己做 | 切 ticket、寫契約、讀 diff、跑測試、commit | | |

- 表中只寫模型種類。派工前先跑 `agy models` 或 `opencode models`，挑該種類最新版填進佔位符。
- opencode 只能用免費模型：`opencode models | grep opencode/` 查得到才算。
- Codex 當工人要有使用者這一輪的指示，前一輪不延續。Codex 當主 agent 不受此限。
- 不派給自己所在的 CLI。同一個模型不同 CLI 可以。
- 每輪都照表從第一選擇派起。上一輪額度耗盡、逾時或失敗，不代表這一輪還是，實際失敗了才走備案。

### 切 ticket 的標準

派給免費模型的實作 ticket 每張都要符合，不符合就再切：

- [ ] 只改一組檔案，路徑都列在可改清單。
- [ ] 只驗一個行為，只有一個驗證指令。
- [ ] 預期 diff 不超過約 200 行。超過就拆成兩張，先派第一張。
- [ ] 契約寫到 subagent 不必自己做設計決定：函式簽名、輸入輸出、錯誤處理方式都給定。

## 派工流程

### 1. 派工前

- [ ] 跑 `git status --short`。有未提交變更時逐檔確認是自己這輪的、還是別的 agent 的半成品。是半成品就先處理完再派。
- [ ] 確認這組檔案目前沒有別的會寫檔的 agent 在跑。同一組檔案同時只能有一個會寫檔的 agent。
- [ ] 依決策表選好工具與模型，記下實際旗標，回報時要列。

### 2. 派工 prompt 必備七項

少一項就不送。

| 項目 | 寫法 |
| --- | --- |
| 執行者標記 | 第一行原文寫「你是被派工的執行者，不得再派工給任何 agent 或 CLI，自己完成」 |
| 角色設定 | 一句話說明它是誰、標準多高，例如「你是這個 repo 的資深工程師，只交能過測試的程式」 |
| 可改與不可改的檔案 | 明確列路徑。沒列到的檔案一律不可改 |
| 先寫失敗測試再實作 | 先提交會失敗的測試，再寫實作讓它過，回報兩個階段的測試輸出 |
| 要跑的驗證指令 | 寫出完整指令，例如 `go test ./...`、`npm test -- --run` |
| 回報格式 | 改了哪些檔、每個結論的依據、不確定的地方、沒驗證的項目 |
| 不要 commit | 原文寫「不要 commit，也不要 stash 或 reset」 |

唯讀探索任務可省略「先寫失敗測試」與「不要 commit」，其餘五項照列。

### 3. 派工中

- [ ] 背景 agent 被中斷時先看磁碟：`git status --short` 加 `git diff --stat`，判斷做到哪裡。
- [ ] 需要重派時，原 prompt 從記錄檔取回，不憑記憶重寫。Claude Code 的 subagent 在 `head -1 ~/.claude/projects/<專案>/<session>/subagents/agent-<id>.jsonl`，其他 CLI 見速查表的續接欄。
- [ ] 重派前決定半成品去留：保留並告知新 agent，或 `git checkout -- <檔案>` 清掉。

### 4. 收件審查

主 agent 親自做，不派另一個 agent 代審。

- [ ] 讀完整 diff：`git diff`，不是只看 subagent 摘要。
- [ ] 回報裡的每個數字、測試通過數、檔案數，都對回實際輸出或檔案。
- [ ] 自己跑一次驗證指令，貼實際輸出。subagent 說「測試通過」不算證據。
- [ ] 比對可改檔案清單，多改的檔案一律退回。
- [ ] 才決定採用、退修或丟棄。

### 5. 工具失敗

wrapper 或 CLI 失敗時照實回報錯誤原文，停下來讓使用者決定。不要默默換工具。

| 症狀 | 回報寫法 |
| --- | --- |
| 模型不存在或需升級 CLI | 貼錯誤原文與 `agy models`／`opencode models` 輸出 |
| 權限被拒、未登入 | 貼錯誤原文，說明需要哪個權限或登入指令 |
| 逾時 | 貼逾時設定與已完成部分，問要不要延長或拆小 |
| 額度耗盡（rate limit、quota、usage limit） | 貼錯誤原文，這一輪走備案並在回報註明。下一輪仍從第一選擇派起 |

### 6. 回報

每次回報獨立一段列出宿主與每次派工：

```
宿主：Claude Code
工具與模型：agy / <實際 opus 模型名> / --mode accept-edits
工具與模型：opencode / <實際免費模型名> / --agent build
```

沒派工就寫「工具與模型：無」。派工 prompt 骨架直接照第 2 節七項依序寫，每項一行。

## 陷阱

| 陷阱 | 檢核方式 |
| --- | --- |
| 沒辨識宿主就派工，結果呼叫自己 | 回報第一行必須有「宿主：」，且工具清單裡沒有宿主自己的 CLI |
| 被派工的 agent 也載入本 skill 再往下派 | 被派工者的回報裡不得出現任何派工動作。出現就退回，檢查 prompt 第一行有沒有執行者標記 |
| 主 agent 覺得改動很小就自己寫 | 動到任何程式檔就算寫程式，查決策表 |
| 上一輪額度耗盡，這一輪直接走備案 | 回報裡出現備案工具時，必須附上這一輪第一選擇的實際錯誤原文 |
| ticket 太大丟給免費模型 | 派出前對切 ticket 四項，不符合就拆 |
| 兩個 agent 同時改同一個檔 | 派第二個前重跑 `git status --short`，路徑重疊就等第一個完成 |
| 只看 subagent 摘要就採用 | 回報裡必須有主 agent 自己跑的驗證輸出 |
| 模型不存在時自動換成別的種類 | 回報的模型必須屬於決策表指定的種類，且與派工前記下的一致 |
| Codex 沒被點名卻當工人 | 回報的工具清單裡有 codex 時，要能指出使用者這一輪哪句話要求它 |
