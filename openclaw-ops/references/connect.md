# 連線設定:本機 vs SSH

這份 skill 兩種環境都支援。差別**只在指令怎麼跑到目標機器上**;後面的 runbook 是
一樣的。

---

## 0. 開門先問

> 「要操作的 OpenClaw 是跑在**本機**,還是要 **SSH 連到別台**?」

依答案走下面對應分支。

---

## 1. 本機

直接用本機 shell。沒有額外步驟。

```bash
openclaw --version
openclaw doctor
cat ~/.openclaw/openclaw.json
```

注意:Claude Code 在 Windows 機器上不一定有 `openclaw` 的 PATH。先測:

```powershell
where.exe openclaw
# 或
openclaw --version
```

找不到的話,別用 Bash 工具瞎跑;問使用者實際安裝位置(常見:
`%APPDATA%\npm\openclaw.cmd`、`~/.local/share/pnpm`、`~/Library/pnpm/bin/openclaw`)。

---

## 2. SSH 遠端

### 2A. 收集連線資訊

向使用者問齊:

1. **主機**:IP 或域名
2. **port**(預設 22)
3. **登入帳號**
4. **驗證方式**:
   - **SSH 金鑰**(最推薦):金鑰路徑,或對方 `~/.ssh/config` 裡的 Host 別名
   - **既有 SSH config Host 別名**(也很好):直接用 `ssh <alias>`
   - **密碼**:可接受,但要提醒使用者:「密碼會出現在這段對話與下面的指令中,
     建議事後考慮改用 SSH 金鑰」。不要拒絕協助,但要讓對方知情

**處理憑證的硬規則**:

- 拿到金鑰路徑/密碼後**只用於建立連線**
- **絕不**寫進任何檔案、log,或在後續回覆裡複述
- 用完丟掉;不寫進 memory

### 2B. 連線測試

跑一個 cheap 指令確認連得上 + `openclaw` 也找得到:

```bash
ssh <target> "openclaw --version && uname -a"
```

連不上就先解決連線,不要硬往下做。常見原因:

- SSH key 沒授權(對方 `~/.ssh/authorized_keys` 沒加)
- 對方 SSH port 不是 22(`ssh -p <port>`)
- known_hosts fingerprint 不符(`ssh-keyscan` 後加進去)
- 對方 `openclaw` 不在登入 shell 的 PATH(SSH 跑的是 non-interactive shell)

#### 解 PATH 問題

SSH 跑的 non-interactive shell 通常不會 source `~/.bashrc` / `~/.zshrc`,所以
`pnpm`/`npm global` 安裝的 `openclaw` 可能找不到。三招:

```bash
# 1) 看哪裡有
ssh <target> "command -v openclaw || ls ~/.local/bin/openclaw ~/Library/pnpm/openclaw 2>/dev/null"

# 2) 用 login shell 跑
ssh <target> "bash -lc 'openclaw --version'"

# 3) 直接給絕對路徑
ssh <target> "~/.local/bin/openclaw --version"
```

如果是 system-wide 安裝(`sudo npm i -g openclaw`),`/usr/local/bin/openclaw`
應該都找得到。

### 2C. 建立 reusable 連線(避免每次都認證)

每跑一個 `ssh` 都重新認證很慢,密碼模式更會被問到爆。用 ControlMaster:

```bash
# 第一次建好控制 socket,跑在背景
ssh -M -S /tmp/oc-ssh-%r@%h:%p -fN \
  -o ControlPersist=10m \
  -o ServerAliveInterval=30 \
  <target>

# 之後每個指令都複用這個 socket
ssh -S /tmp/oc-ssh-%r@%h:%p <target> "openclaw doctor"
ssh -S /tmp/oc-ssh-%r@%h:%p <target> "openclaw status --deep"

# 任務結束關閉
ssh -O exit -S /tmp/oc-ssh-%r@%h:%p <target>
```

或者寫進 `~/.ssh/config`(更好,持久化):

```
Host oc-host
  HostName <ip-or-domain>
  User <user>
  Port 22
  IdentityFile ~/.ssh/<key>
  ControlMaster auto
  ControlPath ~/.ssh/cm-%r@%h:%p
  ControlPersist 10m
  ServerAliveInterval 30
```

之後 `ssh oc-host "openclaw status"` 就行。

### 2D. 密碼登入(只在使用者要求時)

如果使用者只能用密碼,用 `sshpass`(本機要先裝)。密碼會短暫出現在指令中,操作
完不要留存,**不要 echo 出來,不要寫進檔案**:

```bash
# 密碼從 env 來(較好)
SSHPASS='<password>' sshpass -e ssh <user>@<host> "openclaw --version"

# 密碼從檔案讀(用完刪)
sshpass -f /tmp/oc-pw ssh <user>@<host> "openclaw --version"
rm -f /tmp/oc-pw
```

