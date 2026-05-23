# Messaging — `openclaw message`

`openclaw message` 是非常大的子表面,涵蓋從一般文字訊息到 Discord 管理、emoji/sticker
上傳、thread 操作、permission 查詢都有。所有 subcommand 走 gateway,所以**需要 gateway
在跑**才能用。

來源:`src/cli/program/register.message.ts` 與 `src/cli/program/message/register.*.ts`。

---

## 1. 子指令地圖

| 群組 | 子指令 |
|---|---|
| 一般 | `send`、`broadcast` |
| 互動 | `poll`、`react`、`reactions`、`emoji <list\|upload>`、`sticker <send\|upload>` |
| 訊息生命週期 | `read`、`edit`、`delete`、`pin`、`unpin`、`pins` |
| Thread | `thread create\|list\|reply` |
| Discord admin | `permissions`、`search`、`timeout`、`kick`、`ban`、`role <info\|add\|remove>`、`channel <info\|list>`、`member info`、`voice status`、`event <list\|create>` |

---

## 2. 通用基底參數

幾乎每個 message 子指令都需要兩件事:**target**(寄到哪裡)與 **channel/account**
(從哪個帳號送)。

| Flag | 用途 |
|---|---|
| `--channel <ch>` | telegram\|discord\|slack\|whatsapp\|signal\|imessage\|googlechat\|msteams\|mattermost\|matrix\|tlon\|... |
| `--account <id>` | account id(預設 `default`) |
| `--target <dest>` | 目的地。各 channel 形式不同(見下) |
| `--from-message-id <id>` | 對某個既有訊息操作(react/edit/delete/pin) |
| `--json` | 輸出 JSON,給腳本用 |
| `--url`/`--token`/`--password`/`--timeout` | Gateway RPC 連線設定 |

### `--target` 的形式(依 channel)

| Channel | 範例 target |
|---|---|
| telegram | `<chat-id>` 或 `+E.164`(若已 resolve) |
| discord | `channel:<id>` / `dm:<userId>` / `guild:<id>:channel:<id>` |
| whatsapp | `+E.164`(個人)或 `group:<jid>` |
| signal | `+E.164` 或 `group:<id>` |
| imessage | `+E.164` 或 `email@...` |
| slack | `channel:<id>` / `user:<id>` / 頻道名 `#name` |
| matrix | `!room:server` 或 `@user:server` |

不確定 target 怎麼寫:用 `openclaw channels resolve <name>` 或 `openclaw directory ...`。

---

## 3. 常用 Playbook

### 3A. 發一則文字訊息

```bash
openclaw message send \
  --channel telegram --account default \
  --target <chat-id> \
  --message "Hello"
```

帶媒體:

```bash
openclaw message send \
  --channel whatsapp --target +15555550123 \
  --message "Look at this" \
  --media ./image.jpg
```

WhatsApp 把影片當 GIF 播:`--gif-playback`。

Telegram inline keyboard:

```bash
openclaw message send --channel telegram --target <id> \
  --message "Pick one" \
  --buttons '[[{"text":"A","callback_data":"a"},{"text":"B","callback_data":"b"}]]'
```

Discord components / Adaptive Card 用 `--components <json>` / `--card <json>`。

回某則訊息:`--reply-to <message-id>`。Telegram forum thread:`--thread-id <id>`。
靜默推送:`--silent`。

### 3B. 發一則 poll(Discord/Telegram)

```bash
openclaw message poll \
  --channel discord --target channel:<id> \
  --poll-question "晚餐?" \
  --poll-option "披薩" \
  --poll-option "壽司" \
  --poll-option "拉麵"
```

### 3C. 對訊息做反應

```bash
openclaw message react \
  --channel discord --target channel:<id> \
  --message-id <mid> \
  --emoji "✅"
```

看現有 reactions:`openclaw message reactions --channel ... --target ... --message-id <mid>`。

### 3D. 讀 / 編 / 刪

```bash
# 讀某 channel 最近訊息
openclaw message read --channel slack --target channel:<id> --limit 50

# 編輯
openclaw message edit --channel telegram --target <chat> --message-id <mid> --message "新內容"

# 刪
openclaw message delete --channel discord --target channel:<id> --message-id <mid>
```

> 編 / 刪是高敏感:Telegram 對 bot 有時限,Discord 對 channel 有權限要求。失敗多半
> 是該 channel 的政策,不是 OpenClaw bug。

### 3E. Pin / Unpin / 看 pins

