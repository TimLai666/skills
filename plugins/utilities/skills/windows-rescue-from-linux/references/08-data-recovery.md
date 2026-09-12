# 08 — 資料救援

任何修復前優先把資料拿出來。這份涵蓋：

- 一般檔案備份（rsync）
- 整碟映像（ntfsclone、ddrescue）
- 已刪除檔案救援（testdisk、ntfsundelete、photorec、foremost）
- 失敗硬碟救援（ddrescue 完整流程）

## 第零步：判斷狀況等級

| 狀況 | 對應方法 |
|---|---|
| 磁碟健康、檔案系統正常、就是想備份 | rsync 或 ntfsclone |
| 磁碟健康、檔案系統有問題 | 先 ddrescue 做原始映像，在副本上處理 |
| 磁碟在壞（SMART 警告、有怪聲、I/O error） | ddrescue **務必** |
| 想救剛刪除的檔案 | testdisk / ntfsundelete（檔案還在原處） |
| 檔案系統毀掉，但資料區可能仍在 | photorec / foremost（檔案 carving） |

## 一般備份：rsync

磁碟穩定且檔案系統可讀時使用。先依 [安全原則](01-safety-principles.md) 確認來源與目標為不同實體儲存裝置；有 I/O 錯誤時改走下方 ddrescue 流程。

```bash
# 唯讀掛載來源
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 掛載備份目的地（外接碟）
sudo mount /dev/sdb1 /mnt/backup

# rsync
sudo rsync -avh --info=progress2 /mnt/win/Users/USERNAME/ /mnt/backup/$(date +%Y%m%d)/
```

選項：

| flag | 意義 |
|---|---|
| `-a` | archive 模式（保留權限、時間、符號連結等） |
| `-v` | verbose |
| `-h` | 人類可讀單位 |
| `--info=progress2` | 整體進度條（rsync 3.1+） |
| `--exclude=PATTERN` | 排除 |
| `--include=PATTERN` | 包含 |
| `--dry-run` | 只看會做什麼 |
| `-z` | 壓縮（傳網路時有用，本機沒必要） |
| `--partial` | 中斷後可續傳 |

**重要 exclude**（不浪費空間在垃圾上）：

```bash
sudo rsync -avh --info=progress2 \
    --exclude='AppData/Local/Temp' \
    --exclude='AppData/Local/Microsoft/Windows/INetCache' \
    --exclude='AppData/Local/Microsoft/Windows/Explorer' \
    --exclude='AppData/Roaming/Microsoft/Windows/Recent' \
    --exclude='.Trash*' \
    /mnt/win/Users/USERNAME/ \
    /mnt/backup/$(date +%Y%m%d)/
```

備份多使用者：

```bash
for user in /mnt/win/Users/*/; do
    [[ -d "$user" ]] || continue
    name=$(basename "$user")
    [ "$name" = "Public" ] && continue
    [ "$name" = "Default" ] && continue
    [ "$name" = "All Users" ] && continue
    echo "Backing up $name..."
    sudo rsync -avh --info=progress2 "$user" "/mnt/backup/$(date +%Y%m%d)/$name/" || break
done
```

備份特定關鍵資料夾（依本案需求選擇）：

```bash
RESCUE_USER=USERNAME
DEST=/mnt/backup/$(date +%Y%m%d)/$RESCUE_USER
sudo mkdir -p "$DEST"

for sub in Desktop Documents Downloads Pictures Videos Music; do
    [[ -d "/mnt/win/Users/$RESCUE_USER/$sub" ]] || continue
    sudo rsync -avh --info=progress2 \
        "/mnt/win/Users/$RESCUE_USER/$sub/" \
        "$DEST/$sub/" || break
done

# 瀏覽器資料（Chrome / Edge）
sudo rsync -avh \
    "/mnt/win/Users/$RESCUE_USER/AppData/Local/Google/Chrome/User Data/" \
    "$DEST/Chrome_UserData/"

sudo rsync -avh \
    "/mnt/win/Users/$RESCUE_USER/AppData/Local/Microsoft/Edge/User Data/" \
    "$DEST/Edge_UserData/"

# Outlook PST/OST
sudo rsync -avh \
    "/mnt/win/Users/$RESCUE_USER/AppData/Local/Microsoft/Outlook/" \
    "$DEST/Outlook/"
```

rsync 回傳非零代表有未完成或錯誤，保留日誌並查明原因後才判定完成。核對選定範圍的數量、大小，抽查重要檔案能開啟；需要內容比對時再核對雜湊。互動式選取與失敗處理見 [backup-user-data.sh](../scripts/backup-user-data.sh)。

## 映像：ntfsclone vs ddrescue 怎麼選

