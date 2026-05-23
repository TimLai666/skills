# 雜項模組 — browser / approvals / acp / pairing / system

中小型子表面,各自不大但需要時就要會用。

---

## 1. `openclaw browser` — 專用 Chrome 控制

OpenClaw 有一個專用 Chrome / Chromium / Brave / Edge 實例,可以從 CLI 完整遙控:
開頁、點擊、輸入、截圖、抓 console、抓 network。給 agent 用來執行「真的去某網站
做某事」的能力。

來源:`src/cli/browser-cli*.ts`。

### 1A. 子指令地圖

| 群組 | 子指令 |
|---|---|
| 管理 | `status`、`start`、`stop`、`reset-profile`、`tabs`、`open <url>`、`focus <id>`、`close [id]` |
| Profile | `profiles`、`create-profile`、`delete-profile` |
| 觀察 | `screenshot`、`snapshot`、`console`、`pdf` |
| 動作 | `navigate`、`resize`、`click`、`type`、`press`、`hover`、`drag`、`select`、`upload`、`fill`、`dialog`、`wait`、`evaluate` |

### 1B. 通用 flag

```
--target-id <id>      # 哪個 tab(從 tabs / open 拿)
--browser-profile <n> # 哪個 profile
--url <gw-url>        # Gateway URL(走 RPC)
--token <token>       # Gateway token
--timeout <ms>
--json
```

### 1C. 常用 Playbook

#### 開啟 + 截圖

```bash
openclaw browser start
openclaw browser open https://example.com
# 取得 target id
openclaw browser tabs --json
# 截圖
openclaw browser screenshot <targetId> --full-page
openclaw browser screenshot <targetId> --element "#hero" --type png
```

#### 操作頁面

```bash
# 拍 snapshot(取得頁面結構與 element ref)
openclaw browser snapshot --target-id <id> --format aria --compact > /tmp/snap.txt

# 用 ref(從 snapshot 來)點擊 / 輸入
openclaw browser click <ref> --target-id <id>
openclaw browser type <ref> "Hello" --target-id <id> [--submit] [--slowly]
openclaw browser press Enter --target-id <id>
openclaw browser select <ref> "Option A" "Option B" --target-id <id>
openclaw browser upload ./file.pdf --ref <ref> --target-id <id>
```

#### Form 批次填

```bash
openclaw browser fill --target-id <id> --fields '{"#name":"Alice","#email":"a@b.c"}'
openclaw browser fill --target-id <id> --fields-file ./form.json
```

#### Dialog(alert/confirm/prompt)

```bash
openclaw browser dialog --accept --target-id <id>
openclaw browser dialog --dismiss --target-id <id>
openclaw browser dialog --accept --prompt "答案" --target-id <id>
```

#### 等待

```bash
openclaw browser wait --time 2000 --target-id <id>
openclaw browser wait --text "Loaded" --target-id <id> --timeout-ms 10000
openclaw browser wait --text-gone "Loading" --target-id <id>
```

#### JS 求值

```bash
openclaw browser evaluate --fn "() => document.title" --target-id <id>
openclaw browser evaluate --fn "(el) => el.dataset" --ref <ref> --target-id <id>
```

#### Console / Network

```bash
openclaw browser console --target-id <id>
openclaw browser console --target-id <id> --level error
```

#### Profile 隔離

```bash
openclaw browser profiles
openclaw browser create-profile --name work --color "#5A0"
openclaw browser delete-profile --name old
openclaw browser start --browser-profile work
```

#### 匯出 PDF

```bash
openclaw browser pdf --target-id <id> > out.pdf
```

#### Reset(清登入 / cookies)

```bash
openclaw browser reset-profile           # 留 profile 結構,清登入
```

> 這是**破壞性**(會清掉登入狀態)。走 destructive.md。

### 1D. Debug browser

| 症狀 | 看哪 |
|---|---|
| `browser start` 失敗 | `which chrome / brave-browser` 等;`status` 看設定的 binary 路徑 |
| 點擊 / 輸入沒反應 | snapshot 是否最新;頁面動態載入要先 `wait` |
| Element ref 對不上 | snapshot 是 stateful;頁面變了要重 snapshot |
| 截圖空白 | 頁面還在 load;先 `wait --text "..."` |

---

## 2. `openclaw approvals` — Exec approvals 管理

控制 agent 能 / 不能跑哪些 shell command,以及哪些要先 approve。三層:

- **Gateway 層**(全域預設)
- **Node 層**(每台 node 各自設)
- **Local 層**(直接讀 / 寫本機檔)

來源:`src/cli/exec-approvals-cli.ts`。

### 2A. 子指令

