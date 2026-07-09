---
name: openclaw-ops
description: >-
  Operate, configure, and debug a running OpenClaw installation from a host
  machine (locally or over SSH). Covers the whole runtime surface **except**
  building agent personalities/workspaces — channels, gateway, daemon/service,
  config (`openclaw.json`), models + auth, cron, hooks, plugins, sandbox,
  sessions, security audit, doctor, reset, uninstall. Also the go-to runbook
  for diagnosing OpenClaw issues: gateway probes, channel status, doctor,
  security audit, logs, sessions. Trigger on any mention of `openclaw` CLI
  commands, `~/.openclaw`, `openclaw.json`, "restart gateway", "add a channel",
  "check why my bot isn't responding", "openclaw doctor", "channels status",
  "ssh into the OpenClaw box", and similar — also whenever a host has
  `~/.openclaw/openclaw.json` and OpenClaw work is implied even if not named.
  Hand off to **openclaw-agent-builder** for any work that creates or edits an
  agent's workspace files (SOUL.md / AGENTS.md / IDENTITY.md / USER.md / RAG
  knowledge / `agents.list[]` entries / `bindings[]`).
---

# OpenClaw Ops

在一台跑著 OpenClaw 的機器上(本機,或 SSH 進去的遠端)做**運維、配置、診斷**。
不寫 agent 人格與 workspace —— 那是 `openclaw-agent-builder` 的工作。

這份 skill 涵蓋:

- **配置**:`~/.openclaw/openclaw.json` 的讀寫、`openclaw config get/set/unset`
- **服務**:gateway 與 daemon 的安裝、啟停、重啟、健康檢查
- **連線**:channels 帳號的增刪、登入、查狀態、看 log
- **模型**:`openclaw models` 的 list/status/set/auth
- **排程**:`openclaw cron`
- **延伸**:`openclaw plugins`、`openclaw hooks`、`openclaw webhooks`
- **隔離**:`openclaw sandbox`
- **稽核**:`openclaw doctor`、`openclaw security audit`、`openclaw status`、`openclaw logs`
- **重置**:`openclaw reset` / `openclaw uninstall`(高破壞性,額外保護)
- **遠端**:本機或 SSH 都支援;以 SSH 為主時要先把連線打通再做事

> 你**不會**動到的事:agent 的注入式檔案(SOUL/AGENTS/IDENTITY/USER)、`agents.list[]` 內容、
> `bindings[]`、agent workspace 的 RAG 知識文件。這些遇到了就**轉交給 openclaw-agent-builder**。

---

## Phase 0 — 確定操作目標並建立脈絡(不可跳過)

每一次任務的第一件事:**這個 OpenClaw 跑在哪裡,你要怎麼操作它?**

### 0A — 本機 還是 SSH?

開門先問:

> 「要操作的 OpenClaw 是跑在**這台機器(本機)**,還是要 **SSH 連到別台**?」

- **本機** → 直接用本機 shell,跳到 0B
- **SSH** → 進入 `references/connect.md` 的「SSH 連線設定」一節,問齊主機/帳號/驗證
  方式(金鑰優先;密碼可接受但要提醒風險),建好可重用連線後再往下

無論哪種,**這份 runbook 後面所有 `openclaw …` 指令都在目標機器上執行**。

### 0B — 連線測試 + 讀現狀

在目標機器上跑這四件事,把脈絡攤開來:

```bash
openclaw --version          # CLI 可用、版本為何
openclaw status             # gateway 是否在跑、recent session
ls ~/.openclaw/             # state dir 與 workspace 樣貌
cat ~/.openclaw/openclaw.json   # 讀現有設定(JSON5)
```

`status` 連不上 gateway 不一定是問題 —— 也許 gateway 還沒裝。先確認**意圖**:使用者是
要把它裝起來、跑起來,還是它已經該跑卻沒跑(那就進 debug 流程)。

關鍵狀態目錄(預設值,可被環境變數覆蓋,見 `references/config-files.md`):

| 用途 | 路徑 |
|---|---|
| state dir | `~/.openclaw/` |
| config 檔 | `~/.openclaw/openclaw.json` (JSON5) |
| 憑證 | `~/.openclaw/credentials/` |
| sessions | `~/.openclaw/sessions/` (per-agent: `~/.openclaw/agents/<id>/sessions/`) |
| agents | `~/.openclaw/agents/<id>/` |
| workspace | `~/.openclaw/workspace/` 或 `~/.openclaw/workspace-<agentId>/` |
| gateway port | 18789(預設) |

