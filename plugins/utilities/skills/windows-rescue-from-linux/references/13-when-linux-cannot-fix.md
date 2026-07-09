# 13 · Linux 救不了的時候

> **核心觀念**：誠實面對 Linux 端的極限。有些事必須 Windows 自己的 servicing 堆疊才能做。準備好 Windows 安裝媒體（ISO 燒進 Ventoy）和 WinRE 環境，並且知道每個指令的對應位置，才不會把使用者卡死在「沒辦法救」的死巷。

---

## 1. Linux 完全做不到的清單

| 任務 | 為什麼 Linux 做不到 | 必須的 Windows 環境 |
|---|---|---|
| `sfc /scannow` 系統檔完整性檢查 | sfc 走 Windows Component Servicing API | WinRE 或 Windows 內 |
| `DISM /RestoreHealth` 修 Component Store | 同上 | WinRE + Windows ISO |
| 安裝/重裝 driver 並註冊到 PnP | 走 PnP Manager / SetupAPI | Windows 內 |
| 解除特定 KB 更新（`wusa /uninstall`） | 走 Windows Update Agent | WinRE 或 Windows 內 |
| Reset This PC（保留/不保留檔案） | 走 WinRE 內建流程 | WinRE |
| In-place upgrade（修復安裝） | 要跑 setup.exe | Windows 內或 ISO |
| 從 WinSxS 嚴重損壞恢復（pending operation 卡死無法清） | 要 Servicing Stack | WinRE + ISO |
| 重建 Driver Store | 走 `pnputil` | Windows 內 |
| 修復嚴重損壞的 winlogon.exe / csrss.exe | 要 sfc/DISM | WinRE |
| 修 WMI Repository（壞掉的話） | 要 `winmgmt /resetrepository` | Windows 內 |
| TPM-only BitLocker 解密 | 沒 TPM 沒辦法解 | 原機 + Windows |
| Storage Spaces 池修復 | 要 Storage Spaces 服務 | Windows 內 |
| 重灌（fresh install） | 跑 Windows 安裝程式 | Windows ISO |

---

## 2. 準備 Windows 安裝媒體

把 Windows 11 ISO 放進你的救援 USB（Ventoy 多開機）是必備動作：

### 下載 ISO

- 官方：https://www.microsoft.com/zh-tw/software-download/windows11
- 選「下載 Windows 11 磁碟映像（ISO）」
- 24H2 或更新版本

### 放進 Ventoy

```bash
# 救援 USB 已經是 Ventoy（參見 00-rescue-usb-preparation.md）
# Ventoy 的儲存分割區會自動 mount，丟 ISO 進去就行
cp ~/Downloads/Win11_24H2_TraditionalChinese_x64.iso /media/$USER/Ventoy/
```

開機時 Ventoy 選單會列出 ISO，選它就能進 Windows 安裝環境。

### Win10/Win11 通用 vs 特定版本

- 救人時帶 **Win10 22H2** 和 **Win11 24H2** 兩個 ISO（涵蓋大部分情境）
- 注意：Windows 安裝媒體版本要**相同或更新**於要修的系統，**不能用更舊版**做 in-place upgrade

---

## 3. 進入 WinRE（Windows Recovery Environment）

### 從 ISO 進 WinRE

開機進 Windows 安裝畫面後：
1. 「修復您的電腦」（Repair your computer）
2. 「疑難排解」（Troubleshoot）
3. 「進階選項」（Advanced options）
4. 「命令提示字元」（Command Prompt）

### 從硬碟內建 WinRE 進

如果 Windows 還能進到登入畫面：
- 按住 Shift 點重新啟動 → 自動進 WinRE

如果連登入都進不去：
- 強制中斷開機 3 次（按電源鍵切電）→ 第 4 次會自動進 Windows Recovery

---

## 4. 在 WinRE 命令提示字元裡能做什麼

### 4.1 找對碟代號

