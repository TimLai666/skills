# 12 · 使用者 Profile 損壞處理

> **核心觀念**：使用者登入後變成 Temp Profile、桌面是空的、文件全不見 —— 多半是 `NTUSER.DAT` 損壞或 ProfileList 指向錯地方。從 Linux 端能做兩件事：救出舊 profile 的資料、修 ProfileList registry 讓 Windows 重新指認 profile。重建乾淨的新 profile 必須回到 Windows 才能完整完成（建立帳號需要 Windows API），Linux 只能搬資料。

備份與掛載先讀 [01](01-safety-principles.md)、[03](03-mount-windows.md)；所有 hive 修改使用 [06 的工作副本合併與比對流程](06-registry-edit.md)。

---

## 1. 症狀識別

| 症狀 | 待查方向 |
|---|---|
| 「You've been signed in with a temporary profile」 | NTUSER.DAT 損壞 / ProfileList 指錯 |
| 桌面空了，預設背景，所有設定都不見 | 同上 |
| 「The User Profile Service failed the sign-in」 | ProfileList 裡的 SID 標 `.bak` |
| 登入很慢然後桌面空 | hive 讀取、磁碟或設定載入失敗 |
| 進桌面後特定 App 開不起來 | 該 App 在 NTUSER.DAT 的設定壞了 |
| 「Group Policy Client service failed sign-in」 | 群組原則服務、權限或 hive 載入問題 |

---

## 2. 先弄懂 ProfileList 結構

```text
# 掛 Windows
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# Profile 列表在 SOFTWARE hive
cd /mnt/win/Windows/System32/config
# 依 06 把 hive 與日誌備份到外接健康磁碟

sudo hivexsh SOFTWARE
> cd Microsoft\Windows NT\CurrentVersion\ProfileList
> ls
# 看到一堆 S-1-5-XX-... 開頭的 key，這些是使用者 SID
```

### ProfileList 結構

```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\
├── S-1-5-18                         ← LocalSystem
├── S-1-5-19                         ← LocalService
├── S-1-5-20                         ← NetworkService
├── S-1-5-21-XXXXXXXXXX-1001         ← 第一個本機/網域使用者
├── S-1-5-21-XXXXXXXXXX-1001.bak    ← 出問題會多這個 .bak 版本
└── ...
```

每個 SID 底下有：
- `ProfileImagePath` = `C:\Users\Alice`（指向 profile 資料夾）
- `State` = profile 狀態旗標，非零不一定表示損壞
- `RefCount` = 參照計數，並非每次登入累積的次數
- `Flags` = 帳號類型

---

## 3. 修 ProfileList

先匯出問題 SID 與同名 `.bak` 分支，檢查 `ProfileImagePath` 指向的資料夾、NTUSER.DAT 是否可讀、原使用者 SID 與服務事件紀錄。兩個分支存在不代表 `.bak` 多餘，不能直接刪除或假設 Windows 會自動合併。

### 路徑或狀態值錯誤

若證據已確認正確資料夾是 `C:\Users\Alice`，在 SOFTWARE 工作副本合併對應變更。以下 SID 為範例，需換成實際使用者；只放入本案確認需要修改的值。

```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-21-1234567890-1234567890-1234567890-1001]
"ProfileImagePath"=hex(2):43,00,3a,00,5c,00,55,00,73,00,65,00,72,00,73,00,5c,00,41,00,6c,00,69,00,63,00,65,00,00,00
"State"=dword:00000000
```

`hex(2)` 保留 REG_EXPAND_SZ 型別，上例編碼的是 `C:\Users\Alice`。更換路徑時重新產生 UTF-16LE 加結尾零位元的資料，不沿用範例位元組。若只修正 `State`，省略路徑那一列；先查其非零原因，不能把所有非零狀態清成 0。

```python
# 將已確認的 Windows 路徑轉為 .reg 的 REG_EXPAND_SZ 資料
path = r"C:\Users\Alice"
print('"ProfileImagePath"=hex(2):' + ','.join(f'{b:02x}' for b in (path + '\0').encode('utf-16le')))
```

