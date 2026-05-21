# Channels、Bindings 與 Session 範圍

這份說明如何把 channel 接到 agent 上。所有 config 鍵名以 host 上的
`openclaw config schema` 與官方文件為準 —— 下面是依現行文件整理的起點。

## 目錄

1. 三個核心概念：agentId / accountId / binding
2. Binding 路由規則
3. dmPolicy（誰能 DM 這個 agent）
4. session.dmScope（多使用者對話隔離）
5. 各 channel 的帳號設定
6. 完整範例

---

## 1. 三個核心概念

- **agentId** —— 一個「腦」（workspace、per-agent auth、session store）。
- **accountId** —— 一個 channel 帳號實例（例如 WhatsApp 的 `personal` vs `biz`）。
- **binding** —— 把 inbound 訊息依 `(channel, accountId, peer)` 路由到某個 agentId。

一個 Gateway 可以同時跑很多 agent、很多 channel 帳號。

---

## 2. Binding 路由規則

`bindings[]` 是**決定性**的，**最具體者勝**。優先序（高到低）：

1. `peer` 精確比對（特定 DM / 群組 / 頻道 id）
2. `parentPeer`（thread 繼承）
3. `guildId` + `roles`（Discord 角色路由）
4. `guildId`（Discord）
5. `teamId`（Slack）
6. `accountId` 比對
7. channel 層級比對（`accountId: "*"`）
8. 預設 agent（`agents.list[].default`，否則第一筆，預設 `main`）

補充：

- 同一層有多個 binding 命中，**config 順序在前者勝**。
- 一個 binding 設了多個 match 欄位（如 `peer` + `guildId`），所有欄位都要符合
  （AND 語意）。
- binding 省略 `accountId` 時，只比對 default 帳號；要 channel 全帳號 fallback 用
  `accountId: "*"`。

binding 形狀：

```json5
{
  agentId: "cram-support",
  match: {
    channel: "line",
    accountId: "default",
    // 可選：peer: { kind: "direct" | "group" | "channel", id: "…" }
  },
}
```

---

## 3. dmPolicy（誰能 DM 這個 agent）

DM 存取控制是**per channel 帳號**的（不是 per agent）。OpenClaw 把 inbound DM 當成
不可信輸入，預設就偏保守。

| dmPolicy | 行為 | 用在 |
|---|---|---|
| `pairing` | 陌生人收到配對碼，訊息不被處理；需 `openclaw pairing approve` | 私人助理（預設） |
| `allowlist` | 只有 `allowFrom` 名單內的識別碼能用 | 半開放服務型 |
| `open` | 公開可用，需在 allowlist 放 `"*"` | 對公眾開放的服務型（理解風險） |

`allowFrom` 放的是**已驗證識別碼**（E.164 電話、`tg:<id>`、`discord:<id>` 等），
這就是「身份」防線的真正閘門。

私人助理範例：

```json5
channels: {
  whatsapp: {
    dmPolicy: "allowlist",
    allowFrom: ["+886912345678"],   // 只有主人
  },
}
```

對公眾開放的服務型：用 `open` 並理解所有來訊者都是不可信顧客；務必搭配下面的
`session.dmScope` 與 `security-hardening.md` 的全套防線。

---

## 4. session.dmScope（多使用者對話隔離）

**服務型 agent 必檢查這一項。** 預設所有 DM 共用一個 session —— 多顧客情境下，A 的
私訊會出現在 B 的脈絡裡。

| dmScope | 行為 |
|---|---|
| `main`（預設） | 所有 DM 共用一個 session |
| `per-peer` | 依 sender 隔離（跨 channel） |
| `per-channel-peer` | 依 channel + sender 隔離（**服務型建議值**） |
| `per-account-channel-peer` | 依 account + channel + sender 隔離 |

服務型 agent 設定：

```json5
session: {
  dmScope: "per-channel-peer",
}
```

- 私人助理（只有一個人）用 `main` 即可。
- 同一個人從多個 channel 來，可用 `session.identityLinks` 把身份連起來共用 session。
- `session.dmScope` 是全域設定還是可 per-agent，以 host 上的 `config schema` 確認。

---

## 5. 各 channel 的帳號設定

> **務必先驗證**：每個 channel 的 config 鍵名與登入指令可能隨版本不同。動手前對該
> channel 跑 `openclaw channels --help` 與查 `docs.openclaw.ai/channels/<channel>`。

**Discord** —— 每個 agent 一個 bot 帳號，需在 Developer Portal 開 Message Content
Intent。token 放 `channels.discord.accounts.<id>.token`。

**Telegram** —— 用 BotFather 各建一個 bot。token 放
`channels.telegram.accounts.<id>.botToken`。

**WhatsApp** —— 啟動 gateway 前先掃碼登入：
`openclaw channels login --channel whatsapp --account <id>`。支援多帳號（多支號碼）。

**LINE** —— OpenClaw 支援 LINE channel。LINE 通常需要 Messaging API channel 的
access token / secret（透過 LINE Developers Console 取得）。**確切的 config 鍵名與
設定流程請查 `docs.openclaw.ai/channels`（或 host 上 `openclaw channels --help`）後
再寫入** —— 不要照抄未驗證的鍵名。

**Slack** —— 用 `teamId` 路由。

**WebChat** —— 內建網頁聊天介面，適合先在本機測試 agent，不必先接外部 channel。

通用：支援多帳號的 channel 用 `accountId` 區分每個登入。`channels.<channel>.
defaultAccount` 可設 channel 層級的預設帳號。

---

## 6. 完整範例

**服務型：補習班 LINE 客服**（鍵名待 host 驗證）

```json5
{
  agents: {
    list: [
      {
        id: "cram-support",
        name: "補習班客服",
        workspace: "~/.openclaw/workspace-cram-support",
        agentDir: "~/.openclaw/agents/cram-support/agent",
        model: "anthropic/claude-sonnet-4-6",
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "browser", "canvas", "nodes", "cron", "gateway"],
        },
        sandbox: { mode: "non-main" },
      },
    ],
  },
  bindings: [
    { agentId: "cram-support", match: { channel: "line", accountId: "default" } },
  ],
  session: {
    dmScope: "per-channel-peer",
  },
  channels: {
    line: {
      dmPolicy: "open",          // 對公眾開放；理解所有來訊者皆不可信
      // accounts: { default: { … } }  ← LINE 帳號鍵名待 host 驗證後填
    },
  },
}
```

**私人助理：WhatsApp 個人助理**

```json5
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "default" } },
  ],
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+886912345678"],
    },
  },
}
```
