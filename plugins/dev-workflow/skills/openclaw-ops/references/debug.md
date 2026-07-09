# Debug Runbook

當使用者說「壞了 / 不動 / 怪怪的」,先**取證、再假設、再動手**。亂改設定是反模式。

---

## 0. 開場(每次都做)

1. **症狀澄清**:讓使用者具體說
   - 期待什麼 vs 實際發生什麼
   - 哪個 channel / agent / session
   - 什麼時候開始壞的?之前有改過什麼嗎?(更新?加 plugin?改 config?)
   - 重現的步驟
2. **不要急著動 config**:gateway 沒 restart、token 沒過期、provider 沒 down 之前,
   90% 的「壞了」其實只是某一個元件死了或被擋住

---

## 1. 黃金順序(萬用流程)

每一步看完都先**判斷有沒有發現異常**,再決定要不要往下一步。**不要無腦把全部跑完**。

### Step 1 — `openclaw doctor`

```bash
openclaw doctor                  # 純報告,不要加 --fix
openclaw doctor --deep           # 加 system services 掃描
```

doctor 是 OpenClaw 自帶的健診,會檢查:

- gateway service 安裝狀態
- config 是否符合 schema
- 鍵名 migration(舊版鍵)
- channel module 載入錯誤
- workspace 路徑是否存在
- 認證檔案權限

**重要**:doctor 的輸出**就是你 debug 的第一手證據**。逐條看,有「red」或「warn」
就先聚焦那條。

### Step 2 — `openclaw status --deep`

```bash
openclaw status --all            # 完整 read-only 狀態(可貼)
openclaw status --deep           # 加 channel probe
openclaw status --usage          # 加 provider 用量(token 用完也會讓 agent 壞)
```

看點:

- Gateway 是不是真的在跑(`running`、port、PID)
- 每個 channel 的狀態(`connected` / `failed` / `disabled`)
- 最近的 session(對應到 agent / channel / peer)
- Provider usage(若快爆 quota,先處理這個)

### Step 3 — `openclaw channels status --probe`

```bash
openclaw channels status --probe --timeout 15000
openclaw channels capabilities --channel <ch>
```

`--probe` 會對每個 channel 做活探測(對 Telegram 是 getMe,Discord 是 self lookup,
等等)。失敗 → 那個 channel 的 token / 連線 / 設定有問題。

### Step 4 — `openclaw gateway probe`

```bash
openclaw gateway probe
openclaw gateway health
```

`probe` 會嘗試本地連、遠端連、檢查 binding。`health` 是直接打 health RPC。

兩個都失敗 → gateway 不在跑、port 被佔、token 不對、或 service 沒起來。

```bash
openclaw gateway status --deep    # 看 system service 角度的狀態
```

### Step 5 — Log

```bash
openclaw logs --follow            # 即時 log(問題重現時最強)
openclaw logs --limit 500         # 最近 500 行
openclaw logs --json              # JSON,給 grep 用
openclaw channels logs --channel telegram --lines 200
openclaw channels logs --channel all --lines 100
```

log 找這幾種模式:

- `error` / `failed` / `unauthorized`(顯而易見)
- `disconnect` / `reconnect`(連線抖動)
- `rate limit` / `429` / `quota`(被 provider 擋)
- `schema` / `validation` / `migrate`(config 有問題)
- `plugin <name>` failed to load(plugin 壞了)

### Step 6 — Security audit

```bash
openclaw security audit
openclaw security audit --deep
```

有時候「行為怪」其實是安全設定打架(dmPolicy 太嚴擋掉訊息、allowlist 沒包含發訊者
等等)。security audit 會點出 footgun。

### Step 7 — Sessions(路由問題)

```bash
openclaw sessions --active 60
openclaw sessions --json
openclaw agents list --bindings
```

看點:

- 發訊者的訊息有沒有產生新 session?
- session 落到哪個 agent?是不是預期的那個?
- 對應的 binding 條件對得上嗎?(channel + account + peer)

---

## 2. 常見故障 → root cause

### 2A. 「Channel 收到訊息但 agent 沒回應」

**最可能**:

1. **沒對應的 binding** → `agents list --bindings`,看那個 channel + peer 有沒有被綁
   到一個 agent。沒有就不會觸發。
2. **dmPolicy 擋下** → 看 `openclaw config get channels.<ch>.dmPolicy`。預設可能是
   `pairing`,沒 pair 過的不會接。看 `pairing list <ch>`。
3. **session.dmScope 設錯** → 服務型 agent 用 `main` 會讓所有人共用 session,訊息
   表面上「沒回」其實是 agent 在處理別人的脈絡(這偏 agent-builder 的問題,但你 debug
   時要會分辨)
4. **agent 沒授權發訊到那個 channel** → 看 `agents list --bindings` 與 agent 的
   tools/allow
5. **token 失效** → `channels status --probe`
6. **provider quota 爆 / API key 失效** → `models status --probe`、`status --usage`

### 2B. 「重啟 gateway 後 channel 全部紅」

1. **token 在 config 用 `${ENV}` 引用,但 env 沒設** → 看 service 的 env(systemd
   `Environment=`、launchd `EnvironmentVariables`)
2. **token 過期**(Discord 重發 / Telegram revoke 過) → 看 `channels logs`,有
   `unauthorized` 就是
