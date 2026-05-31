# 14 · CLI 工具完整目錄

> **這份文件做什麼**：把 Linux 上能修 Windows 的所有 CLI 工具集中一覽 —— 安裝指令、用途、典型範例、限制、何時用。當 agent 需要某類功能時，先翻這份找對的工具，再去 references 找詳細操作。
>
> **使用慣例**：所有 `sudo apt install -y <pkg>` 都假設 Ubuntu / Debian。RHEL / Arch 對應套件名請自查。

---

## 0. 必裝五大金剛（救 Windows 的核心）

這五個是 Linux 救 Windows 的核心，缺一不可。先把它們裝齊再說其他。

### `testdisk` —— 分割表修復 / 救已刪檔
```bash
sudo apt install -y testdisk
```
- **能做**：修壞掉的分割表（Windows 磁碟變成 RAW、看不到分割區）；undelete NTFS / FAT 上被刪除的檔案
- **典型用法**：`sudo testdisk /dev/sda` → 互動選單走 Analyse → Quick Search → 看分割區清單 → Write
- **限制**：互動式介面（用方向鍵 + Enter），不能 pipe；寫入前**一定**先 `sfdisk -d /dev/sda > sda.bak` 備份目前分割表
- **詳見**：[05-filesystem-repair.md](05-filesystem-repair.md)

### `photorec` —— 不靠檔案系統的檔案救援
```bash
sudo apt install -y testdisk   # photorec 包在 testdisk 套件裡
```
- **能做**：磁碟磁區層級掃描，靠檔案 signature（magic number）救檔。即使整個檔案系統壞掉、被格式化、表頭被覆蓋，只要實際資料還沒被新資料覆寫，就能撈回來
- **典型用法**：`sudo photorec /dev/sda` → 選分割區 → 選輸出目標（**必須在另一顆碟**） → 選檔案類型 → 等
- **限制**：不會還原檔名（變成 `f000001.jpg`）、不還原目錄結構；耗時很久（500GB 碟可能跑 6+ 小時）
- **詳見**：[08-data-recovery.md](08-data-recovery.md)

### `ddrescue` —— 壞軌硬碟救援
```bash
sudo apt install -y gddrescue
```
> 注意套件名是 `gddrescue` 不是 `ddrescue`（後者是另一個古老不維護的同名工具，**不要裝錯**）。執行檔是 `ddrescue`。
- **能做**：把壞軌中、隨時會死的硬碟，用最溫和的策略複製到映像檔或新碟。先跳過壞段快速撈好區，再回頭重試壞段
- **典型用法（三階段）**：
  ```bash
  # 階段 1：快撈好區（不重試）
  sudo ddrescue -f -n /dev/sda /mnt/external/disk.img /mnt/external/disk.log
  # 階段 2：對壞段重試 3 次
  sudo ddrescue -f -r3 /dev/sda /mnt/external/disk.img /mnt/external/disk.log
  # 階段 3：反向再試（最後手段）
  sudo ddrescue -f -R -r20 /dev/sda /mnt/external/disk.img /mnt/external/disk.log
  ```
- **限制**：映像目標必須有**比來源碟更多空間**，且不能跟來源同碟；不要存到 USB 隨身碟（寫入慢）
- **絕對不要用 `dd`**：`dd` 遇到壞軌會卡死、會反覆嘗試讀同一個壞磁區，可能直接把碟讀掛
- **詳見**：[08-data-recovery.md](08-data-recovery.md)

### `chntpw` —— Windows 密碼清除 / SAM 編輯
```bash
sudo apt install -y chntpw
```
- **能做**：清除 / 啟用 / 解鎖本機 Windows 帳號；改 SYSTEM / SOFTWARE / NTUSER.DAT 任何 registry hive
- **典型用法**：
  ```bash
  cd /mnt/win/Windows/System32/config
  sudo cp SAM SAM.bak            # 必備動作：先備份
  sudo chntpw -i SAM             # 互動式選單
  # 選 1 編輯使用者 → 選帳號 → 1 清密碼 / 2 解鎖 / 3 升管理員
  ```
- **限制**：**不支援 Microsoft 線上帳號**（那個密碼存在 MS 雲端，不在本機 SAM）。Microsoft 帳號的處理見 [06-registry-edit.md](06-registry-edit.md) 第 4 節（轉本機帳號或啟用 Administrator）
- **詳見**：[06-registry-edit.md](06-registry-edit.md)

