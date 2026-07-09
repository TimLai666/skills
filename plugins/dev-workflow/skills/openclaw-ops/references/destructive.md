# 破壞性操作 — 安全檢查表

下面這些指令會**刪資料、改線上行為、不可逆**。每一個都走「**列清楚 → 二次確認 →
備份 → 執行(或 dry-run 先看)→ 驗收**」流程,不可省略。

---

## 清單 — 哪些算破壞性

| 指令 | 為什麼 | 破壞範圍 |
|---|---|---|
| `openclaw reset` | 重設本地 state | 視 `--scope`:config / + creds / + sessions / 全部 |
| `openclaw uninstall` | 移除 service + 本地資料 | 視 flag:service / state / workspace / app |
| `openclaw doctor --fix` / `--force` | 自動套修補 | 會改 config、service 設定 |
| `openclaw security audit --fix` | 自動套安全預設 | 會改 config、檔案權限 |
| `openclaw gateway uninstall` | 拆 gateway service | service 沒了;config 留著 |
| `openclaw daemon uninstall` | (legacy 別名)同上 | 同上 |
| `openclaw channels remove --delete` | 連 config 一起刪 channel | 該 account 的 config + auth 全砍 |
| `openclaw channels remove`(無 `--delete`) | disable channel | 半破壞;config 留著,但 channel 立即停 |
| `openclaw plugins uninstall <id>` | 拔 plugin | plugin 檔案與 config entry 都會處理 |
| `openclaw config unset <path>` | 砍一個 config 鍵 | 影響面看那個鍵;通常重啟才生效 |
| `openclaw cron rm <id>` | 刪排程 | 那個 job 沒了(歷史 runs 通常還在) |
| `openclaw agents delete <id>` | **agent-builder 領域**,但會列在這裡警示 | agent workspace + state + sessions 通通沒 |
| `openclaw models auth …` 砍 profile | 認證資料消失 | 對應 channel / agent 要重 auth |
| `rm -rf ~/.openclaw` | 暴力清 | **永遠不要這樣做**,改用 `openclaw uninstall --state` |

> 規則:**flag 含 `--delete` / `--force` / `--fix` / `--all` 都按破壞性對待**。

---

## 標準流程

### 1. 列清楚會發生什麼

用具體的字。例:

> 「我要跑 `openclaw uninstall --state --workspace --yes --non-interactive`,這會:
> - 刪掉 `~/.openclaw/openclaw.json`(你的整份設定)
> - 刪掉 `~/.openclaw/credentials/`(所有 OAuth token)
> - 刪掉 `~/.openclaw/sessions/`(所有對話歷史)
> - 刪掉 `~/.openclaw/workspace*/`(所有 agent workspace 與 RAG 知識)
> - **不會**碰 gateway service(那要另外跑 `--service`)
> 跑完後 OpenClaw 設定回到剛裝完的狀態,但 channel 都要重新登入。
> 確認要繼續嗎?」

不要說「跑 reset 對嗎?」這種沒指明範圍的話。

### 2. 取得「明確」二次確認

不接受「嗯」「OK」「好」之類含糊回答。要對方覆述他知道會發生什麼,或對你列的條目
點頭。如果他語氣猶豫,**就再列一遍**。

### 3. 備份

**永遠先備份**:

```bash
ts=$(date +%Y%m%d-%H%M%S)
cp -r ~/.openclaw "~/.openclaw.backup-$ts"

# 或只備重要的
cp ~/.openclaw/openclaw.json "~/.openclaw/openclaw.json.bak-$ts"
cp -r ~/.openclaw/credentials "~/.openclaw/credentials.bak-$ts"
```

SSH 版本:

```bash
ssh oc-host "ts=\$(date +%Y%m%d-%H%M%S); cp -r ~/.openclaw ~/.openclaw.backup-\$ts && echo backup-\$ts"
```

把備份名稱告訴使用者。對方知道萬一要回滾時去哪找。

### 4. 用 `--dry-run` 先看一遍(支援的指令)

