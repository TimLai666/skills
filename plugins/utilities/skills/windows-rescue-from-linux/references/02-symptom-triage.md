# 02 — 症狀分流（細部）

SKILL.md 的對應表是快速分流，這裡是細部。問題經常不只一個，這份幫你判斷修哪個優先、哪些症狀其實同源。

## 分流原則

1. **先救命再修系統**：硬碟在死、資料還沒備份——這件事永遠優先於任何系統層級修復
2. **由外而內**：先確認電源、硬體、BIOS 設定，再看系統
3. **問清楚「最後一次能用是什麼時候、之間發生過什麼」**：使用者上次能進系統是昨天，中間裝了什麼軟體、跑了 Windows Update、有沒有不正常斷電——這是最關鍵的線索
4. **錯誤代碼是黃金**：完整的 BSOD 文字（如 `0x0000007B INACCESSIBLE_BOOT_DEVICE`）比「藍底白字」這四個字有用一千倍

## 需要補足的資訊

從使用者已提供的內容補足會影響判斷的資訊：

1. **症狀**：開機畫面卡哪？跳什麼錯？多少代碼？是否能進到安全模式（透過 WinRE 的啟動設定）？
2. **時序**：上一次正常是什麼時候？中間做了什麼？（軟體更新、Windows Update、新硬體、停電、跌摔）
3. **頻率**：每次都這樣 / 隨機 / 開機一陣子才出問題
4. **硬體警示**：開機 BIOS 有沒有嗶聲？硬碟有沒有怪聲？開機 LED 有沒有閃？風扇有沒有轉？
5. **資料**：最重要的資料是什麼、在哪裡、有沒有備份過？

## 症狀分類詳表

### 完全無法 POST（連 BIOS 都沒進）

不是 Windows 問題，是硬體。Linux 救援碟也開不了。先檢查：

- 電源線、電池
- 記憶體：斷電並依硬體手冊重新插妥。多條記憶體可逐條測試
- 螢幕：換螢幕、換線
- 主機板設定：依手冊檢查，重設前記錄儲存控制器與開機設定
- 嗶聲：對照主機板手冊翻譯嗶聲代碼

POST 過了但 BIOS 進不去 USB——進 BIOS 改 boot order，確認 USB 是否支援目前開機模式，必要時停用 Fast Boot；Secure Boot 問題依媒體相容性判斷。

### POST 過了但 BIOS 沒看到硬碟

```
BIOS 顯示硬碟「Not Detected」或 size 顯示 0
```

SATA 線鬆掉 / 電源接頭鬆掉 / 硬碟死透了。先換線、換 SATA 口。仍未偵測到時，還需區分磁碟、連接介面與控制器故障。

Linux 開機後 `lsblk` 也看不到——同上。

### Linux 看得到磁碟、smartctl 失敗

```bash
sudo smartctl -a /dev/sdX
# 回 "Smartctl open device: /dev/sdX failed: No such device"
# 或回但所有欄位都是 0
```

SMART 讀取失敗代表狀態未知。先核對裝置路徑、工具錯誤與外接盒支援，不能直接認定磁碟損壞。若同時有異音、I/O 錯誤或掉線，先依 [08-data-recovery.md](08-data-recovery.md) 做映像救援。

### POST 後黑屏，沒看到 Windows logo

可能 bootloader 死了。BIOS 找不到開機磁區。Linux 開機後檢查：

```bash
# UEFI 模式：efibootmgr 看開機項
sudo efibootmgr -v
# 應該看到 Windows Boot Manager 或類似的項
# 不見了 → 04-boot-repair.md 的 UEFI 章節

# Legacy BIOS 模式：看 MBR
sudo dd if=/dev/sda bs=512 count=1 2>/dev/null | xxd | tail -1
# 結尾要 55aa
# 缺少簽章是線索；須對照磁碟與開機方式，見 04-boot-repair.md
```

### 出現 Windows logo 但卡住、無限轉圈

