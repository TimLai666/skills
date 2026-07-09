# 01 — 安全準則（必讀）

救援的本質是「在已經壞的系統上動手，希望它更好不是更壞」。每個操作都有風險。這份是完整的安全清單，每次救援前都該過一遍。

## 三條最高鐵則

### 1. 先備份再修

任何寫入動作前必須有備份。沒備份過就 `ntfsfix`、`chntpw`、`testdisk write` 是新手最常犯的錯。

最低標準：使用者資料夾完整 rsync 到外接碟。
較高標準：整個 Windows 系統碟用 `ntfsclone` 或 `ddrescue` 做完整映像。
最高標準：兩份備份在不同實體裝置上。

### 2. 不確定就停手

每個指令執行前問自己：
- 它會寫入哪個裝置？
- 如果寫錯了，能救回來嗎？
- 我清楚每個 flag 的意思嗎？

任何一題答不出來就先停，去查清楚。多花十分鐘查文件，勝過五秒鐘把人家資料毀掉。

### 3. 不要在掛載中的磁碟上做檔案系統操作

`ntfsfix /dev/sda3` 但 `/dev/sda3` 還掛在 `/mnt/win` 上——這會直接損毀 NTFS 結構。一定先 `umount`。

```bash
# 確認掛載狀態
mount | grep -E 'sd|nvme'

# 確認沒人在用該磁碟
sudo lsof /mnt/win

# 卸載
sudo umount /mnt/win
# 卸不掉時看是誰在用
sudo fuser -vm /mnt/win
```

## 讀寫順序：永遠先 ro

第一次掛載一律 read-only：

```bash
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
```

這樣即使指令打錯也不會寫到使用者磁碟。先確認：
- 檔案系統能讀
- 重要資料還在
- 症狀對得上你的判斷

需要寫入時才 `umount` 之後重新 `rw` 掛載：

```bash
sudo umount /mnt/win
sudo mount -t ntfs-3g -o rw /dev/sda3 /mnt/win
```

## 裝置名稱對到位

最容易出大事的錯誤：寫錯 `/dev/sdX`。

```bash
# 出事前永遠先看清楚
lsblk -f -o NAME,FSTYPE,LABEL,SIZE,MOUNTPOINT,UUID

# 用 UUID 比較安全
sudo blkid

# nvme 是 /dev/nvme0n1 + 分割區 /dev/nvme0n1p1 不是 /dev/nvme0n11
ls /dev/nvme* 2>/dev/null
```

判斷哪個是 Windows 系統碟的方法：
- 通常是最大的 NTFS 分割區
- 通常含有 `/Windows/System32` 資料夾（掛載後 `ls /mnt/win/Windows/System32` 確認）
- LABEL 常常是 `Windows`、`OS`、`SYSTEM`

EFI 分割區：
- 100-500MB 大小
- FAT32
- LABEL 常為 `EFI`、`SYSTEM`、`ESP`
- 有 `/EFI/Microsoft/Boot/` 資料夾

Recovery 分割區：
- 約 500MB-1GB
- NTFS
- LABEL 為 `Recovery`、`WinRE`
- 含有 `Recovery/WindowsRE/Winre.wim`

## SMART 警告就先停

`sudo smartctl -H /dev/sdX` 顯示 `FAILED` 或 `failing_now`，或 `-a` 看到：
- `Reallocated_Sector_Ct` > 0 且在增加
- `Current_Pending_Sector` > 0
- `Offline_Uncorrectable` > 0
- `Reported_Uncorrect` > 0

**不要再對這顆碟動任何寫入**。每多寫一次都讓僅存資料更危險。流程改成：

1. `ddrescue` 把碟整個 dump 成檔案
2. 後續所有操作都對 dump 出來的映像檔做，不碰實體碟

詳見 `08-data-recovery.md` 的 ddrescue 章節。

## BitLocker 偵測

掛載 NTFS 前先看 `blkid` 有沒有 `TYPE="BitLocker"`：

```bash
sudo blkid /dev/sda3
# 如果回 TYPE="BitLocker" 就不要用 ntfs-3g 掛
```

硬幹會什麼都看不到、誤以為磁碟壞掉。看 `10-bitlocker.md`。

## Hibernation 與 Fast Startup

Windows 沒乾淨關機（hibernation、fast startup 都算）時，NTFS 是 dirty 狀態。`ntfs-3g` 預設拒絕讀寫掛載。

```bash
# 錯誤訊息會是：
# The disk contains an unclean file system (0, 0).
# The file system wasn't safely closed on Windows. Fix it and try again.
```

選項：
- **唯讀讀資料就好**：`-o ro` 可以無視
- **強制讀寫**：`-o remove_hiberfile` 會把 hibernation state 丟掉（使用者重開機時會「冷開機」，未存的工作會掉）
- **更安全**：在 Windows 還能進去的情況下叫使用者 `shutdown /s /f /t 0` 完整關機

