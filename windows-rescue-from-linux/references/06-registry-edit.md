# 06 — Registry 編輯（密碼重設、服務停用、帳號操作）

從 Linux 編輯 Windows registry 主要靠兩個工具：

- **chntpw**：互動式、最適合密碼重設、SAM/SYSTEM hive 操作
- **hivexsh**：腳本化、適合精確修改特定 key/value

## Registry hive 位置

```
/mnt/win/Windows/System32/config/
├── SAM        ← 本機帳號、密碼 hash
├── SECURITY   ← 安全性原則
├── SOFTWARE   ← HKLM\SOFTWARE，安裝的軟體、自動啟動
├── SYSTEM     ← HKLM\SYSTEM，服務、driver、開機設定
├── DEFAULT    ← .DEFAULT 使用者
├── BCD-Template ← BCD 範本
└── RegBack/   ← 舊版自動備份（Windows 10 1803 之前才有）
```

每個使用者的 NTUSER.DAT 在：

```
/mnt/win/Users/USERNAME/NTUSER.DAT
```

## 動手前必做：備份

```bash
cd /mnt/win/Windows/System32/config
sudo cp SAM SAM.bak.$(date +%Y%m%d)
sudo cp SYSTEM SYSTEM.bak.$(date +%Y%m%d)
sudo cp SOFTWARE SOFTWARE.bak.$(date +%Y%m%d)
```

弄壞了：

```bash
sudo cp SAM.bak.YYYYMMDD SAM
```

## 掛載方式

可以唯讀讀內容、確認要改什麼。實際改的時候要 rw 掛載：

```bash
sudo umount /mnt/win
sudo mount -t ntfs-3g -o remove_hiberfile,rw /dev/sda3 /mnt/win
```

## chntpw：密碼重設與帳號操作

### 重設使用者密碼

```bash
cd /mnt/win/Windows/System32/config

sudo chntpw -i SAM
```

進到選單：

```
<>========<> chntpw Main Interactive Menu <>========<>

Loaded hives: <SAM>

  1 - Edit user data and passwords
  2 - List groups
      - - -
  9 - Registry editor, now with full write support!
  q - Quit (you will be asked if there is something to save)
```

按 `1`：

```
=== chntpw Edit User Info & Passwords ====

| RID -|---------- Username ------------| Admin? |- Lock? --|
| 01f4 | Administrator                  | ADMIN  | dis/lock |
| 03e8 | john                           | ADMIN  |          |
| 03e9 | guest                          |        | dis/lock |

Select: ! - quit, . - list users, 0x<RID> - User with RID (hex)
or simply enter the username to change: [Administrator]
```

輸入要操作的使用者名稱（或 hex RID）：

```
================= USER EDIT ====================

RID     : 1000 [03e8]
Username: john
fullname: John Doe
comment :
homedir :

User is member of 2 groups:
00000220 = Administrators (which has 2 members)
00000221 = Users (which has 4 members)

Account bits: 0x0010 =
[ ] Disabled        | [ ] Homedir req.    | [ ] Passwd not req.
[ ] Temp. duplicate | [X] Normal account  | [ ] NMS account
...

Failed login count: 0, while max tries is: 0
Total login count: 35

- - - - User Edit Menu:
  1 - Clear (blank) user password
  2 - Unlock and enable user account [seems unlocked already]
  3 - Promote user (make user an administrator)
  4 - Add user to a group
  5 - Remove user from a group
  q - Quit editing user, back to user select
Select: [q] >
```

選 `1` 清空密碼。

回到主選單按 `q`，問是否寫入時答 `y`。

接著告訴使用者：重開機後 Windows 登入直接按 Enter 不用打密碼。進去之後一定要重新設密碼（**不要繼續用空密碼**）。

### 「我用的是 Microsoft 帳號（線上）登入」

chntpw 只能改本機帳號密碼，沒辦法改 Microsoft 帳號（線上）的密碼。處理方式：

選項 A：把該帳號轉成本機帳號
```
chntpw 主選單 → 9 (Registry editor)
> cd SAM\SAM\Domains\Account\Users\<RID>
# 找 F 或 V 值改動 ── 較複雜，不建議新手做
```

選項 B（推薦）：啟用 Administrator（內建管理員，本機帳號），用它登入，再從 Windows 內部改 Microsoft 帳號