| 工具 | 適用場景 | 優點 | 缺點 |
|---|---|---|---|
| `ntfsclone` | 磁碟健康、NTFS 結構完整、只想備份用到的空間 | 只 copy used space，快、檔案小 | 結構毀掉就跑不了 |
| `ddrescue` | 磁碟在壞、結構毀掉、有 I/O error | 容錯強、可重試、map 檔紀錄進度 | 整碟 dump 含 free space，慢 |
| `dd` | 簡單測試 | 內建到處有 | 缺少 ddrescue 的 mapfile 與多階段救援控制 |

**碟有任何懷疑就用 ddrescue，不要用 dd**。

## ntfsclone 範例

`--save-image` 產生專用格式，不能直接 loop mount；只適用健康且結構可解析的 NTFS 分割區。還原至裝置會覆寫該分割區，須先確認目標與授權。

```bash
# 必須先 umount
sudo umount /mnt/win

# 存到檔案（特殊格式，比較小）
sudo ntfsclone --save-image -o /mnt/backup/win.img /dev/sda3

# 還原到別的（同大小或更大）分割區
sudo ntfsclone --restore-image --overwrite /dev/sdc1 /mnt/backup/win.img

# 還原到映像檔內（讓你用 loop mount 後讀）
# 輸出到新的原始映像檔，大小由原映像決定
sudo ntfsclone --restore-image --output /mnt/backup/win-raw.img /mnt/backup/win.img
sudo mount -o loop,ro /mnt/backup/win-raw.img /mnt/win-restored
```

## ddrescue：救快壞的硬碟

**核心觀念**：壞碟越讀越壞。ddrescue 用三階段策略：先撈簡單能讀的、再花時間慢慢試難讀的、不會卡在某個壞區無限重試。

### 擷取流程

先確認來源磁碟及所有分割區未掛載，目的地在另一顆健康磁碟且空間足夠。以下 `/dev/sda` 是整碟來源；只取單一分割區時須改用該分割區，並記錄映像種類。映像與 mapfile 成對保留，續跑時核對磁碟身分與原參數。

```bash
# 第一輪跳過 scraping，優先取得容易讀取的區段
sudo ddrescue -n /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
sudo ddrescuelog -t /mnt/backup/sda.map
```

第一輪後依未救出量、錯誤變化、溫度與異音決定是否重試。來源惡化或資料價值高時停止並交專業救援。來源穩定且仍有值得救的區段，才用同一組映像與 mapfile 做有限重試：

```bash
sudo ddrescue -d -r1 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
```

| 選項 | 用途 |
|---|---|
| `-n` | 跳過 scraping 階段，不逐區刮取難讀資料 |
| `-d` | 直接讀取來源，受裝置與扇區對齊限制；不支援時查明錯誤再調整 |
| `-r N` | 重試 pass 數量，依救援狀況設定 |
| `-R` | 反向讀取，可在有理由調整方向時使用 |

不需對一般映像檔加 `-f`。該選項允許覆寫裝置類型的輸出，不能用它略過目的地確認。

### ddrescue 進度判讀

跑的時候畫面：

```
ipos:    123456 MB, non-trimmed:   1024 kB,  current rate:   25600 kB/s
opos:    123456 MB, non-scraped:   2048 kB,  average rate:   18500 kB/s
non-tried:  256000 MB,  bad-sector:    512 B,    error rate:     128 B/s
rescued:   144000 MB,   bad areas:        3,        run time:      45m 12s
pct rescued:  56.25%, read errors:        7,  remaining time:      1h 23m
                              time since last successful read:          5s
```

- **rescued**：已成功讀取量；比例不能證明重要檔案完整
- **non-tried**：還沒讀的（會繼續減少）
- **non-trimmed**：讀過但有些 sector 失敗，沒去細分（後面 stage 處理）
- **non-scraped**：細分後的，每個 sector 試讀失敗
- **bad-sector**：目前未成功讀出的 sector，不代表後續必然無法讀取

### 映像存哪？空間需求？

要存 1TB 的硬碟映像需要 ≥1TB 的目的地空間。實務做法：

1. **目的地用新買的同樣大小硬碟**：dump 完直接 mount 那顆當還原版
2. **用外接硬碟存映像檔**：之後想用就 loop mount
3. **NAS / 網路硬碟**：用 NFS 或 SMB 掛起來當目的地

不要 dump 到 USB 隨身碟（太慢且 USB 隨身碟也容易出問題）。

### 擷取後：保留原始映像，唯讀取檔，修復用副本

```bash
sudo ddrescuelog -t /mnt/backup/sda.map
# 整碟映像需要分割區掃描；記錄回傳的 loop 裝置
sudo losetup --read-only --find --partscan --show /mnt/backup/sda.img
sudo lsblk /dev/loopX
sudo mount -t ntfs-3g -o ro /dev/loopXpY /mnt/recovered
# 依前節 rsync 選取資料並驗證
sudo umount /mnt/recovered
sudo losetup -d /dev/loopX
```

