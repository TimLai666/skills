# 12 · 使用者 Profile 損壞處理

> **核心觀念**：使用者登入後變成 Temp Profile、桌面是空的、文件全不見 —— 多半是 `NTUSER.DAT` 損壞或 ProfileList 指向錯地方。從 Linux 端能做兩件事：救出舊 profile 的資料、修 ProfileList registry 讓 Windows 重新指認 profile。重建乾淨的新 profile 必須回到 Windows 才能完整完成（建立帳號需要 Windows API），Linux 只能搬資料。

---

## 1. 症狀識別

| 症狀 | 多半原因 |
|---|---|
| 「You've been signed in with a temporary profile」 | NTUSER.DAT 損壞 / ProfileList 指錯 |
| 桌面空了，預設背景，所有設定都不見 | 同上 |
| 「The User Profile Service failed the sign-in」 | ProfileList 裡的 SID 標 `.bak` |
| 登入很慢然後桌面空 | NTUSER.DAT 大到爆 / loaded 失敗 |
| 進桌面後特定 App 開不起來 | 該 App 在 NTUSER.DAT 的設定壞了 |
| 「Group Policy Client service failed sign-in」 | NTUSER.DAT 嚴重損壞 |

---

## 2. 先弄懂 ProfileList 結構

```bash
# 掛 Windows
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# Profile 列表在 SOFTWARE hive
cd /mnt/win/Windows/System32/config
sudo cp SOFTWARE SOFTWARE.bak  # 備份

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
- `State` = 0 表示正常，0x8000 / 0x0001 / 0x0080 表示有問題
- `RefCount` = 載入次數
- `Flags` = 帳號類型

---

## 3. 修 ProfileList：拿掉 `.bak`

**最常見的修法**：Windows 看到 SID 有兩個項目（`S-1-5-21-...` 和 `S-1-5-21-....bak`），優先用 `.bak` 那個但路徑可能指錯，所以給 Temp Profile。

```bash
cd /mnt/win/Windows/System32/config
sudo cp SOFTWARE SOFTWARE.bak

# 進去看狀況
sudo hivexsh -w SOFTWARE
> cd Microsoft\Windows NT\CurrentVersion\ProfileList
> ls
# 找到問題使用者的 SID，例如：
#   S-1-5-21-1234567890-1234567890-1234567890-1001
#   S-1-5-21-1234567890-1234567890-1234567890-1001.bak  ← 多餘的

# 看兩個分別指到哪
> cd S-1-5-21-1234567890-1234567890-1234567890-1001
> lsval
# ProfileImagePath: "C:\Users\TEMP"（指錯了）
> cd ..
> cd S-1-5-21-1234567890-1234567890-1234567890-1001.bak
> lsval
# ProfileImagePath: "C:\Users\Alice"（這才是正確的）
```

### 解法 A：把 `.bak` 改名回正常 SID

`hivexsh` 沒有 rename key 的直接指令，要先記下 `.bak` 的 values，刪掉沒 `.bak` 的，再把 `.bak` 改名。

**但 hivexsh 也不能改 key 名**。比較簡單的做法是：

```
> cd S-1-5-21-1234567890-1234567890-1234567890-1001
> setval 1
ProfileImagePath
string:C:\Users\Alice
> setval 1
State
dword:00000000
> commit
```

也就是**直接把沒 `.bak` 的那個指到正確路徑、State 清零**，然後讓 Windows 自己處理 `.bak` 那個（Windows 開機看到 `.bak` 通常會自己合併或丟）。

如果想保險點，把 `.bak` 那個 key 整個刪掉：

```
> cd ..
> del-node S-1-5-21-1234567890-1234567890-1234567890-1001.bak
> commit
```

### 解法 B：State 值清零

有時候 SID 沒兩個版本，但 State 值不是 0：

```
> cd S-1-5-21-1234567890-1234567890-1234567890-1001
> lsval
# State: 0x00008000  ← 有問題
> setval 1
State
dword:00000000
> commit
```

State 的位元意義（部分）：
- `0x0001` (PROFILE_MANDATORY)
- `0x0002` (PROFILE_USE_CACHE)
- `0x0004` (PROFILE_NEW_LOCAL)
- `0x0080` (PROFILE_TEMPORARY) ← 強制變 temp profile
- `0x8000` (PROFILE_GUEST_USER)

設成 0 就是「正常 profile，沒有特殊狀態」。

---

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

```bash
sudo cp /mnt/win/Users/Alice/NTUSER.DAT /tmp/test-ntuser.dat