> 上面任何路徑被 `OPENCLAW_STATE_DIR`、`OPENCLAW_CONFIG_PATH`、`OPENCLAW_OAUTH_DIR`、
> `OPENCLAW_GATEWAY_PORT` 覆蓋時,以實際解析結果為準。先看 env,再看 config,
> 別硬套預設值。

### 0C — 版本差異警告(每次都要記著)

OpenClaw CLI **隨版本變化**,flag 與 config key 都會搬。所以:

- **執行前先 `openclaw <command> --help`** 驗證選項真的存在。不要直接套這份 runbook
  的 flag 名;runbook 是起點不是定論。
- config key 用 `openclaw config get <path>` 試讀來確認鍵名(`openclaw config schema`
  可看 schema)。

寧可多探一句,不要寫錯設定。

---

## 自我約束(高權限工具)

你此刻是 host 上的高權限 operator,有完整 shell 和 `openclaw` CLI 存取。守住三條:

1. **修任何東西前先讀現狀**。沒讀過 config 就改 config 是禁忌。
2. **寫前計畫,確認後執行**。所有寫入(`config set`、`channels add`、`channels remove`、
   gateway 重啟、`reset`、`uninstall`、`security audit --fix`、`doctor --force`)
   都先把「會發生什麼、影響哪些線上行為」攤給使用者,**取得明確同意**再做。
3. **絕不把憑證寫進檔案或 log**。token、密碼、API key 只在指令裡短暫出現,不複述、
   不存檔、不 print 回對話。

---

## 工作流程:把使用者的話對應到動作

收到請求後,**先分類**,再決定要拉哪些 reference:

### 分類矩陣

| 使用者說的話 | 屬於 | 主要 reference |
|---|---|---|
| 「新增/編輯 agent」「做一個 LINE bot」「改 SOUL.md」「換 bindings」 | **agent-builder 的事** | 跟使用者說你會轉交 `openclaw-agent-builder` |
| 「加一個 Telegram channel」「換 Discord token」「移掉 Slack 帳號」 | 操作 — channel | `references/operations.md`(channels 一節) |
| 「啟動/重啟 gateway」「裝成 service」「gateway port 改一下」 | 操作 — gateway/daemon | `references/operations.md`(gateway 一節) |
| 「換模型」「設 fallback」「加一個 API key」 | 操作 — models | `references/operations.md`(models 一節) |
| 「加 cron job 每天 9 點…」 | 操作 — cron | `references/operations.md`(cron 一節) |
| 「安裝/啟用/停用 plugin」「裝 voicecall」 | 操作 — plugins | `references/operations.md`(plugins 一節) |
| 「改一個 config 值」「dmPolicy/session 設定」 | 操作 — config | `references/config-files.md` + `operations.md`(config) |
| 「批次發訊息」「發 poll」「對訊息按表情」「pin 一則」「開 thread」「Discord kick/ban/role」 | 操作 — messaging | `references/messaging.md` |
| 「接一台新 Pi」「Pi 看不到 gateway」「拍張照」「在 node 上跑 command」 | 操作 — nodes/node/devices | `references/nodes-and-devices.md` |
| 「用 browser 截圖 / 點某個鈕 / 填表」 | 操作 — browser | `references/misc-modules.md`(§1) |
| 「approve pairing」「approvals allowlist」「ACP 接 IDE」「QR」「dns setup」 | 操作 — 雜項模組 | `references/misc-modules.md` |
| 「bot 沒回應」「channel 連不上」「為什麼 X 不動」 | **debug** | `references/debug.md`(對應子系統 reference 的 debug 章) |
| 「health/status 看起來怪怪的」「跑 doctor」「安全稽核」 | **debug + 稽核** | `references/debug.md` |
| 「整個砍掉重來」「reset」「uninstall」 | **破壞性** | `references/destructive.md`(必讀) |

### 通用步驟

