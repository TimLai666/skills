# 06 — Registry 編輯（密碼重設、服務停用、帳號操作）

從 Linux 檢查與編輯 Windows registry：

- **chntpw**：互動式、最適合密碼重設、SAM/SYSTEM hive 操作
- **hivexsh**：唯讀巡覽 key/value
- **hivexregedit**：匯出與合併精確的 key/value 變更

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

## 共通準備與還原

先讀 [01 安全原則](01-safety-principles.md) 與 [03 掛載](03-mount-windows.md)。唯讀檢查原 hive，在外接健康磁碟保留原始 hive 與同名交易日誌，另建工作副本；不要直接編輯唯一原件。以下假設 `/media/external/rescue/registry/` 是本案新建目錄。

```bash
mkdir -p /media/external/rescue/registry
sudo cp -a /mnt/win/Windows/System32/config/SYSTEM \
    /media/external/rescue/registry/SYSTEM.original
sudo cp -a /media/external/rescue/registry/SYSTEM.original \
    /media/external/rescue/registry/SYSTEM.work
```

實際要改 SAM、SOFTWARE 或 NTUSER.DAT 時，以對應 hive 套用此步驟。修改後重新開啟副本、匯出並比對，確認只有預定 key/value 改變。依 03 切換可寫掛載後，再備份並將驗證過的副本寫回原檔，保留原有檔案與 NTFS 權限；同步、卸載後測試。失敗就由備份還原本次修改，勿繼續疊加猜測。髒 hive 或未完成的交易日誌須先處理，不能靠清除休眠檔修復 registry。

## chntpw：密碼重設與帳號操作

### 重設使用者密碼

離線清除本機密碼前，確認 EFS 檔案、憑證與保存的認證是否另有復原方式；重設密碼可能使它們無法解密。

```bash
cd /media/external/rescue/registry

# 已依上節建立 SAM.original 與 SAM.work
sudo chntpw -i SAM.work
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

chntpw 不能重設 Microsoft 帳號的線上密碼。使用官方帳號復原流程；若目標是本機資料救援，改走 [08 資料救援](08-data-recovery.md)。啟用另一個本機管理員不會復原原帳號的加密金鑰。

### 啟用隱藏的 Administrator

Windows 預設裝完會把內建 Administrator 帳號停用。要啟用：

```
chntpw -i SAM.work
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
chntpw -i SAM.work
> 1
> <username>
> 3   # Promote to administrator
> q ...
```

### 解鎖被鎖住的帳號

帳號被「太多次登入失敗」鎖住：

```
chntpw -i SAM.work
> 1
> <username>
> 2   # Unlock
> q ...
```

## 唯讀檢查與精確修改

需要修改服務、惡意啟動項或 ProfileList 時，都使用本節的副本合併流程。`hivexsh setval` 會替換目前 key 的**全部 values**，不適合當成單值更新；`hivexregedit --merge` 保留未指定的其他 values 與子 key。

Debian / Ubuntu 的 `hivexsh` 在 `libhivex-bin`，`hivexregedit` 在 `libwin-hivex-perl`。安裝後以 `command -v hivexregedit` 確認工具可用。

```bash
sudo apt install libhivex-bin libwin-hivex-perl
```

### 找到實際 ControlSet

```bash
sudo hivexregedit --export \
    /media/external/rescue/registry/SYSTEM.original '\Select'
```

依 `Current` 決定 `ControlSet001`、`ControlSet002` 等路徑，同時記下 `Default`、`LastKnownGood`。離線 hive 沒有可直接編輯的 `CurrentControlSet` 別名。

### 唯讀巡覽

```text
sudo hivexsh /mnt/win/Windows/System32/config/SYSTEM
> cd ControlSet001\Services\Eventlog
> lsval
> cd ..
> ls
> exit
```

`ls` 列子 key，`lsval` 列 values。範例的 ControlSet 必須換成本案值。從 hive 根目錄開始輸入完整相對路徑，或用 `cd \` 回根目錄再切換。

### 修改一個值：停用已確認有問題的服務

`Start` 值：0 = Boot、1 = System、2 = Auto、3 = Manual、4 = Disabled。先用事件紀錄、傾印與 `ImagePath` 對上服務，不以檔名相似就停用開機必要的儲存驅動。

以下假設已確認 `ControlSet001\Services\BadDriver` 是要停用的服務。將 `.reg` 存為 UTF-8、Unix 換行；這是給 hivexregedit 的輸入格式。

```bash
sudo hivexregedit --export /media/external/rescue/registry/SYSTEM.work \
    '\ControlSet001\Services\BadDriver' \
    > /media/external/rescue/registry/service.before.reg

