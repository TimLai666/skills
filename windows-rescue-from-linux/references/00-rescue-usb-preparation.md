# 00 · 救援碟準備 + Bootstrap

> **這份要做的事**：把一支 USB 隨身碟做成「裝好工具的救援碟」。一次做好以後拿著就能修任何 Windows。
>
> **本份文件分三層**：
> 1. **§1-3**：實體準備（USB、Ubuntu Live、必裝套件）
> 2. **§4-6**：Node.js + Claude Code + Codex 安裝（讓 AI agent 在 USB 上能跑）
> 3. **§7-9**：把這個 skill 裝進 Claude Code、驗證、離線備援

---

## 1. 硬體需求

- **USB 3.0 隨身碟**，建議 **64GB 以上**（要塞 Ubuntu + 工具 + persistence + Windows ISO）
- 32GB 也能用但很擠，16GB 不夠
- **品質很重要**：救援時讀寫很頻繁，廉價碟容易壞。SanDisk Extreme / Samsung BAR / Kingston DataTraveler Max 等 USB 3.2 規格穩
- **另一支 USB 或外接硬碟**專用來放備份出來的資料，救援碟不該變成倉庫
- **可選**：手機網路熱點（無線網路裝完套件時要用）

---

## 2. 做一支 Ubuntu Live USB

兩種做法，**強烈推薦做法 A（Ventoy）**：

### 做法 A：Ventoy 多開機 + persistence（最有彈性）

優點：同一支 USB 能塞多個 ISO（Ubuntu + Kaspersky Rescue + Hiren's PE + Windows ISO），開機選單挑。

