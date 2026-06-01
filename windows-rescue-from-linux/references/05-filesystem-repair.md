# 05 — 檔案系統與分割表修復

NTFS 修復、分割表壞掉的救援、磁碟看不到分割區的恢復。

## ntfsfix 的能力與限制

`ntfsfix` 不是 Linux 版的 chkdsk。它只能修：

- NTFS journal（log file）狀態
- 某些 dirty 旗標
- 小型 metadata 不一致

它**修不了**：
- 嚴重的檔案系統結構損壞
- 壞磁區造成的資料毀損
- MFT 損壞
- 索引損壞

修不了的東西最終要 Windows 端的 `chkdsk /f /r`，但 ntfsfix 先把表面狀態整理好，能讓 Windows 重新進去跑 chkdsk。

## ntfsfix 操作

```bash
# 一定要先 umount
sudo umount /mnt/win

# Dry run 看會做什麼
sudo ntfsfix --no-action /dev/sda3

# 實際修
sudo ntfsfix /dev/sda3
```

可能輸出：

```
Mounting volume... OK
Processing of $MFT and $MFTMirr completed successfully.
Checking the alternate boot sector... OK
NTFS volume version is 3.1.
NTFS partition /dev/sda3 was processed successfully.
```

→ OK，可以掛 rw 試。

```
Volume is corrupt. You should run chkdsk.
```

→ ntfsfix 修不了。下面有 workaround。

```
Failed to read $MFT: Input/output error
```

→ 壞磁區。直接跳 `08-data-recovery.md` 的 ddrescue。

## 修不動時的 workaround

ntfsfix 失敗但磁碟硬體 OK 時，幾個方向：

### A. 強制清 dirty bit

ntfsfix 修不了通常是因為 NTFS 標記為 dirty 太嚴重。可以強制清 dirty 旗標讓 Windows 認為一切正常——但這只是表面工夫，Windows 進去後還是會在背景觸發 chkdsk：

```bash
# 不建議常規使用，但作為「先讓 Windows 進去再說」的招數
sudo ntfsfix -d /dev/sda3
```

### B. 重新整理 logfile

```bash
sudo ntfsfix -b /dev/sda3
```

### C. 從備份的 boot sector 還原

NTFS 在分割區最後保留一份 boot sector 副本。前面的壞了可以從後面複製：

```bash
# 看當前 boot sector
sudo dd if=/dev/sda3 bs=512 count=1 2>/dev/null | xxd | head

# 該分割區的最後 sector（小心算對位置）
# 用 testdisk 介面化操作會更安全（見後段）
```

### D. 用 testdisk 修

`testdisk` 比 `ntfsfix` 更強，可以：
- 修復 NTFS boot sector
- 從備份還原 boot sector
- 重建 MFT mirror

跳到後面的 testdisk 章節。

### E. 投降，回 Windows

老實告訴使用者：需要 Windows 安裝媒體 → 命令提示字元 → `chkdsk C: /f /r`。Linux 真的修不動嚴重 NTFS 損壞。

## 分割表壞掉

症狀：

- `lsblk` 看不到 Windows 的分割區
- `fdisk -l` 顯示 GPT 損壞警告
- 分割區編號錯亂

### GPT 損壞修復

GPT 有主備兩份。一份壞了還可以從另一份還原。

```bash
sudo apt install gdisk

sudo gdisk /dev/sda
# 進到 gdisk 互動界面
# 按 r 進 recovery & transformation menu
# 按 c 把 backup GPT 載入到 main location
# 按 w 寫入

# 或反過來：把 main 內容寫到 backup
# r → d (build backup GPT from main)
```

或直接：

```bash
sudo sgdisk -e /dev/sda   # 把 backup GPT 移到磁碟末端（修被截斷的）
sudo sgdisk -b /tmp/gpt-backup.bin /dev/sda   # 備份目前 GPT
```

### 分割區整個不見：testdisk

```bash
sudo testdisk /dev/sda
```

testdisk 是互動式工具，流程：

1. **Create new log** → Create
2. 選 `/dev/sda`
3. 選 partition table type（一般 `Intel` for MBR, `EFI GPT` for GPT；testdisk 通常會自動偵測）
4. 選 `Analyse`
5. 選 `Quick Search`
6. 它會列出找到的分割區。看清楚對不對：
   - 大小對嗎？
   - 起始 sector 對嗎？
   - 標籤對嗎？
7. 按 `P` 可以列出該分割區內的檔案，視覺化確認
8. 確認後按 `Enter` 回到分割區列表
9. 用上下箭頭把要保留的分割區設定 type（`P` for Primary, `*` for Bootable）
10. 按 `Enter` 進確認頁
11. 選 `Write`
12. 重開機驗證

`Quick Search` 找不到 → 試 `Deeper Search`（很慢，可能跑幾小時）。

### 重要：testdisk 寫之前一定要備份分割表