# 試著 load
sudo hivexsh /tmp/test-ntuser.dat
> ls
# 如果出來是 Software / Console / Control Panel 等就 OK
# 如果報錯 "hivex_open: bad magic"，hive 損壞
```

### 4.2 用備份還原

Windows 沒有 NTUSER.DAT 的自動備份機制（不像 RegBack），但有兩個地方可能有舊版：

```bash
# 1. NTUSER.DAT.LOG1/LOG2 不是備份，是 transaction log
#    但可以用 reglookup 等工具搭配 .LOG 還原損壞的 .DAT
sudo apt install registry-tools  # reglookup 在這
sudo reglookup -i /mnt/win/Users/Alice/NTUSER.DAT | head

# 2. System Restore Point（如果開著）
ls /mnt/win/System\ Volume\ Information/
# 但這個從 Linux 解非常麻煩，不值得
```

### 4.3 重置該使用者的 NTUSER.DAT（破壞性，先備份）

從 Default profile 複製一份乾淨的：

```bash
# 1. 備份原本壞的
sudo cp /mnt/win/Users/Alice/NTUSER.DAT \
        /mnt/win/Users/Alice/NTUSER.DAT.broken-$(date +%Y%m%d)

# 2. 從 Default 拿一份新的（必須要 rw 掛載）
sudo cp /mnt/win/Users/Default/NTUSER.DAT \
        /mnt/win/Users/Alice/NTUSER.DAT

# 3. 把 LOG 檔清掉（不一致就丟）
sudo rm /mnt/win/Users/Alice/NTUSER.DAT.LOG1 \
        /mnt/win/Users/Alice/NTUSER.DAT.LOG2 2>/dev/null
sudo rm /mnt/win/Users/Alice/NTUSER.DAT*.blf 2>/dev/null
sudo rm /mnt/win/Users/Alice/NTUSER.DAT*.regtrans-ms 2>/dev/null
```

**警告**：這會清掉 Alice 帳號的所有應用程式設定（瀏覽器、Office、桌面排列、捷徑等）。資料還在（D:\、Documents\、Desktop\），但開啟 Edge 會變初始狀態。

### 4.4 移 hive size 超大的問題

NTUSER.DAT 變肥（>200MB）會導致登入超慢：

```bash
ls -lh /mnt/win/Users/Alice/NTUSER.DAT
# 健康範圍：1-50MB
# 太大（200MB+）：通常某個 App 一直寫 registry
```

Linux 端沒辦法「壓縮」hive。要回到 Windows 用 PowerShell 重建：
```powershell
# Windows 內：
Export-Item HKCU\... -Path D:\backup.reg  # 看狀況
```

或乾脆走 4.3 重置。

---

## 5. 建立全新 profile 給使用者

**Linux 端做不到完整建帳號**（需要 LSA / SAM API），但能幫使用者搬資料：

### 5.1 在 Linux 端準備新資料夾

```bash
# 從 Default 複製
sudo cp -r /mnt/win/Users/Default /mnt/win/Users/Alice2
```

但 Windows 不會自動認這個資料夾，**還是要回到 Windows**：

1. 開機進 Windows，用 Administrator 或另一個管理員帳號
2. 控制台 → User Accounts → 建立新本機帳號 `Alice2`
3. 登入新帳號讓 Windows 建立完整 profile
4. 從原本 Alice 的資料夾搬資料過去（下節）

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

例如使用者把 `C:\Users\Alice` 自己改名成 `C:\Users\Alice-old`，登入時 Windows 找不到。

```bash
sudo mount -t ntfs-3g -o rw,remove_hiberfile /dev/sda3 /mnt/win

# 修法 1：把資料夾改回原名
sudo mv /mnt/win/Users/Alice-old /mnt/win/Users/Alice

