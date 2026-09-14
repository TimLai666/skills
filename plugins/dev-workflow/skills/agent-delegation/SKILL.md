---
name: agent-delegation
description: >-
  Fixed rules for handing work to subagents or external coding CLIs. This skill
  MUST be loaded when the user mentions subagent、分工、派工、antigravity、agy、
  opencode、codex, or the Claude Code Agent tool, and MUST be loaded before the
  main agent dispatches any task to another agent, even when the task looks
  small. It SHOULD be loaded when the user asks who should write the code or
  which model to use. The main agent MUST NOT write production code itself while
  a delegation path in the decision table is available, and MUST NOT use Codex
  unless the user asks for it in the current task. An agent whose own prompt
  marks it as the dispatched worker MUST NOT apply this skill and MUST NOT
  delegate further.
metadata:
  version: "1.1.0"
---

# Agent 派工規範

## Overview

主 agent 負責指揮、寫契約與 ticket、審查、驗證、提交，不自己寫程式。程式、探索與雜事依下表派給對應工具與模型。每條規則都寫成可檢核的形式，派工前後各對一次。

### 適用對象

只有直接和使用者對話的主 agent 適用。載入後先做一個判斷：

- 自己的任務 prompt 含「你是被派工的執行者」這句，或同時含可改檔案清單與「不要 commit」，就是被派工者。被派工者立刻停用本 skill，自己動手做完 prompt 交代的事，不得再呼叫 Agent 工具、agy、opencode、codex。
- 兩者都沒有，才是主 agent，往下走。

派工者這邊的義務是把標記寫進 prompt，見第 2 節第一項。

## 決策表

| 任務類型 | 工具 | 模型 | 指令樣板 |
| --- | --- | --- | --- |
| 寫程式、改程式、修 bug | agy 的 Claude（優先） | Claude Opus 系列最新版 | `agy -p --model <opus-model> --mode accept-edits "<prompt>"` |
| 寫程式，agy 不可用時 | Claude Code Agent 工具 | Opus 系列 | Agent 工具，`subagent_type: general-purpose`，`model: opus` |
| 寫程式，使用者當次指定 Codex | codex | 使用者指定，未指定用預設 | `codex exec -m <model> "<prompt>"` |
| 快速唯讀探索、找檔案、問「X 在哪」 | agy 的 Gemini Flash | Gemini Flash 系列最新版 | `agy -p --model <flash-model> --mode plan "<prompt>"` |
| 雜事：機械性文件段落、證據整理、大量套版改寫 | opencode | 免費模型，推薦 `opencode/big-pickle` | `opencode run -m <free-model> "<prompt>"` |
| 主 agent 自己做 | 無 | 無 | 寫契約、寫 ticket、讀 diff、跑測試、commit |

- 表中只寫模型種類，不寫死名稱。派工前先跑 `agy models` 或 `opencode models`，從輸出挑該種類的最新版填進 `<opus-model>`、`<flash-model>`、`<free-model>`。
- opencode 只能用名稱含 `-free` 或列在免費清單的模型，`opencode models | grep opencode/` 查得到才算。
- Codex 沒有使用者當次指示就不用，前一輪的指示不延續到這一輪。

## 派工流程

### 1. 派工前

- [ ] 跑 `git status --short`。有未提交變更時，逐檔確認是自己這輪的、還是別的 agent 的半成品。是半成品就先處理完再派。
- [ ] 確認這組檔案目前沒有別的會寫檔的 agent 在跑。同一組檔案同時只能有一個會寫檔的 agent。
- [ ] 依決策表選好工具與模型，記下實際要用的旗標，回報時要列。

### 2. 派工 prompt 必備七項

少一項就不送。

| 項目 | 寫法 |
| --- | --- |
| 執行者標記 | 第一行原文寫「你是被派工的執行者，不得再派工給任何 agent 或 CLI，自己完成」 |
| 角色設定 | 一句話說明它是誰、標準多高，例如「你是這個 repo 的資深工程師，只交能過測試的程式」 |
| 可改與不可改的檔案 | 明確列路徑。沒列到的檔案一律不可改 |
| 先寫失敗測試再實作 | 要求先提交會失敗的測試，再寫實作讓它過，並回報兩個階段的測試輸出 |
| 要跑的驗證指令 | 寫出完整指令，例如 `go test ./...`、`npm test -- --run` |
| 回報格式 | 改了哪些檔、每個結論的依據、不確定的地方、沒驗證的項目 |
| 不要 commit | 原文寫「不要 commit，也不要 stash 或 reset」 |