### `ntfsfix` —— NTFS 快速修復 + 掛載前處理
```bash
sudo apt install -y ntfs-3g
```
> 包在 `ntfs-3g` 套件，跟 NTFS 掛載驅動是同一包。
- **能做**：修 NTFS journal、清 dirty 旗標、處理 Fast Startup / hibernation 造成的掛載拒絕；讓 NTFS 能重新被 Linux 掛起來
- **典型用法**：
  ```bash
  sudo umount /dev/sda3                  # 先卸載
  sudo ntfsfix --no-action /dev/sda3     # dry run，不寫入
  sudo ntfsfix /dev/sda3                 # 實際修
  # 強制清 Windows 標的 dirty flag：
  sudo ntfsfix -d /dev/sda3
  ```
- **限制**：只能修小毛病。嚴重 MFT / 索引 / 結構損壞要用 `testdisk` 或回 Windows 跑 `chkdsk /f /r`
- **詳見**：[05-filesystem-repair.md](05-filesystem-repair.md)

---

## 1. NTFS 工具家族（ntfs-3g / ntfsprogs 套件）

裝 `ntfs-3g` 後一次有一整組 NTFS 操作工具：

```bash
sudo apt install -y ntfs-3g
```

| 工具 | 用途 |
|---|---|
| `mount.ntfs-3g` | 掛載 NTFS（`mount -t ntfs-3g` 就是叫它） |
| `ntfsfix` | NTFS 快速修復（見上） |
| `ntfsundelete` | NTFS 已刪除檔案救援 |
| `ntfsclone` | NTFS 高效克隆（只複製已使用空間，比 `dd` 快很多倍） |
| `ntfscp` | 不掛載直接複製檔到 NTFS |
| `ntfscat` | 不掛載直接 cat NTFS 上的檔 |
| `ntfsls` | 不掛載列 NTFS 目錄 |
| `ntfsresize` | NTFS 大小調整 |
| `ntfslabel` | 改 NTFS volume label |
| `ntfsinfo` | NTFS volume 詳細資訊 |
| `ntfsdecrypt` | EFS 加密檔處理（少用） |

### `ntfsundelete` 範例
```bash
sudo umount /dev/sda3  # 必須先卸載
sudo ntfsundelete /dev/sda3                       # 列可救的檔
sudo ntfsundelete -u -m '*.docx' -d /tmp/recovered /dev/sda3  # 救所有 docx
```

### `ntfsclone` 範例
```bash
# 健康碟的完整備份（只複製已用空間）
sudo ntfsclone --save-image --output=/mnt/external/win.img /dev/sda3
# 還原
sudo ntfsclone --restore-image --overwrite=/dev/sda3 /mnt/external/win.img
```

---

## 2. 分割表 / 磁碟工具

```bash
sudo apt install -y gdisk parted util-linux dosfstools mtools sfdisk wipefs
```

| 工具 | 用途 |
|---|---|
| `lsblk` | 樹狀列出區塊裝置（util-linux 內建） |
| `blkid` | 看分割區的 UUID / TYPE / LABEL |
| `fdisk -l` | MBR / GPT 分割表瀏覽 |
| `sfdisk` | 可 pipe 的 fdisk，**強推用來備份/還原分割表** |
| `gdisk` | GPT 專用互動工具，含修復選項 |
| `sgdisk` | gdisk 的 CLI 版（可 script） |
| `parted` | 通用分割工具（互動或 CLI） |
| `partclone` | 智慧型分割區克隆（NTFS / ext / FAT），只複製已用部分 |
| `wipefs` | 清除檔案系統 / 分割表 signature |
| `mkfs.fat` / `dosfstools` | 建立 / 修 FAT32（修 EFI 分割區用） |
| `mtools`（mcopy / mdir 等） | 不掛載操作 FAT |

### 備份分割表（極度重要）
```bash
# 在做任何分割表修改前一定做：
sudo sfdisk -d /dev/sda > ~/sda-partitions-$(date +%Y%m%d).bak

# 還原：
sudo sfdisk /dev/sda < ~/sda-partitions-20260531.bak
```