```
chntpw -i SAM
> 1
> Administrator
> 1   # 清空密碼
> 2   # unlock + enable
> q
> q
> y   # 寫入
```

選項 C：直接到 https://account.microsoft.com 線上改 MSA 密碼，不用碰到本機 registry。

### 啟用隱藏的 Administrator

Windows 預設裝完會把內建 Administrator 帳號停用。要啟用：

```
chntpw -i SAM
> 1
> Administrator
> 2   # Unlock and enable
> 1   # Clear password
> q
> q
> y
```

### 把使用者升為管理員

```
chntpw -i SAM
> 1
> <username>
> 3   # Promote to administrator
> q ...
```

### 解鎖被鎖住的帳號

帳號被「太多次登入失敗」鎖住：

```
chntpw -i SAM
> 1
> <username>
> 2   # Unlock
> q ...
```

## hivexsh：精確修改

chntpw 適合互動，hivexsh 適合知道路徑就直接改。

### 安裝

```bash
sudo apt install libhivex-bin
```

### 唯讀檢查

```bash
sudo hivexsh /mnt/win/Windows/System32/config/SYSTEM

# 在 hivexsh 提示下
> ls
> cd ControlSet001
> ls
> cd Services
> ls
> cd Eventlog
> lsval        # 列出 values
> exit
```

操作邏輯：

- `ls` 列子 key
- `cd <key>` 進去
- `cd ..` 回上層
- `lsval` 列當前 key 的 value
- `exit` 不存檔離開

### 可寫修改

```bash
sudo hivexsh -w /mnt/win/Windows/System32/config/SYSTEM
> commit    # 在做完所有修改後存檔
```

### 停用問題服務（不讓它在開機時載入）

服務在 `ControlSet001\Services\<服務名>`。`Start` 值控制啟動類型：

| Start 值 | 意義 |
|---|---|
| 0 | Boot（kernel-level driver） |
| 1 | System |
| 2 | Auto |
| 3 | Manual |
| 4 | Disabled |

把問題服務改成 4：

```bash
sudo hivexsh -w /mnt/win/Windows/System32/config/SYSTEM
> cd ControlSet001\Services\<服務名>
> lsval
# 看現有 Start 值
> setval 1
Type of value? dword
Value to assign? 4
Name of value? Start
> commit
> exit
```

或一行 setval（看 hivex 版本可能不同）。如果 setval 互動式語法在你版本上不一樣：

```bash
hivexget /mnt/win/Windows/System32/config/SYSTEM \
    'ControlSet001\Services\ServiceName' 'Start'

# 用 hivexml 整個 dump 出來改完再 import 也行
```

### 場景：driver 載入後黑屏

某次 Windows Update 後裝了爛 driver，每次開機載入就黑屏。從 Linux 停用該 driver：

```bash
# 找出嫌疑 driver
ls /mnt/win/Windows/System32/drivers/*.sys -lt | head -20
# 看最近修改的，跟事件發生時間對得起來的

# 假設是 BadDriver.sys，對應服務名通常是 BadDriver
sudo hivexsh -w /mnt/win/Windows/System32/config/SYSTEM
> cd ControlSet001\Services\BadDriver
> lsval
> setval ... Start = 4 (disabled)
> commit
> exit

# 也可以連 .sys 一起移走（不要刪，搬到別處先）
sudo mkdir /tmp/quarantine
sudo mv /mnt/win/Windows/System32/drivers/BadDriver.sys /tmp/quarantine/
```

### 場景：移除惡意自動啟動

惡意軟體最常見的 persistence 在：

- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce`
- `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`（在 NTUSER.DAT）

```bash
# 看 HKLM 的 Run
sudo hivexsh /mnt/win/Windows/System32/config/SOFTWARE
> cd Microsoft\Windows\CurrentVersion\Run
> lsval
# 看到不認識的項目
> exit