依 [06](06-registry-edit.md) 合併並匯出前後差異，確保 `Flags`、`Sid` 等其他資料保留。

### 正確設定都在 `.bak` 分支

需要更名整個 SID 分支時，優先在另一個管理員帳號或 WinRE 載入 SOFTWARE 後，用 Registry Editor 對照並改名，保留衝突分支的匯出備份。若在 Linux 做，須完整匯出來源分支、將 key 路徑改成確認的目的 SID，再於工作副本合併並逐項比對子 key 與所有型別、值。先處理目的分支衝突，確認新分支完整後才移除舊分支；不要只抄 ProfileImagePath 與 State 重建整個 SID。

## 4. NTUSER.DAT 損壞處理

每個使用者的 registry 都在他自己資料夾的 `NTUSER.DAT`：

```bash
ls -la /mnt/win/Users/Alice/NTUSER.DAT*
# NTUSER.DAT          ← 主檔
# NTUSER.DAT.LOG1     ← 寫入日誌
# NTUSER.DAT.LOG2
# NTUSER.DAT{<guid>}.TM.blf  ← Transactional Manager
# NTUSER.DAT{<guid>}.TMContainer*  ← TM container
```

### 4.1 看 NTUSER.DAT 健不健康

```text
sudo cp /mnt/win/Users/Alice/NTUSER.DAT /tmp/test-ntuser.dat

# 試著 load
sudo hivexsh /tmp/test-ntuser.dat
> ls
# 能讀出這些 key 只代表可解析，不能證明全部設定與交易狀態完整
# 如果報錯 "hivex_open: bad magic"，hive 損壞
```

### 4.2 用備份還原

保留 NTUSER.DAT 與所有同名交易日誌，再從已知良好的使用者備份或 Windows 還原點復原。`.LOG1` / `.LOG2` 是交易日誌，不能當成整份 hive 複製；需要能重播 Windows registry 日誌的工具。只會列出 hive 內容的工具不等於能重播日誌。

### 4.3 重置 NTUSER.DAT

重置會丟失此 hive 內的使用者與應用程式設定。優先依下一節在 Windows 建立新 profile 並搬資料，讓 Windows 建立正確權限與帳號關聯。

若選擇以 Default 的 hive 嘗試重置，先完整備份原 NTUSER.DAT 與同名日誌、交易檔，確認 Default hive 可讀；將舊日誌移到備份位置而非刪除，再替換 hive 並保留目的檔案的 NTFS 權限。測試失敗需整組還原 hive 與日誌，不能混用新 hive 和舊交易檔。

### 4.4 Hive 異常增大

檔案大小或成長速度可作為線索，但沒有通用的健康大小門檻。對照登入事件、近期安裝的應用程式與 hive 內容，找出是否有大量重複設定。不要只因超過某個 MB 數就重置；需整理 hive 時，備份後回 Windows 使用適合該問題的登錄工具，或建立新 profile。

## 5. 建立全新 profile 給使用者

**Linux 端做不到完整建帳號**（需要 LSA / SAM API），但能幫使用者搬資料：

### 5.1 讓 Windows 建立新 profile

1. 在 Windows 用另一個管理員帳號建立新本機帳號 `Alice2`。
2. 登入新帳號，讓 Windows 建立 profile 與權限。
3. 從舊 Alice 的備份挑選資料搬入，避免整包覆蓋新的 AppData 與 hive。

目前無法登入時，Linux 先把資料備份到外接碟；單獨複製 Default 資料夾不會建立可登入的帳號。

### 5.2 從舊 profile 搬資料到新 profile

這是 Linux 端能做的事，而且很適合：

