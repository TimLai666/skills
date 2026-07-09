# 常見運維 Playbook

每個 task 都假設你**已經完成 Phase 0**(本機 / SSH 確定、`openclaw --version` 通了、
讀過現有 `openclaw.json`)。

每個 playbook 的標準三段:**準備 → 動作 → 驗收**。

---

## A. Channels

### A1. 加一個新 channel 帳號

例:加 Telegram bot。

**準備**:

```bash
openclaw channels list                  # 確認還沒有
openclaw channels capabilities --channel telegram   # 看支援的 features
```

讓使用者準備好 token(BotFather 拿)。**不要替使用者去要 token**;不要把 token
複述在對話裡。

**動作**(用 env var 引用,不要明文):

```bash
# 法一:env + config(推薦)
export TELEGRAM_BOT_TOKEN='...'
openclaw channels add --channel telegram --account default \
  --name "MyBot" --use-env

# 法二:直接傳 token(token 會短暫出現在 process list)
openclaw channels add --channel telegram --account default \
  --name "MyBot" --token "$TELEGRAM_BOT_TOKEN"
unset TELEGRAM_BOT_TOKEN
```

要重啟 gateway 才生效:

```bash
openclaw gateway restart
```

**驗收**:

```bash
openclaw channels list
openclaw channels status --probe          # 對該 channel 做活探測
openclaw channels logs --channel telegram --lines 50
```

> 加 channel 後,如果要把訊息路由到某個 agent,**那是 binding 的事 → 轉
> openclaw-agent-builder**。

---

### A2. 移掉一個 channel 帳號

**準備**:

```bash
openclaw channels list                  # 看當前帳號
# 找出該 channel 是否還有 binding 指向 agent
openclaw agents list --bindings
```

如果還有 binding,先讓使用者決定 binding 怎麼處理(留著會壞、或要重新指)。

**動作**(預設只 disable,不刪):

```bash
openclaw channels remove --channel discord --account work
```

要連 config 一起砍掉:

```bash
openclaw channels remove --channel discord --account work --delete
```

**這是破壞性操作 — 走 destructive.md 的確認流程**。

**驗收**:

```bash
openclaw channels list
openclaw doctor
```

---

### A3. WhatsApp 重新登入(QR 掃碼)

**必須在 TTY 跑**。SSH 要 `-t`:

```bash
# 本機
openclaw channels login --channel whatsapp

# SSH
ssh -t oc-host "openclaw channels login --channel whatsapp"
```

掃碼後保持前景到完成。完成後 `openclaw channels status --probe` 驗。

如果使用者在 headless 機器上沒有任何 TTY 出口,**這個只能他自己上去掃**;告訴他別的
協作方式幫不上忙。

---

### A4. 換 token / 更新 channel 設定

**優先用 `channels add` 重跑一次**(同 channel + 同 account 是 idempotent update):

```bash
openclaw channels add --channel telegram --account default --token <new-token>
openclaw gateway restart
openclaw channels status --probe
```

不要直接編 `openclaw.json` 去改 token,除非有特殊原因。

---

## B. Gateway / Daemon

### B1. 起 gateway(foreground)

```bash
openclaw gateway run --bind loopback --port 18789
```

看 log 即時:同一終端就會印出來。長跑要 service。

### B2. 把 gateway 裝成系統服務

預設 Node runtime(bun 不推薦):

```bash
openclaw gateway install --port 18789 --runtime node
openclaw gateway start
openclaw gateway status
```

`install` 會根據平台選 launchd / systemd / schtasks。要重裝:

```bash
openclaw gateway install --force
```

### B3. 重啟 gateway

config 改完通常都要這步:

```bash
openclaw gateway restart
openclaw gateway status        # 確認回到 healthy
openclaw channels status --probe
```

**警告**:重啟會中斷正在跑的 session。如果正在跟使用者 / agent 對話,等一下。
若使用者要求「立刻重啟」,先告知中斷成本,確認後再做。

### B4. 改 gateway port

```bash
openclaw config set gateway.port 18800
openclaw gateway restart
openclaw gateway probe --url ws://127.0.0.1:18800   # 驗
```

如果 service 的環境變數 `OPENCLAW_GATEWAY_PORT` 在用,**env 會贏過 config**。改完 config
還是連舊 port → 去看 service 的 env(launchd plist / systemd unit / `~/.profile`)。

### B5. 砍掉所有 gateway service(深度清)

```bash
openclaw gateway status --deep    # 先看有幾個(profile-named 不算 extra)
openclaw gateway uninstall
```

**這是破壞性 — 走 destructive.md**。

---

## C. Config 改動

### C1. 改一個值

```bash
# 備份
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)

# 改
openclaw config set session.dmScope "per-channel-peer"
openclaw config set gateway.bind "tailnet"

# 看
openclaw config get session.dmScope

# 套
openclaw gateway restart
openclaw doctor
```

### C2. 加複雜結構(陣列 / 物件)

```bash
# JSON5 字串
openclaw config set bindings '[{ channel: "telegram", account: "default", peer: "12345", agent: "ops" }]' --strict-json
```