WinRE 裡 `C:` 不一定是真的 Windows 碟，常常變 `D:` 或 `E:`：

```cmd
diskpart
list volume
exit
```

或：
```cmd
bcdedit | find "osdevice"
```

下面範例假設 Windows 在 `D:\`、EFI 分割區是 `S:\`。

### 4.2 修 boot（對應 Linux 的 efibootmgr）

```cmd
:: 列出 OS 安裝
bootrec /scanos

:: 重建 BCD
bootrec /rebuildbcd

:: 修 MBR（只對 Legacy/MBR 有意義）
bootrec /fixmbr

:: 修 boot sector
bootrec /fixboot

:: UEFI：用 bcdboot 重建整個 boot
:: 把 Windows 在 D:\ 的 boot 設定寫到 EFI 分割區 S:\
bcdboot D:\Windows /s S: /f UEFI /l zh-tw
```

`bcdboot` 是修 UEFI 開機最有效的單一指令，**Linux 沒有直接對應**（你只能複製檔案 + efibootmgr 註冊，bcdboot 一行解決）。

### 4.3 sfc（修系統檔）

```cmd
:: 對離線系統跑（D:\ 是要修的 Windows）
sfc /scannow /offbootdir=D:\ /offwindir=D:\Windows
```

跑完看結果：
- `did not find any integrity violations` → 沒事
- `successfully repaired` → 修好了
- `found corrupt files but was unable to fix some` → 走 DISM

### 4.4 DISM（修 Component Store）

```cmd
:: 檢查（不修）
dism /Image:D:\ /Cleanup-Image /CheckHealth

:: 詳細掃描
dism /Image:D:\ /Cleanup-Image /ScanHealth

:: 修（需要 source，從 ISO 的 install.wim 拿）
:: ISO 多半在 E:\ 或 F:\，先找
dir E:\sources\install.*

:: install.wim 或 install.esd
dism /Image:D:\ /Cleanup-Image /RestoreHealth /Source:WIM:E:\sources\install.wim:1 /LimitAccess
:: 如果是 esd：
dism /Image:D:\ /Cleanup-Image /RestoreHealth /Source:ESD:E:\sources\install.esd:1 /LimitAccess
```

`install.wim` 後面的 `:1` 是 image index，可以先查：
```cmd
dism /Get-WimInfo /WimFile:E:\sources\install.wim
```

通常 index 1 是 Home，2 是 Home N，... 6 是 Pro 等，看清單挑跟使用者授權對應的版本。

### 4.5 chkdsk（檔案系統檢查，比 ntfsfix 強）

```cmd
chkdsk D: /f /r
:: /f 修錯誤
:: /r 找壞磁區並嘗試讀回（耗時很久）
```

> Linux 的 `ntfsfix` 只能處理輕量問題，**chkdsk 才是 NTFS 的官方檢查工具**。但 chkdsk 對嚴重壞道會試著 read 然後 mark bad，這跟 ddrescue 邏輯衝突 —— 如果你 SMART 看到壞道**已經爆很多**，先 ddrescue 出來再說，不要直接 chkdsk。

### 4.6 解除 KB 更新

```cmd
:: 列出已裝的更新
dism /Image:D:\ /Get-Packages | findstr KB

:: 看完整資訊
dism /Image:D:\ /Get-Packages /Format:Table

:: 移除
dism /Image:D:\ /Remove-Package /PackageName:Package_for_RollupFix~31bf3856ad364e35~amd64~~22621.1928.1.6
```

把 PackageName 換成你要移的（從上面 list 找最近裝的）。

### 4.7 啟用 Administrator 帳號

```cmd
:: 在 WinRE 內，掛載 SAM hive 改 registry
reg load HKLM\TempSAM D:\Windows\System32\config\SAM
:: 改 Administrator F value（複雜）...
:: 比較簡單：先進 Safe Mode

