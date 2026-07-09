# OpenClaw CLI Map

完整頂層指令樹(從 `src/cli/program/command-registry.ts` 與
`src/cli/program/register.subclis.ts` 整理出來)。這是「**有沒有這個指令**」的快查表。

**重要**:每個 flag 與子指令仍以目標機器上 `openclaw <cmd> --help` 為準。版本之間
會搬,別把這份檔案當絕對。

---

## 全局 flag

```
openclaw [global flags] <command>
```

- `--dev` — 把 state 隔離到 `~/.openclaw-dev` 並偏移預設 port
- `--profile <name>` — state 隔離到 `~/.openclaw-<name>`
- `--no-color` — 關 ANSI 色
- `--update` — `openclaw update` 的捷徑(僅 source install)
- `-V` / `--version` / `-v` — 版本

---

## Core 指令(不分 subcli)

| 指令 | 用途 | 重點選項 |
|---|---|---|
| `setup` | 初始化 config + workspace | `--workspace`, `--wizard`, `--non-interactive`, `--mode local\|remote`, `--remote-url`, `--remote-token` |
| `onboard` | 互動式 wizard | 大量 `--auth-choice`、`--gateway-*`、`--remote-*` flag,可走 `--non-interactive` |
| `configure` | 互動式設定(creds/channels/gateway/agent defaults) | `--section` 可指定段落 |
| `config` | 非互動 config 讀寫(無子指令時跑 wizard) | `get <path>` / `set <path> <value>` / `unset <path>` |
| `doctor` | 健診 + 快速修 | `--yes`, `--repair` (`--fix`), `--force`, `--non-interactive`, `--deep`, `--generate-gateway-token` |
| `dashboard` | 開 Control UI | `--no-open` |
| `reset` | 重設本地 config/state(留 CLI) | `--scope config\|config+creds+sessions\|full`, `--yes`, `--non-interactive`, `--dry-run` |
| `uninstall` | 移掉 gateway service + 本地資料(CLI 留下) | `--service`, `--state`, `--workspace`, `--app`, `--all`, `--yes`, `--non-interactive`, `--dry-run` |
| `update` | 更新 OpenClaw + 看更新通道 | — |
| `message` | 收發訊息(多 subcommand) | 見下方 |
| `memory` | 搜尋與重建 memory index | `status`, `index`, `search <query>` |
| `agent` | 跑單次 agent turn | `--message`, `--to`, `--agent`, `--session-id`, `--thinking`, `--channel`, `--local`, `--deliver`, `--json`, `--timeout` |
| `agents` | 管理 agent(workspace/auth/routing) | `list`, `add`, `delete`(細節屬 agent-builder) |
| `status` | linked session 健康與 recent 收件人 | `--all`, `--deep`, `--usage`, `--json`, `--timeout`, `--verbose` |
| `health` | 從 gateway 拿 health | `--json`, `--timeout`, `--verbose` |
| `sessions` | 列 stored sessions | `--store`, `--active`, `--json`, `--verbose` |
| `browser` | 操作 OpenClaw 專用 Chrome/Chromium | 大量 subcommand,見下 |

---

## Sub-CLI(各自有子指令)

來源:`src/cli/program/register.subclis.ts`

| Subcli | 用途 | 子指令 |
|---|---|---|
| `acp` | Agent Control Protocol 橋 | — |
| `gateway` | WebSocket Gateway | `run`, `status`, `install`, `uninstall`, `start`, `stop`, `restart`, `probe`, `discover`, `health`, `call <method>`, `usage-cost` |
| `daemon` | gateway service legacy 別名 | 同 gateway 的 service 系列 |
| `logs` | tail gateway file logs(RPC) | `--follow`, `--limit`, `--json`, `--plain`, `--no-color` |
| `system` | system events / heartbeat / presence | `event --text <t>`, `heartbeat last\|enable\|disable`, `presence` |
| `models` | 模型發現/狀態/設定 | `list`, `status`, `set`, `set-image`, `aliases list\|add\|remove`, `fallbacks list\|add\|remove\|clear`, `image-fallbacks list\|add\|remove\|clear`, `scan`, `auth add\|setup-token\|paste-token`, `auth order get\|set\|clear` |
| `approvals` | 管 exec approvals | `get`, `set`, `allowlist add\|remove` |
| `nodes` | 已 pair 的 node 與 node 指令 | `status`, `describe`, `list`, `pending`, `approve`, `reject`, `rename`, `invoke`, `run`, `notify`, `camera ...`, `canvas ...`, `screen ...`, `location ...` |
| `devices` | 裝置 pairing + token 管理 | — |
| `node` | headless node host 服務 | `run`, `status`, `install`, `uninstall`, `start`, `stop`, `restart` |
| `sandbox` | sandbox container | `list`, `recreate`, `explain` |
| `tui` | Gateway TUI | `--url`, `--token`, `--password`, `--session`, `--message`, `--thinking` |
| `cron` | scheduler | `status`, `list`, `add` (alias `create`), `edit <id>`, `rm <id>`, `enable <id>`, `disable <id>`, `runs --id`, `run <id>` |
| `dns` | wide-area discovery DNS | `setup --apply` |
| `docs` | 線上 docs 搜尋 | `docs <query>` |
| `hooks` | 內建 agent hooks | `list`, `info`, `check`, `enable`, `disable`, `install`, `update` |
| `webhooks` | webhook 整合 | `gmail setup`, `gmail run` |
| `qr` | iOS pairing QR | — |
| `clawbot` | legacy 別名(別用,等同 openclaw) | — |
| `pairing` | DM pairing(批准 inbound) | `list <channel>`, `approve <channel> <code>` |
| `plugins` | 管 plugins / extensions | `list`, `info <id>`, `install <spec>`, `enable <id>`, `disable <id>`, `doctor`, `uninstall`, `update` |
| `channels` | 聊天 channel 帳號 | `list`, `status`, `capabilities`, `resolve`, `logs`, `add`, `remove`, `login`, `logout` |
| `directory` | 聯絡人/群組 ID 查詢 | — |
| `security` | 安全工具 + 本地稽核 | `audit` (`--deep`, `--fix`, `--json`) |
| `skills` | 列出可用 skill | `list`, `info <name>`, `check` |
| `update` | 更新 / 查更新通道 | — |
| `completion` | 產 shell completion 腳本 | — |