```bash
openclaw reset --scope full --dry-run
openclaw uninstall --all --dry-run
```

dry-run 會印出要刪哪些檔。把那個輸出貼給使用者,**再次確認**。

### 5. 執行

```bash
# 帶 --yes / --non-interactive 避免中途互動
openclaw reset --scope config+creds+sessions --yes --non-interactive
```

但**不要**在沒先 dry-run 過的情況下加 `--yes` 直接跑。`--yes` 是讓非互動環境用的,
不是「跳過確認」。

### 6. 驗收

```bash
openclaw doctor
openclaw status
ls ~/.openclaw/                 # 看實際剩什麼
ls "~/.openclaw.backup-$ts"     # 確認備份還在
```

回報使用者:做了什麼、刪了什麼、備份在哪、現在狀態為何、接下來要不要重新 setup。

---

## 各指令的注意點

### `openclaw reset`

```
--scope config | config+creds+sessions | full
--yes
--non-interactive   # 要求 --scope + --yes
--dry-run
```

- `config` — 只重設 config 檔
- `config+creds+sessions` — config + OAuth token + 對話歷史
- `full` — 連 workspace 都砍(**agent 全沒**)

**不要**在使用者沒明確說「整個重來」的情況下用 `full`。

### `openclaw uninstall`

```
--service     # gateway service
--state       # state + config
--workspace   # workspace dir
--app         # macOS app(若安裝)
--all         # 以上全部
--yes / --non-interactive / --dry-run
```

`--all` 等於完全清除(CLI 本身還在)。**這比 `reset --scope full` 還狠**。

### `openclaw doctor --fix` / `--repair` / `--force`

doctor 的修補分三級:

- **不加 flag** — 純報告
- **`--repair` / `--fix`** — 自動套「推薦修補」(不問)
- **`--force`** — **覆寫使用者自訂的 service 設定**

`--force` 是核武器,只在使用者明確說「請覆寫」時用。`--repair` 在絕大多數情境
可以接受,但仍要先看 doctor 的純報告,**知道它要改什麼**,再決定。

### `openclaw security audit --fix`

會做:

- 把 `dmPolicy` 等鍵收緊到推薦預設
- `chmod` config 與 credentials 檔案到較嚴的權限
- 可能改 `session.dmScope` 等

跑前先讀 `audit`(不帶 `--fix`)的報告;有不想被改的鍵要明確說(或先備份再跑,跑完
對 diff)。

### `openclaw gateway uninstall`

只拆 service,不刪 config / state / workspace。但 gateway 沒了 channel 也不會工作。
重裝走 `gateway install`。

### `openclaw channels remove --delete`

把該 account 的 channel config 完整移除(token reference、設定值全沒)。**要重設一切。**
沒 `--delete` 是 disable(設 `enabled: false`),保留設定可以隨時開回來。

---

## 回滾

如果做完發現不對:

```bash
# 設定回滾
cp "~/.openclaw/openclaw.json.bak-$ts" ~/.openclaw/openclaw.json
openclaw gateway restart

# 整份回滾(reset / uninstall 後)
mv ~/.openclaw "~/.openclaw.broken-$(date +%Y%m%d-%H%M%S)"
cp -r "~/.openclaw.backup-$ts" ~/.openclaw
openclaw gateway restart
openclaw doctor
```

OAuth token 通常還能用(只要 OAuth file 還在),channel 多半不用重 login。但
WhatsApp 的 session 一旦砍掉就要重掃 QR。

---

## 最後一個守門員

如果使用者在 SSH 連線、又是生產用的 host、又要 `reset --scope full` 或 `uninstall
--all` —— **再問一次**:

> 「這台是不是還有真人在用 / 是不是線上 bot 在跑?清完所有 channel 都要重新登入,
> WhatsApp 還要重掃 QR。如果是生產機器,建議先在 maintenance window 再跑,或
> 先把 channel 訊息接到別處再說。確認要現在就跑嗎?」

寧可被嫌囉嗦,不要把對方的 bot 弄死又不知道怎麼救。