# 修法 2：改 registry 指到新路徑
cd /mnt/win/Windows/System32/config
sudo cp SOFTWARE SOFTWARE.bak
sudo hivexsh -w SOFTWARE
> cd Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-21-...
> setval 1
ProfileImagePath
string:C:\Users\Alice-old
> commit
```

---

## 7. 完整流程範例：使用者一直進 Temp Profile

```bash
# 場景：Alice 每次登入都是 Temp Profile，桌面空白

# 1. 掛 ro 先看狀況
sudo mkdir -p /mnt/win
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 2. 確認 Alice 的資料還在
ls -la /mnt/win/Users/Alice/Desktop/
ls -la /mnt/win/Users/Alice/Documents/
# 還在 → 太好了，是 profile load 失敗不是檔案不見

# 3. 看 ProfileList
cd /mnt/win/Windows/System32/config
sudo hivexsh SOFTWARE
> cd Microsoft\Windows NT\CurrentVersion\ProfileList
> ls
# 找到兩個版本：
#   S-1-5-21-XXX-1001
#   S-1-5-21-XXX-1001.bak

> cd S-1-5-21-XXX-1001
> lsval
# ProfileImagePath: "C:\Users\TEMP"   ← 錯
# State: 0x8000                       ← 有問題

> cd ..
> cd S-1-5-21-XXX-1001.bak
> lsval
# ProfileImagePath: "C:\Users\Alice"  ← 對
# State: 0
> quit

# 4. 重新 rw 掛載修
sudo umount /mnt/win
sudo mount -t ntfs-3g -o rw,remove_hiberfile /dev/sda3 /mnt/win
cd /mnt/win/Windows/System32/config
sudo cp SOFTWARE SOFTWARE.bak.$(date +%Y%m%d)

# 5. 動手
sudo hivexsh -w SOFTWARE <<'EOF'
cd Microsoft\Windows NT\CurrentVersion\ProfileList
del-node S-1-5-21-XXX-1001
EOF

# 把 .bak 那個改名成沒 .bak 的版本
# 因為 hivexsh 不能 rename key，最簡單做法是把 .bak 的內容寫到沒 .bak 的位置：
sudo hivexsh -w SOFTWARE <<'EOF'
cd Microsoft\Windows NT\CurrentVersion\ProfileList\S-1-5-21-XXX-1001.bak
lsval
EOF
# 記下 ProfileImagePath / Flags / State / Sid 等

# 然後手動建回沒 .bak 的 key、設好值，再 del-node .bak 那個

# 6. 卸載重開
sudo umount /mnt/win
```

> 老實說：**ProfileList 的 `.bak` 處理在 hivexsh 裡很麻煩**，比較實用的做法是在 Windows 內走 WinRE → 命令提示字元 → `reg load` → `regedit` 圖形化處理。Linux 端能做的最有效一招是「**把 State 改 0**」，多半就夠了。

---

## 8. 常見錯誤

### 改完 State 還是 Temp Profile
- 確認 `ProfileImagePath` 真的指到正確路徑（看 `Users\Alice` 資料夾真的存在）
- 確認沒有 `.bak` 版本同時存在（兩個都在 Windows 優先吃 `.bak`）
- `Users\Alice` 的 NTFS ACL 可能不對（要回 Windows 用 `icacls` 修）

### 還原 NTUSER.DAT 後 Windows 還是說 profile 壞掉
- 沒清 `.LOG1` `.LOG2` `.blf` 檔，這些檔記著舊 hive 的 transaction
- 全部清掉再開機

### hivexsh: 'bad magic' on NTUSER.DAT
- NTUSER.DAT 本身嚴重損壞
- 試 LOG 還原工具，或乾脆用 Default 重置（4.3 節）
- 終極方案：建新帳號搬資料（5 節）

### 改了沒生效
- 沒下 `commit` 就 `quit`
- 改錯 hive（NTUSER.DAT 是該使用者的，ProfileList 在 SOFTWARE）
- 沒 rw 掛載

---

## 9. 給使用者的善後建議

修好 profile 後務必：

- 建議使用者用 `OneDrive` 或其他雲端同步 Desktop / Documents（出包不會丟資料）
- 啟用「System Restore」（雖然不是萬靈丹）
- Outlook 使用者：定期把 PST 複製出來
- Chrome / Edge：登入 Google / Microsoft 帳號讓 bookmark/密碼上雲
