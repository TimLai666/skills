---
name: windows-rescue-from-linux
description: Use when repairing a broken Windows PC from a Linux Live USB. Handles boot failure, BCD or UEFI corruption, NTFS damage, lost partitions, forgotten passwords, malware infection, profile corruption, BitLocker decryption, failing disks, and data backup before destructive repair. Also bootstraps the rescue USB itself with Node.js, Claude Code, and tools like ntfsfix, chntpw, testdisk, photorec, ddrescue, smartctl, clamav, dislocker, efibootmgr. Trigger on Windows 開不了機, BSOD 救援, 救資料, BitLocker, chntpw, ntfsfix, testdisk, photorec, ddrescue, BCD 修復, 重設 Windows 密碼, 離線掃毒, 隨身碟救援系統, Live USB rescue Windows, fix Windows from Ubuntu, 把 Ubuntu 弄成救援碟, 救援工具安裝. Default language is Traditional Chinese for Taiwan.
metadata:
  version: "1.0.0"
---

# Windows 救援工具箱（從 Linux Live USB 修 Windows）

這個 skill 假設你已經處在一個從隨身碟開機的 Linux 環境（Ubuntu / Debian / SystemRescue 都可以），目標是修一台壞掉的 Windows 電腦——它可能無法開機、藍底白字、忘記密碼、感染惡意軟體、或硬碟正在壞掉。

你（Claude / Codex）跑在 Linux 上，沒辦法用 Windows 內建的 sfc、DISM、chkdsk、WinRE。你的工具是 Linux 那邊的 `ntfsfix`、`chntpw`、`testdisk`、`photorec`、`ddrescue`、`smartctl`、`clamav`、`dislocker`、`efibootmgr`、`hivexsh` 這些。這份 skill 就是怎麼把這套工具組合起來解決 Windows 問題。

完整工具目錄（含安裝指令、用途、典型範例）見 [`references/14-cli-tools-catalog.md`](references/14-cli-tools-catalog.md)。

---

## 🚀 階段零：Bootstrap 環境檢查（每次 skill 啟動先跑）

> **這是 agent 進入這個 skill 時的第一件事**。在問使用者症狀之前，先確認自己手上的工具齊不齊。

跑體檢腳本：

```bash
bash scripts/bootstrap-check.sh
```

腳本會回報核心工具（ntfsfix / chntpw / testdisk / photorec / ddrescue / smartctl ...）、Node.js / Claude Code 是否齊全、有無網路、是不是在 Live USB 環境。

### 根據結果決定下一步