```bash
# 重要：先 ro 掛載確認資料還在
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 看舊 profile
ls /mnt/win/Users/Alice/

# 要搬的（白名單）：
# - Desktop          ← 桌面檔案
# - Documents
# - Downloads
# - Pictures / Videos / Music
# - Favorites        ← IE/Edge 我的最愛
# - AppData/Local/Google/Chrome/User Data    ← Chrome 整包
# - AppData/Local/Microsoft/Edge/User Data   ← Edge 整包
# - AppData/Roaming/Microsoft/Outlook        ← Outlook PST
# - AppData/Roaming/Microsoft/Signatures     ← Outlook 簽名
# - AppData/Roaming/Mozilla/Firefox          ← Firefox 整包

# 不要搬的（黑名單）：
# - NTUSER.DAT*                              ← 這是壞的，搬過去白搬
# - AppData/Local/Temp                       ← 暫存
# - AppData/Local/Microsoft/Windows/INetCache
# - AppData/Local/Microsoft/Windows/WebCache
# - AppData/Local/Microsoft/Windows/Explorer ← thumbcache
# - AppData/Local/Packages                   ← Windows Store App settings
#   (這個有些重要，例如 Sticky Notes 內容，看情況挑)

# 範例：先備份到外接碟（不要直接 Linux 端寫 NTFS 系統碟）
sudo rsync -aHv --info=progress2 \
    --exclude='NTUSER.DAT*' \
    --exclude='ntuser.*' \
    --exclude='AppData/Local/Temp' \
    --exclude='AppData/Local/Microsoft/Windows/INetCache' \
    --exclude='AppData/Local/Microsoft/Windows/WebCache' \
    --exclude='AppData/Local/Microsoft/Windows/Explorer' \
    --exclude='AppData/LocalLow/Temp' \
    /mnt/win/Users/Alice/ \
    /mnt/external/Alice-old-profile/
```

進 Windows 後再從外接碟搬到新 profile。

---

## 6. ProfileImagePath 路徑被改錯

例如已確認使用者把 `C:\Users\Alice` 改成 `C:\Users\Alice-old`：若只是資料夾誤更名，備份並檢查目的名稱無衝突後改回原名。若確定要保留新路徑，依第 3 節修改 ProfileImagePath，並在 Windows 檢查其他應用程式的絕對路徑與 ACL。

## 7. 範例：每次登入都是 Temp Profile

先確認 Alice 原來的 Documents、Desktop 仍在，讀取 User Profile Service 的錯誤並比對 SID、路徑、NTUSER.DAT。如果路徑錯誤就修路徑；hive 不能解析則保留日誌並嘗試備份復原；ACL 問題交給 Windows 處理。修完一項測試登入，確認載入的是原 profile 與資料，不以桌面出現就判定完成。

## 8. 常見錯誤

### 改完 State 還是 Temp Profile
- 確認 `ProfileImagePath` 真的指到正確路徑（看 `Users\Alice` 資料夾真的存在）
- 對照 `.bak` 分支與事件紀錄，確認實際使用的 SID 設定
- `Users\Alice` 的 NTFS ACL 可能不對（要回 Windows 用 `icacls` 修）

### 還原 NTUSER.DAT 後 Windows 還是說 profile 壞掉
- 檢查是否混用了不同時點的 hive 與日誌，依備份整組復原

### hivexsh: 'bad magic' on NTUSER.DAT
- NTUSER.DAT 本身嚴重損壞
- 試 LOG 還原工具，或乾脆用 Default 重置（4.3 節）
- 終極方案：建新帳號搬資料（5 節）

### 改了沒生效
- 工作副本合併或寫回失敗
- 改錯 hive（NTUSER.DAT 是該使用者的，ProfileList 在 SOFTWARE）
- 沒 rw 掛載

---

## 9. 給使用者的善後建議

修好 profile 後務必：

- 建議使用者用 `OneDrive` 或其他雲端同步 Desktop / Documents（仍需保留可回復舊版的備份）
- 啟用「System Restore」（雖然不是萬靈丹）
- Outlook 使用者：定期把 PST 複製出來
- Chrome / Edge：登入 Google / Microsoft 帳號讓 bookmark/密碼上雲
