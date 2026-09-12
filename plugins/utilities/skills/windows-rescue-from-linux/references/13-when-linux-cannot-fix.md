# 13 — Windows 原生修復工具交接

> **核心觀念**：誠實面對 Linux 端的極限。有些事必須 Windows 自己的 servicing 堆疊才能做。準備好 Windows 安裝媒體（ISO 燒進 Ventoy）和 WinRE 環境，並且知道每個指令的對應位置，才不會把使用者卡死在「沒辦法救」的死巷。

---

## 1. 需要 Windows 原生工具的工作

| 任務 | 為什麼 Linux 做不到 | 必須的 Windows 環境 |
|---|---|---|
| `sfc /scannow` 系統檔完整性檢查 | sfc 走 Windows Component Servicing API | WinRE 或 Windows 內 |
| `DISM /RestoreHealth` 修 Component Store | 同上 | WinRE + Windows ISO |
| 安裝/重裝 driver 並註冊到 PnP | 走 PnP Manager / SetupAPI | Windows 內 |
| 解除特定 KB 更新 | Windows 內可用 wusa，離線使用 DISM | Windows 或 WinRE |
| Reset This PC（保留/不保留檔案） | 走 WinRE 內建流程 | WinRE |
| In-place upgrade（修復安裝） | 要在執行中的 Windows 啟動 setup.exe | 能進 Windows，另備相容 ISO |
| 從 WinSxS 嚴重損壞恢復（pending operation 卡死無法清） | 要 Servicing Stack | WinRE + ISO |
| 重建 Driver Store | 走 `pnputil` | Windows 內 |
| 多個相依系統組件或元件儲存區損壞 | SFC／DISM 處理版本與元件關係 | WinRE |
| 修 WMI Repository（壞掉的話） | 要 `winmgmt /resetrepository` | Windows 內 |
| TPM-only BitLocker 解密 | 沒 TPM 沒辦法解 | 原機 + Windows |
| Storage Spaces 池修復 | 要 Storage Spaces 服務 | Windows 內 |
| 重灌（fresh install） | 跑 Windows 安裝程式 | Windows ISO |

---

個別檔案的提取與替換可以從 Linux 嘗試，包含告知版本差異後的試改，見 [15](15-image-file-replacement.md)。單檔複製不等於重建元件儲存區或完成正式更新。

## 2. 準備 Windows 安裝媒體

本案需要 Windows 原生修復工具時，準備對應架構與用途的官方安裝媒體：

### 下載 ISO

- 官方：https://www.microsoft.com/zh-tw/software-download/windows11
- 選「下載 Windows 11 磁碟映像（ISO）」
- 核對目標版本、架構、語言與修復用途

### 放進 Ventoy

```bash
# 救援 USB 已經是 Ventoy（參見 00-rescue-usb-preparation.md）
# Ventoy 的儲存分割區會自動 mount，丟 ISO 進去就行
cp /path/to/Windows.iso /media/$USER/Ventoy/
```

開機時 Ventoy 選單會列出 ISO，選它就能進 Windows 安裝環境。

### Win10/Win11 通用 vs 特定版本

- 依目標 Windows 準備來源，修復來源與離線系統的更新層級、語言及版本需求見 [Microsoft 說明](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-a-windows-repair-source?view=windows-11)。
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
- 優先使用安裝媒體的「修復您的電腦」，避免反覆強制斷電加重既有故障。

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

下面範例假設 Windows 在 `D:\`、EFI 分割區是 `S:\`。先用 `dir D:\Windows` 確認，ESP 由 `diskpart` 查核後指派代號。命令依診斷選用，不把所有修復連續執行。

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
sfc /scannow /offbootdir=S:\ /offwindir=D:\Windows
```

此例 `S:` 是已確認的離線開機分割區，實際代號依配置調整。跑完看結果：
- `did not find any integrity violations` → 此次檢查未找到完整性問題
- `successfully repaired` → SFC 報告已修復，另測試原故障
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

:: 先查來源中的 index，以下 1 僅為已選定 index 的例子
dism /Get-WimInfo /WimFile:E:\sources\install.wim

