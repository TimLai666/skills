# CLI 速查表

五個 CLI 的常用旗標。CLI 更新後以各自 `--help` 為準並回報差異。Copilot 的詳細介面見 `copilot --help`、`copilot help permissions` 與 [官方指令參考](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)。

## 對照表

| 需求 | OpenCode | Antigravity（agy） | GitHub Copilot CLI | Codex | Claude Code |
| --- | --- | --- | --- | --- | --- |
| 非互動執行 | `opencode run --auto '<prompt>'` | `agy -p='<prompt>'`，`-p=` 放所有旗標之後 | `copilot --model auto --allow-all-tools --trust-folder -p '<prompt>'` | `codex exec --approve-for-me '<prompt>'` | `claude -p --permission-mode auto '<prompt>'` |
| 指定模型 | `-m <provider>/<name>` | `--model <name>` | 固定 `--model auto`，不指定具體模型 | `-m <name>` | `--model <name>` |
| 推理強度 | `--variant <level>`，依 provider | `--effort low\|medium\|high`，Gemini 改選模型名結尾 `-low`／`-medium`／`-high` 的版本 | 交給 Auto，不指定 | `-c model_reasoning_effort=high`，無獨立旗標 | `--effort low\|medium\|high\|xhigh\|max` |
| 列模型 | `opencode models` | `agy models` | 固定 Auto，不挑模型 | 無指令 | 無指令，用 `opus`、`sonnet`、`haiku` 別名 |
| 可寫檔 | `--agent build --auto` | `--mode accept-edits` | `--allow-all-tools`，可改範圍依 prompt | `--approve-for-me` | `--permission-mode auto` |
| 唯讀任務 | 沿用上述模式，prompt 寫「不得修改任何檔案」 | 同左 | 同左 | 同左 | 同左 |
| 結構化輸出 | `--format json` | `--output-format json` | `--output-format json`（JSONL） | `--json`，或 `-o <file>` 只寫最後一則訊息 | `--output-format json` |
| 續接上一次 | `-c`、`-s <id>` | `--continue`、`--conversation <id>` | `--continue`、`--resume <id>` | `codex exec resume --last` | `--continue`、`--resume <id>` |
| 逾時 | 無 | `--print-timeout 5m` | 由呼叫端設定逾時 | 無 | 無，用 Bash 的 timeout 參數 |
| 指定工作目錄 | `--dir <dir>` | 先 `cd`，額外工作區用 `--add-dir <dir>` | `-C <dir>` | `-C <dir>` | 先 `cd` |
| 自我辨識 | `OPENCODE` | `ANTIGRAVITY_AGENT` | 依當前宿主資訊，不以登入或模型設定變數判定 | `CODEX_THREAD_ID` | `CLAUDECODE` |

## 背景執行

五個都不需要各自的背景機制。從 Claude Code 派工時用 Bash 的 `run_in_background`，完成會自動叫醒主 agent。從其他宿主派工時用 shell 的 `&` 加輸出導向到檔案，再輪詢檔案。

## 常見錯誤原文

| 錯誤片段 | 意思 | 處置 |
| --- | --- | --- |
| `requires a newer version of Codex` | 預設模型比 CLI 新 | 轉決策表該列右邊的下一個，回報時附錯誤原文，建議使用者升級 |
| `-p took "--mode" as its prompt` | agy 的 `-p` 沒用 `=` 接 prompt | 改成 `-p='...'` 並放最後 |
| `Model metadata for ... not found` | Codex 找不到模型描述 | 轉決策表該列右邊的下一個，回報時附 `-m` 實際值 |
