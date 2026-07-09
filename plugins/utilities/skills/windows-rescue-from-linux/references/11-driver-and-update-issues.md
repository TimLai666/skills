# 11 · Driver 與 Windows Update 卡死的處理

> **核心觀念**：Windows 升級或裝 driver 之後開不了機，從 Linux 端能做的有兩件事 —— 把卡住的 update 中止讓 Windows 能正常進入桌面、把壞 driver 的 .sys 移除讓系統不去 load 它。其他 driver 重裝、SFC 修復這些 Linux 做不到，得回到 Windows 內處理。

---

## 1. Windows Update 卡住的症狀

| 症狀 | 多半原因 |
|---|---|
| 「Working on updates / 請勿關閉電腦」轉圈圈幾小時 | update 的 pending operation 卡住 |
| 「Undoing changes made to your computer」反覆 | update 安裝失敗回滾失敗 |
| 開機後一進桌面又重開 | post-update 階段失敗 |
| BSOD 0xC1900101 / 0x80070005 / WHEA after update | driver 不相容 |
| Windows 開機跳「Failure configuring updates」 | servicing stack 出錯 |

---

## 2. 中止 pending update

掛起 Windows 系統碟（必須 `rw`，所以要先處理 hibernation，參見 [03-mount-windows.md](03-mount-windows.md)）：

```bash
sudo mount -t ntfs-3g -o rw,remove_hiberfile /dev/sda3 /mnt/win
```

### 2.1 移除 pending.xml（最常見有效的招）

```bash
cd /mnt/win/Windows/WinSxS/
ls -la pending.xml 2>/dev/null && echo "EXISTS"

# 不要直接刪，先改名留後路
sudo mv pending.xml pending.xml.bak-$(date +%Y%m%d)
```

> **為什麼有效**：`pending.xml` 是 Windows 在 boot 期間要繼續做的 update 操作清單。卡住就是因為它指向一個做不完的操作。改名後 Windows 進系統會抱怨上次 update 沒裝完，但至少能進得去，再從 Settings 重跑 update。

### 2.2 清空 SoftwareDistribution\Download

```bash
cd /mnt/win/Windows/SoftwareDistribution/
ls Download/
# 看看裡面有什麼，通常是一堆 KB 編號的資料夾

# 整個資料夾改名（不是刪）
sudo mv Download Download.bak-$(date +%Y%m%d)
sudo mkdir Download
sudo chmod 755 Download
```

進去 Windows 後它會重新下載 update。

### 2.3 處理 PendingFileRenameOperations

```bash
# 看 SYSTEM hive 裡有沒有開機要做的檔案改名
cd /mnt/win/Windows/System32/config
sudo hivexsh SYSTEM
# 在 hivexsh 裡：
> cd ControlSet001\Control\Session Manager
> lsval
# 找 PendingFileRenameOperations
# 如果有而且看起來怪（指向不存在路徑），可以清掉：
> del-val PendingFileRenameOperations
> commit
> quit
```

> 動 registry 前**一定先備份 SYSTEM hive**：`sudo cp SYSTEM SYSTEM.bak`

### 2.4 解開 servicing 卡死的更複雜流程

```bash
cd /mnt/win/Windows/

# 1. 把 ETL log 清掉（卡 servicing 常見原因）
sudo find Logs/CBS -name "*.log" -exec mv {} {}.bak \;

# 2. 砍掉 SessionsPending 旗標
cd /mnt/win/Windows/WinSxS
sudo mv poqexec.log poqexec.log.bak 2>/dev/null

# 3. 看 reboot.xml / setup.xml 卡住的單子
ls -la *.xml
# 把可疑的都改名
```

---

## 3. 找出有問題的 driver

### 3.1 從事件日誌找

從 Linux 看 Windows 事件日誌：