```
症狀：Windows 商標出來，下面圈圈一直轉，永遠進不去
或：出現「準備自動修復」、「自動修復無法修復您的電腦」
或：藍底白字一閃就重開
```

可檢查的方向：
1. **NTFS 損壞**：上次斷電或當機沒收乾淨。`05-filesystem-repair.md`
2. **Windows Update 卡住**：升級中斷或元件處理失敗，需對照更新日誌。`11-driver-and-update-issues.md`
3. **問題 driver 載入失敗**：剛裝的 driver 跟系統不合。`11-driver-and-update-issues.md`

依序排查：
1. 先看事件日誌（從 Linux 讀，見後面「從 Linux 看 Windows 事件日誌」）
2. 有檔案系統錯誤證據時，依 [05-filesystem-repair.md](05-filesystem-repair.md) 判斷適用修復
3. 對照更新事件與 CBS 日誌；`pending.xml` 存在不足以認定故障，也不直接改名
4. 對照最近變更的驅動、錯誤碼與載入紀錄
5. 若指向特定系統檔案損壞，可依 [15-image-file-replacement.md](15-image-file-replacement.md) 從映像取檔替換。版本不同也可說明差異、備份後試修；涉及元件相依性時搭配 WinRE 修復

### BSOD 反覆 + 代碼

把代碼與完整訊息、事件和最近變更交叉查證。以下是排查方向，不是單憑代碼確診：

| 代碼 | 通常原因 | 修復方向 |
|---|---|---|
| `0x0000007B INACCESSIBLE_BOOT_DEVICE` | 找不到開機磁碟 / SATA mode 改了 / boot driver 損壞 | 04 + 05 + BIOS SATA mode |
| `0x000000ED UNMOUNTABLE_BOOT_VOLUME` | NTFS 嚴重損壞 | 05 |
| `0x0000007E SYSTEM_THREAD_EXCEPTION_NOT_HANDLED` | 通常是 driver | 11 |
| `0x000000F4 CRITICAL_OBJECT_TERMINATION` | 關鍵程序終止，可能與儲存裝置、驅動或系統檔案有關 | 09 + 11；有檔案證據再看 15 / 13 |
| `0x000000C5 DRIVER_CORRUPTED_EXPOOL` | driver 損壞 | 11 |
| `0x00000050 PAGE_FAULT_IN_NONPAGED_AREA` | RAM 或 driver | 09（記憶體測試） |
| `0xC000021A FATAL_SYSTEM_ERROR` | 關鍵使用者模式程序終止，可能涉及更新、驅動或系統檔案 | 11 + 13；特定檔案替換見 15 |
| `BAD_SYSTEM_CONFIG_INFO` | registry 損壞 | 06 |
| `0x0000003F NO_MORE_SYSTEM_PTES` | driver leak | 11 |
| `WHEA_UNCORRECTABLE_ERROR` | 硬體錯誤（CPU/RAM/PCIe） | 09 |
| `0xC000007B` | 映像格式錯誤，也可能是架構或相依檔案不符 | 15 + 13，先確認檔案與架構 |

### 帳號相關

- **忘記密碼**：直接 `06-registry-edit.md` 的 chntpw 章節
- **「您的帳戶已被停用」**：chntpw 啟用回來
- **「使用者設定檔服務登入失敗」**：profile 損壞，`12-profile-corruption.md`
- **登入後桌面是空的、檔案不見**：登成了「temp profile」，`12-profile-corruption.md`
- **Microsoft 帳號登不進去**：通常不是本機問題，網路或 MSA 服務。確認登入選項、連線與帳號復原；PIN 不等同本機帳號

### 中毒症狀

- 開機就跳廣告 / 不認識的程式自動跑
- 瀏覽器首頁被綁
- 大量檔案副檔名被改成 `.encrypted` / `.lockbit` / 等怪字尾（勒索病毒）
- CPU 風扇瘋狂轉、系統卡爆（挖礦木馬）
- 不明的網路流量

→ `07-malware-cleanup.md`

