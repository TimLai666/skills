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
| 磁碟健康、檔案系統有問題 | 先 ntfsclone 做映像，在映像上動 |
| 磁碟在壞（SMART 警告、有怪聲、I/O error） | ddrescue **務必** |
| 想救剛刪除的檔案 | testdisk / ntfsundelete（檔案還在原處） |
| 想救已被覆蓋或檔案系統毀掉的檔案 | photorec / foremost（檔案 carving） |

## 一般備份：rsync

最常用、最安全。

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
    name=$(basename "$user")
    [ "$name" = "Public" ] && continue
    [ "$name" = "Default" ] && continue
    [ "$name" = "All Users" ] && continue
    echo "Backing up $name..."
    sudo rsync -avh --info=progress2 "$user" "/mnt/backup/$(date +%Y%m%d)/$name/"
done
```

備份特定關鍵資料夾（最小集合）：

```bash
USER=USERNAME
DEST=/mnt/backup/$(date +%Y%m%d)/$USER
sudo mkdir -p "$DEST"

for sub in Desktop Documents Downloads Pictures Videos Music; do
    sudo rsync -avh --info=progress2 \
        "/mnt/win/Users/$USER/$sub/" \
        "$DEST/$sub/"
done

# 瀏覽器資料（Chrome / Edge）
sudo rsync -avh \
    "/mnt/win/Users/$USER/AppData/Local/Google/Chrome/User Data/" \
    "$DEST/Chrome_UserData/"

sudo rsync -avh \
    "/mnt/win/Users/$USER/AppData/Local/Microsoft/Edge/User Data/" \
    "$DEST/Edge_UserData/"

# Outlook PST/OST
sudo rsync -avh \
    "/mnt/win/Users/$USER/AppData/Local/Microsoft/Outlook/" \
    "$DEST/Outlook/"
```

## 整碟映像：ntfsclone vs ddrescue 怎麼選

| 工具 | 適用場景 | 優點 | 缺點 |
|---|---|---|---|
| `ntfsclone` | 磁碟健康、NTFS 結構完整、只想備份用到的空間 | 只 copy used space，快、檔案小 | 結構毀掉就跑不了 |
| `ddrescue` | 磁碟在壞、結構毀掉、有 I/O error | 容錯強、可重試、map 檔紀錄進度 | 整碟 dump 含 free space，慢 |
| `dd` | 簡單測試 | 內建到處有 | 一遇到 error 就停或無限重試，慢且傷碟 |

**碟有任何懷疑就用 ddrescue，不要用 dd**。

## ntfsclone 範例

```bash
# 必須先 umount
sudo umount /mnt/win

# 存到檔案（特殊格式，比較小）
sudo ntfsclone --save-image -o /mnt/backup/win.img /dev/sda3

# 還原到別的（同大小或更大）分割區
sudo ntfsclone --restore-image --overwrite /dev/sdc1 /mnt/backup/win.img

# 還原到映像檔內（讓你用 loop mount 後讀）
# 先準備一個跟原分割區同樣大的空檔
truncate -s 500G /mnt/backup/win-raw.img
sudo ntfsclone --restore-image --overwrite /mnt/backup/win-raw.img /mnt/backup/win.img
sudo mount -o loop,ro /mnt/backup/win-raw.img /mnt/win-restored
```

## ddrescue：救快壞的硬碟

**核心觀念**：壞碟越讀越壞。ddrescue 用三階段策略：先撈簡單能讀的、再花時間慢慢試難讀的、不會卡在某個壞區無限重試。

### 基本流程

```bash
sudo apt install gddrescue   # 套件叫 gddrescue，指令叫 ddrescue

# 必須有：
# 1. 來源 = 壞的 Windows 系統碟 /dev/sda
# 2. 目的 = 一顆全新或夠大的硬碟，或一個大的映像檔
# 3. mapfile = 紀錄進度，可以中斷後續跑

# 整碟 dump 到映像檔（外接碟空間要夠）
sudo ddrescue -d -r0 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map

# 完成後第二次跑（再試之前失敗的區段）
sudo ddrescue -d -r3 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map

# 更激進（最多花時間搶救剩餘壞區）
sudo ddrescue -d -r5 -R /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
```

選項：

| flag | 意義 |
|---|---|
| `-d` | direct I/O（繞過 OS 快取，比較準） |
| `-r N` | 失敗時重試 N 次（第一次設 0 先快速 copy 能讀的） |
| `-R` | reverse direction（從尾巴開始讀） |
| `-n` | 不 split bad blocks（更省事第一次用） |
| `-c N` | cluster size（預設 64 sector） |

### 多階段策略（救命用）

```bash
# Stage 1: 快速撈所有能讀的（不浪費時間在壞區）
sudo ddrescue -f -n -d /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map