### `partclone` 救當機 Windows 的常見招
```bash
sudo apt install -y partclone
# 把 NTFS 分割區存成映像（只佔已用空間）
sudo partclone.ntfs -c -s /dev/sda3 -o /mnt/external/win.pcl
# 還原
sudo partclone.ntfs -r -s /mnt/external/win.pcl -o /dev/sda3
```

---

## 3. Registry / Hive 編輯

```bash
sudo apt install -y chntpw libhivex-bin
```

| 工具 | 用途 |
|---|---|
| `chntpw -i <hive>` | 互動式編輯 SAM / SYSTEM / SOFTWARE / NTUSER.DAT |
| `reged` | chntpw 套件附的批次 registry 編輯（匯出/匯入 .reg） |
| `hivexsh` | libhivex 提供的 shell，可 pipe 指令 |
| `hivexml` | hive 轉 XML |
| `hivexget` | 從 hive 取單一值 |
| `hivexregedit` | 跟 Windows regedit 兼容的匯入匯出 |

### 進階：`samdump2`（從 SAM 拉密碼 hash）
```bash
sudo apt install -y samdump2
sudo samdump2 SYSTEM SAM > hashes.txt
```
> 用途：取得本機帳號的 NTLM hash。**只用在自己機器或合法授權**，這是密碼學家具不是駭客工具但對象搞錯就違法。

### 進階：`impacket` 套件（多用）
```bash
pip3 install impacket --break-system-packages
# 含 secretsdump.py、ntlmrelayx.py 等
```

### `reglookup` —— registry 查詢工具
```bash
sudo apt install -y registry-tools
reglookup -p '/Microsoft/Windows/CurrentVersion/Run' \
    /mnt/win/Windows/System32/config/SOFTWARE
```

---

## 4. 開機修復

```bash
sudo apt install -y efibootmgr efivar grub-efi-amd64-bin grub-common os-prober dosfstools mtools
```

| 工具 | 用途 |
|---|---|
| `efibootmgr` | 操作 UEFI NVRAM 的開機項清單 |
| `efivar` | 直接讀寫 EFI 變數（efibootmgr 抓不到時用） |
| `grub-install` / `update-grub` | 修雙系統開機選單 |
| `os-prober` | 偵測磁碟上有哪些 OS（給 grub-mkconfig 用） |
| `ms-sys` | 寫 Windows 風格的 MBR / boot sector（Legacy 系統用） |
| `mcopy`（mtools） | 不掛載複製檔到 FAT32（EFI 分割區） |

### `ms-sys` 安裝注意
Ubuntu 預設 repo 沒有，要從 source 編譯或加第三方 PPA：
```bash
# 從 source 編譯（離線備援可先在有網路時 git clone）
git clone https://github.com/pbatard/ms-sys.git
cd ms-sys && make && sudo make install
```
- **用途**：把 Windows 的 MBR / boot sector 寫回去（修 Legacy 模式 Windows 開不了機）
```bash
sudo ms-sys -m /dev/sda      # 寫 Windows MBR
sudo ms-sys -7 /dev/sda1     # 寫 Windows 7+ boot sector
```

詳見 [04-boot-repair.md](04-boot-repair.md)。

---

## 5. 磁碟健康診斷

```bash
sudo apt install -y smartmontools nvme-cli hdparm sdparm sg3-utils
```

| 工具 | 用途 |
|---|---|
| `smartctl` | SATA / NVMe 通用 SMART 工具（**最常用**） |
| `nvme-cli` | NVMe 專用（更多細節） |
| `hdparm` | IDE / SATA 參數調整、效能測試 |
| `sdparm` | SCSI 參數（含 USB 外接盒底層硬碟） |
| `badblocks` | 磁碟壞軌掃描（**永遠用 `-sv` 唯讀模式**，**不要用 `-w`**） |
| `fio` | I/O 效能基準 |

### 典型快速健康檢查
```bash
# SATA
sudo smartctl -H /dev/sda          # 一句話健康判定
sudo smartctl -a /dev/sda          # 完整屬性
sudo smartctl -t short /dev/sda    # 跑短自測（2 分鐘）
sudo smartctl -t long /dev/sda     # 跑長自測（數小時）
sudo smartctl -l selftest /dev/sda # 看自測結果

# NVMe
sudo nvme smart-log /dev/nvme0n1
sudo nvme list
```

詳見 [09-hardware-diagnostics.md](09-hardware-diagnostics.md)。