3. **channel module 沒載入** → `doctor` / `plugins doctor`(部分 channel 是 plugin)
4. **port 衝突** → `gateway status` 看;`ss -ltnp | grep 18789`

### 2C. 「Agent 回但回得很慢 / 超時」

1. **timeout 太短** → `agents.defaults.timeoutSeconds`(預設 600)
2. **thinking level 太高 + 上下文太長** → 看 session log token 數
3. **provider 慢** → `models status --probe --probe-timeout 60000`
4. **fallback 沒設,主模型 down** → `models fallbacks list`

### 2D. 「Plugin 沒生效 / Plugin 載入失敗」

1. **`plugins list` 顯示 disabled** → `plugins enable <id>` + restart
2. **`plugins doctor`** → 看 load error 訊息;常見:peer dep 對不到、`workspace:*`
   寫進 dependencies(plugin 開發者問題)
3. **plugin 在 config 的 `plugins.entries.<id>.enabled` 是 false** → set true
4. **plugin path 在 `plugins.load.paths` 沒列** → 加進去
5. **restart 沒做** → 任何 plugin 動到都要 gateway restart

### 2E. 「config 寫不進去 / 套不上」

1. **JSON5 解析失敗** → `node -e "JSON5.parse(...)"` 或 doctor
2. **schema 校驗失敗** → doctor 會點;或 `openclaw config schema`(如果版本有)
3. **`$include` 的檔不存在** → 看 doctor
4. **權限問題** → `ls -la ~/.openclaw/openclaw.json`,該是 user 自己可寫
5. **改錯 profile** → 注意 `--profile foo` 與 `~/.openclaw-foo`;state dir 弄錯就
   改不到對的檔

### 2F. 「Gateway service 自己掛掉」

1. **`gateway status --deep`** → 看 launchd / systemd 報的 last exit code
2. **看 service 的 stderr / journal**:
   - macOS: `log show --predicate 'subsystem == "ai.openclaw"' --last 30m`
     或 `~/Library/Logs/openclaw/*.log`
   - Linux: `journalctl --user -u openclaw -n 200 --no-pager`
   - 或本 repo 提到的 `scripts/clawlog.sh`(macOS)
3. **記憶體 / 檔案 leak / 自動更新失敗** → 看 service log;考慮 `openclaw update`

### 2G. 「SSH 上跑 `openclaw …` 找不到指令」

不是 OpenClaw 的錯,是 PATH。見 `connect.md` §2B。

### 2H. 「我改了 config 但行為沒變」

1. **沒重啟 gateway** → `openclaw gateway restart`
2. **改錯檔**(`$include` 來源 / 別的 profile)→ `openclaw config get <key>` 看實際值
3. **env 在覆蓋 config**(例如 `OPENCLAW_GATEWAY_PORT=...`)→ 移掉 env 或服務的
   `Environment=`
4. **改到的鍵已被新版改名** → `doctor` 看 migration 警告

---

## 3. Debug 的反模式(不要做)

- **沒讀現狀就改 config**
- **看到 warn 就 `--fix`**:`doctor --fix` 與 `security audit --fix` 會直接寫設定。
  先**讀完報告、了解每條 fix 會改什麼**,確認後再跑(或加 `--dry-run`,但不是每個版本
  都支援)
- **直接 `reset`**:整個重來會丟掉 sessions / credentials / agent workspace。除非
  使用者明確要「乾淨重來」,否則別這樣解
- **盲目 restart**:restart 解不掉的問題就不是 restart 能解的;一直 restart 只是迴避
- **靠 google 的舊範例**:OpenClaw 版本變化快,網路上的範例常常鍵名過時。以
  `--help` 與 `docs/cli/*.md` 為準

---

## 4. 取證套件(complete forensic bundle)

需要丟給別人(社群、Issue、其他 agent)時的標準資料包:

```bash
# 1. 系統與版本
openclaw --version
uname -a               # 或 macOS:sw_vers
echo "Profile: ${OPENCLAW_PROFILE:-default}"

# 2. 狀態快照(read-only,可貼)
openclaw status --all --no-color
openclaw doctor --no-color  # 不要 --fix

# 3. Gateway 角度
openclaw gateway status --deep --no-color

# 4. Channel 角度
openclaw channels status --probe --no-color
openclaw channels list --no-color

# 5. 模型 / 用量
openclaw models status --no-color

# 6. 最近 log(redact 過敏感字串)
openclaw logs --limit 200 --no-color

# 7. 安全稽核
openclaw security audit --no-color
```

**貼出去前一定要 redact**:

- 任何 token / API key / OAuth token
- 完整電話號碼(留國碼 + 末 4 碼即可,如 `+886 ***-***-1234`)
- 對話內容(session log)
- 個人 home path 簡化成 `~`

`openclaw status --all` 與 `security audit` 設計上會做基本 redact;但不要假設它做完
了,**自己再掃一遍**再貼。

---

## 5. 當問題真的找不到 root cause

1. 跑 `openclaw doctor` 看新版有沒有 migration 待做
2. **跨環境比對**:同樣的 config / channel 在乾淨機器上會不會壞?
3. **逐步隔離**:停掉所有 plugin、disable 所有 binding,看核心會不會跑?然後一個一個
   開回來
4. 整理「取證套件」+ 重現步驟 → 開 issue,但**這不是放棄,而是把 root cause 找回來
   的程序**

不要說「修好了」當你只是繞過去。