:: install.wim 或 install.esd
dism /Image:D:\ /Cleanup-Image /RestoreHealth /Source:WIM:E:\sources\install.wim:1 /LimitAccess
:: 如果是 esd：
dism /Image:D:\ /Cleanup-Image /RestoreHealth /Source:ESD:E:\sources\install.esd:1 /LimitAccess
```

`install.wim` 後面的 `:1` 是 image index，可以先查：
```cmd
dism /Get-WimInfo /WimFile:E:\sources\install.wim
```

依實際清單選對應版本、架構與語言，不假設 Home／Pro 永遠在固定 index。DISM 成功後再跑 SFC，最後測試開機。

### 4.5 chkdsk（檔案系統檢查，比 ntfsfix 強）

```cmd
chkdsk D: /f
:: /f 修錯誤
:: 有必要讀取壞磁區時才評估 /r，先保存映像
```

> Linux 的 `ntfsfix` 只能處理輕量問題，**chkdsk 才是 NTFS 的官方檢查工具**。但 chkdsk 對嚴重壞道會試著 read 然後 mark bad，這跟 ddrescue 邏輯衝突 —— 如果磁碟有實體故障疑慮，先 ddrescue 出來再說，不要直接 chkdsk。

### 4.6 解除 KB 更新

```cmd
:: 列出已裝的更新
dism /Image:D:\ /Get-Packages | findstr KB

:: 看完整資訊
dism /Image:D:\ /Get-Packages /Format:Table

:: 移除
dism /Image:D:\ /Remove-Package /PackageName:Package_for_RollupFix~31bf3856ad364e35~amd64~~22621.1928.1.6
```

把 PackageName 換成經日誌、失敗時序與套件資訊確認相關的完整名稱，不只憑「最近安裝」選擇。

### 更新未完成導致無法開機

當更新日誌與開機失敗時序支持回復待完成操作時，保存備份後，在 WinRE 對已安裝但無法開機的 Windows 執行：

```cmd
:: D:\ 已核對是離線 Windows，不是目前執行的 WinRE（通常為 X:\）
dism /Image:D:\ /Cleanup-Image /RevertPendingActions
```

這會回復先前 servicing 的全部待完成操作，不是只刪某個 XML。確認結果後重開測試，不對執行中的 Windows 或 WinRE 映像本身使用。依據：[Microsoft DISM 選項](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options?view=windows-11)。

### 4.7 帳號修復

WinRE 中的 `net user` 不會自動操作離線 Windows 的 SAM。要修本機帳號，依 [06 Registry 編輯](06-registry-edit.md) 的授權與 hive 流程處理，不使用未完成的 SAM 位元組修改範例。

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

如果系統壞但能進桌面（哪怕不穩定），可評估修復安裝：

1. 進 Windows
2. 掛載 ISO 或解開 ISO 到資料夾
3. 跑 `setup.exe`
4. 選「升級這部電腦」「保留個人檔案和應用程式」
5. 走完安裝流程（會花 30-60 分鐘）

**效果**：
- 由安裝程式修復／更新系統
- 選擇保留個人檔案與應用程式後，以安裝程式最終確認畫面為準，先保存備份
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

依 [08](08-data-recovery.md) 完成重要資料備份與可讀性驗證，並保存應用程式資料、所需授權資訊及重新安裝清單。Windows 授權是否可重新啟用，依實際版本與授權狀態確認，不從主機型號推斷。

```bash
# 供重裝時參考，目錄清單不等於完整安裝清單
ls /mnt/win/'Program Files'/ /mnt/win/'Program Files (x86)'/ \
    > /mnt/external/installed-apps-list.txt
```

確認重灌磁碟與要保留的分割區，取得重灌授權後再執行。

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
| 個別系統檔替換 | [15 映像提取與替換](15-image-file-replacement.md) | SFC／DISM |
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
| 元件修復反覆失敗，且使用者接受重裝代價 | 比較取得修復來源、還原備份及重裝的實際成本 |
| 磁碟壞道大量出現 | 救資料後換新碟，舊碟不要繼續用 |
| 使用者本來就要換新電腦 | 沒必要花時間 |

把上面這些情境跟使用者講清楚，他會自己選。**修復師的價值在誠實判斷該修還是該重灌，不在硬要把每台都修好**。

---

## 10. 交接與驗證

向使用者提供已確認的 Windows／ESP 代號、診斷與備份位置、建議執行的修復命令，以及成功／失敗後如何處理。能進入 Windows 才提供修復安裝；無法開機時先走 WinRE 或資料還原。

回報實際命令結果、日誌與開機測試。不要編造成功率、耗時或「一定不掉資料」的承諾。資料備份、元件修復、正常開機分別確認；重灌也無法解決未處理的硬體故障。