```
approvals get        # 看現在的 approval 設定
approvals set        # 套新的(從檔 / stdin)
approvals allowlist add <pattern>
approvals allowlist remove <pattern>
```

通用 flag:

- `--gateway` —— 操作 gateway 層的設定(走 RPC)
- `--node <id>` —— 操作某個 node 的設定(走 gateway → node 的 RPC)
- 都不加 —— 操作本機檔(local 層)
- `--agent <id>` —— 鎖定某個 agent 的設定
- `--file <path>` 或 `--stdin` —— 給 `set` 用,從檔/stdin 讀新設定

### 2B. Playbook

```bash
# 看
openclaw approvals get                     # 本機
openclaw approvals get --gateway --json    # gateway
openclaw approvals get --node garage-pi    # 某 node

# 加 allowlist pattern
openclaw approvals allowlist add "git status"
openclaw approvals allowlist add "ls *"

# 移
openclaw approvals allowlist remove "git status"

# 用檔覆蓋整個設定(慎重)
cat approvals.json5 | openclaw approvals set --stdin
```

### 2C. 注意

- **Approval 是安全的最後一道閘**。放太鬆 = agent 可以亂跑;放太緊 = 體驗差。
  寧緊勿鬆。
- 修這個**走 destructive.md** — 改錯會讓 agent 卡住或亂跑
- 設定變動通常立即生效(RPC),不用重啟

---

## 3. `openclaw acp` — Agent Control Protocol 橋接

ACP 是「給 IDE / 外部工具用的標準協定」,把 Gateway 包成 ACP server,讓任何
ACP-aware IDE(VS Code 等)能直接跟 OpenClaw 對話。

來源:`src/cli/acp-cli.ts`。

### 3A. Serve(把 gateway 包成 ACP)

```bash
openclaw acp \
  [--url <gw-ws-url>] \
  [--token <token> | --token-file <path>] \
  [--password <pw> | --password-file <path>] \
  [--session <key>] \
  [--session-label <label>] \
  [--require-existing] \
  [--reset-session] \
  [--no-prefix-cwd] \
  [-v]
```

**強烈建議用 `--token-file` / `--password-file`** 而不是 inline `--token` /
`--password` —— CLI 會印警告,因為 process list 會看到。

### 3B. Interactive client(測試用)

```bash
openclaw acp client \
  [--cwd <dir>] \
  [--server <cmd>] \
  [--server-args ...] \
  [--server-verbose] \
  [-v]
```

`--server` 預設就是 `openclaw`,等於在本機 spawn 一個 ACP server。

### 3C. 在 IDE 用

IDE 端設定 ACP server command 為 `openclaw acp ...`。具體看 IDE 文件。

### 3D. Debug ACP

| 症狀 | 看哪 |
|---|---|
| IDE 連不上 | acp 啟動 log(`-v`);gateway 在不在跑 |
| Session 訊息亂 | `--session-label` / `--session` 是不是對的;`--require-existing` 可以強制錯誤 |
| Auth 失敗 | token/password 真的在不在 file 裡;`--url` 對不對 |

---

## 4. `openclaw pairing` — DM Pairing 批准

當有人對你的 bot 私訊要求 pairing(走 `dmPolicy: "pairing"` 的 channel),會進
pending queue,要在 host 端 approve。

來源:`src/cli/pairing-cli.ts`。

### 4A. 子指令

```bash
# 列 pending(channel 必填:可在 --channel 或當位置參數)
openclaw pairing list <channel>
openclaw pairing list --channel telegram --account default --json

# 批准
openclaw pairing approve <channel> <code>
openclaw pairing approve --channel telegram --account default <code> --notify
```

`--notify` 會在 approve 後對對方發確認訊息。

### 4B. Playbook:有人想加 bot

```bash
# 1. 列
openclaw pairing list telegram
# 2. 看誰 / 啥時送的、與身份識別碼是否合理
# 3. 批准(或不批)
openclaw pairing approve telegram <code> --notify
# 4. 驗證
openclaw channels status --probe
openclaw agents list --bindings
```

### 4C. 安全

- **不要替不認識的人批准**。pairing 是「該對象就被視為 trusted DM」。
- channel 是 extension(非核心)時,channel 字串會被以正規表達式驗證,但**支援度**
  以該 channel plugin 為準

---

## 5. `openclaw system` — events / heartbeat / presence

對 gateway 注入 system event(讓 agent 知道發生了什麼)、控制 heartbeat、看 presence。

來源:`src/cli/system-cli.ts`。

### 5A. System event(讓 agent 醒來處理事件)

```bash
openclaw system event \
  --text "新訂單進來了" \
  [--mode now|next-heartbeat]
```

