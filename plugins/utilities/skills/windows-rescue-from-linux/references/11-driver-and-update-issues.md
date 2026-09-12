# 11 · Driver 與 Windows Update 卡死的處理

> 從 Linux 先查事件紀錄、更新紀錄與 driver 服務設定，針對有證據的故障停用服務或替換檔案。完整更新回復、driver 安裝與元件存放區修復交由 Windows 工具處理。共通備份與掛載見 [01](01-safety-principles.md)、[03](03-mount-windows.md)，registry 變更先讀 [06](06-registry-edit.md)。

---

## 1. Windows Update 卡住的症狀

| 症狀 | 多半原因 |
|---|---|
| 「Working on updates / 請勿關閉電腦」轉圈圈幾小時 | update 的 pending operation 卡住 |
| 「Undoing changes made to your computer」反覆 | update 安裝失敗回滾失敗 |
| 開機後一進桌面又重開 | post-update 階段失敗 |
| 更新錯誤 0xC1900101 / 0x80070005，或更新後 WHEA 藍畫面 | 分別可能涉及驅動、存取權限或硬體；需保留實際錯誤紀錄 |
| Windows 開機跳「Failure configuring updates」 | servicing stack 出錯 |

---

## 2. 調查與回復未完成的更新

唯讀檢查 `Windows/Logs/CBS/CBS.log`、`Windows/Logs/DISM/dism.log`、`Windows/WinSxS/pending.xml` 與 Setup 事件紀錄，對照故障時間、套件名稱及錯誤碼。`pending.xml` 存在只代表有待完成操作，不能直接推論它造成卡死。

- 需要回復未完成的 servicing 操作時，使用 [13](13-when-linux-cannot-fix.md) 的 WinRE / DISM 路線；保留 XML 與日誌，不以改名所有 XML、刪除 CBS 紀錄或 poqexec.log 取代更新回復。
- 若證據只指向下載快取損壞，回 Windows 停止更新服務後處理 `SoftwareDistribution\Download`。這不能撤銷已進入安裝階段的更新。
- `SYSTEM\ControlSet00N\Control\Session Manager` 的 `PendingFileRenameOperations` 可能同時包含多個合法操作。唯讀匯出後，對照來源、目的檔案及安裝紀錄；需要排除個別操作時保留其餘成對項目與 REG_MULTI_SZ 型別，依 [06 的副本合併流程](06-registry-edit.md) 驗證。不把整個值清掉當作通用解法。

## 3. 找出有問題的 driver

### 3.1 從事件日誌找

從 Linux 看 Windows 事件日誌：

```bash
# 裝 python-evtx
pip install python-evtx --user
# 或：
sudo apt install python3-evtx

# 看 System log
python3 - /mnt/win/Windows/System32/winevt/Logs/System.evtx <<'PYEVTX'
import sys
from Evtx.Evtx import Evtx
with Evtx(sys.argv[1]) as log:
    for record in log.records():
        print(record.xml())
PYEVTX
```

關鍵 Event ID：
- **219**：driver load 失敗（裡面會講哪個 .sys）
- **41**：kernel power（不正常重開）
- **1001**：BugCheck（BSOD，含 STOP code）
- **6008**：unexpected shutdown
- **7000 / 7026**：服務啟動失敗（多半是 driver service）

### 3.2 從最近修改時間找

```bash
# 列出最近 7 天改過的 .sys
sudo find /mnt/win/Windows/System32/drivers/ -name "*.sys" -mtime -7 -ls
```

### 3.3 從 minidump 找（懂逆向才有用）

```bash
ls /mnt/win/Windows/Minidump/
# 檔名格式：MMDDYY-XXXXX-XX.dmp
# 想分析的話要回 Windows 用 WinDbg 或 BlueScreenView
# Linux 端能做的：把這些檔複製到外接碟，事後分析
```

### 3.4 從 BSOD 代碼推測

| BSOD | 通常壞的 driver 類型 |
|---|---|
| WHEA_UNCORRECTABLE_ERROR (0x124) | CPU/記憶體硬體，或晶片組 driver |
| DRIVER_IRQL_NOT_LESS_OR_EQUAL (0xD1) | 任一 driver，看附帶的 .sys |
| SYSTEM_THREAD_EXCEPTION_NOT_HANDLED (0x7E) | 同上 |
| VIDEO_TDR_FAILURE (0x116) | 顯卡 driver（nvlddmkm.sys / amdkmdag.sys / igdkmd64.sys） |
| KMODE_EXCEPTION_NOT_HANDLED (0x1E) | 核心模式例外，需看傾印才能縮小到 driver 或其他原因 |
| PAGE_FAULT_IN_NONPAGED_AREA (0x50) | RAM 壞或記憶體相關 driver |
| INACCESSIBLE_BOOT_DEVICE (0x7B) | 儲存控制器 driver（intelide / iaStorAC / nvme） |

---

## 4. 停用已確認有問題的 driver

### 4.1 對應 service 與檔案

在實際使用的 ControlSet 下查 `Services`，以 `ImagePath` 對應 `.sys`，記下原 `Start`、相依服務及是否為開機必要的儲存驅動。修改方法使用 [06 的單值合併範例](06-registry-edit.md)，保留其他 values。