:: 或在 WinRE 直接：
net user Administrator /active:yes
```

但 `net user` 在 WinRE 通常會說「找不到網路服務」，這時要走 Linux 的 chntpw（[06-registry-edit.md](06-registry-edit.md)）。

---

## 5. Reset This PC

WinRE → 疑難排解 → 重設此電腦

兩個選項：
- **保留我的檔案**：個人檔案留，所有 App 砍光，Windows 重裝
- **移除所有項目**：全清，等於重灌

需要的東西：
- **Local reset**：用硬碟內建的 recovery image（如果還在）
- **Cloud download**：從網路下載最新 Windows 鏡像（穩，建議）

**注意**：BitLocker 加密的碟 reset 前**一定要先有 recovery key**，不然會卡。

---

## 6. In-place Upgrade（修復安裝）

如果系統壞但能進桌面（哪怕不穩定），**這是最佳修復方式**：

1. 進 Windows
2. 掛載 ISO 或解開 ISO 到資料夾
3. 跑 `setup.exe`
4. 選「升級這部電腦」「保留個人檔案和應用程式」
5. 走完安裝流程（會花 30-60 分鐘）

**效果**：
- 系統檔全部換新
- 個人檔案、App、設定**全部保留**
- 比 Reset This PC 溫和很多

**前提**：
- 能進桌面（至少能跑 setup.exe）
- ISO 版本 ≥ 目前系統版本
- 同樣的版本（Home → Home，Pro → Pro，不能跨）
- 同樣的語系（中文 → 中文）
- 同樣的架構（x64 → x64）

---

## 7. 最後手段：乾淨重灌

當 Linux 修不好、WinRE 修不好、in-place upgrade 失敗，剩下的就是重灌。重灌前的 Linux 端準備工作：

```bash
# 1. 用 Linux 端把所有重要資料備份到外接碟
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 整個 Users 資料夾備份（最保險）
sudo rsync -aHv --info=progress2 \
    --exclude='AppData/Local/Temp' \
    --exclude='AppData/Local/Microsoft/Windows/INetCache' \
    /mnt/win/Users/ \
    /mnt/external/Users-backup-$(date +%Y%m%d)/

# 2. 也要救：
# - C:\ProgramData\ 裡的特定 App 設定（看 App 而定）
# - 應用程式的 license key（很多在 registry，先記下來）

# 3. 看 Windows 授權形式（OEM key 嵌在 BIOS 不用記）
sudo dmidecode -s system-product-name
sudo dmidecode -s system-manufacturer
# OEM key 不用記，重灌會自動激活

# 4. 列出已裝的 App（重灌後參考）
ls /mnt/win/Program\ Files/ /mnt/win/Program\ Files\ \(x86\)/ \
    > /mnt/external/installed-apps-list.txt
