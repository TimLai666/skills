# 14 · CLI 工具完整目錄

> **這份文件做什麼**：把 Linux 上能修 Windows 的所有 CLI 工具集中一覽 —— 安裝指令、用途、典型範例、限制、何時用。當 agent 需要某類功能時，先翻這份找對的工具，再去 references 找詳細操作。
>
> **使用慣例**：所有 `sudo apt install -y <pkg>` 都假設 Ubuntu / Debian。RHEL / Arch 對應套件名請自查。

---

## 0. 常用救援工具

依診斷需要選用工具。下列安裝指令是套件對照，不需要全部執行。疑似故障磁碟先做映像，不在來源上加跑掃描、效能或自我測試。

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
- **操作入口**：先確認來源、目標與 mapfile，依資料救援文件決定首輪與後續重試。不要固定追加多輪重讀。
- **限制**：映像目標容量須足以容納來源，且不能在同一實體磁碟。`dd` 不具備 ddrescue 的 mapfile 與救援策略。
- **詳見**：[08-data-recovery.md](08-data-recovery.md)

### `chntpw` —— Windows 密碼清除 / SAM 編輯
```bash
sudo apt install -y chntpw
```
- **能做**：清除 / 啟用 / 解鎖本機 Windows 帳號；改 SYSTEM / SOFTWARE / NTUSER.DAT 任何 registry hive
- **操作入口**：依登錄編輯文件先備份 SAM，核對帳號類型，再選擇適用操作。
- **限制**：不會變更 Microsoft 雲端帳號密碼；清除本機密碼也可能影響 EFS 等憑證保護資料。
- **詳見**：[06-registry-edit.md](06-registry-edit.md)

### `ntfsfix` —— NTFS 快速修復 + 掛載前處理
```bash
sudo apt install -y ntfs-3g
```
> 包在 `ntfs-3g` 套件，跟 NTFS 掛載驅動是同一包。
- **能做**：修正部分基本 NTFS 不一致、重設日誌並要求 Windows 檢查。
- **操作入口**：依檔案系統修復文件確認適用條件，卸載後先用 `--no-action` 檢查。
- **限制**：不是完整 chkdsk，也不是清除休眠狀態的工具；需要完整結構修復時轉 Windows。
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

健康 NTFS 的映像格式、還原與副本掛載見 [08-data-recovery.md](08-data-recovery.md)。

---

## 2. 分割表 / 磁碟工具

```bash
sudo apt install -y gdisk parted util-linux dosfstools mtools
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

分割表備份與還原見 [05-filesystem-repair.md](05-filesystem-repair.md)；`partclone` 與 `ntfsclone` 的映像操作見 [08-data-recovery.md](08-data-recovery.md)。

---

## 3. Registry / Hive 編輯

```bash
sudo apt install -y chntpw libhivex-bin libwin-hivex-perl
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
python3 -m venv /tmp/impacket-env
/tmp/impacket-env/bin/pip install impacket
# 含 secretsdump.py、ntlmrelayx.py 等
```

### `reglookup` —— registry 查詢工具
```bash
sudo apt install -y reglookup
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
`ms-sys -7` 寫入 Windows 7 類型的 **MBR**，目標是整顆磁碟，不是分割區開機磁區。依實際分割表、開機方式與備份選擇操作。

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
| `badblocks` | 磁碟壞軌掃描（讀取掃描仍增加負載；故障來源不掃描，寫入模式會改動資料） |
| `fio` | I/O 效能基準 |

先用 `smartctl -a /dev/已確認的磁碟` 讀取既有資訊，或用 `nvme smart-log` 讀 NVMe 記錄。自我測試與全碟掃描依硬體診斷文件評估，不作為例行下一步。



詳見 [09-hardware-diagnostics.md](09-hardware-diagnostics.md)。

---

## 6. 惡意軟體掃描

```bash
sudo apt install -y clamav clamav-freshclam rkhunter chkrootkit yara
```

| 工具 | 用途 |
|---|---|
| `clamscan` | ClamAV 引擎，結果須檢查漏掃、錯誤與誤判 |
| `freshclam` | 更新 ClamAV 病毒碼 |
| `clamdscan` | 透過 daemon 掃描（快很多） |
| `rkhunter` | Linux 主機 rootkit 檢查，不能替代 Windows 離線掃描 |
| `chkrootkit` | Linux 主機 rootkit 檢查 |
| `yara` | 規則式威脅偵測（可用社群 rule pack） |

### ClamAV 離線掃 Windows
```bash
sudo freshclam   # 先更新病毒碼
sudo clamscan --recursive --infected --log=/tmp/scan.log \
    --max-filesize=2G --max-scansize=4G \
    /mnt/win/Users /mnt/win/ProgramData
```

### 進階：第三方掃描器
- **ESET Online Scanner**：Windows 上的 free standalone scanner，可以放在 Ventoy 另一個 Windows PE 上用
- **Kaspersky Rescue Disk**：完整 Linux-based 救援碟含 KAV 引擎，可依本次需求選擇
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