cat > /media/external/rescue/registry/change.reg <<'EOF'
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Services\BadDriver]
"Start"=dword:00000004
EOF

sudo hivexregedit --merge --prefix 'HKEY_LOCAL_MACHINE\SYSTEM' \
    /media/external/rescue/registry/SYSTEM.work \
    /media/external/rescue/registry/change.reg

sudo hivexregedit --export /media/external/rescue/registry/SYSTEM.work \
    '\ControlSet001\Services\BadDriver' \
    > /media/external/rescue/registry/service.after.reg
diff -u /media/external/rescue/registry/service.before.reg \
    /media/external/rescue/registry/service.after.reg
```

檢查每個命令狀態；`diff` 回傳 1 表示有差異，必須確認只改了 `Start`，2 表示檢查失敗。匯出整個 hive 前後比較可確認其他 key 未受影響。所有檢查通過才寫回；不因 merge exit 0 就省略比對。

### 刪除一個惡意啟動值

在 SOFTWARE 工作副本上，以同一流程合併下列內容；prefix 改為 `HKEY_LOCAL_MACHINE\SOFTWARE`。保留其他合法啟動項。

```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run]
"MalwareName"=-
```

刪除整個 key 的語法是 `[-HKEY_LOCAL_MACHINE\SOFTWARE\完整路徑]`，會連子 key 刪除，只有確認整個分支都是本案要移除的內容才使用。不要以刪除整個 IFEO key 取代刪除惡意 `Debugger` 值。

修改 NTUSER.DAT 時 prefix 使用 `HKEY_CURRENT_USER`，其餘方法相同。其他持續啟動位置見 [07 惡意軟體清除](07-malware-cleanup.md)。

依據：[hivexregedit 手冊](https://libguestfs.org/hivexregedit.1.html)、[合併與單值刪除實作](https://github.com/libguestfs/hivex/blob/master/perl/lib/Win/Hivex/Regedit.pm)、[hivexsh 手冊](https://libguestfs.org/hivexsh.1.html)。

## 嚴重損壞：RegBack 還原

先唯讀列出 `Windows/System32/config/RegBack`，核對備份日期、非零大小及能否解析。Windows 10 1803 起預設不再自動備份 registry；新版也可能由管理員另外啟用，因此不能只憑系統版本或檔名判斷可用。

若有已知良好的備份，先依共通流程保留目前 hive 與交易日誌，再還原確認的備份組。整組 registry 回退會影響備份之後的帳號、服務與安裝狀態，不能只用「檔案大於 1 KB」判定有效，也不要每案都直接覆蓋 SAM、SYSTEM、SOFTWARE。

## 故障排除

### Hive 無法開啟或寫回

先確認讀取錯誤、hive 格式、權限與掛載狀態。保留 hive 及其 `.LOG1`、`.LOG2` 等日誌供復原工具或 WinRE 處理；不要把 registry 交易未完成誤當 NTFS dirty，也不要盲目清除 immutable 屬性或休眠檔。副本不能正常重新開啟就不要寫回。

### 改完開機還是不行

- 你改的可能是 ControlSet001 但實際開機用 ControlSet002（看 `Select\Current` value）
- Windows 在開機時用 LastKnownGood 機制可能回滾你的改動
- 改錯地方了

ControlSet001 不一定是正在使用的控制集，要看 `HKLM\SYSTEM\Select`：

```text
sudo hivexsh /mnt/win/Windows/System32/config/SYSTEM
> cd Select
> lsval
# Current     = 0x1 → 用 ControlSet001
# Current     = 0x2 → 用 ControlSet002
# LastKnownGood = 0x1 or 0x2 → 之前能開機的那組
```

如果 Current 是 2，就要改 `ControlSet002` 才有效。

## 密碼重設後驗證

完成前述備份、帳號確認與 chntpw 操作後，正常卸載再試本機登入。能登入後重新設定密碼，確認重要資料與加密內容仍可用。登入失敗時核對帳號類型與修改是否保存，不重複清除其他帳號密碼。
