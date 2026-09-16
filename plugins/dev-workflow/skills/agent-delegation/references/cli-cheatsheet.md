# CLI 速查表

四個 CLI 的常用旗標。每欄都以本機 `--help` 或實際執行確認過，CLI 更新後若旗標改名，以 `--help` 為準並回報差異。

## 對照表

| 需求 | Claude Code | Codex | Antigravity（agy） | OpenCode |
| --- | --- | --- | --- | --- |
| 非互動執行 | `claude -p '<prompt>'` | `codex exec '<prompt>'` | `agy -p='<prompt>'`，`-p=` 放所有旗標之後 | `opencode run '<prompt>'` |
| 指定模型 | `--model <name>` | `-m <name>` | `--model <name>` | `-m <provider>/<name>` |
| 推理強度 | `--effort low|medium|high|xhigh|max` | `-c model_reasoning_effort=high`，無獨立旗標 | `--effort low|medium|high` | `--variant <level>`，依 provider |
| 列模型 | 無指令，用 `opus`、`sonnet`、`haiku` 別名 | 無指令 | `agy models` | `opencode models` |
| 可寫檔 | `--permission-mode acceptEdits` | `-s workspace-write` | `--mode accept-edits` | `--agent build` |
| 唯讀 | `--allowedTools Read,Grep,Glob` | `-s read-only` | `--mode plan` | `--agent plan`（模型層約束，不是硬擋） |
| 結構化輸出 | `--output-format json` | `--json`，或 `-o <file>` 只寫最後一則訊息 | `--output-format json` | `--format json` |
| 續接上一次 | `--continue`、`--resume <id>` | `codex exec resume --last` | `--continue`、`--conversation <id>` | `-c`、`-s <id>` |
| 逾時 | 無，用 Bash 的 timeout 參數 | 無 | `--print-timeout 5m` | 無 |
| 指定工作目錄 | 先 `cd` | `-C <dir>` | `--add-dir <dir>` | `--dir <dir>` |
| 自我辨識環境變數 | `CLAUDECODE` | `CODEX_THREAD_ID` | `ANTIGRAVITY_AGENT` | `OPENCODE` |

## 背景執行

四個都不需要各自的背景機制。從 Claude Code 派工時用 Bash 的 `run_in_background`，完成會自動叫醒主 agent。從其他宿主派工時用 shell 的 `&` 加輸出導向到檔案，再輪詢檔案。

## 常見錯誤原文

| 錯誤片段 | 意思 | 處置 |
| --- | --- | --- |
| `requires a newer version of Codex` | 預設模型比 CLI 新 | 回報，請使用者升級或用 `-m` 指定舊模型 |
| `-p took "--mode" as its prompt` | agy 的 `-p` 沒用 `=` 接 prompt | 改成 `-p='...'` 並放最後 |
| `Model metadata for ... not found` | Codex 找不到模型描述 | 回報，附 `-m` 實際值 |
