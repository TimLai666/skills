# CLI 說明入口

一般派工先執行 `python3 <skill-dir>/scripts/dispatch.py` 查看總覽，再讀需要的子指令 `--help`。工具順序、層級數、模型限制與推理強度由 [policy.json](../scripts/policy.json) 提供。

| 工具 | 原生說明入口 |
| --- | --- |
| OpenCode | `opencode --help`、`opencode run --help`、`opencode models` |
| Antigravity（agy） | `agy --help`、`agy models` |
| GitHub Copilot CLI | `copilot --help`、`copilot help permissions` |
| Codex | `codex --help`、`codex exec --help` |
| Claude Code | `claude --help` |

CLI 更新後核對實際介面。旗標不支援時保留錯誤並交由 script 接手，不改用未核准的模型或執行模式。

## 內建工具交接

`native_required` 不是已派出。主 agent 使用該結果的模型與完整 prompt 呼叫目前宿主內建工具，不執行同名 CLI。可用模型以宿主實際提供的識別與版本為準；缺少合規模型時回報具體證據再接續。

內建工具執行完成後，主 agent 親自審查與驗證，再向 script 回報結果。派不出去時提供原派工識別碼、實際錯誤與下一層級，不憑上一輪錯誤跳過本輪選項。

## 狀態與半成品

script 的狀態保存原始任務、嘗試紀錄、錯誤與輸出位置。主 agent 接續前讀取紀錄、檢查程序及磁碟差異，補入已核對的經驗。部分成果由主 agent 決定保留與接續方式，script 不自動刪除、stash 或 reset。