```bash
# 裝 python-evtx
pip install python-evtx --user
# 或：
sudo apt install python3-evtx

# 看 System log
python3 -m Evtx.Evtx /mnt/win/Windows/System32/winevt/Logs/System.evtx \
    | grep -A 5 -i "driver\|crash\|stop" | head -100
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
| KMODE_EXCEPTION_NOT_HANDLED (0x1E) | 多半是顯卡或網卡 |
| PAGE_FAULT_IN_NONPAGED_AREA (0x50) | RAM 壞或記憶體相關 driver |
| INACCESSIBLE_BOOT_DEVICE (0x7B) | 儲存控制器 driver（intelide / iaStorAC / nvme） |

---

## 4. 把壞 driver 移除

> **不要直接刪 .sys**！先停用 service 讓 Windows 不去 load，再把 .sys 搬走（不是刪）。這樣有問題還能搬回來。

### 4.1 找出 driver 對應的 service 名

```bash
# 用 hivexsh 看 Services
cd /mnt/win/Windows/System32/config
sudo cp SYSTEM SYSTEM.bak  # 必備動作
sudo hivexsh -w SYSTEM
> cd ControlSet001\Services
> ls
# 找你想停的 driver service 名（通常跟 .sys 檔名一樣或相近）
```

範例：要停掉 `nvlddmkm.sys`（NVIDIA 顯卡 driver）

```
> cd nvlddmkm
> lsval
# 看 Start 值：0=boot 1=system 2=auto 3=manual 4=disabled
> setval 1
Start
dword:00000004
> commit
> quit
```

或用單行：

```bash
sudo hivexsh -w SYSTEM <<'EOF'
cd ControlSet001\Services\nvlddmkm
setval 1
Start
dword:00000004
commit
EOF
```

### 4.2 搬走 .sys 檔

```bash
# 建一個隔離資料夾
sudo mkdir -p /mnt/win/Rescue-quarantine
sudo mv /mnt/win/Windows/System32/drivers/nvlddmkm.sys \
        /mnt/win/Rescue-quarantine/

# 確認搬走了
ls /mnt/win/Windows/System32/drivers/nvlddmkm.sys 2>/dev/null || echo "OK gone"
```

### 4.3 重開測試

如果 Windows 能進入桌面：
- 顯卡會變 Microsoft Basic Display Adapter，解析度很低，正常的
- 進 Device Manager 把問題 driver uninstall 乾淨
- 從官網下載新版 driver 重裝

如果還是進不去：
- 搬回來：`sudo mv /mnt/win/Rescue-quarantine/nvlddmkm.sys /mnt/win/Windows/System32/drivers/`
- 把 Service Start 改回原值
- 換懷疑下一個 driver

### 4.4 一些常見惡名昭彰的 driver

| 檔名 | 廠商/用途 | 出包頻率 |
|---|---|---|
| `nvlddmkm.sys` | NVIDIA 顯卡 | 高（windows update 推錯版本） |
| `amdkmdag.sys` / `atikmdag.sys` | AMD 顯卡 | 高 |
| `iaStorA.sys` / `iaStorAC.sys` | Intel RST 儲存 | 中（升 Windows 後不相容） |
| `Netwtw0X.sys` | Intel 無線網卡 | 中 |
| `bcmwl63a.sys` | Broadcom 無線網卡 | 中 |
| `ndis.sys` | 通用網路堆疊（這壞通常是其他 driver 連帶） | — |
| `tcpip.sys` | TCP/IP 堆疊（同上） | — |
| `igdkmd64.sys` | Intel 內顯 | 低 |
| `Killer*` | Killer 網卡 | 高 |
| `RTKVHD64.sys` | Realtek 音效 | 低 |

---

## 5. Driver Store 路徑

Windows 把所有裝過的 driver 存在 `DriverStore`，移除 .sys 只是停止 load，store 裡面還有副本。回 Windows 後可以從這裡再裝回來：

```
/mnt/win/Windows/System32/DriverStore/FileRepository/
  nv_dispi.inf_amd64_<hash>/        ← NVIDIA driver 整包
  oem<N>.inf_amd64_<hash>/          ← 第三方 driver
  ...