單一分割區映像使用 `losetup --read-only --find --show`，掛載回傳的 `/dev/loopX` 本身，沒有 `pY`。完成唯讀取檔後，若仍需修復 NTFS：

```bash
# 確認輸出副本尚不存在、目的地空間足夠
sudo cp --reflink=auto --sparse=always --no-clobber /mnt/backup/sda.img /mnt/backup/sda-work.img
# 若副本已存在，先確認來源與內容，不沿用未知副本
sudo losetup --find --partscan --show /mnt/backup/sda-work.img
# 確認回傳裝置與目標分割區皆未掛載，再依 05 選擇必要修復
# sudo ntfsfix /dev/loopYpZ
```

只修改工作副本，保留原始映像與 mapfile；中斷、失敗或修復惡化時可重新建立副本。來源壞碟先封存，未確認資料完整前不要處置。BitLocker 映像另接 [加密磁碟處理](10-bitlocker.md)。

## 救已刪除檔案：兩種思路

兩種根本不同：

### 思路 1：metadata 還在（檔案剛刪不久、檔案系統沒大改動）

→ 用 `ntfsundelete` 或 `testdisk`

```bash
# ntfsundelete：簡單直觀
sudo ntfsundelete /dev/sda3                    # 列表
sudo ntfsundelete /dev/sda3 -u -m '*.docx' -d /media/external/recovered/

# testdisk：互動式、視覺化
sudo testdisk /dev/sda
# Advanced → 選 NTFS 分割區 → Undelete → 選檔案複製到其他磁碟
```

成功率高的條件：
- 刪除後沒有大量寫入動作
- 分割區沒被格式化過
- 檔案不超大

### 思路 2：metadata 沒了（格式化過、檔案系統毀了）

→ 用 file carving 工具，掃 raw bytes 找已知檔案類型的 signature

```bash
# PhotoRec（最常用）
sudo apt install testdisk    # photorec 跟 testdisk 同套件

sudo photorec /dev/sda
# 互動式
# 選磁碟 → 選分割區 → 選檔案系統類型（NTFS, Other, ...）→ 選輸出目錄

# Foremost
sudo apt install foremost
sudo foremost -t doc,docx,xls,xlsx,pdf,jpg,png -i /dev/sda3 -o /media/external/foremost/
```

PhotoRec 找到的檔案不會帶原檔名（metadata 已失）。會是 `f1234567.docx` 這樣的命名。能否恢復內容取決於資料是否仍存在、是否碎片化及工具支援；已覆寫的位元無法藉此找回。

**輸出目錄一定要在外接碟，不能在原碟**：寫入會覆蓋掉還沒救到的資料。

PhotoRec 跑得很慢（整碟掃描），可能要幾小時到一天。準備好等。

## 只救資料時的停止點

能讀取且已核對所需檔案，就不必繼續修系統。依前述分流選擇 rsync 或映像取檔，驗證重要檔案後，將成果另存到第二個實體裝置。

## 防止以後再發生：教育使用者

救完之後跟使用者談談備份：

- **3-2-1 原則**：3 份備份，2 種媒介，1 份離線/異地
- **同步不等於獨立備份**：同步不是備份（同步刪除會同步生效）
- **自動化**：減少依賴臨時手動操作，設好排程
- **定期測試**：備份救得回來才算備份

具體建議：
- Windows 內建「檔案歷程記錄」+ 外接碟
- 或 Backblaze / OneDrive / Google Drive（但要開「版本歷史」）
- 或 NAS + Synology Hyper Backup

## 故障排除

### ddrescue 中斷不能續

先核對來源裝置、映像路徑、權限、空間與 map 檔是否一致。檢查 map 檔：

```bash
ddrescuelog -t /mnt/backup/sda.map
# 如果 map 檔有錯它會報
```

map 檔好的話 `ddrescue` 會自動從上次中斷的地方接續。

### 「Device or resource busy」

碟有人在用。先 `umount`，看 `lsof` 是誰：

```bash
sudo umount /mnt/win
sudo lsof /dev/sda
sudo fuser -vm /dev/sda
```

### rsync 速度很慢

- 來源是 USB 2.0 → 換 USB 3.0
- 大量小檔（瀏覽器快取、git repo）→ rsync 對小檔效率低，先打包：
  ```bash
  sudo tar cf - /mnt/win/Users/USERNAME/ | pv | tar xf - -C /mnt/backup/
  ```
- 來源碟在壞 → ddrescue 整碟，不要 rsync

### NTFS permission 跳出 access denied 之類

掛載時加 uid/gid，或忽略權限：

```bash
sudo mount -t ntfs-3g -o ro,uid=$(id -u),gid=$(id -g),umask=022 /dev/sda3 /mnt/win
```

NTFS 上的 Windows ACL 是另一個系統，Linux 端是「猜測對應」。救資料用 root 操作通常就能讀到所有東西。