# 確認後刪除
sudo hivexsh -w /mnt/win/Windows/System32/config/SOFTWARE
> cd Microsoft\Windows\CurrentVersion\Run
> del-val MalwareName
> commit
> exit
```

也要看每個使用者的 NTUSER.DAT：

```bash
for user_dat in /mnt/win/Users/*/NTUSER.DAT; do
    echo "=== $user_dat ==="
    sudo hivexsh "$user_dat" <<EOF
cd Software\Microsoft\Windows\CurrentVersion\Run
lsval
EOF
done
```

詳見 `07-malware-cleanup.md`。

## chntpw 的 Registry Editor（選項 9）

chntpw 主選單按 9 進到通用 registry editor，模仿 regedit 操作：

```
> cd HKLM\System\ControlSet001\Services
> ls
> cat /tmp/keys.txt   # 文字輸出至檔案
> cd ..
> ...
```

用法跟 hivexsh 差不多，但介面互動性較好。

## 嚴重損壞：RegBack 還原（Windows 10 1803 之前才能用）

```bash
ls /mnt/win/Windows/System32/config/RegBack/
# 如果有 SAM、SYSTEM、SOFTWARE 等檔案 → 是舊版備份

cd /mnt/win/Windows/System32/config

# 對照大小，太小（< 1KB）表示沒實際備份
ls -lh
ls -lh RegBack/

# 還原：先備份當前，再從 RegBack 複製
sudo cp SAM SAM.broken.$(date +%Y%m%d)
sudo cp SYSTEM SYSTEM.broken.$(date +%Y%m%d)
sudo cp SOFTWARE SOFTWARE.broken.$(date +%Y%m%d)

sudo cp RegBack/SAM .
sudo cp RegBack/SYSTEM .
sudo cp RegBack/SOFTWARE .
```

Windows 10 1803+ 起 Microsoft 預設關掉 RegBack 自動備份（檔案還在但都是 0 byte）。確認檔案大小再做。

## 故障排除

### chntpw 抱怨 hive 是 dirty

```
hivex: hivex_open: Mounted dirty file
```

NTFS 在 Windows 端沒乾淨關機。重新掛載：

```bash
sudo umount /mnt/win
sudo mount -t ntfs-3g -o remove_hiberfile,rw /dev/sda3 /mnt/win
```

### 改完 commit 沒寫入

權限問題：

```bash
# 確認 hive 檔案不是 read-only
ls -la /mnt/win/Windows/System32/config/SAM
sudo chattr -i /mnt/win/Windows/System32/config/SAM    # 通常不需要

# 確認 mount 是 rw
mount | grep /mnt/win
# 應該包含 rw
```

### 改完開機還是不行

- 你改的可能是 ControlSet001 但實際開機用 ControlSet002（看 `Select\Current` value）
- Windows 在開機時用 LastKnownGood 機制可能回滾你的改動
- 改錯地方了

打 ControlSet001 跟 CurrentControlSet 一樣。但要看 `HKLM\SYSTEM\Select`：

```bash
sudo hivexsh /mnt/win/Windows/System32/config/SYSTEM
> cd Select
> lsval
# Current     = 0x1 → 用 ControlSet001
# Current     = 0x2 → 用 ControlSet002
# LastKnownGood = 0x1 or 0x2 → 之前能開機的那組
```

如果 Current 是 2，就要改 `ControlSet002` 才有效。

## 完整流程：忘記密碼

```bash
# 1. 確認哪個是 Windows 系統碟
sudo blkid
lsblk -f

# 2. 唯讀掛載確認資料還在
sudo mkdir -p /mnt/win
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
ls /mnt/win/Users/   # 確認看得到使用者

# 3. 備份使用者重要資料（保險）
sudo rsync -avh --info=progress2 /mnt/win/Users/USERNAME/Desktop \
    /mnt/win/Users/USERNAME/Documents \
    /media/external/backup/

# 4. 卸載，可寫重掛
sudo umount /mnt/win
sudo mount -t ntfs-3g -o remove_hiberfile,rw /dev/sda3 /mnt/win

# 5. 備份 SAM
cd /mnt/win/Windows/System32/config
sudo cp SAM SAM.bak.$(date +%Y%m%d)

# 6. 跑 chntpw
sudo chntpw -i SAM
# 進選單 → 1 → 輸入帳號 → 1 (清密碼) → q → q → y

# 7. 卸載
cd
sudo umount /mnt/win

# 8. 告訴使用者：重開機後登入留空密碼按 Enter，
#    進去後立刻去設定→帳戶→登入選項 重設密碼
```
