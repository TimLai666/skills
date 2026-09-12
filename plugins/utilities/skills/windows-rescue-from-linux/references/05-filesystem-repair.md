# 05 — 檔案系統與分割表修復

NTFS 修復、分割表壞掉的救援、磁碟看不到分割區的恢復。操作前先讀 [01 安全原則](01-safety-principles.md) 與 [03 掛載](03-mount-windows.md)。有 I/O 錯誤、斷線或硬體退化跡象時，先依 [08 資料救援](08-data-recovery.md) 製作映像，再對副本修復。

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

較完整的 NTFS 修復需交給 Windows 的 `chkdsk /f`；`/r` 會額外掃描磁區，依硬體狀況與備份決定是否需要。ntfsfix 可能讓磁碟區重新掛載，並安排 Windows 下次檢查，不能保證可開機。

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

→ 工具處理完成，先唯讀重掛確認檔案可讀；仍需 Windows 端檢查。

```
Volume is corrupt. You should run chkdsk.
```

→ ntfsfix 修不了。下面有 workaround。

```
Failed to read $MFT: Input/output error
```

→ 讀取失敗，可能涉及磁碟、線材或控制器。停止原碟修復，改走 [08 資料救援](08-data-recovery.md)。

## 修不動時的 workaround

ntfsfix 失敗但磁碟硬體 OK 時，幾個方向：

### A. dirty 旗標

`ntfsfix -d` 只有在磁碟區能修復並掛載時才清除 dirty 旗標，不是強制略過損壞。一般修復保留預設安排 Windows 檢查的行為，不把清旗標當成修復成功。

### B. 複製到健康磁碟後清除舊壞磁區清單

`ntfsfix -b` 清除 NTFS 記錄的壞磁區清單，用於已從故障碟複製到健康新碟的磁碟區。它不修復實體磁區，也不是清理 logfile 的選項；不要拿原故障碟反覆執行。

依據：[ntfsfix 手冊](https://manpages.debian.org/bookworm/ntfs-3g/ntfsfix.8.en.html)。

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

### E. 使用 Windows 檢查

需 Windows 端檢查時，依 [13 Windows 修復](13-when-linux-cannot-fix.md) 確认 WinRE 磁碟代號，再對已備份的磁碟區執行 chkdsk。

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
sudo sgdisk -b /media/external/gpt-backup.bin /dev/sda   # 先備份目前 GPT
# 僅在磁碟容量改變、備份 GPT 位置不符且已核對分割範圍時：
sudo sgdisk -e /dev/sda   # 把 backup GPT 移到目前磁碟末端
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
sudo sfdisk -d /dev/sda > /media/external/sda-pt-backup-$(date +%Y%m%d).txt
# 寫錯了 → 還原
sudo sfdisk /dev/sda < /media/external/sda-pt-backup-YYYYMMDD.txt
```

## NTFS undelete（救剛刪除的檔案）

`testdisk` 也能在 NTFS 上找回剛刪的檔案：

```bash
sudo testdisk /dev/sda3
# Advanced → 選 NTFS 分割區 → Undelete
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

## 壞磁區與 $LogFile 損壞

疑似故障原碟不先跑整碟 badblocks 或長測試，唯讀掃描也會增加負荷。先參照 [09 硬體診斷](09-hardware-diagnostics.md) 判斷，再依 [08 資料救援](08-data-recovery.md) 把可讀資料救到健康媒體。

`badblocks -n` 是會寫入的讀寫測試，不會替 NTFS 更新 `$BadClus`；不能拿它當修復指令。已完成備份、需要驗證可汰換的測試磁碟時，才另外安排表面測試。

`$LogFile` 是 NTFS 交易日誌。一般 ntfsfix 已會重設日誌；報錯時保留原始輸出，依錯誤判斷檔案系統或硬體問題，不連續堆疊 `-d`、`-b` 當作萬用修復。

## 處理「Cannot read MFT, mft=0」

MFT（Master File Table）是 NTFS 的核心。MFT 不能讀 = NTFS 嚴重損壞。

```bash
sudo ntfsfix /dev/sda3
# 如果回 "Failed to read $MFT"
```

testdisk 可以嘗試從 MFT mirror 還原：

```bash
sudo testdisk /dev/sda3
# Advanced → 選 NTFS 分割區 → Boot → Repair MFT
# 比較 MFT 與 MFTMirr；先確認哪份可用，再決定修復方向
```

若是讀取錯誤，先救映像再處理；若硬體可讀但結構仍無法修復，在副本上進行檔案救援。結構損壞本身不代表硬碟必須丟棄。

## ntfsclone（NTFS 專用映像）

當你想完整備份 NTFS（比 dd 智慧、只 copy used space）：

```bash
# 存為 ntfsclone 專用映像，不能直接 loop mount
sudo ntfsclone --save-image -o /media/external/win.img /dev/sda3

# 還原會覆寫指定分割區；先確認目標與備份
sudo ntfsclone --restore-image --overwrite /dev/sda3 /media/external/win.img
```

優點：略過 free space，比 dd 快很多、檔案小。
缺點：需要 NTFS 結構完整（dirty 太嚴重會失敗）。碟在壞時用 ddrescue 不是這個。

## 症狀範例：UNMOUNTABLE_BOOT_VOLUME

先區分「讀不到磁區」與「可讀但 NTFS 結構不一致」。前者先救映像，後者在完成備份後執行本節的 ntfsfix 檢查與必要修復。若仍失敗，依 boot sector、MFT 或分割表證據選 TestDisk，或交給 Windows chkdsk，避免把所有工具依序跑一遍。


TestDisk 操作依據：[NTFS 開機磁區與 MFT 修復](https://www.cgsecurity.org/wiki/Advanced_NTFS_Boot_and_MFT_Repair)、[NTFS undelete](https://www.cgsecurity.org/wiki/Undelete_files_from_NTFS_with_TestDisk)。
