# 15 — 從 Windows 映像提取與替換個別系統檔

有系統檔遺失／損壞線索，並有 Windows ISO、WIM、ESD、分割 WIM（SWM）或系統備份映像時讀這份。目標是提取所需檔案、替換故障系統中的對應檔案，再實際測試能否恢復開機。

## 確定要換哪一份

根據開機錯誤的完整路徑、修復日誌、檔案讀取錯誤或已知正常來源的比對，選出候選檔案。藍畫面提到某個 driver，不一定是該檔案損壞，可能是依賴、設定或硬體問題；把依據與未知部分分開記錄。

先依 [01](01-safety-principles.md) 確認裝置、重要資料與備份，依 [03](03-mount-windows.md) 唯讀掛載。硬碟有讀取故障先走 [08](08-data-recovery.md) 的映像路徑。

來源選擇：

| 手上的映像 | 如何取檔 |
|---|---|
| 安裝 ISO | 唯讀掛載，找 `sources/install.wim`、`install.esd` 或 `install*.swm` |
| WIM／ESD | 用 wimlib 查 index、列檔案與提取；加密 ESD 需先取得可讀來源 |
| SWM | 第一片為來源，透過 `--ref` 提供其他分片，不能缺片 |
| `boot.wim`／`winre.wim` | 是 WinPE／WinRE，內容與已安裝 Windows 不同；核對指定檔案後才作候選，不當完整系統來源 |
| raw 整碟／分割區備份 | 依 [08](08-data-recovery.md) 唯讀掛載正確分割區，複製所需檔案到暫存區 |
| VHD／VHDX 等容器 | 先辨識格式，用支援該格式的唯讀工具呈現分割區；不能直接按 raw offset 掛載 |

優先使用官方或可追溯的正常來源。比較 Windows 架構、build／更新層級、版本與相關語言，以及指定檔案的版本、路徑與依賴。不只看 ISO 名稱，也不把 WIM index 當成固定的 Home／Pro 編號。

版本不符或部分資訊無法確認時，可以嘗試。指出已知差異、為何值得試、可能無效或造成新的開機／相依錯誤，讓使用者選擇，再沿用下列備份、替換與還原流程。版本不符不自動禁止操作；同名也不自動證明可相容。

## 列出與提取

需要時安裝發行版的 `wimtools`。以下在 Linux Bash 執行，先把路徑與 index 換成本案查到的值，暫存區放在健康外接碟。各命令成功才接下一步。

```bash
# ISO 唯讀掛載；已有 WIM／ESD 可略過
sudo mkdir -p /mnt/windows-iso
sudo mount -o loop,ro /path/to/Windows.iso /mnt/windows-iso
ls -l /mnt/windows-iso/sources/install.*

# 先列 index、名稱、架構與版本資訊
wimlib-imagex info /mnt/windows-iso/sources/install.wim
```

選定 index 後，用完整路徑查閱，不讓空路徑變成提取整個映像：

```bash
RESCUE_WIM=/mnt/windows-iso/sources/install.wim
RESCUE_INDEX=1  # 例子：改成實際選定的 index
RESCUE_PATH=/Windows/System32/drivers/example.sys  # 改成已確認的映像內路徑
RESCUE_STAGE=$(mktemp -d /mnt/backup/file-extract.XXXXXX) || exit 1

wimlib-imagex dir "$RESCUE_WIM" "$RESCUE_INDEX" --path="$RESCUE_PATH"
wimlib-imagex extract "$RESCUE_WIM" "$RESCUE_INDEX" "$RESCUE_PATH" \
  --dest-dir="$RESCUE_STAGE" --preserve-dir-structure --no-globs --check
```

ESD 直接換來源路徑。SWM 的提取命令加上 `--ref='/mnt/windows-iso/sources/install*.swm'`，引號保留給 wimlib 處理分片。Linux 路徑比對預設區分大小寫，要依 `dir` 的結果使用確切名稱。提取找不到路徑、缺分片或退出非零時，保留錯誤，不能接著用空檔案替換。

`--check` 只在映像具有完整性資訊時檢查該資訊，不證明檔案版本相容。提取先落到暫存區，不直接把 WIM 展開到故障系統。

## 比較來源與目標

```bash
RESCUE_CANDIDATE="$RESCUE_STAGE$RESCUE_PATH"
RESCUE_TARGET="/mnt/win$RESCUE_PATH"
file -- "$RESCUE_CANDIDATE" "$RESCUE_TARGET"
sha256sum -- "$RESCUE_CANDIDATE" "$RESCUE_TARGET"
stat -- "$RESCUE_TARGET"
```

檢查 PE 的架構、檔案版本與簽章資訊，可用已安裝的 PE 工具，或在 Windows／WinRE 查看。目標系統版本可唯讀讀取 SOFTWARE hive 的 `Microsoft\Windows NT\CurrentVersion`（如 CurrentBuildNumber、UBR、EditionID），方法見 [06](06-registry-edit.md)。檔案已損壞時，無法讀出版本也要記錄。