```

從 Linux 動這個資料夾沒意義，**只在 Windows 內用 `pnputil` 操作**：

```cmd
pnputil /enum-drivers
pnputil /delete-driver oem15.inf /uninstall /force
```

---

## 6. 完整流程範例：升級到新版 Windows 11 後 BSOD

```bash
# 場景：使用者開機就 BSOD WHEA_UNCORRECTABLE_ERROR，剛裝完 Windows Update

# 1. 掛載
sudo mkdir -p /mnt/win
sudo mount -t ntfs-3g -o rw,remove_hiberfile /dev/nvme0n1p3 /mnt/win

# 2. 看最近裝了什麼
python3 -m Evtx.Evtx /mnt/win/Windows/System32/winevt/Logs/Setup.evtx 2>/dev/null \
    | grep -i "installed\|kb" | tail -20

# 3. 看哪些 driver 最近改過
sudo find /mnt/win/Windows/System32/drivers/ -name "*.sys" -mtime -3 -ls

# 4. 砍掉 pending.xml 讓 update 不卡
cd /mnt/win/Windows/WinSxS/
sudo mv pending.xml pending.xml.bak 2>/dev/null

# 5. 清 SoftwareDistribution
cd /mnt/win/Windows/
sudo mv SoftwareDistribution SoftwareDistribution.bak
sudo mkdir SoftwareDistribution

# 6. 看 Minidump 確認壞的 driver（如果有）
ls -la /mnt/win/Windows/Minidump/

# 7. 假設懷疑是 Intel WiFi driver
cd /mnt/win/Windows/System32/config
sudo cp SYSTEM SYSTEM.bak
sudo hivexsh -w SYSTEM <<'EOF'
cd ControlSet001\Services\Netwtw10
setval 1
Start
dword:00000004
commit
EOF

# 8. 搬走 .sys
sudo mkdir -p /mnt/win/Rescue-quarantine
sudo mv /mnt/win/Windows/System32/drivers/Netwtw10.sys /mnt/win/Rescue-quarantine/

# 9. 卸載
cd /
sudo umount /mnt/win

# 10. 拔 USB 重開測試
```

---

## 7. Linux 完全做不到的（要回 Windows）

| 任務 | 為什麼 Linux 做不到 |
|---|---|
| `sfc /scannow` 系統檔案完整性檢查 | sfc 是 Windows 專用，要走 Component Servicing API |
| `DISM /RestoreHealth` 修復 Component Store | 同上 |
| 重裝 driver（含註冊到 Device Manager） | 要走 PnP Manager |
| 解除安裝特定 Windows Update（KBxxxxxxx） | 要走 WUSA / DISM |
| Reset This PC / In-place upgrade | 要 WinRE 環境 |
| 重建 Driver Store | 要 pnputil |

這些情境的解法：準備 Windows 安裝媒體（ISO 燒進 Ventoy），從那個 USB 開機進 WinRE 處理。詳見 [13-when-linux-cannot-fix.md](13-when-linux-cannot-fix.md)。

---

## 8. 常見錯誤

### `mv: cannot move ... Operation not permitted`
- 沒用 `sudo`
- 沒 `rw` 掛載（hibernation 沒清）
- BitLocker 沒解（檔系是加密的）

### 改完 registry 開機還是一樣
- 確認改的是 `ControlSet001` 而不是 `ControlSet002`
- 看 `Select\Current` 確認 Windows 用哪個 ControlSet
- 確認 service 名沒打錯
- 寫完有 `commit`

### 改完 pending.xml 後 Windows 抱怨「修復系統失敗」
- 正常，按取消跳過，進到桌面後跑 Settings → Update 重跑
- 真的進不去就把 pending.xml.bak 改回 pending.xml

### Update 卡更深（DISM 等級的損壞）
- Linux 做不到，需要 Windows ISO 走 in-place upgrade
- 或 Reset This PC（保留檔案）