`--mode now` 立刻喚醒;`next-heartbeat`(預設)等下個心跳。

### 5B. Heartbeat

```bash
openclaw system heartbeat last           # 看最後一次心跳事件
openclaw system heartbeat enable         # 開
openclaw system heartbeat disable        # 關
```

### 5C. Presence

```bash
openclaw system presence                 # 列當前 presence 條目
```

### 5D. 通用 flag

所有 system 指令都吃 `--url` / `--token` / `--password` / `--timeout` /
`--expect-final` / `--json`。

### 5E. Playbook:從外部觸發 agent

```bash
# 外部 cron 排程跑這個,讓 agent 去處理
openclaw system event --text "每日報表" --mode now
```

或更乾淨的方式:用 `openclaw cron` 自己排,讓 OpenClaw 自己 trigger。

---

## 6. `openclaw qr` — iOS 配對 QR

```bash
openclaw qr
```

印出 QR(在終端)讓 iOS app 掃。要 TTY。

```bash
ssh -t oc-host "openclaw qr"
```

---

## 7. `openclaw directory` — 聯絡人 / 群組 ID 查詢

從 channel 拉聯絡人、群組、self 的 ID。給 `--target` 找對的 id 用。

來源:`src/cli/directory-cli.ts`。具體子指令各版本不同,跑 `--help` 看當下。

```bash
openclaw directory --help
```

常見用法:

```bash
# 找 telegram 自己的 bot id
openclaw directory <channel> self

# 列 peers
openclaw directory <channel> peers

# 列 groups
openclaw directory <channel> groups
```

---

## 8. `openclaw dns` — 廣域 discovery DNS

OpenClaw gateway 可以走 Bonjour(local) + 廣域 DNS(Tailscale + CoreDNS)被
discover。`dns setup` 配置這個。

來源:`src/cli/dns-cli.ts`。

```bash
openclaw dns setup --help
openclaw dns setup --apply        # 真的去寫 CoreDNS 設定(要 sudo;macOS)
```

> `--apply` 是寫系統檔的破壞性操作 — 走 destructive.md。

---

## 9. `openclaw webhooks gmail` — Gmail Pub/Sub

Gmail webhook 整合(讓 agent 收信)。

```bash
# 設定(會把 Pub/Sub topic、subscription、label 串起來)
openclaw webhooks gmail setup \
  --account user@example.com \
  --project <gcp-project> \
  --topic <topic> \
  --subscription <sub> \
  --label <label> \
  --hook-url <https-url> \
  --hook-token <token-or-file> \
  [--push-token <token>] \
  [--bind 0.0.0.0] [--port 8080] [--path /webhook] \
  [--include-body] [--max-bytes 1048576] \
  [--renew-minutes 60] \
  [--tailscale serve] [--tailscale-path /webhook] [--tailscale-target ...] \
  [--push-endpoint <url>]

# 跑 runtime(通常以 service 跑)
openclaw webhooks gmail run [...同樣的 override flag]
```

完整 flag 跑 `--help`。

### Debug

- 沒收到信:Pub/Sub subscription 真的有訂?Gmail watch 過期了沒(預設 7 天)?
- 看 `openclaw logs --follow` 與 GCP Pub/Sub 端的 metrics

---

## 10. Skills / Memory / Update / Dashboard / TUI

剩下幾個簡短的:

### `openclaw skills`

```bash
openclaw skills list                    # 全部
openclaw skills list --eligible         # 只看 ready
openclaw skills info <name>
openclaw skills check                   # 看缺什麼
```

裝 / 刪 skill 走 `npx clawhub`(外部工具),不在 OpenClaw CLI 本身。

### `openclaw memory`(向量搜尋)

```bash
openclaw memory status
openclaw memory index                   # 重建 index
openclaw memory search "<query>"
```

對 `MEMORY.md` + `memory/*.md` 做向量搜尋。

### `openclaw update`

```bash
openclaw update                         # source install 適用
sudo npm i -g openclaw@latest           # global install
```

更新後跑 doctor + restart gateway。

### `openclaw dashboard`

```bash
openclaw dashboard                      # 開 Control UI(會用當前 token)
openclaw dashboard --no-open            # 只印 URL
```

### `openclaw tui`

```bash
openclaw tui \
  [--url <ws>] [--token <t>] [--password <pw>] \
  [--session <key>] [--message <text>] [--thinking medium] \
  [--deliver] [--timeout-ms <ms>] [--history-limit <n>]
```

在終端跑出一個跟 gateway 對話的 TUI。SSH 上能跑(吃 SSH terminal 的 size)。