---

## 6. 惡意軟體掃描

```bash
sudo apt install -y clamav clamav-freshclam rkhunter chkrootkit yara
```

| 工具 | 用途 |
|---|---|
| `clamscan` | ClamAV 引擎（開源，偵測率中等但聊勝於無） |
| `freshclam` | 更新 ClamAV 病毒碼 |
| `clamdscan` | 透過 daemon 掃描（快很多） |
| `rkhunter` | rootkit hunter（簽章式） |
| `chkrootkit` | rootkit 檢查（另一個視角） |
| `yara` | 規則式威脅偵測（可用社群 rule pack） |

### ClamAV 離線掃 Windows
```bash
sudo freshclam   # 先更新病毒碼
sudo clamscan --recursive --infected --log=/tmp/scan.log \
    --max-filesize=2G --max-scansize=4G \
    --move=/tmp/quarantine \
    /mnt/win/Users /mnt/win/ProgramData
```

### 進階：第三方掃描器
- **ESET Online Scanner**：Windows 上的 free standalone scanner，可以放在 Ventoy 另一個 Windows PE 上用
- **Kaspersky Rescue Disk**：完整 Linux-based 救援碟含 KAV 引擎，**強烈建議放一份在 Ventoy**
- **Malwarebytes** 沒 Linux 版本

詳見 [07-malware-cleanup.md](07-malware-cleanup.md)。

---

## 7. BitLocker 解密

```bash
sudo apt install -y dislocker fuse3 cryptsetup
```

| 工具 | 用途 |
|---|---|
| `dislocker` | BitLocker 解密、掛載 |
| `dislocker-metadata` | 看 BitLocker 容器資訊 |
| `cryptsetup` | LUKS 工具，也能 `cryptsetup bitlkOpen` 讀 BitLocker（Linux 5.3+） |

### dislocker 標準流程
```bash
sudo mkdir -p /mnt/bitlocker /mnt/win
sudo dislocker -V /dev/sda3 -p<48-digit-recovery-key> -- /mnt/bitlocker
sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file /mnt/win
```

### `cryptsetup` 讀 BitLocker（較新）
```bash
sudo cryptsetup bitlkDump /dev/sda3       # 看 metadata
sudo cryptsetup bitlkOpen /dev/sda3 bitlk # 解密映射
sudo mount -t ntfs-3g -o ro /dev/mapper/bitlk /mnt/win
```

詳見 [10-bitlocker.md](10-bitlocker.md)。

---

## 8. 檔案救援（除了 photorec）

```bash
sudo apt install -y foremost scalpel bulk-extractor magicrescue
```

| 工具 | 用途 |
|---|---|
| `foremost` | 經典檔案 carving，靠 magic number 救檔 |
| `scalpel` | 改良版 foremost，更快但設定檔複雜 |
| `bulk_extractor` | 大規模特徵抽取（email、信用卡號、URL） |
| `magicrescue` | 另一個 carving 工具，rule-based |

### foremost 範例
```bash
sudo foremost -i /dev/sda3 -o /mnt/external/foremost-output -t jpg,pdf,doc,docx,xls,xlsx
```

對比與何時用：
- 想救**檔名 + 目錄結構**：用 `ntfsundelete` 或 `testdisk` undelete
- 檔案系統壞了但想救**特定類型檔案**：用 `photorec`
- 想撈**特徵字串**（信用卡、密碼）：用 `bulk_extractor`

---

## 9. Windows 鑑識 / 事件日誌

```bash
sudo apt install -y python3-evtx libwin-hivex-perl
pip3 install python-evtx --break-system-packages   # 備援裝法
```

| 工具 | 用途 |
|---|---|
| `python-evtx` (`python3 -m Evtx.Evtx`) | 解析 Windows .evtx 事件日誌 |
| `evtx_dump` (Rust 版) | 同上，更快 |
| `regripper` (Perl) | 從 hive 撈取常用鑑識資訊 |
| `libpff-utils` (`pffexport`) | 解析 Outlook PST / OST |
| `volatility` / `volatility3` | 記憶體 dump 分析（少用，需要 hibernation/dump 檔） |

