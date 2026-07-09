# Nodes / Node host / Devices

OpenClaw 把「設備」分成兩種角色:

- **Gateway**(本 skill 的主角)—— 跑 channels、agents、orchestration 的中心
- **Node**(本檔的主角)—— 已 pair 給 gateway 的「邊緣設備」(Raspberry Pi、桌機、
  手機),提供 camera / canvas / screen / location / 任意 exec 能力。**邊緣由
  gateway 遙控**

三個 CLI 子表面:

- `openclaw nodes` —— **從 gateway 端看 / 操作**已 pair 的 node
- `openclaw node` —— 在**邊緣裝置上跑 headless node host**(這就是「我這台是 node」)
- `openclaw devices` —— 設備層級的 pairing / token 管理

來源:`src/cli/nodes-cli/`、`src/cli/node-cli/`、`src/cli/devices-cli.ts`。

---

## 1. `openclaw node`(邊緣裝置)

裝在邊緣設備上,跑 headless node host,連回 gateway。

### 1A. Foreground 跑

```bash
openclaw node run \
  --host <gateway-host> --port 18789 \
  [--tls] [--tls-fingerprint <sha256>] \
  [--node-id <id>] [--display-name <name>]
```

- `--tls` —— 加 TLS,需要 gateway 有 cert
- `--tls-fingerprint <sha256>` —— 釘 cert fingerprint(避免 MITM);**強烈建議用**
- `--node-id` —— 強制重設 node id(清掉 pairing token,等於要重新 approve)

### 1B. 裝成系統服務

```bash
openclaw node install \
  --host <gateway-host> --port 18789 \
  [--tls] [--tls-fingerprint <sha256>] \
  [--runtime node|bun] [--force]

openclaw node status
openclaw node restart
openclaw node stop
openclaw node uninstall
```

跟 gateway 服務一樣,平台用 launchd / systemd / schtasks。

### 1C. 安裝後的驗收

```bash
# 在 node 機上
openclaw node status

# 在 gateway 機上(看 node 是否真的連上來)
openclaw nodes status
openclaw nodes pending          # 看有沒有等批准的 pairing
```

---

## 2. `openclaw devices`(設備 pairing / token)

管設備的 pairing token 與 device identity。子指令會隨版本有微調,跑 `--help` 看
當下的細項。

通用:列、加、移除設備、輪換設備 token。

```bash
openclaw devices --help
openclaw devices list           # 看當前 device 認證狀態
```

iOS / mobile pairing 走 QR:

```bash
openclaw qr                     # 在 gateway 機產 QR(在手機上掃)
```

---

## 3. `openclaw nodes`(從 gateway 操作 node)

### 3A. 看清單

```bash
openclaw nodes status                          # 列 + 即時狀態
openclaw nodes list                            # 比較簡潔的列
openclaw nodes list --connected                # 只看當前連線
openclaw nodes list --last-connected 1h        # 1 小時內有連的
openclaw nodes describe --node <id|name|ip>    # 看單一 node 細節
```

### 3B. Pairing(批准 / 拒絕)

新 node 連上來會進 pending,要在 gateway 端 approve:

```bash
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes reject <requestId>
```

approve 之後 node 才能被遙控。

### 3C. 重命名

```bash
openclaw nodes rename --node <id|name|ip> --name "Living Room Pi"
```

### 3D. Invoke 任意 command(advanced)

```bash
openclaw nodes invoke \
  --node <id> \
  --command <command-name> \
  [--params <json>] \
  [--invoke-timeout <ms>] \
  [--idempotency-key <key>]
```

`--idempotency-key` 對冪等性指令很有用(網路重試不會重複動作)。

### 3E. 在 node 上跑 shell

```bash
openclaw nodes run --node <id> \
  [--cwd <path>] [--env KEY=VAL] \
  [--command-timeout <ms>] [--needs-screen-recording] \
  -- <command...>
```

> **這是高權限操作**。一行就能在邊緣機跑任何指令。**走 destructive.md 的確認流程**,
> 尤其是不熟的 node 或共用設備上。

### 3F. macOS 推播(只在 mac node)

```bash
openclaw nodes notify --node <mac-id> \
  --title "..." --body "..." \
  [--sound default] \
  [--priority passive|active|timeSensitive] \
  [--delivery system|overlay|auto]
```

### 3G. Camera(iOS / Android 手機 node 為主)

```bash
# 列攝像頭
openclaw nodes camera list --node <id>

# 拍一張
openclaw nodes camera snap --node <id> \
  [--facing front|back|both] \
  [--device-id <id>] [--max-width <px>] [--quality 0-1] [--delay-ms <ms>]

# 錄一段(影片)
openclaw nodes camera clip --node <id> \
  [--facing front|back] [--device-id <id>] \
  [--duration 10s] [--no-audio]
```