不同雜湊只證明內容不同，不直接證明損壞。SFC／DISM 需要的修復來源另受元件與更新層級影響，見 [13](13-when-linux-cannot-fix.md)。

## 備份與替換

先保存原檔到本案的外接備份目錄，比對備份內容並記錄雜湊。Windows 權限、替代資料流、硬連結等資料，不會因為在 Linux 上用 `cp -a` 就完整保存；需要完整退回時保留未修改的 NTFS 映像。

Windows 系統檔可能與 WinSxS 共用同一份內容（硬連結）。檢查目標連結數與同卷的對應路徑；原地寫入會一起改變所有共用路徑。先說明這些實際影響，備份涵蓋它們再試，不為了替換一個檔案改動整個 WinSxS 目錄。來源或目標是 reparse point、壓縮指標等特殊檔案時，改用能正確處理其語意的工具，或交接 WinRE。

以下範例適用於已存在的普通檔案，且目標不是符號連結。連結數大於 1 時，先在健康磁碟／映像上用 `sudo find /mnt/win -xdev -samefile "$RESCUE_TARGET" -print` 列出共用路徑，保留未修改的 NTFS 映像，並確認使用者接受這些路徑一起改變。之後用同一組原地覆寫命令，還原時也會一起還原共用內容。取得本次寫入授權、確認可寫掛載後執行：

```bash
# 在唯讀階段先建立唯一備份目錄並保存原檔
RESCUE_BACKUP=$(mktemp -d /mnt/backup/file-original.XXXXXX) || exit 1
test -f "$RESCUE_CANDIDATE" && test -s "$RESCUE_CANDIDATE" || exit 1
test -f "$RESCUE_TARGET" && test ! -L "$RESCUE_TARGET" || exit 1
stat -c 'inode=%i links=%h size=%s' -- "$RESCUE_TARGET"
sudo cp -- "$RESCUE_TARGET" "$RESCUE_BACKUP/original"
sudo cmp -- "$RESCUE_TARGET" "$RESCUE_BACKUP/original" || exit 1
sha256sum -- "$RESCUE_BACKUP/original" "$RESCUE_CANDIDATE"

# 依 03 重新掛為可寫，再次核對掛載來源、路徑與原檔未變後：
sudo cmp -- "$RESCUE_TARGET" "$RESCUE_BACKUP/original" || exit 1
sudo cp --no-preserve=mode,ownership -- "$RESCUE_CANDIDATE" "$RESCUE_TARGET" || exit 1
sudo cmp -- "$RESCUE_CANDIDATE" "$RESCUE_TARGET" || exit 1
sudo sync
sudo umount /mnt/win
```

此例覆寫既有檔案內容，避免刪掉原 inode 再建檔。它不宣稱可還原所有 Windows 中繼資料。若目標原本遺失，記錄「原本不存在」，另確認父目錄、ACL 與相依元件如何建立，不能把新增檔案套進上述既有檔案範例。

若先在修復副本試改，需將該副本置於替代磁碟並接回原機測試，或在確認還原目標後還原該分割區。不要只改映像就聲稱故障電腦已修好。需要正式處理元件關係時，也可選擇 SFC／DISM。

## 開機驗證與還原

檔案比較通過、正常卸載後再試開機。檢查原錯誤是否消失、有無新錯誤，以及相關功能是否可用。能進 Windows 後，依需要用 SFC／DISM 檢查系統一致性，尤其是跨版本替換。

失敗時回到 Linux，先保存這次錯誤與現況。原地覆寫的例子，可在核對同一裝置、同一路徑與共用路徑後恢復原內容：

```bash
# 已依 03 掛為可寫，且核對替換後檔案沒有其他變更
sudo cp --no-preserve=mode,ownership -- "$RESCUE_BACKUP/original" "$RESCUE_TARGET" || exit 1
sudo cmp -- "$RESCUE_BACKUP/original" "$RESCUE_TARGET" || exit 1
sudo sync
sudo umount /mnt/win
```

若重開後變數已消失，從救援紀錄還原路徑，不能猜原備份是哪一份。涉及硬連結、ACL 或新增檔案時，依事先選定的映像／檔案還原方式處理。不要連續覆蓋唯一備份或無依據地試遍不同版本。

回報來源映像、index、目標路徑、版本差異、備份位置與三項結果：提取、替換、開機。尚未測試開機就明確記錄待驗證。

## 工具依據

- [wimextract](https://wimlib.net/man1/wimextract.html)：個別路徑提取、index、SWM、大小寫與輸出位置。
- [wimapply](https://wimlib.net/man1/wimapply.html)：Unix 目錄提取的 Windows 中繼資料限制；完整 apply 不適合拿來覆蓋故障系統做單檔修復。
- [Microsoft 修復來源](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-a-windows-repair-source?view=windows-11)：元件來源的更新層級與語言要求。