**勒索病毒特例**：檔案已被加密，clamav 清掉病毒不會解開檔案。重要事項：
1. **馬上斷網**（拔網路線、關 Wi-Fi）防止橫向擴散
2. 看勒索訊息找出是哪一種變種
3. 上 https://www.nomoreransom.org/ 查是否有免費解密工具
4. 沒解密工具就決定：付贖金（不建議，可能拿不到金鑰）/ 接受損失 / 等以後可能出工具
5. 保留加密檔、勒索訊息與必要證據，隔離受感染系統；確認資料已保存後再決定重灌

### 硬體疑似損壞

- 開機隨機重開、不規律當機
- 跑某些遊戲 / 軟體必當
- 風扇全速但沒做什麼事
- 螢幕花屏 / 顯卡 artifact

→ `09-hardware-diagnostics.md`

## 多重症狀怎麼判先後

例：「開機卡住 + 之前感覺很慢」
- 先 SMART：碟在死才是根本原因
- SMART 未回報警告仍不能排除磁碟故障，再對照 I/O 錯誤與 NTFS
- NTFS 沒事再看 BCD/registry

例：「藍底白字 + 忘記密碼」
- 藍底白字代表現在沒辦法進系統，連登入畫面都不會出現
- 修藍底白字優先；密碼問題等能進到登入畫面再說

例：「中毒了 + 開不了機」
- 開不了機優先（救資料、修開機）
- 進到能讀資料後再掃毒
- 「修完開機 → 立刻又中毒」表示沒清乾淨，重來

例：「想救資料 + 也想修系統」
- 先救資料：健康磁碟可用 rsync，故障磁碟先做映像，再動系統
- 系統修壞了還能重灌，資料沒了真的沒了

## 從 Linux 看 Windows 事件日誌

很多時候症狀模糊，看事件日誌能拿到實質線索。

安裝 `python3-evtx`，或在 Python 虛擬環境安裝 `python-evtx`。以下將事件轉為 XML；也可執行 [boot-diagnostic.sh](../scripts/boot-diagnostic.sh) 篩選開機相關事件。

```bash
python3 - /mnt/win/Windows/System32/winevt/Logs/System.evtx > /tmp/system.xml <<'PYEVTX'
import sys
from Evtx.Evtx import Evtx
with Evtx(sys.argv[1]) as log:
    print("<Events>")
    for record in log.records():
        print(record.xml())
    print("</Events>")
PYEVTX
```

解析失敗時保留原始錯誤，不把空輸出當成沒有異常。需要交接的原始日誌與輸出應存到持久儲存裝置。

API 用法見 [python-evtx 的 evtx_dump.py](https://github.com/williballenthin/python-evtx/blob/master/evtx_scripts/evtx_dump.py)。

最有用的事件 ID：

| Event ID | 來源 | 意義 |
|---|---|---|
| 41 | Kernel-Power | 沒乾淨關機（停電/當機/強制斷電） |
| 1001 | BugCheck | BSOD 紀錄（含完整代碼） |
| 6008 | EventLog | 沒乾淨關機 |
| 7000 | Service Control Manager | 服務啟動失敗 |
| 219 | Kernel-PnP | driver 載入失敗 |
| 55 | Ntfs | 檔案系統損壞 |
| 98 | Ntfs | 磁碟錯誤 |
| 153 | disk | 磁碟 I/O 錯誤 |

以 XML 的 EventID 篩選事件，並查看時間、來源與事件資料；文字關鍵字可能漏掉未展開的事件訊息。

## 何時要切換到「資料優先模式」

只要看到以下任一個訊號：

- SMART FAILED，或壞區／待處理磁區持續增加
- 硬碟有怪聲
- `dmesg` 噴 I/O error
- 掛載失敗伴隨讀取錯誤或裝置反覆掉線
- 使用者說「最重要的就是裡面 OOO 資料」

→ 先依 [08-data-recovery.md](08-data-recovery.md) 選擇備份方式。硬體故障走映像救援；磁碟正常而使用者只要資料，可直接複製重要檔案。