**注意**:對 `bindings` / `agents.list` 動手是 agent-builder 的領域。這裡只是說語法。

### C3. 移除一個鍵

```bash
openclaw config unset discovery.wideArea.domain
openclaw gateway restart
```

### C4. 大規模改 — 直接編檔

```bash
# 1. 拿一份草稿(本機 Write 出來)
# 2. 推到目標機器(見 connect.md §3B)
# 3. 驗證 JSON5 + schema
node -e "JSON5.parse(require('fs').readFileSync('~/.openclaw/openclaw.json','utf8'))"  # 路徑要展開
openclaw doctor

# 4. Restart
openclaw gateway restart
```

---

## D. Models

### D1. 換預設模型

```bash
openclaw models list
openclaw models status
openclaw models set claude-opus-4-7
openclaw models status         # 確認
```

### D2. 設 fallback 鏈

```bash
openclaw models fallbacks list
openclaw models fallbacks add claude-sonnet-4-6
openclaw models fallbacks add claude-haiku-4-5-20251001
```

### D3. 加 API key / OAuth

```bash
# OAuth(Anthropic 推薦)
openclaw models auth setup-token --provider anthropic
# 然後跟著流程

# Paste token
openclaw models auth paste-token --provider openai --profile-id manual

# 互動式 helper
openclaw models auth add
```

### D4. 驗證 auth 真的能打

```bash
openclaw models status --probe --probe-timeout 10000
```

**會真的打 provider 一次,可能消耗 token / 觸發 rate limit。**告訴使用者後再跑。

---

## E. Cron

### E1. 加排程 job

```bash
# 一次性(at)
openclaw cron add --name "morning-check" \
  --at "2026-06-01T09:00:00+08:00" \
  --message "早上的狀態摘要"

# 重複(every duration)
openclaw cron add --name "hourly-sync" \
  --every 1h --system-event "sync"

# Cron 表達式
openclaw cron add --name "weekly-report" \
  --cron "0 9 * * MON" --message "週報"
```

**任一 `--at / --every / --cron` 三選一**,**任一 `--system-event / --message` 二選一**。

### E2. 看 / 改 / 停

```bash
openclaw cron list
openclaw cron edit <id>             # patch
openclaw cron disable <id>          # 暫停
openclaw cron enable <id>
openclaw cron rm <id>               # 刪
openclaw cron runs --id <id>        # 看歷史執行
openclaw cron run <id>              # 手動觸發一次
```

---

## F. Plugins

### F1. 列 / 安裝 / 啟用

```bash
openclaw plugins list
openclaw plugins info <id>
openclaw plugins install <npm-spec | path | .tgz>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw gateway restart        # 多數 plugin 改動要重啟
```

### F2. Plugin 出問題

```bash
openclaw plugins doctor         # 看 load errors
```

詳見 `debug.md`。

---

## G. Hooks

```bash
openclaw hooks list
openclaw hooks info <name>
openclaw hooks check
openclaw hooks enable <name>
openclaw hooks disable <name>
openclaw hooks install <spec>
openclaw hooks update
```

Hooks 改動通常要重啟 gateway。

---

## H. Webhooks(Gmail)

```bash
openclaw webhooks gmail setup --account <email>
# 完成後跑 runner(通常以 service 跑)
openclaw webhooks gmail run
```

完整 flag 看 `--help` 或 docs 連結。

---

## I. Sandbox

```bash
openclaw sandbox list
openclaw sandbox recreate <name>    # 重建 container
openclaw sandbox explain <name>     # 解釋為何這樣設
```

---

## J. Status / Sessions / Memory

```bash
openclaw status                  # 快速狀態
openclaw status --all            # 完整(read-only,可貼)
openclaw status --deep           # 加 channel probe
openclaw status --usage          # 加 provider 用量

openclaw sessions                # 列 stored sessions
openclaw sessions --active 60    # 過去 60 分鐘有活動的

openclaw memory status
openclaw memory index            # 重建 vector index
openclaw memory search "<q>"
```

---

## K. Update

```bash
openclaw update                  # 更新 CLI(source install 適用)
# 或在系統上
sudo npm i -g openclaw@latest    # global install 要 root
```

更新後務必跑:

```bash
openclaw doctor
openclaw gateway restart
openclaw channels status --probe
```

新版可能改了鍵名/路徑 — `doctor` 通常會點出來。

---

## L. Dashboard / TUI

```bash
openclaw dashboard               # 開 Control UI(會用當前 token)
openclaw dashboard --no-open     # 只印 URL

openclaw tui                     # 終端 UI
```

`tui` 在 SSH 上也行(吃當前 terminal 的 size)。

---

## 通用提醒

- **每個寫入 op 後跑 doctor + status**。debug 之外的工作流也該收尾驗收。
- **token / 密碼**:任何時候都不要寫進 config 明文、不要 echo 到 log、不要在對話複述。
- **`channels remove --delete` / `gateway uninstall` / `reset` / `uninstall`** —
  走 `destructive.md`。
