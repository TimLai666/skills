# 09 — 硬體診斷

電腦不開機、隨機當機，可能不是 Windows 問題而是硬體。Linux 救援碟可以做硬體層的診斷。

## 概覽

| 元件 | 工具 | 限制 |
|---|---|---|
| 硬碟健康 | `smartctl` | 無法讀取或未支援時為未知；通過也不能排除故障 |
| 硬碟壞磁區 | `badblocks` | 唯讀也增加負載；疑似故障碟先映像 |
| 記憶體 | `memtester`（OS 內）/ memtest86+（boot） | OS 內測試覆蓋率有限，正式測要 boot memtest86+ |
| CPU 溫度 | `sensors` (lm-sensors) | 簡單可靠 |
| GPU / 顯示卡 | `lspci`, `lshw` | 只能識別與基本資訊 |
| 主機板 / BIOS | `dmidecode` | 列出硬體清單與韌體版本 |
| 整體 stress | `stress-ng` | 模擬負載找問題 |
| PSU / 電源 | 沒有軟體可測 | 看症狀 |

## 第一站：列出有什麼

```bash
sudo lshw -short
# 一頁式硬體摘要

sudo lshw -html > /tmp/hardware.html
# 詳細版

sudo dmidecode -t system     # 主機/主機板/廠商
sudo dmidecode -t memory     # 記憶體規格
sudo dmidecode -t bios       # BIOS 版本

lspci -nnk     # PCI 裝置（顯卡、網卡、SATA 控制器）
lsusb          # USB 裝置
inxi -Fxz      # 視覺化整體報告（要 sudo apt install inxi）
```

存一份起來，後面對照。

## 硬碟健康：smartctl

```bash
# 一句話健康狀態
sudo smartctl -H /dev/sda

# 詳細
sudo smartctl -a /dev/sda

# SATA-USB adapter 需要 -d
sudo smartctl -a -d sat /dev/sdb
```

關鍵屬性看這幾個：

| Attribute | 警戒值 |
|---|---|
| `Reallocated_Sector_Ct` (5) | > 0 警惕；增加中 → 立刻備份 |
| `Current_Pending_Sector` (197) | > 0 警惕 |
| `Offline_Uncorrectable` (198) | > 0 嚴重 |
| `UDMA_CRC_Error_Count` (199) | 觀察是否持續增加，並檢查線材與連接 |
| `Reported_Uncorrect` (187) | > 0 嚴重 |
| `Power_On_Hours` (9) | 看碟使用時間 |
| `Wear_Leveling_Count` (177, SSD) | 廠商定義不同，須按型號解讀 |

SSD 多看：
- `Media_Wearout_Indicator` / `SSD_Life_Left`：可能表示磨耗或剩餘量，依廠商定義核對
- `Total_LBAs_Written`：累計寫入量

範例輸出片段（要警惕的）：

```
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0033   050   050   050    Pre-fail  Always   FAILING_NOW 1234
197 Current_Pending_Sector  0x0032   100   100   000    Old_age   Always       -       42
```

`FAILING_NOW` 或 `WHEN_FAILED` 是過去式都嚴重。

SMART 無法讀取、USB 轉接器不支援或屬性缺漏時，狀態是未知。NVMe 需查看其健康紀錄、Critical Warning、Media Errors 與 Percentage Used，不能套用 ATA 屬性編號。

### 自我測試

先完成必要資料備份；有 I/O 錯誤、異音或惡化跡象時不要加做測試，直接接 [映像救援](08-data-recovery.md)。只有穩定裝置且診斷需要時才手動啟動。

```bash
# 短測（幾分鐘）
sudo smartctl -t short /dev/sda

# 看結果
sudo smartctl -l selftest /dev/sda

# 長測（幾小時）
sudo smartctl -t long /dev/sda
sudo smartctl -l selftest /dev/sda
```

自我測試是硬碟韌體跑的，不是 Linux 跑的。會增加裝置負載，應避免同時執行救援讀取。

「Completed without error」表示該次測試未報錯，不是整體健康保證；中斷、未完成與錯誤須分別判讀。

## 壞磁區掃描：badblocks

```bash
# 僅用於已備份且無故障跡象的裝置，唯讀仍會讀完整個範圍
sudo badblocks -sv /dev/sda3

# 結果：
# Checking blocks 0 to N
# Pass completed, 0 bad blocks found.    ← 這次掃描未發現壞區
# 或：
# Pass completed, 17 bad blocks found.   ← 有問題
```

注意：
- `-w` 是寫入測試會洗光資料，**不要用**
- `-n` 會寫入再還原，救援原碟不使用
- 壞區數量大量增加 → 整碟在死亡邊緣

### 記錄錯誤位置

```bash
sudo badblocks -sv /dev/sda3 -o /tmp/badblocks-sda3.txt
# 結果存到檔案
cat /tmp/badblocks-sda3.txt
```

跟 NTFS metadata 同步要回 Windows 跑 `chkdsk /r`，Linux 無對應工具。這不是故障原碟應先執行的步驟。

## 記憶體測試

### OS 內測（有限）

```bash
# 測 1GB
sudo memtester 1G

# 多次
sudo memtester 1G 5
```

限制：
- 只能測「目前 free 的記憶體」
- OS 本身、kernel 用的部分測不到
- 通過不代表 RAM 真沒問題

### 完整測：memtest86+

要從 boot 進去測（OS 沒在跑）。

選項 A：**從 GRUB**

Ubuntu 預設 GRUB 選單有 memtest86+ 項目。重開機 → 進 GRUB → 選 Memory test。

選項 B：**從 Ventoy**

把 memtest86+ 的 ISO 放到 Ventoy 上，開機選它。
下載：https://www.memtest.org/