**準備（在另一台健康電腦做）：**
1. 下載 Ventoy：https://www.ventoy.net/
2. 跑 `Ventoy2Disk.sh` 或 `Ventoy2Disk.exe`，把 USB 格式化成 Ventoy 格式
3. 下載 [Ubuntu 24.04 LTS Desktop ISO](https://ubuntu.com/download/desktop)
4. **直接把 .iso 複製到 USB**（Ventoy 把整支 USB 當 ISO 倉庫，不用解壓）

**開 persistence 讓改動保留下來：**
- Ventoy 預設 Live 模式重開會清空。要保留套件安裝必須建 persistence 檔。
- Ubuntu：建 `ubuntu.dat` 同名 persistence 檔（用 `Ventoy/CreatePersistentImg.sh`）
- 詳見 Ventoy 官網「Persistence」章節

**也順便丟下去的 ISO（建議）：**
- `kasperskyrescue.iso` — Kaspersky 救援碟，掃毒能力遠勝 ClamAV
- `Win11_24H2_TraditionalChinese_x64.iso` — Windows 安裝媒體（Linux 修不了時切過去走 WinRE）
- `systemrescue-amd64.iso` — 預裝救援工具的 distro，備援

### 做法 B：直接把 Ubuntu 安裝到 USB（更穩定但失彈性）

```
1. 用 Ubuntu ISO 開機
2. 選 Install Ubuntu
3. 在「Installation type」選 Something else（手動）
4. 把目標「安裝裝置」和「bootloader 安裝位置」都選到 USB
   ⚠ 千萬不要選到主機硬碟！
5. 走完安裝，下次用 USB 開機就跟一般 Ubuntu 一樣（可裝套件、改設定、留檔）
```

優點：每次開機環境一致，Claude Code / Codex / API key 都會保留。
缺點：USB 損耗較大、不能裝其他 ISO。

---

## 3. 第一次開機 + 裝套件

開機後選 **Try Ubuntu**（不要 Install），進到桌面後開 Terminal，**確認有網路**（手機熱點或網路線都行），然後：

### 最快做法：用我們的腳本

```bash
# 假設這個 skill 資料夾已經放在 USB 上
cd ~/windows-rescue-from-linux  # 或你解壓的位置
sudo bash scripts/install-rescue-tools.sh
```

腳本會：
1. 更新 apt
2. 一次裝所有救援工具（NTFS / chntpw / testdisk / ddrescue / smartctl / clamav / dislocker / efibootmgr / hivexsh ...）
3. 初始化 ClamAV 病毒碼
4. 偵測溫度感應器
5. 驗證每個工具可用

### 手動做法（懶人一行）

```bash
sudo apt update && sudo apt install -y \
    ntfs-3g chntpw libhivex-bin testdisk gddrescue \
    smartmontools nvme-cli hdparm \
    parted gdisk dosfstools mtools partclone \
    efibootmgr grub-efi-amd64-bin grub-common os-prober \
    clamav clamav-freshclam rkhunter \
    dislocker fuse3 cryptsetup \
    foremost p7zip-full \
    python3-evtx wimtools cabextract \
    tmux screen mc pv pigz rsync rclone \
    htop iotop nethogs \
    lshw hwinfo dmidecode pciutils usbutils inxi \
    lm-sensors memtester stress-ng \
    curl wget openssh-client magic-wormhole \
    vim nano less tree \
    python3-pip git build-essential
```

工具的詳細用途見 [14-cli-tools-catalog.md](14-cli-tools-catalog.md)。

---

## 4. 安裝 Node.js（Claude Code / Codex 必備）

Claude Code 和 Codex CLI 都是 npm 套件，**需要 Node.js 18 或更新**。Ubuntu 24.04 預設套件庫的 `nodejs` 版本可能太舊，建議走 NodeSource 拿穩定新版。

### 方法 A：NodeSource（推薦，最穩定）

```bash
# 加 NodeSource 的 apt repo（指定 Node 20.x LTS）
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# 裝 nodejs（npm 內建）
sudo apt install -y nodejs

# 驗證
node --version    # 應該 v20.x.x
npm --version     # 應該 10.x.x
```

### 方法 B：nvm（最有彈性，可切多版本）

```bash
# 裝 nvm（不需要 sudo，裝到 ~/.nvm）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新載入 shell（或開新 terminal）
source ~/.bashrc

# 裝 Node 20 LTS
nvm install 20
nvm use 20
nvm alias default 20

# 驗證
node --version
```

### 方法 C：apt 預設套件（最簡單但可能版本舊）

```bash
sudo apt install -y nodejs npm
node --version    # 確認 >= 18，太舊的話換方法 A
```

### 方法 D：直接 binary（離線備援）

如果救援當下沒網路、或 NodeSource 連不上：

```bash
# 在有網路的電腦先下載 binary tarball
wget https://nodejs.org/dist/v20.18.0/node-v20.18.0-linux-x64.tar.xz
# 複製到救援 USB

# 在 USB 上解壓到自己家目錄
mkdir -p ~/local
tar -xJf node-v20.18.0-linux-x64.tar.xz -C ~/local/
# 加進 PATH
echo 'export PATH="$HOME/local/node-v20.18.0-linux-x64/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 驗證
node --version
```

> **方法 D 是最重要的離線備援**。建議事前就先把 Node binary 放在救援 USB 上，現場沒網路也能起得來。

### npm 全域路徑設定（避免 sudo）

直接 `sudo npm install -g` 會把套件裝到 `/usr/local/lib`，下次 Live 開機可能消失。建議：

```bash
# 設定 npm 全域目錄在家目錄
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

之後 `npm install -g` 不用 sudo，也會跟著家目錄 persistence 保留。

---

## 5. 安裝 Claude Code

```bash
npm install -g @anthropic-ai/claude-code

# 驗證
claude --version
```

### 首次設定

```bash
claude
```

第一次跑會引導：
- **方式一**：用 Anthropic 帳號登入（適合 Claude Pro/Max 使用者）
- **方式二**：用 API key（從 https://console.anthropic.com 取得，pay-as-you-go）

設定檔位置：
- 認證：`~/.claude/.credentials.json`
- 設定：`~/.claude/settings.json`

**USB persistence 場景特別注意**：上面這些檔案要存在 USB 的 persistence 區，下次開機才會在。如果是 Ventoy persistence，預設家目錄就在 persistence 區，沒問題。

### 設定預設模型（可選）

```bash
# 在 ~/.claude/settings.json
{
  "model": "claude-opus-4-7"
}
```

救援場景建議用 Opus（推理品質好），Sonnet 也行（快、便宜）。

---

## 6. 安裝 Codex CLI（OpenAI，可選）

如果你習慣用 OpenAI 的 agent，或想兩個都裝來互相備援：

```bash
npm install -g @openai/codex

# 驗證
codex --version

# 首次跑會問 API key（從 https://platform.openai.com/api-keys 取得）
codex
```

兩個 CLI 並存沒問題，分別存在不同設定檔。救援時哪個有 quota / 連得上就用哪個。

---

## 7. 把這個 skill 裝進 Claude Code

```bash
# Claude Code 預設 skill 路徑
mkdir -p ~/.claude/skills

# 解壓 skill zip 到該位置
unzip ~/Downloads/windows-rescue-from-linux.zip -d ~/.claude/skills/

# 確認
ls ~/.claude/skills/windows-rescue-from-linux/SKILL.md
```

Claude Code 啟動後會自動掃描 `~/.claude/skills/`。跟它說「Windows 開不了機」「ntfsfix」「chntpw」「BitLocker 救援」等關鍵字就會載入這個 skill。

### Codex 的 skill 位置

Codex 的 skill 機制和 Claude Code 不同（截至 2026 年仍在演進）。最簡單作法：把整個 skill 資料夾放到專案根目錄，跟 Codex 說「讀 `windows-rescue-from-linux/SKILL.md` 並照它做」。

---

## 8. 驗證救援碟可用

裝完後一次性檢查：

```bash
# 工具齊全（不該有任何一行說「not found」）
for tool in ntfsfix chntpw hivexsh testdisk photorec ddrescue \
            smartctl clamscan dislocker efibootmgr rsync \
            tmux node claude; do
    if command -v "$tool" >/dev/null; then
        printf "  ✓ %-12s %s\n" "$tool" "$(command -v "$tool")"
    else
        printf "  ✗ %-12s MISSING\n" "$tool"
    fi
done

# ClamAV 病毒碼有更新（要網路）
sudo freshclam

# Node + Claude Code 通的
node --version
claude --version

# USB 自身健康
sudo smartctl -a /dev/sdX   # X = 你救援碟的字母（通常不是 USB 而是看不到 SMART，正常）
```

全部 ✓ 就 OK，這支救援碟可以走天下。

---

## 9. 離線備援（沒網路的現場）

很多救援場景到現場才發現沒網路（壞主機不能上、客戶網路壞、機房沒 Wi-Fi）。**事前準備好離線備援**：

### 9.1 預先下載的東西放在 USB 上

```
USB-root/
├── ventoy/                         # Ventoy 開機檔（自動產生）
├── ubuntu-24.04-desktop-amd64.iso  # 開機用
├── kasperskyrescue.iso             # 離線掃毒（不用網路病毒碼會舊但能用）
├── Win11_24H2_zh-TW_x64.iso        # Windows 安裝媒體
├── offline-binaries/
│   ├── node-v20.18.0-linux-x64.tar.xz   # Node binary（4.7 節方法 D）
│   ├── claude-code-offline.tgz          # npm pack 出來的 tarball
│   └── apt-cache/                       # 預先下載的 .deb 套件
└── windows-rescue-from-linux/      # 這個 skill 整包
```

### 9.2 預先快取 apt 套件

在有網路的環境執行一次：

```bash
# 把所有救援工具的 .deb 檔下載到一個資料夾（不安裝）
mkdir -p ~/apt-cache && cd ~/apt-cache
sudo apt update
sudo apt install --download-only -y \
    ntfs-3g chntpw libhivex-bin testdisk gddrescue \
    smartmontools dislocker fuse3 efibootmgr clamav \
    foremost python3-evtx tmux pv rsync

# .deb 都在 /var/cache/apt/archives/
cp /var/cache/apt/archives/*.deb ~/apt-cache/
# 把這資料夾複製到 USB
```

之後在沒網路的救援現場：

```bash
cd /media/$USER/Ventoy/offline-binaries/apt-cache
sudo dpkg -i *.deb
sudo apt-get install -f   # 修依賴關係
```

### 9.3 預先 `npm pack` Claude Code

在有網路的電腦：
```bash
npm install -g npm-pack-all
mkdir ~/claude-code-bundle && cd ~/claude-code-bundle
npm pack @anthropic-ai/claude-code
# 這會在當前目錄產生 anthropic-ai-claude-code-X.Y.Z.tgz
# 包含所有依賴
```

複製到 USB，之後離線安裝：
```bash
npm install -g ./anthropic-ai-claude-code-X.Y.Z.tgz
```

> **限制**：Claude Code 跑起來還是需要連 api.anthropic.com 才能對話。離線 install 解決的是「裝不起來」的問題，不是「沒網路也能對話」。

### 9.4 救援場景沒網路怎麼辦

如果**現場真的完全沒網路**而又需要 AI 協助：

1. **手機熱點分享**：救援時連手機 4G/5G 熱點
2. **預先離線討論**：之前先在有網路時跟 Claude 把要做的事討論完，存成步驟筆記 (.md)，到現場照著做
3. **走純人工**：照本份 skill 的 `references/` 文件操作（人類版救援手冊）

---

## 10. 額外建議

1. **建一個 `~/rescue-toolbox/` 資料夾**：放救援腳本、之前累積的紀錄、常用 registry 範本、客戶聯絡資訊等
2. **準備自己的測試環境**：找一台不重要的舊筆電或 VM 當練習對象。沒練過就在使用者實機上動容易出事
3. **印出緊急流程紙本**：BIOS 沒設好 USB 開機順序時連 Linux 都進不去，先把「進 BIOS → 改開機順序 → 從 USB 開機」這幾步印出來夾在 USB 旁
4. **記錄常見品牌的 BIOS 熱鍵**：
   - HP: F9 / Esc
   - Dell: F12
   - Lenovo: F12 / Nano Button
   - ASUS: F8 / Esc
   - Acer: F12
   - MSI: F11
   - Apple Mac: 開機按住 Option

---

## 11. Agent 自動 Bootstrap 模式

> **這節是給 AI agent（Claude Code / Codex）看的**

如果使用者剛把這個 skill 載進來，你（agent）應該主動檢查環境狀態。檢查順序：

```bash
# 1. 在哪？
cat /etc/os-release | head -3
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "Legacy"

# 2. 救援工具齊嗎？
for t in ntfsfix chntpw testdisk ddrescue smartctl efibootmgr dislocker; do
    command -v "$t" >/dev/null && echo "✓ $t" || echo "✗ $t MISSING"
done

# 3. Node.js + Claude Code（你自己）跑起來嗎？
node --version 2>/dev/null || echo "✗ Node.js MISSING"
which claude 2>/dev/null || echo "✗ Claude Code MISSING"

# 4. 有沒有網路？
ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1 && echo "✓ Internet" || echo "✗ No Internet"
```

根據結果：

| 狀況 | 你要主動做 |
|---|---|
| 工具有缺 + 有網路 | 問使用者是否要跑 `scripts/install-rescue-tools.sh`，得到 yes 就跑 |
| 工具有缺 + 沒網路 | 提醒使用者：「目前沒網路。可以開手機熱點，或從 USB 上的 offline-binaries 安裝。」 |
| Node 缺 + 你還能讀指令 | 表示你（agent）是用其他方式跑的（例如另一台機器 SSH）。提醒使用者裝 Node 的方式（§4 方法 A 或 D） |
| 全 OK | 進到 SKILL.md 的「症狀分流」階段 |

**不要默默裝東西**。每次裝套件都要先告訴使用者「我要跑 `sudo apt install ...`，這會花約 X 分鐘並占用 Y MB 空間。可以嗎？」

詳細的安全規則見 [01-safety-principles.md](01-safety-principles.md)。