唯讀探索任務可省略「先寫失敗測試」與「不要 commit」，其餘五項照列。

### 3. 派工中

- [ ] 背景 agent 被中斷時，先看磁碟：`git status --short` 加 `git diff --stat`，判斷做到哪裡。
- [ ] 需要重派時，原 prompt 從該 agent 的記錄檔第一行取回：`head -1 ~/.claude/projects/<專案>/<session>/subagents/agent-<id>.jsonl`。不要憑記憶重寫。
- [ ] 重派前把上一次的半成品決定好：保留並告知新 agent，或 `git checkout -- <檔案>` 清掉。

### 4. 收件審查

主 agent 親自做，不派另一個 agent 代審。

- [ ] 讀完整 diff：`git diff`，不是只看 subagent 的摘要。
- [ ] subagent 回報裡的每個數字、測試通過數、檔案數，都對回實際輸出或檔案。
- [ ] 自己跑一次驗證指令，貼實際輸出。subagent 說「測試通過」不算證據。
- [ ] 比對可改檔案清單，多改的檔案一律退回。
- [ ] 才決定採用、退修或丟棄。

### 5. 工具失敗

wrapper 或 CLI 失敗時照實回報錯誤原文，並停下來讓使用者決定。不要默默換工具。

| 症狀 | 回報寫法 |
| --- | --- |
| 模型不存在 | 貼 `agy models` 或 `opencode models` 輸出，說明該種類目前沒有可用模型 |
| 權限被拒 | 貼錯誤原文，說明需要哪個權限 |
| 未登入 | 貼錯誤原文，請使用者執行對應登入指令 |
| 逾時 | 貼逾時設定與已完成部分，問要不要延長或拆小 |

### 6. 回報

每次回報獨立一段列出：

```
工具與模型：agy / <實際用的 opus 模型名> / --mode accept-edits
工具與模型：opencode / <實際用的免費模型名> / 無額外旗標
```

沒派工就寫「工具與模型：無」。

## 陷阱

| 陷阱 | 檢核方式 |
| --- | --- |
| 主 agent 覺得改動很小就自己寫 | 改動涉及任何 `.go`、`.ts`、`.py` 等程式檔就算寫程式，查決策表 |
| 兩個 agent 同時改同一個檔 | 派第二個前重跑 `git status --short`，有重疊路徑就等第一個完成 |
| 派工 prompt 漏掉「不要 commit」或執行者標記 | 送出前對七項清單，七項齊才送 |
| 被派工的 agent 也載入本 skill 再往下派 | 被派工者的回報裡不得出現任何派工動作。出現就退回，並檢查派工 prompt 第一行有沒有執行者標記 |
| 只看 subagent 摘要就採用 | 回報裡必須有主 agent 自己跑的驗證輸出 |
| 模型不存在時自動換成別的種類 | 回報裡的模型必須屬於決策表指定的種類，且與派工前記下的一致 |
| Codex 沒被點名卻用了 | 回報的工具清單裡出現 codex 時，要能指出使用者這一輪的哪句話要求它 |
| opencode 用到付費模型 | 回報的模型名稱要在免費清單內 |
| 憑記憶重寫中斷 agent 的 prompt | 重派前貼出 `head -1` 取回的原文 |

## Suggested Prompt

派工 prompt 骨架，照填即可：

```
你是被派工的執行者，不得再派工給任何 agent 或 CLI，自己完成。
你是 <repo> 的資深工程師，只交能過測試的程式。
可改：<路徑清單>。不可改：其餘所有檔案。
步驟：先寫會失敗的測試並貼輸出，再實作讓它過並貼輸出。
驗證指令：<完整指令>。
回報：改了哪些檔、每個結論的依據、不確定的地方、沒驗證的項目。
不要 commit，也不要 stash 或 reset。
```