### 看最近 BSOD（從 System.evtx 撈關鍵 ID）
```bash
python3 -m Evtx.Evtx /mnt/win/Windows/System32/winevt/Logs/System.evtx | \
    grep -B 2 -A 10 -E "EventID.*>(41|1001|6008|219)<"
# 41   = kernel power（不正常重開機）
# 1001 = BugCheck（BSOD，含 STOP code）
# 6008 = unexpected shutdown
# 219  = driver load failure
```

詳見 [02-symptom-triage.md](02-symptom-triage.md)。

---

## 10. Windows 安裝媒體 / 映像處理

```bash
sudo apt install -y wimtools cabextract p7zip-full
```

| 工具 | 用途 |
|---|---|
| `wimtools` / `wimlib-imagex` | 處理 .wim / .esd（Windows 安裝映像） |
| `cabextract` | 解 .cab 檔（Windows update 包） |
| `7z` | 解幾乎任何 Windows 壓縮格式（含 .iso） |
| `woeusb-ng` | 從 Linux 燒 Windows ISO 到 USB（緊急做安裝碟用） |

### 從 install.wim 列出 image 版本
```bash
wimlib-imagex info /media/cdrom/sources/install.wim
```

### 從 ISO 解 install.wim
```bash
7z x Win11.iso -o/tmp/win11
# /tmp/win11/sources/install.wim
```

---

## 11. 救援過程的便利工具

```bash
sudo apt install -y tmux screen mc ranger pv pigz rsync rclone htop iotop nethogs zenity
```

| 工具 | 用途 |
|---|---|
| `tmux` / `screen` | **救援必裝**：避免 ddrescue 跑一半 SSH 斷線就毀 |
| `mc` (Midnight Commander) | 雙窗格檔案管理，TUI |
| `ranger` | vim-like 檔案管理 |
| `pv` | pipe 進度條 |
| `pigz` | 平行 gzip（備份壓縮快很多倍） |
| `rsync` | 同步 / 備份（最常用） |
| `rclone` | 雲端同步（備份到 Google Drive / OneDrive） |
| `htop` | 系統監控 |
| `iotop` | I/O 監控（找誰在拖慢碟） |
| `nethogs` | 網路用量 by process |
| `zenity` | shell script 開 GUI 對話框 |

### `tmux` 救援場景必備動作
```bash
tmux new -s rescue                 # 開新工作階段
# 跑 ddrescue 或 photorec
# Ctrl+B 然後 D 離開（程式繼續跑）
# 萬一斷線重連：
tmux attach -t rescue
```

---

## 12. 跨機傳檔（救資料常用）

```bash
sudo apt install -y rsync rclone openssh-client magic-wormhole
```

| 工具 | 用途 |
|---|---|
| `rsync` over SSH | 救出來的資料丟到客戶另一台機器 |
| `magic-wormhole` | 一條指令傳檔，自動產 6-word code（給技術小白也能收） |
| `rclone` | 推上雲端 |
| `scp` | OpenSSH 自帶 |

### `magic-wormhole` 範例
```bash
# 送：
wormhole send /mnt/external/Alice-Documents.tar.gz
# → 顯示 6-word code 例如 7-crossover-clockwork

# 收（在任何另一台裝 wormhole 的電腦）：
wormhole receive 7-crossover-clockwork
```

---

## 13. PE / Windows binary 分析（偶爾用）

```bash
sudo apt install -y pev binutils file
```

| 工具 | 用途 |
|---|---|
| `pev`（含 readpe / peres / pestr） | PE 檔案分析 |
| `objdump -p` | 看 binary 結構 |
| `strings` | 撈字串（找 C2 URL、可疑指令） |
| `file` | 識別檔案類型 |

### 看可疑 .exe
```bash
file suspicious.exe          # 確認是不是 PE
readpe suspicious.exe        # PE header 完整資訊
pestr suspicious.exe         # 撈所有字串
strings suspicious.exe | grep -iE "http|cmd|powershell|reg add"
```

---

## 14. 工具速查表（依任務）