### 3H. Canvas(顯示介面)

把網頁 / a2ui jsonl 推到 node 的「畫布」上:

```bash
openclaw nodes canvas snapshot --node <id> [--format png|jpg] [--max-width <px>]
openclaw nodes canvas present --node <id> --target <urlOrPath> [--x] [--y] [--width] [--height]
openclaw nodes canvas hide --node <id>
openclaw nodes canvas navigate <url> --node <id>
openclaw nodes canvas eval --node <id> --js "<javascript>"

# A2UI(structured UI)
openclaw nodes canvas a2ui push --node <id> --jsonl ./ui.jsonl
openclaw nodes canvas a2ui push --node <id> --text "..."
openclaw nodes canvas a2ui reset --node <id>
```

### 3I. Screen(桌面截/錄)

```bash
openclaw nodes screen record --node <id> \
  [--screen 0] [--duration 10s] [--fps 30] [--no-audio] [--out ./out.mp4]
```

### 3J. Location(設備定位)

```bash
openclaw nodes location get --node <id> \
  [--max-age 60000] \
  [--accuracy coarse|balanced|precise] \
  [--location-timeout 10000]
```

> **隱私敏感**:取手機定位前先確認使用者授權,不要當常規 polling 跑。

---

## 4. 完整 Playbook:從零接一台新 node

**情境**:你有一台新的 Raspberry Pi 要接到既有 gateway。

### 步驟 1 — 在 Pi 上裝 OpenClaw 並起 node host

```bash
ssh pi@<pi-host> "sudo npm i -g openclaw@latest"
ssh pi@<pi-host> "openclaw node install \
  --host <gateway-host> --port 18789 \
  --tls --tls-fingerprint <sha256> \
  --display-name 'Garage Pi'"
ssh pi@<pi-host> "openclaw node status"
```

Fingerprint 怎麼拿:在 gateway 機跑 `openclaw gateway probe --json` 或看 TLS cert。

### 步驟 2 — 在 gateway 上批准

```bash
# 在 gateway 機上
openclaw nodes pending           # 看新請求
openclaw nodes approve <id>
openclaw nodes status            # 確認進 connected
```

### 步驟 3 — 驗收

```bash
openclaw nodes describe --node <id>
openclaw nodes run --node <id> --command-timeout 5000 -- uname -a
# 若是手機:openclaw nodes camera list --node <id>
```

### 步驟 4 — 命名

```bash
openclaw nodes rename --node <id> --name "garage-pi"
```

---

## 5. Debug node 出問題

### 5A. 「Node 不在 nodes list 裡」

1. `ssh pi@... "openclaw node status"` —— node host 真的在跑?
2. Node host 連得到 gateway 嗎?(網路、防火牆、TLS fingerprint)
3. 看 node 那台的 service log(`journalctl --user -u openclaw-node` 或 launchd plist)
4. Gateway 那台 `gateway probe`:port 有沒有開、bind mode 對不對(loopback 只能本機;
   要遠端 node 連進來要 `lan` 或 `tailnet`)

### 5B. 「Node 卡 pending,approve 沒反應」

1. `nodes pending` 看 pending 是否真的存在
2. `nodes approve <id>` 後 `nodes status`,該 node 應該變成 connected
3. 還是不行 → 看 gateway log;node 那台的 fingerprint 對不對(MITM 防護會擋)

### 5C. 「Invoke 超時 / Run 不回」

1. `--invoke-timeout` 加大
2. Node 那台 CPU / disk 滿不滿
3. `--needs-screen-recording`:macOS 要在 System Settings 給 screen recording 權限

### 5D. 「Camera/Canvas/Screen 不動」

- 手機 node 通常要 app 開著或在背景常駐(看平台政策)
- macOS canvas 要授權 Accessibility / Screen Recording
- 看 node 那台的 app log

---

## 6. 安全

- **Node 是 gateway 的延伸**。Gateway 上的權限漏洞會擴散到所有 node。Gateway 收緊,
  node 才安全
- **TLS fingerprint 一定要釘** —— `--tls-fingerprint <sha256>`。沒釘等於信任任何
  自稱是 gateway 的東西
- **`nodes run` / `nodes invoke`** 是**任意 exec**,走 `references/destructive.md`
  的二次確認流程
- **camera/screen/location** 是隱私敏感能力。常規 polling 之前讓使用者明確同意
- **離開設備時要 `nodes` 那邊把它移掉**(或 token rotate),不要把舊機留在 list 上
