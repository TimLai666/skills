# 09 — 硬體診斷

電腦不開機、隨機當機，可能不是 Windows 問題而是硬體。Linux 救援碟可以做硬體層的診斷。

## 概覽

| 元件 | 工具 | 限制 |
|---|---|---|
| 硬碟健康 | `smartctl` | 大致準確 |
| 硬碟壞磁區 | `badblocks` | 唯讀掃描安全；寫入測試會洗資料 |
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
| `UDMA_CRC_Error_Count` (199) | > 100 → SATA 線/接觸問題 |
| `Reported_Uncorrect` (187) | > 0 嚴重 |
| `Power_On_Hours` (9) | 看碟使用時間 |
| `Wear_Leveling_Count` (177, SSD) | SSD 壽命指標，接近 0 表示快寫滿了 |

SSD 多看：
- `Media_Wearout_Indicator` / `SSD_Life_Left`：剩餘壽命 %
- `Total_LBAs_Written`：累計寫入量

範例輸出片段（要警惕的）：

```
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  5 Reallocated_Sector_Ct   0x0033   050   050   050    Pre-fail  Always   FAILING_NOW 1234
197 Current_Pending_Sector  0x0032   100   100   000    Old_age   Always       -       42
```

`FAILING_NOW` 或 `WHEN_FAILED` 是過去式都嚴重。

### 自我測試

```bash
# 短測（幾分鐘）
sudo smartctl -t short /dev/sda

# 看結果
sudo smartctl -l selftest /dev/sda

# 長測（幾小時）
sudo smartctl -t long /dev/sda
sudo smartctl -l selftest /dev/sda
```

自我測試是硬碟韌體跑的，不是 Linux 跑的。可以一邊跑一邊用電腦。

「Completed without error」→ OK；其他結果都要警惕。

## 壞磁區掃描：badblocks

```bash
# 唯讀掃描（安全）
sudo badblocks -sv /dev/sda3

# 結果：
# Checking blocks 0 to N
# Pass completed, 0 bad blocks found.    ← 健康
# 或：
# Pass completed, 17 bad blocks found.   ← 有問題
```

注意：
- `-w` 是寫入測試會洗光資料，**不要用**
- `-n` non-destructive write 試比較安全但慢且還是寫
- 壞區數量大量增加 → 整碟在死亡邊緣

### 找壞區的具體位置給之後修

```bash
sudo badblocks -sv /dev/sda3 -o /tmp/badblocks-sda3.txt
# 結果存到檔案
cat /tmp/badblocks-sda3.txt
```

跟 NTFS metadata 同步要回 Windows 跑 `chkdsk /r`，Linux 無對應工具。

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
sudo sensors-detect    # 自動偵測 sensor，按 YES 一路下
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

這種訊息基本上是硬碟在死。立刻切到 ddrescue 模式。

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

### SSD 過保固期 = 壽命到了

NAND 寫入次數有上限。看 `Total_LBAs_Written` / 製造商保證寫入量（TBW）。接近或超過就規劃換新。

### TRIM 沒啟用

SSD 用久變慢的常見原因。Windows 那邊問題，但 Linux 救援期間可以看 TRIM 設定：

```bash
sudo fstrim --dry-run /mnt/win    # NTFS 不支援，會錯誤；只是檢查邏輯
```

實際 Windows 那邊讓使用者跑：

```cmd
# 看 TRIM 狀態
fsutil behavior query DisableDeleteNotify
# 結果為 0 = TRIM 啟用，1 = 停用

# 啟用
fsutil behavior set DisableDeleteNotify 0
```

## 完整硬體健檢腳本

`scripts/disk-health-report.sh` 把上面的 smartctl / SMART self-test 自動做完，輸出一份報告。詳見該檔。

如果使用者報告「電腦會自己關機 / 隨機當機」，但不確定是什麼，這個流程：

```bash
# 1. 硬碟 SMART
for d in /dev/sd? /dev/nvme?n?; do
    [ -b "$d" ] || continue
    echo "=== $d ==="
    sudo smartctl -H "$d"
done

# 2. 看溫度
sensors

# 3. 開壓力測試，邊跑邊看
stress-ng --cpu $(nproc) --vm 2 --vm-bytes 1G --timeout 600s &
watch -n 2 sensors

# 4. 跑記憶體測試（要重開機進 memtest86+）

# 5. 看 dmesg 有沒有 I/O error
dmesg -T | grep -iE 'error|fail'
```

# 何時該叫使用者送修

- 連 POST 都沒過：主機板問題，自己換不來
- SSD 韌體 bug 但對方有保固：聯絡廠商
- 筆電：通常拆機麻煩，建議送修
- 你不熟的硬體問題：誠實告訴使用者「這超出我能診斷的範圍，建議送修」