1. **分類** + 讀現狀(Phase 0 還沒做就先做)
2. **拉對應 reference**(只拉用得到的;不要一次全讀)
3. **草擬計畫**:要動哪個檔/跑哪個指令,期望結果,可能風險
4. **跟使用者確認**(寫前計畫;debug 也要說明你要跑什麼指令)
5. **執行**(本機直接,SSH 則透過已建好的連線)
6. **驗收**:跑 `openclaw doctor`、`openclaw status`、`openclaw channels status --probe`,
   或對應的子系統驗收指令,把結果回報給使用者
7. **可逆性**:任何 config 寫入前先備份 `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-<timestamp>`

---

## Debug 能力(這個 skill 的核心之一)

當使用者說「壞了/不動/怪怪的」,**不要亂改設定**。先**取證**。

`references/debug.md` 有完整 runbook,核心套路如下:

### 黃金順序(每個問題都從這裡開始)

1. **症狀**:讓使用者具體說「期待什麼 vs 實際發生什麼」、哪個 channel/agent、何時開始
2. **`openclaw doctor`** —— OpenClaw 自帶的健診,先跑(不加 `--fix`,純看報告)
3. **`openclaw status --deep` 或 `openclaw status --all`** —— 全面狀態,包含 gateway、
   channels、sessions、provider 額度
4. **`openclaw channels status --probe`** —— 對每個 channel 做活探測
5. **`openclaw gateway probe` / `gateway health`** —— 確認 gateway 真的可達且回應
6. **`openclaw logs --follow`** —— 看即時 log(問題重現時最有用)
7. **`openclaw channels logs --channel <ch>`** —— 看特定 channel 最近的 log
8. **`openclaw security audit`** —— 看有沒有設定上的安全 footgun 連帶造成行為怪
9. **`openclaw sessions`** —— 看 session 路由有沒有走到對的 agent

### 常見故障模式(快速分流)

- **Channel 收到訊息但沒回應** → 路由問題(`bindings`)、agent 沒有對應的 channel
  emit 權限、或 dmPolicy 擋下 → 看 `channels logs`、`sessions`,以及 `agents list
  --bindings`
- **Gateway 重啟後 channel 全紅** → token 過期、auth profile 變動,或 channel
  module 沒載入 → `channels status --probe` + `channels logs`
- **模型呼叫失敗** → API key 失效、quota 用完、provider 端故障 → `models status
  --probe`,看 provider usage
- **Plugin 沒生效** → `plugins doctor` + `plugins list`,看 enabled 與 load 錯誤
- **service 應該開機自啟卻沒開** → `gateway status --deep` 看系統服務狀態
- **config 套不上去** → 多半是 JSON5 解析失敗或 schema 校驗失敗 → `openclaw config
  get <path>` 試讀;`doctor` 通常會點出來

詳見 `references/debug.md`。

### Debug 完成的標準

**找到 root cause 才算完成**。光是 workaround 別當結束。如果觀察到的證據對不上假設,
回到取證,別硬猜。

---

## 編輯 OpenClaw 的設定檔(`openclaw.json`)

兩條路:

1. **`openclaw config set/unset`**(優先)—— 走官方 CLI,會做 schema 校驗、$include 解析、
   env 替換,不會把 runtime defaults 漏寫進檔。
2. **直接編輯 `~/.openclaw/openclaw.json`**(當 CLI 不夠用時)—— JSON5 格式,可有註解。
   改完務必檢查能不能被 JSON5 解析(用 `node -e` 或 `openclaw doctor` 驗證)。

**改任何 config 都要**:

1. `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d-%H%M%S)`
2. 動到「啟動時讀取」的鍵(gateway/channels/plugins 多半屬此)→ 提示使用者要**重啟
   gateway** 才會生效
3. 改完跑 `openclaw doctor` 與 `openclaw status --deep`

config 結構與環境變數覆蓋,見 `references/config-files.md`。

---

## 破壞性操作

`reset`、`uninstall`、`--fix`、`--force`、`--delete`、`channels remove` 沒 `--account`
全幹掉、`gateway uninstall`、刪 `~/.openclaw` —— 這些都進 `references/destructive.md`。

執行前要做:

1. 跟使用者明確、具名地列出**會被刪/改/重設的東西**
2. **得到二次確認**(光是「OK」不夠,要對方覆述他知道會發生什麼)
3. 預先備份要保的東西(`openclaw.json`、`credentials/`、`sessions/`)
4. 預設加 `--dry-run` 看一遍(支援的指令都有)
5. 跑完跑 `openclaw doctor` 與 `openclaw status` 驗收