例如，傾印與事件紀錄都指向 `nvlddmkm.sys`，且 `ImagePath` 確認對應 `nvlddmkm` 時，才把該服務的 `Start` 改為 4。近期修改時間只用來找候選，不足以單獨決定停用。

### 4.2 是否需要搬走 .sys

先測試單一服務變更。只有仍有其他載入路徑、且已確認要隔離該檔案時，才在外接健康磁碟保留原檔、路徑與雜湊，再移出原位置。缺少 driver 本身也可能讓開機失敗，不把搬檔當成每次停用的固定下一步。

如果問題是 driver 檔案損壞而非不相容，可依主檔的映像檔案替換路線提取候選檔；安裝完整 driver 套件仍需 Windows。

### 4.3 重開測試

如果 Windows 能進入桌面：
- 顯卡可能改用 Microsoft Basic Display Adapter；確認顯示功能與登入狀況
- 進 Device Manager 把問題 driver uninstall 乾淨
- 從官網下載新版 driver 重裝

如果還是進不去：
- 若有搬檔，從本案備份恢復該檔案與原路徑
- 把 Service Start 改回原值
- 對照測試結果重新判讀傾印與事件紀錄，再決定下一個候選

### 4.4 常見檔名與用途

| 檔名 | 廠商/用途 |
|---|---|
| `nvlddmkm.sys` | NVIDIA 顯卡 |
| `amdkmdag.sys` / `atikmdag.sys` | AMD 顯卡 |
| `iaStorA.sys` / `iaStorAC.sys` | Intel RST 儲存 |
| `Netwtw0X.sys` | Intel 無線網卡 |
| `bcmwl63a.sys` | Broadcom 無線網卡 |
| `ndis.sys` | 通用網路堆疊（這壞通常是其他 driver 連帶） |
| `tcpip.sys` | TCP/IP 堆疊（同上） |
| `igdkmd64.sys` | Intel 內顯 |
| `Killer*` | Killer 網卡 |
| `RTKVHD64.sys` | Realtek 音效 |

---

## 5. Driver Store 路徑

Windows 把所有裝過的 driver 存在 `DriverStore`，移除 .sys 只是停止 load，store 裡面還有副本。回 Windows 後可以從這裡再裝回來：

```
/mnt/win/Windows/System32/DriverStore/FileRepository/
  nv_dispi.inf_amd64_<hash>/        ← NVIDIA driver 整包
  oem<N>.inf_amd64_<hash>/          ← 第三方 driver
  ...
```

可唯讀檢查套件來源與內容；解除安裝套件由 Windows 的 `pnputil` 處理。以下 oem15.inf 須換成本案已核對的套件：

```cmd
pnputil /enum-drivers
pnputil /delete-driver oem15.inf /uninstall /force
```

---

## 6. 範例：更新後出現 WHEA 藍畫面

保留 STOP code、傾印、更新紀錄與硬體診斷。WHEA 優先調查硬體回報的錯誤，不因剛更新就停用 Wi-Fi driver。若傾印明確指向某個非開機必要的 driver，再用上述單一服務變更測試；沒有這項證據就不順手清更新快取或移除 pending.xml。

## 7. Linux 完全做不到的（要回 Windows）

| 任務 | 為什麼 Linux 做不到 |
|---|---|
| `sfc /scannow` 系統檔案完整性檢查 | sfc 是 Windows 專用，要走 Component Servicing API |
| `DISM /RestoreHealth` 修復 Component Store | 同上 |
| 重裝 driver（含註冊到 Device Manager） | 要走 PnP Manager |
| 解除安裝特定 Windows Update（KBxxxxxxx） | 要走 WUSA / DISM |
| Reset This PC / In-place upgrade | 前者可走 WinRE，保留應用程式的就地升級需從可運作的 Windows 啟動 |
| 重建 Driver Store | 要 pnputil |

準備 Windows 安裝媒體，依任務選 WinRE 或可運作的 Windows 內執行。詳見 [13-when-linux-cannot-fix.md](13-when-linux-cannot-fix.md)。

---

## 8. 常見錯誤

### `mv: cannot move ... Operation not permitted`
- 沒用 `sudo`
- 掛載仍是唯讀，或 NTFS / 權限狀態不允許寫入
- BitLocker 沒解（檔系是加密的）

### 改完 registry 開機還是一樣
- 看 `Select\Current` 確認 Windows 用哪個 ControlSet
- 確認 service 名沒打錯
- 工作副本合併成功、比對符合預期，並已寫回正確原檔

### 先前手動移動過 pending.xml
- 保留目前狀態與原始備份，使用 WinRE 的 servicing 工具檢查，不能把修復失敗訊息當成正常。

### Update 卡更深（DISM 等級的損壞）
- 依 13 使用 WinRE 修復；可進 Windows 後才考慮保留應用程式的就地升級
- 或 Reset This PC（保留檔案）

事件檔讀取 API 依據：[python-evtx](https://github.com/williballenthin/python-evtx)。