不要把密碼當 inline argument(`sshpass -p`),它會留在 process list 與 shell history。

---

## 3. 在 SSH 上做檔案讀寫

### 3A. 讀

```bash
ssh oc-host "cat ~/.openclaw/openclaw.json"
ssh oc-host "ls -la ~/.openclaw/"
```

### 3B. 寫

不要 inline echo 大檔(quoting hell + 機密問題)。用 stdin 餵:

```bash
# 本機產草稿
nano /tmp/openclaw.json.draft   # 或讓 Claude 自己 Write 出來

# 推到遠端臨時檔
ssh oc-host "tee ~/.openclaw/openclaw.json.new > /dev/null" < /tmp/openclaw.json.draft

# 在遠端做備份 + atomic move
ssh oc-host "cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-\$(date +%Y%m%d-%H%M%S) && mv ~/.openclaw/openclaw.json.new ~/.openclaw/openclaw.json"

# 驗證
ssh oc-host "openclaw config get gateway"
```

或用 `scp`:

```bash
scp /tmp/openclaw.json.draft oc-host:~/.openclaw/openclaw.json.new
ssh oc-host "mv ~/.openclaw/openclaw.json.new ~/.openclaw/openclaw.json"
```

`rsync` 也行;檔案小就用上面任一個。

### 3C. 編輯既有檔(小改)

優先用 `openclaw config set`,它會幫你保持 JSON5 格式正確 + 不漏寫 runtime defaults:

```bash
ssh oc-host "openclaw config set gateway.port 18789"
ssh oc-host "openclaw config get gateway.port"
```

只有當需要批次改多個 key 或新增複雜結構時才碰原檔。

---

## 4. SSH 上跑互動式指令

幾個 OpenClaw 指令需要 TTY(prompt/QR/掃碼):

- `openclaw onboard`
- `openclaw configure`
- `openclaw channels login --channel whatsapp`(掃 QR)
- `openclaw doctor`(沒帶 `--non-interactive` 或 `--yes` 時會問)
- `openclaw reset` / `openclaw uninstall`(沒帶 `--yes` 時會問)

在 SSH 上跑這些要分配 PTY:

```bash
ssh -t oc-host "openclaw channels login --channel whatsapp"
```

注意:`ssh -t` 與背景化(`&` / `nohup`)不相容。QR 模式必須是前景。

### 規避互動的旁路

很多互動指令有 non-interactive flag:

| 互動指令 | 非互動旁路 |
|---|---|
| `onboard` | `--non-interactive` + 完整 flag 組 |
| `configure` | `openclaw config set <path> <value>` 一個個設 |
| `doctor` | `--yes` 接受預設;`--non-interactive` 只跑安全 migration |
| `reset` | `--non-interactive --scope <s> --yes` |
| `uninstall` | `--non-interactive --yes` + 明確 scope |
| WhatsApp login | **無旁路**;必須在 TTY 跑掃 QR |

---

## 5. 連線收尾

任務結束(或要交回給使用者)時:

1. 跑 `openclaw doctor` 或 `openclaw status` 確認狀態正常
2. 關 ControlMaster socket:`ssh -O exit oc-host`
3. 刪所有暫存密碼檔(`rm -f /tmp/oc-pw*`)
4. 不要把連線資訊複述到對話裡

---

## 6. 故障排除速查

| 症狀 | 可能原因 | 處理 |
|---|---|---|
| `ssh: Permission denied (publickey,password)` | 金鑰沒授權 / 帳號錯 / 對方 sshd 設定限制 | 確認 user@host、金鑰路徑、`PubkeyAuthentication yes` 與 `PasswordAuthentication` 設定 |
| `ssh: Host key verification failed` | known_hosts fingerprint 變了(對方重裝/IP 更換) | `ssh-keygen -R <host>` 然後重連,**並確認 fingerprint 是預期的**(別盲目接受) |
| `command not found: openclaw` 在 SSH 上 | non-interactive shell 沒有對應 PATH | 用 `bash -lc` 或絕對路徑 |
| WhatsApp login 在 SSH 上 QR 不顯示 | 沒分配 PTY | `ssh -t`;若 QR 還是亂掉,讓使用者改在那台終端直接看 |
| 重啟 gateway 後 SSH 斷線 | gateway 跟 SSH 沒關係 — 真正斷的是網路 / sshd | 用 ControlMaster + ServerAliveInterval 提早察覺 |
| ControlMaster socket 卡住 | 上次沒乾淨關 | `ssh -O exit <target>`;或直接刪 socket 檔 |
