# Config 檔案與環境

OpenClaw 把所有狀態放在一個 state dir,設定統一在一個 JSON5 檔。這份檔列出
**路徑、環境變數、主要 config 鍵**。

來源:`src/config/paths.ts`、`src/cli/config-cli.ts`、`src/config/io.ts`,以及
`docs/cli/index.md`。

---

## 1. State dir 與 config path

| 用途 | 預設路徑 | 環境變數(覆蓋用) |
|---|---|---|
| State dir | `~/.openclaw/` | `OPENCLAW_STATE_DIR`(舊名 `CLAWDBOT_STATE_DIR`) |
| Config 檔 | `<state-dir>/openclaw.json` | `OPENCLAW_CONFIG_PATH`(舊名 `CLAWDBOT_CONFIG_PATH`) |
| 憑證 | `<state-dir>/credentials/` | `OPENCLAW_OAUTH_DIR` |
| OAuth 檔 | `<state-dir>/credentials/oauth.json` | (跟著 OAuth dir) |
| Gateway port | `18789` | `OPENCLAW_GATEWAY_PORT`(舊名 `CLAWDBOT_GATEWAY_PORT`) |
| Gateway lock | `$TMPDIR/openclaw-<uid>` | (從 `os.tmpdir()` 算) |

**Legacy 容忍**:也認 `~/.clawdbot`、`~/.moldbot`、`~/.moltbot`(舊名)。對應的
config 檔名也認 `clawdbot.json`、`moldbot.json`、`moltbot.json`。如果 host 上同時
有新舊路徑,**新的優先**;沒有新的就用最舊的存在的那個。

**Nix mode**:`OPENCLAW_NIX_MODE=1` 時不自動安裝 / 修改 config(config 被視為唯讀)。
看到這個 env 設定,請先停下來問使用者 —— 對 Nix-managed host 多半要從 Nix flake 而非
CLI 改設定。

**Dev/profile 隔離**:

- `openclaw --dev …` → state 進 `~/.openclaw-dev`,port 偏移
- `openclaw --profile foo …` → state 進 `~/.openclaw-foo`

這意味著同一台機器可以有多份隔離的 OpenClaw。動 config 前先確認:

```bash
openclaw status                  # 看實際載入的 state dir
ls -d ~/.openclaw* 2>/dev/null   # 看有哪些 profile/dev 存在
```

---

## 2. `openclaw.json` 的格式

**JSON5**,所以可以有註解(`//` 與 `/* */`)、尾逗號、無引號鍵名。常見頂層鍵:

```jsonc
{
  // gateway 配置
  gateway: {
    port: 18789,
    bind: "loopback",       // loopback | tailnet | lan | auto | custom
    auth: "token",          // token | password
    // 不要在這裡明文存 token!用 ${TOKEN} 從 env 取,或走 credentials/
  },

  // 訊息通道
  channels: {
    telegram: {
      enabled: true,
      accounts: {
        default: { /* token via env or credentials store */ },
        alerts: { /* ... */ },
      },
    },
    discord: { /* ... */ },
    whatsapp: { /* ... */ },
    slack: { /* ... */ },
    signal: { /* ... */ },
    imessage: { /* ... */ },
    msteams: { /* ... */ },
    matrix: { /* ... */ },
    // ...
  },

  // routing:哪個 channel/peer 要交給哪個 agent
  bindings: [
    { channel: "telegram", account: "default", peer: "<chat-id>", agent: "ops" },
    // ...
  ],

  // agents
  agents: {
    defaults: {
      model: { primary: "claude-opus-4-7", fallbacks: ["claude-sonnet-4-6"] },
      imageModel: { primary: "...", fallbacks: [] },
      timeoutSeconds: 600,
      // ...
    },
    list: [
      {
        id: "ops",
        workspace: "~/.openclaw/workspace-ops",
        // ... 其餘細節屬 agent-builder 的領域
      },
    ],
  },

  // session 設定
  session: {
    dmScope: "main",        // 或 "per-channel-peer";服務型 agent 用後者
    // ...
  },

  // plugins
  plugins: {
    entries: {
      "voicecall": { enabled: true },
      // ...
    },
    load: {
      paths: ["~/.openclaw/plugins/local-thing"],
    },
  },

  // hooks
  hooks: { /* ... */ },

  // discovery
  discovery: {
    wideArea: { domain: "..." },
  },

  // commands(slash commands 開關)
  commands: { debug: false },

  // approvals(exec approvals)
  approvals: { /* ... */ },

  // 也可以 $include 別的 fragment 進來
  $include: ["./fragments/extra.json5"],
}
```

> 上面是**示意**,不是完整 schema。**每個 key 的真實名稱要以
> `openclaw config schema` 或 host 上的官方文件為準**。版本之間鍵名會搬。

### 環境變數替換

config 內的 `"${MY_VAR}"` 字串在 load 時會被 env 值替換。常見用法:

