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
  in an earlier turn, and MUST NOT use Codex as a worker unless the user asks
  for it in the current task. An agent whose own prompt marks it as
  the dispatched worker MUST NOT apply this skill and MUST NOT delegate further.
metadata:
  version: "2.6.0"
---

# Agent 派工規範

## Overview

主 agent 是強模型，負責寫骨架與每個格子的想要的結果、審查、驗證、提交。骨架鎖住範圍，弱模型照規格寫測試或填實作。成本原則：Antigravity（agy）與 OpenCode 最便宜，是主力。測試與實作交給 OpenCode 的免費模型，前端設計與探索交給 agy 的 Gemini。Claude Opus 只用來寫規則、架構、review 與接手 Sonnet 也寫不出來的格子，使用者指定時 review 改用 Codex。任何 CLI 都能當主 agent，所以派工前先辨識自己是誰。各 CLI 的旗標見 [references/cli-cheatsheet.md](references/cli-cheatsheet.md)。

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
| 寫測試、填格子實作、照清單修 bug | `opencode run --agent build -m <free-model> '<prompt>'` | 同一個格子在同一級連續兩次沒過驗證就往下一級。先派 Haiku，再派 Sonnet：宿主是 Claude Code 用 Agent 工具（`model: haiku`／`model: sonnet`），其他宿主用 `claude -p --model haiku --permission-mode acceptEdits '<prompt>'`，Sonnet 把 `haiku` 換成 `sonnet`。最後派低 effort 的 Opus：`agy --model <opus-model> --effort low --mode accept-edits -p='<prompt>'`，失敗再改宿主是 Claude Code 用 Agent 工具（`model: opus`），其他宿主用 `claude -p --model opus --effort low --permission-mode acceptEdits '<prompt>'` | 免費模型，推薦 `opencode/big-pickle` → Haiku 5.5 以上 → Sonnet 5.5 以上 → Claude Opus 系列加低 effort |
| 前端設計、版面、樣式 | agy 的 Gemini Flash：`agy --model <flash-model> --mode accept-edits -p='<prompt>'` | 使用者當次指定 Codex 時用 Codex，否則派 Sonnet：宿主是 Claude Code 用 Agent 工具（`model: sonnet`），其他宿主用 `claude -p --model sonnet --permission-mode acceptEdits '<prompt>'` | Gemini Flash 系列最新版 → Codex 或 Sonnet 5.5 以上 |
| 快速唯讀探索、找檔案、問「X 在哪」 | agy 的 Gemini Flash：`agy --model <flash-model> --mode plan -p='<prompt>'` | 宿主是 Claude Code 用 Agent 工具 `Explore`（`model: haiku`）；其他宿主用 `opencode run --agent plan -m <free-model> '<prompt>'` | Gemini Flash 系列最新版 → Haiku 5.5 以上或免費模型 |
| 雜事：機械性文件段落、證據整理、大量套版改寫 | `opencode run --agent build -m <free-model> '<prompt>'` | 先派 agy 的 Gemini Flash。再派 Haiku：宿主是 Claude Code 用 Agent 工具（`model: haiku`），其他宿主用 `claude -p --model haiku --permission-mode acceptEdits '<prompt>'` | 免費模型 → Gemini Flash 系列最新版 → Haiku 5.5 以上 |
| Review：審 diff、找漏洞、對契約 | 使用者當次指定 Codex 時 `codex exec -s read-only -m <luna-model> -c model_reasoning_effort=high '<prompt>'`，否則 agy 的 Claude：`agy --model <opus-model> --mode plan -p='<prompt>'` | 宿主是 Claude Code 用 Agent 工具（`model: opus`）；其他宿主用 `claude -p --model opus '<prompt>'` | Codex luna 系列 > Claude Opus 系列 |
| 寫規則與架構：skill、prompt 與規則檔條文，模組邊界、資料模型等架構決策 | agy 的 Claude：`agy --model <opus-model> --mode accept-edits -p='<prompt>'` | 宿主是 Claude Code 用 Agent 工具（`model: opus`）；其他宿主用 `claude -p --model opus --permission-mode acceptEdits '<prompt>'` | Claude Opus 系列 |
| 主 agent 自己做 | 寫骨架與想要的結果、審測試、派出去不划算的格子、讀 diff、跑測試、commit | | |