---

## Channels 子指令的選項熱區

`channels add` 一次接很多 channel 的 token/URL/account:

```
--channel <name>              whatsapp|telegram|discord|googlechat|slack|mattermost|signal|imessage|msteams|matrix|tlon
--account <id>                帳號 id(預設 "default")
--name <label>                顯示名
--token <token>               Telegram/Discord bot token
--token-file <path>           Telegram token 從檔案讀
--bot-token <token>           Slack xoxb-...
--app-token <token>           Slack xapp-...
--signal-number <e164>        Signal 號碼
--cli-path <path>             signal-cli / imsg
--db-path <path>              iMessage 資料庫
--service imessage|sms|auto
--region <region>             iMessage(SMS)區域
--auth-dir <path>             WhatsApp auth dir override
--http-url|--http-host|--http-port    Signal HTTP daemon
--webhook-path|--webhook-url|--audience-type|--audience    Google Chat / BlueBubbles
--homeserver|--user-id|--access-token|--password|--device-name|--initial-sync-limit    Matrix
--ship|--url|--code|--group-channels|--dm-allowlist|--auto-discover-channels    Tlon
--use-env                     使用 env token(預設帳號)
```

`channels remove` 預設 disable;加 `--delete` 才真砍 config。

`channels login` / `channels logout`:`--channel`, `--account`, `--verbose`。需要 QR
掃碼的 channel(WhatsApp Web)必須在有 TTY 的環境跑(SSH 要 `-t`)。

---

## Gateway 子指令的選項熱區

`openclaw gateway run`:

```
--port <port>                 預設 18789
--bind loopback|tailnet|lan|auto|custom
--token <token>
--auth token|password
--password <password>
--tailscale off|serve|funnel
--tailscale-reset-on-exit
--allow-unconfigured
--force                       搶占 port
--ws-log auto|full|compact    (--compact 是別名)
--raw-stream / --raw-stream-path
--verbose
```

`gateway install` / `uninstall` / `start` / `stop` / `restart` 都吃 `--json`。
`gateway install` 額外:`--port`, `--runtime node|bun`, `--token`, `--force`。

`gateway status`:`--url`, `--token`, `--password`, `--timeout`, `--no-probe`,
`--deep`, `--json`。

`gateway call <method>`:`--params <json>`。常用方法:`config.apply`、`config.patch`、
`update.run`。`config.set/patch/apply` 直呼建議帶 `baseHash`(從 `config.get` 拿)。

---

## Cron 子指令

```
cron add --name <n> --at <iso>|--every <dur>|--cron "<expr>" \
         --system-event <text> | --message <text>
cron list [--all] [--json]
cron edit <id>     # patch fields
cron rm <id>
cron enable|disable <id>
cron runs --id <id> [--limit <n>]
cron run <id> [--force]
```

所有 `cron` 指令吃 `--url`, `--token`, `--timeout`, `--expect-final`(因為是 RPC)。

---

## Models 重點

```
models set <model>             # 設 agents.defaults.model.primary
models set-image <model>       # 設 agents.defaults.imageModel.primary
models aliases add <alias> <model>
models fallbacks add <model> / clear
models image-fallbacks add <model> / clear
models auth add                # 互動 helper
models auth setup-token --provider anthropic
models auth paste-token --provider <p> --profile-id <id> [--expires-in <duration>]
models auth order set --provider <p> --agent <id> <profileIds...>
```

`models status` 可加 `--probe`(真打一次)、`--probe-provider`、`--probe-profile`、
`--probe-timeout`、`--probe-concurrency`、`--check`(exit code 表 0/1/2)。

---

## Security audit

```
openclaw security audit            # 報告
openclaw security audit --deep     # 加 live gateway probe
openclaw security audit --fix      # 套安全預設 + chmod state/config
openclaw security audit --json
```

---

## Docs 與全局指令

- `openclaw docs <query>` — 對 live docs 做關鍵字搜尋(本機就能跑)
- `openclaw skills list` — 列可用 skills
- `openclaw skills info <name>` — 看 skill 細節
- `openclaw skills check` — ready vs missing

---

## 注意:plugin 會加 top-level 指令

例如裝了 voicecall plugin 後會有 `openclaw voicecall`。用 `openclaw --help` 或
`openclaw plugins list` 看當下實際有什麼。