```bash
# 唯讀（最安全）
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 強制讀寫（讓使用者明白會丟掉未存工作）
sudo mount -t ntfs-3g -o remove_hiberfile /dev/sda3 /mnt/win
```

注意：Fast Startup 跟 hibernation 是同一機制（hiberfil.sys）。使用者「明明有關機」但磁碟還是 dirty 是這個原因。

## 寫入 registry 前複製整個 hive

`chntpw`、`hivexsh` 都能毀 hive，毀完開機會直接死透。

```bash
cd /mnt/win/Windows/System32/config

# 至少把要動的那個 hive 備份
sudo cp SAM SAM.bak.$(date +%Y%m%d)
sudo cp SYSTEM SYSTEM.bak.$(date +%Y%m%d)
sudo cp SOFTWARE SOFTWARE.bak.$(date +%Y%m%d)

# 更完整：整個 config 資料夾打包
sudo tar czf /tmp/registry-backup-$(date +%Y%m%d).tar.gz .
```

弄壞了就 `cp SAM.bak SAM`。

## destructive 指令清單（執行前要兩段式確認）

這些操作改完原狀基本上回不去，每個都要跟使用者覆述一次再執行：

| 指令 | 風險 |
|---|---|
| `dd if=X of=/dev/sdX` | 寫錯目標 = 整個磁碟資料消失 |
| `mkfs.*` | 重新格式化、資料全失 |
| `fdisk` / `gdisk` / `parted` 任何寫入動作 | 分割表寫錯 = 看似空碟 |
| `ntfsfix` | 一般安全，但極少數情況會讓 NTFS 更壞 |
| `testdisk` 的 Write 模式 | 改分割表，寫錯難救 |
| `chntpw -e` / `hivexsh -w` | 改 registry，弄壞開不了機 |
| `rm` 於 `/mnt/win/Windows/` | 不用解釋 |
| `rsync --delete` | 目標端的東西會被刪 |
| `mount -o remove_hiberfile` | 使用者未存工作會消失 |
| `dislocker` 寫入模式 | BitLocker 卷有風險 |
| `clamscan --remove` | 自動刪檔，可能誤刪 |

兩段式確認的標準腳本：

> 「我接下來要執行 `<指令>`。它會 `<具體效果>`。如果寫錯會 `<最壞情況>`。目標是 `<裝置/路徑>`，我已經確認過這是正確的因為 `<理由>`。確定要執行嗎？」

使用者答「確定 / yes / 繼續」之後再執行。

## 修壞了的退路

幾乎每個操作都該有「退路」：

| 操作 | 退路 |
|---|---|
| 改 registry | 改前 cp 出 `.bak`，弄壞 cp 回去 |
| `ntfsfix` | 改前用 `ntfsclone` 做映像 |
| 改分割表 | testdisk 的 List 模式只看不改；要寫前用 `sfdisk -d` 備份分割表 |
| 修 BCD | 改前 `cp BCD BCD.bak` |
| `efibootmgr` 刪項 | `efibootmgr -v` 留下原本完整列表的截圖 |

備份分割表：

```bash
# 備份
sudo sfdisk -d /dev/sda > /tmp/sda-partition-table.txt
# 還原
sudo sfdisk /dev/sda < /tmp/sda-partition-table.txt
```

## 紀錄日誌

每次救援都留紀錄。出事可以回溯、修不好可以給技師看。

```bash
# 開始救援時
RESCUE_LOG=/tmp/rescue-$(date +%Y%m%d-%H%M).log
script -a "$RESCUE_LOG"
# 所有後續操作都會被記錄
# 結束時 Ctrl-D 退出 script
```

或手寫筆記寫到 `~/rescue-notes-YYYYMMDD.md`，每動一步寫一句：
```
14:32 - 確認 /dev/sda3 是 Windows 系統碟（含 /Windows/System32）
14:35 - smartctl -H /dev/sda 結果 PASSED
14:37 - rsync /mnt/win/Users/john/ → /media/external/backup/
14:50 - 備份完成，95GB
14:52 - ntfsfix /dev/sda3 → NTFS volume version 3.1, ok
...
```

## 什麼時候該叫停

不要硬撐到把事情弄更糟。下列情況該停下來：

1. **三次同樣的修法都失敗** —— 不是你的方法，是症狀理解錯了，重新分流
2. **使用者顯得疲憊或催促** —— 急著修最容易出錯，先停手讓他冷靜
3. **SMART 開始劣化** —— 操作過程中 reallocated sector 數字在跳，碟在加速死亡，立刻切到 ddrescue 模式
4. **連續兩個 reference 都解決不了** —— 可能是 `13-when-linux-cannot-fix.md` 的場景，需要 Windows 媒體進 WinRE

停下來不丟臉。把已經做過的事告訴使用者，建議下一步（送修、買新硬碟、找 Windows 安裝媒體），是負責的做法。