選項 C：**從 Windows 內建**

Win+R → `mdsched.exe` → Restart now。Microsoft 自己的記憶體診斷。

跑至少一個完整 pass（30 分鐘 - 數小時，視 RAM 大小）。看到任何錯誤行就是 RAM 有問題。

多條 RAM 的話一條一條測：
1. 拔掉除了一條外其他都拔
2. memtest 過 → 換下一條
3. 找出有問題的那條

或記憶體插槽壞：
1. 一條 RAM 在每個插槽各測一次

## CPU / 溫度

```bash
sudo apt install lm-sensors
sudo sensors-detect    # 僅在感測器未識別時依硬體選擇探測項目
sensors
```

範例輸出：

```
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +52.0°C  (high = +100.0°C, crit = +100.0°C)
Core 0:        +50.0°C  (high = +100.0°C, crit = +100.0°C)
Core 1:        +51.0°C  ...
```

正常情況：
- 待機：30-50°C
- 中度負載：50-70°C
- 重度負載：70-85°C
- > 90°C 危險

異常情況：
- 待機就 80°C+ → 散熱問題（風扇積灰、散熱膏乾掉、heatsink 沒接觸好）
- 一加負載就 95°C+ throttle → 同上

### 看 CPU throttling

```bash
# 看當前頻率
watch -n 1 'grep MHz /proc/cpuinfo'

# 跑全速 stress
sudo apt install stress-ng
stress-ng --cpu $(nproc) --timeout 60s &

# 旁邊看頻率：突然掉一半 → thermal throttling
```

## GPU / 顯卡

```bash
lspci -nn | grep -i vga
lspci -nn | grep -i nvidia
lspci -nn | grep -i amd

# 詳細
sudo lshw -C display

# NVIDIA（要有 driver）
nvidia-smi

# AMD
sudo apt install radeontop
radeontop
```

顯卡壞掉的線索：
- BIOS 開機看不到畫面（換內顯試試）
- 進 OS 後花屏、artifact
- 跑遊戲突然當機 / 黑屏

## 整體 stress test

完成資料保全後，依症狀選測試負載並監看溫度；不把壓力測試當成每案必跑。救援碟或故障磁碟仍連接時，不加入磁碟 I/O 壓力負載。

```bash
sudo apt install stress-ng

# CPU + 記憶體一起壓
stress-ng --cpu $(nproc) --vm 2 --vm-bytes 1G --timeout 300s --metrics-brief

# 加 io
stress-ng --cpu $(nproc) --vm 2 --vm-bytes 1G --io 4 --timeout 300s
```

5-10 分鐘壓力測試：
- 如果系統當機 / 重開 → 不穩定（PSU 不足、RAM 不穩、CPU/GPU 過熱）
- 旁邊開 `sensors` 監看溫度
- 旁邊開 `dmesg -w` 看有沒有 kernel error

## 電源（PSU）問題

沒有軟體能直接測 PSU 健康。線索：
- 隨機重開機（特別是高負載時）
- 電腦會自己關機
- BIOS 報「不穩定電壓」
- 老 PSU（5 年以上）
- 加新顯卡後問題出現

判斷邏輯：所有元件單獨測都過，但組合起來不穩定 → 高度懷疑 PSU。換一顆已知好的 PSU 換上去測。

## I/O error 在 dmesg

```bash
dmesg -T | grep -iE 'error|fail|critical' | tail -50

# I/O error 範例
# [12345.678] sd 1:0:0:0: [sda] tag#0 FAILED Result: hostbyte=DID_OK driverbyte=DRIVER_OK
# [12345.679] critical medium error
```

這些錯誤可能來自媒體、線材、供電或控制器。先停止修復與全面掃描，保全資料並依 [08](08-data-recovery.md) 評估映像；再辨識故障來源。

## 系統開機異常表單

```bash
# 看開機過程的錯誤
journalctl -b -p err
journalctl -b -p warning | head -50

# 看上次開機（如果是 Linux）
journalctl -b -1
```

對 Windows 端的硬體事件，看 `02-symptom-triage.md` 的事件日誌章節。

## SSD 特殊問題

### SSD 突然「消失」（從 BIOS 偵測不到）

某些 SSD 韌體 bug 會卡死狀態。冷重開機可能會復原。
- 拔電源、拔 SATA、放 30 秒
- 重新接、開機

仍偵測不到 → 韌體壞掉或 SSD 死了。某些品牌（Crucial、Samsung 等）有 power-cycle recovery 程序，查該型號的官方文件。

### SSD 磨耗與 TRIM

保固到期不等於壽命耗盡。核對該型號的寫入量、磨耗指標、媒體錯誤及實際症狀，再判斷是否換新。救已刪除資料時不要執行 TRIM；它可能使仍可救的內容不可讀。

若救援完成後要檢查 Windows 的刪除通知設定，可在 Windows 執行：

```cmd
fsutil behavior query DisableDeleteNotify
```

回傳 0 表示對應檔案系統的刪除通知未停用，不代表整條儲存路徑必然已成功處理 TRIM；後續依實際裝置與 Windows 設定處理。

## 完整硬體健檢腳本

[disk-health-report.sh](../scripts/disk-health-report.sh) 收集既有 SMART 資料，不自動啟動自我測試或 badblocks。依當機症狀選擇本頁的溫度、記憶體或負載測試；有磁碟錯誤時先處理資料保全。

# 何時該叫使用者送修

- 連 POST 都沒過：主機板問題，自己換不來
- SSD 韌體 bug 但對方有保固：聯絡廠商
- 筆電：通常拆機麻煩，建議送修
- 你不熟的硬體問題：誠實告訴使用者「這超出我能診斷的範圍，建議送修」