```

備份完才能安心重灌。

---

## 8. 對應表：Linux 工具 vs Windows 工具

| 任務 | Linux 端 | Windows 端 |
|---|---|---|
| NTFS 修檔系統 | `ntfsfix` | `chkdsk /f /r` |
| 修 EFI boot 註冊 | `efibootmgr` | `bcdboot` |
| 重建 BCD | (沒有，要手動) | `bootrec /rebuildbcd` |
| 改 registry | `chntpw` / `hivexsh` | `regedit` / `reg.exe` |
| 改密碼 | `chntpw` | `net user` |
| 看 driver 載入 | 看 `services` registry | `Get-WindowsDriver` (DISM) |
| 移除 driver | 改 Service Start=4 | `pnputil /delete-driver` |
| 系統檔修復 | （無） | `sfc /scannow` |
| Component Store 修復 | （無） | `DISM /RestoreHealth` |
| 救資料 | `rsync` / `ddrescue` | `robocopy` |
| 病毒掃描 | `clamav` | Defender / 第三方 |
| 解 BitLocker | `dislocker` | `manage-bde -unlock` |
| 磁碟健康 | `smartctl` | `WMIC diskdrive get status`（弱）/ CrystalDiskInfo |
| 分割表修復 | `testdisk` | `diskpart`（弱） |
| 救刪除檔 | `photorec` / `ntfsundelete` | Recuva 等第三方 |

---

## 9. 何時建議使用者「直接重灌就好」

老實跟使用者講「修不值得」的時機：

| 狀況 | 為什麼建議重灌 |
|---|---|
| 嚴重 rootkit / bootkit 感染 | 信任邊界完全瓦解，修了也不知道乾不乾淨 |
| 勒索病毒（含活躍 payload） | 同上，且 backup 也可能被加密 |
| 嚴重 WinSxS 損壞 + 沒有同版本 ISO | 修起來時間比重灌長很多 |
| 系統超過 5 年沒重灌過 + 慢到爆 | 累積太多垃圾，重灌讓使用體驗好太多 |
| 磁碟壞道大量出現 | 救資料後換新碟，舊碟不要繼續用 |
| 使用者本來就要換新電腦 | 沒必要花時間 |

把上面這些情境跟使用者講清楚，他會自己選。**修復師的價值在誠實判斷該修還是該重灌，不在硬要把每台都修好**。

---

## 10. 完整流程範例：使用者堅持要修不想重灌

```bash
# 場景：使用者說「我有重要工作不能重灌，硬修」
# Linux 端發現：WinSxS 嚴重損壞，pending.xml 移除後還是進不去

# 1. 先確定資料安全（Linux 端能做）
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
sudo rsync -aHv --info=progress2 \
    /mnt/win/Users/$USER/Documents/ \
    /mnt/external/safe-backup/

# 2. 跟使用者確認「資料備份完成」後才動手

# 3. 拔 USB 重開，這次選 Windows 11 ISO（Ventoy 多開機）

# 4. 進 WinRE → Command Prompt
diskpart
list volume
# 確定 Windows 在哪個 letter，假設 D:
exit

# 5. 試 sfc
sfc /scannow /offbootdir=D:\ /offwindir=D:\Windows

# 6. 走 DISM 修 Component Store
dism /Image:D:\ /Cleanup-Image /CheckHealth
dism /Image:D:\ /Cleanup-Image /ScanHealth
dism /Get-WimInfo /WimFile:E:\sources\install.wim
dism /Image:D:\ /Cleanup-Image /RestoreHealth \
     /Source:WIM:E:\sources\install.wim:6 /LimitAccess
# 跑很久（30 分鐘起跳）

# 7. 再跑一次 sfc
sfc /scannow /offbootdir=D:\ /offwindir=D:\Windows

# 8. 修 boot
bcdboot D:\Windows /s S: /f UEFI

# 9. 重開機看能不能進
# 如果還是不行 → 進 Windows 跑 in-place upgrade（最終）
# 還是不行 → 跟使用者說「資料有備份了，重灌吧」
```

---

## 11. 跟使用者溝通的話術

當你判斷要走 Windows ISO / 重灌時：

```
您的問題在 Linux 救援環境下沒辦法完整修復，必須走以下其中一條：

  選項 A：用 Windows 安裝媒體進入 WinRE，跑 sfc 和 DISM 修復系統檔
         耗時約 1-2 小時，成功率約 70%，您的資料和 App 都會留著。

  選項 B：In-place upgrade（修復安裝），保留檔案和 App 重裝 Windows
         耗時約 1 小時，成功率 90%+，極少數情況某些 App 要重新設定。

  選項 C：乾淨重灌
         耗時約 30 分鐘 + 重裝 App 時間，成功率 100%，App 全部要重裝。

我已經幫您把 Documents / Desktop / Pictures / 瀏覽器資料備份到外接碟，
不管選哪條都不會掉資料。建議從 A 試起。
```

誠實、給選項、講清楚代價，使用者會自己選對的那條。