唯讀解鎖使用 `sudo dislocker -r -V /dev/已確認的分割區 -p -- /mnt/bitlocker`，由提示輸入復原密碼。`cryptsetup open --type bitlk --readonly` 是另一選項；完整掛載與清理步驟見下方文件。



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
python3 -m venv /tmp/evtx-env
/tmp/evtx-env/bin/pip install python-evtx   # 套件庫沒有時的備援
```

| 工具 | 用途 |
|---|---|
| `python-evtx`（Python API） | 解析 Windows .evtx 事件日誌 |
| `evtx_dump` (Rust 版) | 同上，更快 |
| `regripper` (Perl) | 從 hive 撈取常用鑑識資訊 |
| `libpff-utils` (`pffexport`) | 解析 Outlook PST / OST |
| `volatility` / `volatility3` | 記憶體 dump 分析（少用，需要 hibernation/dump 檔） |

讀取 API 與開機事件篩選見下方症狀分流文件，或執行 [boot-diagnostic.sh](../scripts/boot-diagnostic.sh)。



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

從 ISO／WIM／ESD 找出映像索引、提取系統檔案、備份替換與回復，見 [15-image-file-replacement.md](15-image-file-replacement.md)。版本不相符時也可評估試修，須記錄差異與可回復方式。

---

## 11. 救援過程的便利工具

```bash
sudo apt install -y tmux screen mc ranger pv pigz rsync rclone htop iotop nethogs zenity
```

| 工具 | 用途 |
|---|---|
| `tmux` / `screen` | 遠端長任務可保留終端工作階段；無法抵抗斷電或 Live USB 當機 |
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

### `tmux` 遠端長任務範例
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
| 判斷 NTFS 掛載失敗 | 先查錯誤，適用時用 `ntfsfix`（見 03 / 05） |
| 修 NTFS 嚴重損壞 | 回 Windows 跑 `chkdsk`，Linux 沒對應 |
| 清 Windows 密碼 | `chntpw -i SAM` |
| 改 registry | `chntpw -i <hive>` 或 `hivexregedit`（見 06） |
| 解 BitLocker | `dislocker` 或 `cryptsetup bitlkOpen` |
| 重註冊 UEFI 開機項 | `efibootmgr -c` |
| 修 Legacy MBR | `ms-sys`（依 04 選擇類型） |
| 掃毒 | `clamscan` / `yara`，再依結果處理 |
| 看磁碟健康 | `smartctl -H`、`smartctl -a` |
| 看開機是不是 UEFI | `[ -d /sys/firmware/efi ] && echo UEFI \|\| echo Legacy` |
| 找 Windows 在哪個分割區 | `lsblk -f`、`blkid` |
| 從 .evtx 看 BSOD | `python-evtx` API（見 02） |
| 從 Windows 映像替換特定系統檔案 | `wimlib-imagex`（見 15） |
| 壓力測試硬體 | `stress-ng`、`memtester`、`memtest86+`（從 USB 開） |
| 跑長時間任務怕斷線 | `tmux new` 保留工作階段 |

---

## 15. 依任務安裝

[install-rescue-tools.sh](../scripts/install-rescue-tools.sh) 提供 core、registry、recovery、boot、malware、bitlocker、image、diagnostics 群組。例如 `sudo bash scripts/install-rescue-tools.sh --group image` 只安裝映像工具；未選取的工具不會安裝。病毒碼更新與 AI 環境依實際需要另行準備。

---

## 16. 額外工具（按情況裝）

### Kaspersky Rescue Disk（可選救援媒體）
不是 apt 套件，是 ISO，丟進 Ventoy：
```
1. 下載 https://support.kaspersky.com/utility/142
2. cp kasperskyrescue.iso /media/$USER/Ventoy/
```
Ventoy 開機選單會列出來。使用前確認媒體版本、硬體相容性與病毒碼能否更新。

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

### Tails / Kali
分別偏向隱私使用與安全測試；使用特定發行版不會自動保證鑑識完整性。需要鑑識時仍須規劃唯讀取得、雜湊與保管紀錄。

---

## 17. 工具是哪個套件的對照

當 agent 不確定某指令哪個套件時：

```bash
apt-file search wimlib-imagex   # 需要先 sudo apt install apt-file && sudo apt-file update
# 或：
dpkg -S "$(command -v wimlib-imagex)"        # 查已裝的指令屬於哪個套件
```

常被搞混的：
| 指令 | 套件 |
|---|---|
| `ddrescue` | `gddrescue`（不是 `ddrescue`） |
| `ntfsfix` | `ntfs-3g` |
| `photorec` | `testdisk` |
| `hivexsh` | `libhivex-bin` |
| `hivexregedit` | `libwin-hivex-perl` |
| `sfdisk` / `wipefs` | `util-linux` 系列，依發行版拆包確認 |
| `smartctl` | `smartmontools` |
| `efibootmgr` | `efibootmgr`（同名） |
| `clamscan` | `clamav` |
| `pffexport` | `libpff-utils` |
| `wimlib-imagex` | `wimtools` |

套件對照查證：[Ubuntu libhivex-bin 檔案清單](https://packages.ubuntu.com/noble/amd64/libhivex-bin/filelist)、[libwin-hivex-perl 檔案清單](https://packages.ubuntu.com/noble/amd64/libwin-hivex-perl/filelist)。