```bash
sudo sfdisk -d /dev/sda > /tmp/sda-pt-backup-$(date +%Y%m%d).txt
# 寫錯了 → 還原
sudo sfdisk /dev/sda < /tmp/sda-pt-backup-YYYYMMDD.txt
```

## NTFS undelete（救剛刪除的檔案）

`testdisk` 也能在 NTFS 上找回剛刪的檔案：

```bash
sudo testdisk /dev/sda3
# Analyse → 選分割區 → 按 P 進去看檔案結構
# 紅色標記的是已刪除的
# 選好按 c 複製到別處（不要回原碟，會覆蓋掉資料）
```

或專門的工具 `ntfsundelete`：

```bash
sudo apt install ntfs-3g

# 列出可救的已刪除檔案
sudo ntfsundelete /dev/sda3

# 救特定 inode
sudo ntfsundelete /dev/sda3 -u -i 12345 -d /media/external/recovered/

# 依名稱 pattern 救
sudo ntfsundelete /dev/sda3 -u -m '*.docx' -d /media/external/recovered/
```

注意：刪除後磁碟有寫入過，被覆蓋的位置就回不來了。**越早救成功率越高**。

## 壞磁區掃描

```bash
# 唯讀掃描（安全，不會寫）
sudo badblocks -sv /dev/sda3

# 結果類似：
# Reading and comparing: done
# Pass completed, X bad blocks found. (X/X/0 errors)
```

有壞磁區的話：

```bash
# 把 NTFS metadata 標記這些位置不可用
# 先掛 -o ro 確認資料還在再做這步
sudo umount /mnt/win

# 在 NTFS 標記壞區（讀寫掛載的相反操作）
sudo badblocks -nsv /dev/sda3 > /tmp/badblocks.txt   # non-destructive write test，慢
# 不要用 -wsv！會洗掉資料
```

NTFS 自己有 `$BadClus` 處理壞磁區。Linux 沒有完美對應的工具更新它。最終 Windows 端跑 `chkdsk /r` 比較可靠。

實務做法：
1. badblocks -sv 確認真有壞磁區
2. SMART 看數量趨勢
3. 壞磁區多且在成長 → 不修，買新硬碟，先 ddrescue 救資料
4. 壞磁區少且穩定 → ddrescue 救資料、整碟 dump 後在新碟上跑 NTFS

## $LogFile 損壞

Windows 沒乾淨關機留下的 $LogFile 不一致是最常見的 dirty 原因。`ntfsfix` 會清掉。

如果 ntfsfix 抱怨 logfile：

```bash
sudo ntfsfix -d /dev/sda3   # 清 dirty
sudo ntfsfix -b /dev/sda3   # 清 logfile bad sectors（如有）
```

## 處理「Cannot read MFT, mft=0」

MFT（Master File Table）是 NTFS 的核心。MFT 不能讀 = NTFS 嚴重損壞。

```bash
sudo ntfsfix /dev/sda3
# 如果回 "Failed to read $MFT"
```

testdisk 可以嘗試從 MFT mirror 還原：

```bash
sudo testdisk /dev/sda3
# Advanced → Boot
# Backup BS：用 backup boot sector 還原 main
# Rebuild BS：完全重建（風險高）
```

兩個都失敗 → ddrescue 整碟，丟掉這顆硬碟。

## ntfsclone（NTFS 專用映像）

當你想完整備份 NTFS（比 dd 智慧、只 copy used space）：

```bash
# 整個分割區存成檔案
sudo ntfsclone --save-image -o /media/external/win.img /dev/sda3

# 還原
sudo ntfsclone --restore-image --overwrite /dev/sda3 /media/external/win.img
```

優點：略過 free space，比 dd 快很多、檔案小。
缺點：需要 NTFS 結構完整（dirty 太嚴重會失敗）。碟在壞時用 ddrescue 不是這個。

## 完整流程範例

「Windows 開機後跳 UNMOUNTABLE_BOOT_VOLUME 藍白字」：

```bash
# 1. SMART 確認硬體
sudo smartctl -H /dev/sda

# 2. 唯讀掛載看資料
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
ls /mnt/win/Users/

# 3. 備份重要資料
sudo rsync -avh --info=progress2 /mnt/win/Users/USERNAME/ /media/external/backup/

# 4. 卸載
sudo umount /mnt/win

# 5. ntfsfix
sudo ntfsfix --no-action /dev/sda3
sudo ntfsfix /dev/sda3

# 6. 試 rw 掛載
sudo mount -t ntfs-3g /dev/sda3 /mnt/win
# 成功 → 卸載讓 Windows 上次自然走 chkdsk
sudo umount /mnt/win

# 7. 告訴使用者重開機。Windows 進到桌面前可能會自動跑一次 chkdsk，那是正常的
```

修不動的話依次往下：testdisk → ddrescue → Windows 安裝媒體 chkdsk。