```jsonc
{
  channels: {
    telegram: {
      accounts: {
        default: { token: "${TELEGRAM_BOT_TOKEN}" },
      },
    },
  },
}
```

這樣就**不會**把明文 token 寫進 config 檔。`OPENCLAW_*` env 變數見 `~/.profile`
或 systemd unit / launchd plist。

### `$include`

config 支援把片段抽到別檔 `$include` 進來。看到 `$include: [...]` 表示完整 config
其實是多檔合併;改某個鍵時要找到**它最終定義在哪個檔**。`openclaw config get`
讀的是合併後的視圖。

---

## 3. 編 config 的兩條路

### A. `openclaw config` CLI(優先)

```bash
openclaw config get <path>            # 讀
openclaw config set <path> <value>    # 寫(value 是 JSON5;非 JSON5 會 fallback 成 raw string)
openclaw config set <path> <value> --strict-json   # 強制 JSON5(失敗就報錯,不要 fallback)
openclaw config unset <path>          # 刪
```

**Path 語法**:dot + bracket。範例:

```
gateway.port
channels.telegram.accounts.default.token
agents.list[0].id
bindings[2].agent
plugins.entries["voicecall"].enabled    # 鍵名含特殊字元時用 ["..."]
```

**好處**:

- 走官方 read/write,會解 `$include` 與 `${ENV}`
- 不會把 runtime defaults 漏寫進檔(走 `snapshot.resolved` 而非 `snapshot.config`)
- 自動 schema 校驗(失敗會擋下)

**改完都會提示「Restart the gateway to apply」**。重啟才生效。

### B. 直接編 `~/.openclaw/openclaw.json`

當需要批次改、加註解、或操作複雜結構時。流程:

```bash
# 1. 備份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)

# 2. 編輯(Read → Edit / Write)

# 3. 驗證 JSON5 解析
node -e "console.log(require('json5').parse(require('fs').readFileSync(process.env.HOME+'/.openclaw/openclaw.json','utf8')) ? 'ok' : 'bad')"

# 4. 跑 doctor 看 schema / 邏輯校驗
openclaw doctor

# 5. 真的要套用 → 重啟 gateway
openclaw gateway restart
```

---

## 4. 重啟才生效的鍵

config 改了**幾乎都要重啟 gateway** 才生效。例外是某些 hot-reload 的東西(視版本)。
規則:不確定就重啟。

```bash
# service 模式
openclaw gateway restart

# foreground 模式
# 先 Ctrl-C 舊的,再 openclaw gateway run
```

---

## 5. 憑證儲存

OAuth token 走 `~/.openclaw/credentials/oauth.json`。channel token 可以三條路:

1. **環境變數 + config 用 `${VAR}` 引用**(最乾淨)
2. **直接寫進 config**(token 字串明文。**不要**這樣做,除非別無選擇)
3. **走 channel-specific auth store**(`channels add --token-file`、WhatsApp 的 auth-dir 等)

讀現有 config 時,看到 `${...}` 表示這個值來自 env。要確認 env 真的有設(尤其 SSH
non-interactive shell):

```bash
ssh oc-host "bash -lc 'echo TELEGRAM=\$TELEGRAM_BOT_TOKEN | sed s/=.*=/=set/'"
# 上面 sed 是為了不要把 token 明文 echo 出來,只回 "set" 或 "" 之一
```

更實用的做法:

```bash
ssh oc-host "test -n \"\$TELEGRAM_BOT_TOKEN\" && echo set || echo missing"
```

---

## 6. 不要碰的檔

- `~/.openclaw/sessions/*.jsonl` — 對話歷史,不要手動編
- `~/.openclaw/credentials/oauth.json` — OAuth token,改錯會要重 login
- `~/.openclaw/agents/<id>/agent/*` — agent 的 internal state(model registry、
  auth profile),也不要手動編。動 agent 內容是 agent-builder 的事
- `~/.openclaw/workspace*/skills/` 下的 skill 檔 — 用 `openclaw skills` 或 clawhub
  管理

---

## 7. 看當下實際生效的 config

`openclaw config get` 不帶 path 行不通(必須給 path)。要看整份用:

```bash
# 整份合併後的 config(包含 $include 與 ${ENV})
openclaw config get .  # 不行 —— path 必須非空

# 退而求其次:讀檔
cat ~/.openclaw/openclaw.json

# 看 schema(各版本支援度不同)
openclaw config schema 2>/dev/null || echo "no schema cmd in this version"
```

`openclaw doctor` 也會印出實際 config 路徑與 state dir。

---

## 8. 多 host / 多 profile 環境

如果同一個使用者管多台機器,**先確認你連到對的那台**:

```bash
ssh <target> "hostname && cat /etc/os-release | head -1 && openclaw --version"
ssh <target> "ls -d ~/.openclaw*"
```

`~/.openclaw-foo` 表示有個 `--profile foo`。對它操作要帶 `--profile foo`:

```bash
ssh <target> "openclaw --profile foo doctor"
ssh <target> "openclaw --profile foo channels list"
```