| 體檢結果 | agent 該做什麼 |
|---|---|
| **全部 ✓** | 直接跳到下面「動手前必讀」、開始問使用者症狀 |
| **核心工具缺 + 有網路** | 跟使用者說「你的救援環境少了 X、Y、Z，要我跑 `sudo bash scripts/install-rescue-tools.sh` 一次裝完嗎？」得到明確 yes 才執行 |
| **核心工具缺 + 沒網路** | 告訴使用者：(1) 可以開手機熱點；(2) 從 USB 上的 `offline-binaries/` 用 dpkg 裝（見 `00-rescue-usb-preparation.md §9`）；(3) 純人工照 reference 操作 |
| **Node.js 缺** | 提示使用者目前是用什麼方式跟 agent 對話（可能是另一台機 SSH 進來），看要不要在這台 Live USB 也裝個 Claude Code |
| **Skill 沒在 ~/.claude/skills/** | 提醒使用者 symlink 過去，下次開新 Claude Code 才會自動載入 |

### 安裝救援工具的指令

```bash
# 互動式（每塊問一次，推薦）
sudo bash scripts/install-rescue-tools.sh

# 只裝核心
sudo bash scripts/install-rescue-tools.sh --core

# 含 Node.js + Claude Code
sudo bash scripts/install-rescue-tools.sh --with-node

# 全裝（不問）
sudo bash scripts/install-rescue-tools.sh --full
```

詳細的 USB 準備、Node.js 多種安裝法、Claude Code / Codex 安裝、離線備援見 [`references/00-rescue-usb-preparation.md`](references/00-rescue-usb-preparation.md)。

### Agent 行為原則

- **不要默默安裝**：每次裝套件都先問使用者「我要跑 X 指令，會花約 Y 分鐘、占用 Z MB 空間。可以嗎？」
- **節省網路**：如果使用者只想解決一個小問題（例如改密碼），不用堅持把全套救援工具裝完。`chntpw` 一個套件就夠
- **善用 tmux**：要跑 `ddrescue`、`photorec` 等長時間任務，永遠先 `tmux new -s rescue` 包起來。SSH 斷線 / Live USB 死機都不會把任務毀掉

---

## ⚠️ 動手前必讀（鐵則）

這幾條鐵則任何狀況都不能違反，違反一次可能就把資料毀掉：

1. **先讀後寫**：第一次掛載 Windows 磁碟一律 `ro`（read-only）。確認資料還在、症狀對得上，才考慮可寫掛載。
2. **動手前先備份**：任何寫入動作（ntfsfix、chntpw、删 pending.xml、清病毒）之前，至少把使用者重要資料 `rsync` 到外接碟。硬碟有 SMART 警告時，先 `ddrescue` 做整碟映像再說。
3. **掛載中的磁碟不要修**：`ntfsfix`、`fsck`、`testdisk` 寫入模式，這些都要先 `umount`。
4. **BitLocker 沒有金鑰先停手**：如果是 BitLocker 加密磁碟而使用者拿不出 recovery key，硬幹只會多寫垃圾資料。先去 https://account.microsoft.com/devices/recoverykey 找。
5. **碟正在死別硬讀**：SMART 顯示有 reallocated/pending sector，或讀的時候卡死、有怪聲——立刻停掉，改用 `ddrescue` 做映像，之後在映像上動。原碟每多讀一次都可能把僅存的好磁區也死掉。
6. **改 registry 前先複製整個 hive**：`cp SAM SAM.bak` 再 `chntpw`。
7. **跟使用者確認再執行有破壞性的步驟**：「我接下來要把 hiberfil.sys 刪掉以便正常掛載，你確定 Windows 不需要保留待機狀態嗎？」這種確認永遠值得問。

詳細的安全清單見 `references/01-safety-principles.md`。

---

## 工作流程

每次救援都照這個五階段走，不要跳：

### 階段一：盤點環境

先弄清楚你在哪、目標在哪、有什麼工具：

```bash
# 確認自己在 live USB 環境
cat /etc/os-release
lsb_release -a 2>/dev/null

# 列出所有磁碟和分割區
lsblk -f -o NAME,FSTYPE,LABEL,SIZE,MOUNTPOINT,UUID
sudo fdisk -l
sudo parted -l

# 確認檔案系統類型（NTFS / FAT32 / BitLocker）
sudo blkid

# 確認是 UEFI 還是 Legacy BIOS 模式開機
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "Legacy BIOS"
```

把結果留下來——你要知道：
- Windows 系統碟在哪個 `/dev/sdX` 或 `/dev/nvmeXnY`（通常是最大的 NTFS）
- 有沒有 EFI 分割區（FAT32, ~100-500MB）
- 有沒有 Recovery 分割區
- 有沒有 BitLocker（`blkid` 會顯示 `TYPE="BitLocker"`）
- 內部碟健康狀態（`sudo smartctl -H /dev/sdX`，不健康就先別動）

### 階段二：症狀分流（重要）

問使用者實際發生什麼事，照下面的「症狀 → 修復路徑」對應表決定要讀哪個 reference。**不要一次讀全部**，只讀對應的那幾個。

### 階段三：備份

幾乎所有情況都先做這一步。最少：

```bash
# 唯讀掛載
sudo mkdir -p /mnt/win
sudo mount -t ntfs-3g -o ro /dev/sdX1 /mnt/win

# 備份使用者資料夾到外接碟
sudo rsync -avh --info=progress2 \
    /mnt/win/Users/USERNAME/ \
    /media/USERNAME/external/backup-$(date +%Y%m%d)/
```

碟有疑慮時改用 `ddrescue`（見 `references/08-data-recovery.md`）。

### 階段四：修復

讀對應的 reference 後執行。每動一個破壞性指令都跟使用者覆述一次再執行。

### 階段五：驗證

修完先別重開 Windows，先在 Linux 這邊確認結果：

```bash
# 重新檢查檔案系統
sudo umount /mnt/win
sudo ntfsfix --no-action /dev/sdX1   # dry-run
sudo ntfsfix /dev/sdX1

# 重新看 SMART
sudo smartctl -a /dev/sdX

# 看 BCD / EFI 結構
ls /mnt/efi/EFI/Microsoft/Boot/
```

之後請使用者重開機並回報狀況。如果還是壞，回到階段二重新分流——但這次有了更多線索。

---

## 症狀 → 修復路徑

> 找最接近使用者描述的那一行，讀對應的 reference 檔。多個症狀疊加時，**先處理優先級高的那個**（B級＞A級）。

### B 級：先救命的（硬體 / 加密 / 資料）

| 症狀 | 優先讀 |
|---|---|
| 硬碟有怪聲、讀取卡死、SMART 警告 | `08-data-recovery.md` → 先 `ddrescue` 做映像 |
| BitLocker 加密、需要進到資料 | `10-bitlocker.md` |
| 「我只想救資料，不修了」 | `08-data-recovery.md` |
| 想救已刪除的檔案 | `08-data-recovery.md` →「PhotoRec / testdisk undelete」 |

### A 級：開機 / 系統層級

| 症狀 | 優先讀 |
|---|---|
| 開機顯示 BOOTMGR is missing / Operating System not found | `04-boot-repair.md` |
| 開機卡在 Windows logo、轉圈無限轉、自動修復失敗 | `04-boot-repair.md` + `05-filesystem-repair.md` |
| UEFI 找不到 Windows Boot Manager | `04-boot-repair.md` →「UEFI / efibootmgr」 |
| 雙系統裝完 Linux 後 Windows 不見了 | `04-boot-repair.md` →「dual boot 修復」 |
| 反覆藍底白字（BSOD）、`INACCESSIBLE_BOOT_DEVICE` | `05-filesystem-repair.md` + `11-driver-and-update-issues.md` |
| Windows Update 安裝失敗無限重啟 | `11-driver-and-update-issues.md` →「移除 pending.xml」 |
| 磁碟分割表壞掉、看不到 Windows 分割區 | `05-filesystem-repair.md` →「testdisk 修分割表」 |

### A 級：帳號 / 設定檔

| 症狀 | 優先讀 |
|---|---|
| 忘記 Windows 密碼 | `06-registry-edit.md` →「password reset (chntpw)」 |
| 帳號被鎖住 / 停用 | `06-registry-edit.md` →「帳號狀態」 |
| 想啟用隱藏的 Administrator | `06-registry-edit.md` →「啟用內建管理員」 |
| 登入後桌面空白、只看到暫存設定檔 | `12-profile-corruption.md` |
| 「使用者設定檔服務登入失敗」 | `12-profile-corruption.md` |

### A 級：惡意軟體

| 症狀 | 優先讀 |
|---|---|
| 中毒 / 勒索病毒 / 開機就跳廣告 | `07-malware-cleanup.md` |
| 瀏覽器被綁架、hosts 被改 | `07-malware-cleanup.md` →「hosts 與 DNS 還原」 |
| 怪怪的程式每次開機自動啟動 | `07-malware-cleanup.md` →「自動啟動清理」 |

### A 級：檔案系統 / 硬體

| 症狀 | 優先讀 |
|---|---|
| `ntfs-3g` 掛載失敗 / 提示 hibernated | `03-mount-windows.md` |
| 磁碟容量怪、檔案開啟錯誤、隨機檔案消失 | `05-filesystem-repair.md` + `09-hardware-diagnostics.md` |
| 想知道 RAM/CPU/SSD 健康度 | `09-hardware-diagnostics.md` |
| 系統很慢、想知道是不是硬碟壞了 | `09-hardware-diagnostics.md` |

### 不知道發生什麼事

跑 `scripts/boot-diagnostic.sh`，它會收集 BCD、EFI、最近的事件日誌（透過 chntpw + python），然後給你一個摘要。

---

## Reference 檔索引

> 按需讀取，不要一次全部讀。

| 檔案 | 內容 |
|---|---|
| `00-rescue-usb-preparation.md` | 怎麼準備這支救援碟（USB、Ubuntu、套件、**Node.js / Claude Code / Codex 安裝**、離線備援） |
| `01-safety-principles.md` | 詳細安全清單、什麼時候該停手 |
| `02-symptom-triage.md` | 更細的症狀分流（含罕見組合） |
| `03-mount-windows.md` | 掛載 NTFS、處理 hibernation、fast startup、BitLocker 偵測 |
| `04-boot-repair.md` | UEFI / BCD / MBR / EFI 分割區、雙系統修復 |
| `05-filesystem-repair.md` | ntfsfix、testdisk 修分割表、partition undelete |
| `06-registry-edit.md` | chntpw 密碼重設、hivexsh 編輯、停用問題服務 |
| `07-malware-cleanup.md` | clamav 離線掃描、autorun 清理、hosts 還原、排程工作檢查 |
| `08-data-recovery.md` | rsync 備份、ddrescue 映像、PhotoRec 救刪除檔、testdisk undelete |
| `09-hardware-diagnostics.md` | smartctl、badblocks、memtester、lshw、sensors |
| `10-bitlocker.md` | dislocker 完整流程、recovery key 取得方式 |
| `11-driver-and-update-issues.md` | pending.xml、SoftwareDistribution、問題 driver 移除 |
| `12-profile-corruption.md` | NTUSER.DAT、ProfileList registry、重建使用者資料夾 |
| `13-when-linux-cannot-fix.md` | 這些問題 Linux 救不了，要請使用者準備 Windows 安裝媒體 |
| **`14-cli-tools-catalog.md`** | **完整 CLI 工具目錄：每個工具的 apt 安裝、用途、典型指令、限制（agent 想找工具先翻這份）** |

---

## Scripts 索引

scripts 是可直接執行的輔助工具，每個都會列印它要做什麼、等你確認：

| Script | 用途 |
|---|---|
| **`bootstrap-check.sh`** | **環境體檢（不安裝，只回報）。agent 進 skill 第一個跑這個** |
| `install-rescue-tools.sh` | 在剛開機的 Ubuntu Live 上一次裝完所有工具 + Node.js + Claude Code / Codex（支援 `--core` / `--with-node` / `--full` / `--auto`） |
| `identify-windows-volumes.sh` | 自動偵測哪一個分割區是 Windows 系統、EFI、Recovery |
| `mount-windows-safe.sh` | 安全掛載（先 ro，處理 hibernation） |
| `backup-user-data.sh` | 使用者資料夾備份到外接碟，帶進度條 |
| `disk-health-report.sh` | 一次性出健康度報告（SMART + badblocks dry-run） |
| `boot-diagnostic.sh` | 收集 BCD/EFI/registry 開機相關資訊出摘要 |
| `malware-quick-scan.sh` | clamav 更新病毒碼後針對常見路徑掃描 |

---

## 跟使用者互動的原則

1. **先問症狀，不要先動手**：使用者說「不能開機」要再問「卡在哪一個畫面、有沒有錯誤代碼、什麼時候開始的、最近有沒有更新或裝什麼東西」。同樣是不能開機，BCD 損壞、NTFS 損壞、硬碟壞掉的修法完全不同。
2. **每個 `sudo` 指令都先解釋**：使用者可能不熟 Linux。「我要跑 `sudo ntfsfix /dev/sda3`，這會嘗試修 NTFS 上的小毛病，如果碟有實體損壞它會中止不會把事情弄更糟。要繼續嗎？」
3. **destructive 動作要兩段式確認**：第一次說明會做什麼、影響什麼、是否可逆；使用者答 yes 後第二次覆述指令再執行。
4. **修不完不要硬修**：有些東西（深層 WinSxS 損壞、特定 driver 黑屏）Linux 救不了，老實告訴使用者「這部分需要 Windows 安裝媒體進 WinRE 跑 sfc/DISM」，見 `13-when-linux-cannot-fix.md`。
5. **記錄做過什麼**：每修一個地方就寫到 `/tmp/rescue-log-$(date +%Y%m%d).md`，使用者之後送修才有東西給技師看。

---

## 預設語言

繁體中文（台灣）。指令、檔名、技術名詞保留英文。錯誤訊息引用時保留原文再附中譯。