- 表中只寫模型種類。派工前先跑 `agy models` 或 `opencode models`，挑該種類最新版填進佔位符。
- opencode 只能用免費模型：`opencode models | grep opencode/` 查得到才算。
- Codex 當工人要有使用者這一輪的指示，前一輪不延續，指定後 review 與實作都改由 Codex 做。只用名稱含 luna 的模型，effort 只能 `high` 或 `xhigh`，寫在 `-c model_reasoning_effort=`。Codex 當主 agent 不受指示限制。
- Haiku 只用 5.5 以上版本，用在唯讀探索、雜事與簡單的寫程式任務。
- Sonnet 只用 5.5 以上版本，用在中等偏低算力的任務與 Haiku 寫不出來的寫程式任務。其他中階算力任務也用 Sonnet。
- Opus 只用在寫規則、架構、review，以及 Sonnet 也沒過驗證的寫程式格子，其他任務一律不派 Opus。接手寫程式格子時 agy 與 `claude -p` 都加 `--effort low`，Agent 工具沒有 effort 參數就直接 `model: opus`。
- 不派給自己所在的 CLI。同一個模型不同 CLI 可以。
- 每輪都照表從第一選擇派起。上一輪額度耗盡、逾時或失敗，不代表這一輪還是，實際失敗了才走備案。
- 唯一例外：主 agent 判斷很難的寫程式格子，若這次任務裡 opencode 已在同類型的格子交出不完整或沒過驗證的結果，可以跳過免費模型直接從 Haiku 派起，其餘往下升級的規則不變。

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

wrapper 或 CLI 失敗時直接照決策表轉下一個備案，不停下來問使用者。錯誤原文在回報裡照實列出，不默默換工具。該列的選項全部失敗才停下來，讓使用者決定。下一輪仍從第一選擇派起。

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
工具與模型：opencode / <實際免費模型名> / --agent build
```

沒派工就寫「工具與模型：無」。派工 prompt 直接照第 2 節七項依序寫，每項一行。

## 陷阱

| 陷阱 | 檢核方式 |
| --- | --- |
| 沒辨識宿主就派工，結果呼叫自己 | 回報第一行必須有「宿主：」，且工具清單裡沒有宿主自己的 CLI |
| 被派工的 agent 也載入本 skill 再往下派 | 被派工者的回報裡不得出現任何派工動作。出現就退回，檢查 prompt 第一行有沒有執行者標記 |
| 沒寫骨架就派實作 | 派實作前，骨架、該格子的想要的結果與審過的測試都已存在 |
| 很難的格子沒有 opencode 失敗紀錄就直接派 Haiku | 跳過免費模型時，回報要指出這次任務裡 opencode 在哪個同類型格子交出不完整或沒過驗證的結果，並附該次輸出 |
| 上一輪額度耗盡，這一輪直接走備案 | 回報裡出現備案工具時，必須附上這一輪前一級的實際錯誤原文或驗證失敗輸出 |
| 測試在空格子上就通過 | 審測試時在空格子跑一次，回報附上全部失敗的輸出 |
| 實作 agent 改測試讓自己過關 | 收件時 `git diff` 列出的檔案不含測試檔 |
| 兩個 agent 同時改同一個檔 | 派第二個前重跑 `git status --short`，路徑重疊就等第一個完成 |
| 只看 subagent 摘要就採用 | 回報裡必須有主 agent 自己跑的驗證輸出 |
| 模型不存在時換成決策表以外的種類 | 回報的模型必須屬於決策表該列第一選擇或備案的種類，且與派工前記下的一致 |
| Codex 沒被點名卻當工人，或用了非 luna 模型、effort 低於 high | 回報的工具清單裡有 codex 時，要能指出使用者這一輪哪句話要求它，且旗標含 luna 與 `model_reasoning_effort=high` 或 `xhigh` |
| Opus 用在寫規則、架構與 review 以外的任務 | 回報的模型名稱含 opus 時，該次派工必須屬於決策表「Review」或「寫規則與架構」那一列，或是附上 Sonnet 在同一個格子連續兩次沒過驗證的輸出，且旗標含 `--effort low` |
| 任務派給 5.5 以下的 Sonnet 或 Haiku | 回報的模型名稱含 sonnet 或 haiku 時，版本必須是 5.5 以上 |