```bash
openclaw message pin --channel discord --target channel:<id> --message-id <mid>
openclaw message unpin --channel discord --target channel:<id> --message-id <mid>
openclaw message pins --channel discord --target channel:<id>
```

### 3F. Thread

```bash
# 開 thread
openclaw message thread create --channel discord --target channel:<id> --name "討論"

# 列 thread
openclaw message thread list --channel discord --target channel:<id>

# 回 thread
openclaw message thread reply --channel discord --target thread:<id> --message "..."
```

### 3G. Broadcast(一對多)

```bash
openclaw message broadcast \
  --channel telegram \
  --targets <chat1>,<chat2>,<chat3> \
  --message "公告"
```

或從檔讀:`--targets-file ./list.txt`。

> **謹慎**:broadcast 一次發給多個對象,觸發 rate limit 機率高。先小批測試。違反
> channel ToS(垃圾訊息)會被封 bot。

### 3H. Emoji / Sticker(管理)

```bash
openclaw message emoji list --channel discord --target guild:<id>
openclaw message emoji upload --channel discord --target guild:<id> --name happy --file ./emoji.png

openclaw message sticker send --channel telegram --target <chat> --sticker-id <id>
openclaw message sticker upload --channel discord --target guild:<id> --file ./sticker.png
```

### 3I. Discord 管理 (admin)

需要 bot 有對應 permission:

```bash
# 查 permissions
openclaw message permissions --channel discord --target channel:<id>

# 搜尋訊息(Discord)
openclaw message search --channel discord --target channel:<id> --query "keyword"

# Timeout / Kick / Ban
openclaw message timeout --channel discord --target guild:<id> --user-id <uid> --duration 10m
openclaw message kick --channel discord --target guild:<id> --user-id <uid> --reason "..."
openclaw message ban --channel discord --target guild:<id> --user-id <uid> --reason "..."

# Role 操作
openclaw message role info --channel discord --target guild:<id> --role-id <rid>
openclaw message role add --channel discord --target guild:<id> --user-id <uid> --role-id <rid>
openclaw message role remove --channel discord --target guild:<id> --user-id <uid> --role-id <rid>

# Channel / Member 資訊
openclaw message channel list --channel discord --target guild:<id>
openclaw message channel info --channel discord --target channel:<id>
openclaw message member info --channel discord --target guild:<id> --user-id <uid>

# Voice / Event
openclaw message voice status --channel discord --target channel:<id>
openclaw message event list --channel discord --target guild:<id>
openclaw message event create --channel discord --target guild:<id> --name "..." --start <iso> --end <iso>
```

> Kick / Ban / Timeout 是**破壞性 channel 操作**:會看到的訊息會在那台 Discord
> 留紀錄。走 destructive.md 的二次確認流程。

---

## 4. Debug message 出問題

### 4A. 「訊息送不出去」

1. `openclaw channels status --probe --timeout 15000` — 該 channel 有沒有連上
2. `openclaw channels logs --channel <ch> --lines 100` — 看送訊那一刻有什麼錯
3. **Permission 問題**(Discord 最常見):`message permissions` 看 bot 在那個 channel
   能不能 send
4. **Target 格式錯**:`openclaw channels resolve <name>` 把名字轉成 id
5. **Rate limit**(broadcast 後最常見):看 log 有沒有 `429` / `Too Many Requests`;
   退讓重試
6. **Token 過期**:`channels status --probe` 會抓出來;`channels add` 重設 token

### 4B. 「Bot 一直收到訊息但 agent 沒回」

不是 `message send` 的問題,是 routing。見 `debug.md` §2A。

### 4C. 「Discord poll/event 失敗」

Discord 對 channel type 與 bot scope 有限制:

- poll 只能在 guild text channel(不能在 DM)
- event create 需要 `MANAGE_EVENTS` permission
- 看 `message permissions` 的輸出

---

## 5. 安全提醒

- **不要把訊息內容當 binding 的判斷依據** —— 訊息送進來,routing 是由 channel + peer +
  account 決定,不是訊息文字。任何「靠關鍵字權限提升」的設計都不安全(那是 agent
  application logic,屬 agent-builder 的事)。
- **broadcast 容易踩 ToS**。對 Telegram / WhatsApp 尤其是。先做小規模驗證再放量。
- **timeout/kick/ban 留 audit 痕跡**。問清楚使用者真的要做。
- **emoji/sticker upload 會耗 channel quota**(Discord guild 上限固定)。