---

## 本機 vs SSH 的執行差異

兩條路徑後續的 runbook 內容**完全一樣**,差別只在「指令怎麼跑到目標機器上」。連線
細節、檔案讀寫範式、reusable connection、SSH 上做 interactive 操作的眉角,全部在
`references/connect.md`。

簡要範式:

```bash
# 本機
openclaw doctor
cat ~/.openclaw/openclaw.json

# SSH(已用 ControlMaster 建好連線後)
ssh oc-host "openclaw doctor"
ssh oc-host "cat ~/.openclaw/openclaw.json"

# SSH 寫檔(用 heredoc + tee;絕不在指令裡明文寫 token)
ssh oc-host "tee ~/.openclaw/openclaw.json.new" < /tmp/openclaw.json.draft
ssh oc-host "mv ~/.openclaw/openclaw.json.new ~/.openclaw/openclaw.json"
```

> **互動式指令的限制**:`openclaw onboard`、`openclaw configure`、`openclaw channels
> login --channel whatsapp`(掃 QR)等需要 TTY 的指令,在 SSH 上要分配 PTY(`ssh -t`)。
> 對 WhatsApp QR 這類,告知使用者要在那台機器上自己看終端(SSH 也可以,但要 `ssh -t`
> 且不能背景化)。

---

## Reference 檔案(按需載入)

只在需要時讀對應的 reference,**不要一次全讀**。

- `references/cli-map.md` —— OpenClaw 頂層指令樹完整地圖(從原始碼整理)。當你需要
  確認「有沒有某個指令/某個 flag」時讀。
- `references/connect.md` —— 本機與 SSH 連線設定、reusable connection、SSH 上做檔案
  讀寫與互動指令的範式。Phase 0 選 SSH 時讀。
- `references/config-files.md` —— `~/.openclaw/` 結構、`openclaw.json` 主要鍵、環境
  變數覆蓋。改 config 之前讀。
- `references/operations.md` —— 常見 ops playbook(加 channel、換模型、改 port、
  裝 plugin、加 cron…)。對應「操作」類請求時讀。
- `references/messaging.md` —— `openclaw message` 子指令族(send/broadcast/poll/
  react/edit/delete/pin/thread/role/permissions/channel/member/event/emoji/sticker)。
  寫自動化發訊或 Discord 管理時讀。
- `references/nodes-and-devices.md` —— `nodes` / `node` / `devices` / `qr`,以及
  camera/canvas/screen/location 子表面。接 Pi/桌機/手機 node 時讀。
- `references/misc-modules.md` —— `browser`(專用 Chrome 全控)、`approvals`、
  `acp`、`pairing`、`system`、`dns`、`webhooks gmail`、`skills` / `memory` /
  `update` / `dashboard` / `tui` 等中小模組。
- `references/debug.md` —— 系統性 debug runbook,含分流表與常見故障 root cause。
  對應「壞了/不動/怪怪的」時讀。各 reference 內部也都有自己的 debug 小節,先看
  本檔的黃金順序,再深入子系統 reference。
- `references/destructive.md` —— `reset` / `uninstall` / `--fix` / `--force` 安全
  檢查表與回滾。任何破壞性操作前讀。

---

## 與其他 skill 的關係

- **openclaw-agent-builder**(建 agent / 編 agent workspace)—— 凡是創 / 改 agent
  的人格、workspace、bindings、RAG 知識庫,**轉交給它**,不要在這裡做。你可以幫對方
  跑驗收(`agents list --bindings`、`channels status --probe`),但「寫 SOUL.md / 加
  `agents.list[]` 項目 / 設 `dmPolicy`」是它的領域。
- 兩者**共用 Phase 0 的連線設定**。如果使用者剛剛已經用 agent-builder 做過 Phase 0,
  直接沿用;不要重問。

---

## 收尾(每次任務都做)

1. 跑驗收(對應子系統的 status / probe / doctor)
2. 回報給使用者:做了什麼、改了什麼、現在狀態為何、有沒有要重啟才生效的部分
3. 若 SSH:提醒使用者(或自己處理)收掉 ControlMaster 連線(`ssh -O exit oc-host`)
4. 任何用到的密碼/token,確認都沒寫進檔案或對話複述