# Stage 2: 切割壞區域，多試幾次能讀的
sudo ddrescue -d -r3 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map

# Stage 3: 反方向讀（有時讀寫頭往不同方向能多救一點）
sudo ddrescue -d -r3 -R /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map

# Stage 4: 大絕招（會花很久）
sudo ddrescue -d -r20 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
```

期間如果磁碟越來越燙、噪音越來越大 → 停手，可能要進無塵實驗室。一般使用者到 stage 2 結束就差不多了。

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

- **rescued**：已救出量（%多少最重要）
- **non-tried**：還沒讀的（會繼續減少）
- **non-trimmed**：讀過但有些 sector 失敗，沒去細分（後面 stage 處理）
- **non-scraped**：細分後的，每個 sector 試讀失敗
- **bad-sector**：確定壞掉的 sector

### 映像存哪？空間需求？

要存 1TB 的硬碟映像需要 ≥1TB 的目的地空間。實務做法：

1. **目的地用新買的同樣大小硬碟**：dump 完直接 mount 那顆當還原版
2. **用外接硬碟存映像檔**：之後想用就 loop mount
3. **NAS / 網路硬碟**：用 NFS 或 SMB 掛起來當目的地

不要 dump 到 USB 隨身碟（太慢且 USB 隨身碟也容易出問題）。

### ddrescue 完成後

```bash
# 看 mapfile 統計
sudo ddrescuelog -t /mnt/backup/sda.map

# 試 mount 救出來的映像
sudo losetup -fP --show /mnt/backup/sda.img    # 顯示 /dev/loopX
sudo lsblk /dev/loopX                          # 看分割區
sudo mount -t ntfs-3g -o ro /dev/loopXpY /mnt/recovered/

# 在 recovered 映像上跑後續修復（不會傷原本壞掉的硬碟）
sudo ntfsfix /dev/loopXpY    # 範例
```

之後所有 ntfsfix、testdisk、chntpw 等動作都對映像做。原本的壞硬碟封存或丟掉。

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
# Analyse → 選分割區 → P 進去看檔案 → 紅色是刪除的 → c 複製到別處
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

PhotoRec 找到的檔案不會帶原檔名（metadata 已失）。會是 `f1234567.docx` 這樣的命名。但內容會在。

**輸出目錄一定要在外接碟，不能在原碟**：寫入會覆蓋掉還沒救到的資料。

PhotoRec 跑得很慢（整碟掃描），可能要幾小時到一天。準備好等。

## 為了救資料而救資料：最小流程

「電腦壞了，我只要把照片救出來，系統不修了」：

```bash
# 1. 先 SMART 確認碟的狀態
sudo smartctl -H /dev/sda
sudo smartctl -a /dev/sda | grep -E "Reallocated|Pending|Uncorrectable"

# 健康 → 走 rsync 流程

# 健康但檔案系統有問題 → ntfsclone 做映像，loop mount 救資料
sudo ntfsclone --save-image -o /mnt/backup/win.img /dev/sda3
# 然後 mount 那個映像來救

# 不健康 → ddrescue 整碟
sudo ddrescue -d -n /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
sudo ddrescue -d -r3 /dev/sda /mnt/backup/sda.img /mnt/backup/sda.map
# 之後 loop mount 在 sda.img 上救資料

# 2. 救完驗證
ls -lh /mnt/backup/...
# 抽幾個檔案打開看內容是不是真的（不是 0 byte 或損毀）

# 3. 至少做兩份備份（不同實體裝置）
sudo cp -a /mnt/backup/USERNAME /mnt/backup2/
```

## 防止以後再發生：教育使用者

救完之後跟使用者談談備份：

- **3-2-1 原則**：3 份備份，2 種媒介，1 份離線/異地
- **雲端不算備份**：同步不是備份（同步刪除會同步生效）
- **自動化**：手動備份十次有八次會忘，設好排程
- **定期測試**：備份救得回來才算備份

具體建議：
- Windows 內建「檔案歷程記錄」+ 外接碟
- 或 Backblaze / OneDrive / Google Drive（但要開「版本歷史」）
- 或 NAS + Synology Hyper Backup

## 故障排除

### ddrescue 中斷不能續

map 檔損壞。檢查：

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