| 「我要…」 | 用 |
|---|---|
| 把整顆壞硬碟搬出來 | `ddrescue` |
| 找回分割表 | `testdisk` |
| 救已刪 NTFS 檔（保留檔名） | `ntfsundelete` 或 `testdisk` |
| 救已刪檔（不在乎檔名） | `photorec` |
| 修 NTFS 掛不起來 | `ntfsfix` |
| 修 NTFS 嚴重損壞 | 回 Windows 跑 `chkdsk`，Linux 沒對應 |
| 清 Windows 密碼 | `chntpw -i SAM` |
| 改 registry | `chntpw -i <hive>` 或 `hivexsh` |
| 解 BitLocker | `dislocker` 或 `cryptsetup bitlkOpen` |
| 重註冊 UEFI 開機項 | `efibootmgr -c` |
| 修 Legacy MBR | `ms-sys -m` |
| 掃毒 | `clamscan` + `rkhunter` + Kaspersky Rescue |
| 看磁碟健康 | `smartctl -H`、`smartctl -a` |
| 看開機是不是 UEFI | `[ -d /sys/firmware/efi ] && echo UEFI \|\| echo Legacy` |
| 找 Windows 在哪個分割區 | `lsblk -f`、`blkid` |
| 從 .evtx 看 BSOD | `python3 -m Evtx.Evtx` |
| 壓力測試硬體 | `stress-ng`、`memtester`、`memtest86+`（從 USB 開） |
| 跑長時間任務怕斷線 | 永遠 `tmux new` 包起來 |

---

## 15. 一行命令裝齊全（懶人版）

```bash
sudo apt update && sudo apt install -y \
    ntfs-3g chntpw libhivex-bin testdisk gddrescue \
    smartmontools nvme-cli hdparm \
    parted gdisk dosfstools mtools sfdisk wipefs partclone \
    efibootmgr efivar grub-efi-amd64-bin grub-common os-prober \
    clamav clamav-freshclam rkhunter chkrootkit yara \
    dislocker fuse3 cryptsetup \
    foremost scalpel bulk-extractor \
    python3-evtx libwin-hivex-perl libpff-utils \
    wimtools cabextract p7zip-full woeusb-ng \
    tmux screen mc ranger pv pigz rsync rclone \
    htop iotop nethogs zenity \
    pev binutils file \
    samdump2 registry-tools \
    util-linux pciutils usbutils inxi lshw hwinfo dmidecode \
    lm-sensors memtester stress-ng \
    network-manager curl wget openssh-client magic-wormhole \
    vim nano less tree \
    python3-pip git build-essential
```

完整版見 [scripts/install-rescue-tools.sh](../scripts/install-rescue-tools.sh)，含錯誤處理和 ClamAV 病毒碼初始化。

---

## 16. 額外工具（按情況裝）

### Kaspersky Rescue Disk（強烈建議）
不是 apt 套件，是 ISO，丟進 Ventoy：
```
1. 下載 https://support.kaspersky.com/utility/142
2. cp kasperskyrescue.iso /media/$USER/Ventoy/
```
Ventoy 開機選單會列出來。離線掃毒能力遠勝 ClamAV。

### Hiren's BootCD PE（Windows PE 救援）
Windows PE 環境，能跑 Windows 原生工具（sfc、DISM、bcdedit、regedit GUI）：
```
1. 下載 https://www.hirensbootcd.org/
2. 丟進 Ventoy
```
Linux 救不了的時候切過去用，見 [13-when-linux-cannot-fix.md](13-when-linux-cannot-fix.md)。

### SystemRescue（內建救援碟）
全套 Linux 救援工具預裝好的 distro：
```
1. 下載 https://www.system-rescue.org/
2. 丟進 Ventoy
```
如果不想自己裝套件，直接用這個。但客製化彈性比較低。

### Tails / Kali（鑑識專用）
碰到企業環境 / 法律情境（要保持鑑識完整性）才用。一般救援用不到。

---

## 17. 工具是哪個套件的對照

當 agent 不確定某指令哪個套件時：

```bash
apt-file search <command_name>   # 需要先 sudo apt install apt-file && sudo apt-file update
# 或：
dpkg -S $(which <command>)        # 查已裝的指令屬於哪個套件
```

常被搞混的：
| 指令 | 套件 |
|---|---|
| `ddrescue` | `gddrescue`（不是 `ddrescue`） |
| `ntfsfix` | `ntfs-3g` |
| `photorec` | `testdisk` |
| `hivexsh` | `libhivex-bin` |
| `smartctl` | `smartmontools` |
| `efibootmgr` | `efibootmgr`（同名） |
| `clamscan` | `clamav` |
| `pffexport` | `libpff-utils` |
| `wimlib-imagex` | `wimtools` |
