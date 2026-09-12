---
name: windows-rescue-from-linux
description: >-
  This skill MUST be used when rescuing an unbootable Windows PC from Linux,
  preparing a Linux rescue USB, or extracting Windows image files to replace
  damaged system components. Covers Windows 開不了機, BSOD 救援, 救資料,
  BCD 修復, NTFS 損壞, BitLocker, 離線掃毒, 重設 Windows 密碼,
  系統檔替換, Windows 映像提取, 隨身碟救援系統 and 救援工具安裝.
  It SHOULD also be used when symptoms imply offline Windows recovery even
  without naming a tool. Default language is Traditional Chinese for Taiwan.
metadata:
  version: "1.2.3"
---

# Windows 救援工具箱（從 Linux 救援系統 修 Windows）

## Overview

從 Linux 救援系統 診斷無法正常使用的 Windows，救出資料並依原因修復。也能準備救援碟，或從 Windows 映像提取個別檔案、替換故障系統中的損壞檔案。需要 Windows 原生修復工具時，交接到 WinRE。

## Input Contract

先從對話與現有資料確認目標：準備救援碟、只救資料，或修復 Windows。實機救援需要知道卡住的畫面與錯誤代碼、最近變更、重要資料與備份位置，以及 Linux、Windows 磁碟和可用映像在哪裡。只補問會影響下一步的缺項，已有資訊直接沿用。

## Workflow

### 1. 依目標進入

- **準備救援碟**：讀 [00-rescue-usb-preparation.md](references/00-rescue-usb-preparation.md)。使用者同意製作並確認目標 USB 與清除範圍後，由 AI 完成下載、工具準備、原有資料完整備份、USB 完整系統安裝、工具預裝與開機驗證；備份驗證通過後才清除 USB。交付目標是插入相容電腦即可使用，不能以 Live USB 代替或把工具安裝留到救援現場。這是獨立任務，不先要求故障電腦的症狀。
- **實機救援**：先讀 [01-safety-principles.md](references/01-safety-principles.md)，確認目標磁碟、備份與硬體狀態。只需救資料時，完成資料驗證即可交付。
- **缺工具或不確定用哪個**：讀 [14-cli-tools-catalog.md](references/14-cli-tools-catalog.md)，檢查本次會用的工具。可用 `bash scripts/bootstrap-check.sh` 盤點，缺少無關工具不阻擋救援。Node.js 與 AI CLI 只在使用者要於救援碟上執行它們時準備。

### 2. 先辨識磁碟，再掛載

用 `lsblk`、`blkid` 與裝置型號、序號、UUID 對應 Windows 碟、救援 USB、備份碟。分割區大小與標籤只能當線索，還要核對 Windows 目錄、ESP 類型與開機項指向。

有異音、讀取卡住、I/O 錯誤或健康警示時，先讀 [08-data-recovery.md](references/08-data-recovery.md) 評估映像救援，停止一般全碟掃描與原碟修復。SMART 無法取得時標為未知。

BitLocker 先讀 [10-bitlocker.md](references/10-bitlocker.md) 解鎖。一般掛載讀 [03-mount-windows.md](references/03-mount-windows.md)，第一次唯讀。Linux 自己的 UEFI／Legacy 開機模式不能單獨判定 Windows 的安裝模式。

### 3. 依症狀查閱與修復

只讀本案相關參考。多重症狀或原因不明時讀 [02-symptom-triage.md](references/02-symptom-triage.md)，以日誌與檢查結果縮小原因。

| 症狀或需求 | 何時讀哪份參考 |
|---|---|
| 壞碟、分割區讀不出、只救資料、救已刪檔案 | [08 資料救援](references/08-data-recovery.md)，區分檔案備份、映像與刪除檔救援 |
| BOOTMGR missing、Windows Boot Manager 不見、BCD／EFI 損壞、雙系統選單異常 | [04 開機修復](references/04-boot-repair.md) |
| NTFS 掛載失敗、容量異常、分割表或檔案系統錯誤 | [05 檔案系統修復](references/05-filesystem-repair.md) |
| 忘記本機密碼、帳號鎖定、修改服務或 registry | [06 Registry 編輯](references/06-registry-edit.md)，寫入前備份整個 hive |
| 中毒、瀏覽器綁架、不明自動啟動 | [07 惡意軟體清理](references/07-malware-cleanup.md)，先掃描再判斷處置 |
| 隨機當機、RAM／CPU／磁碟健康疑慮 | [09 硬體診斷](references/09-hardware-diagnostics.md) |
| 更新後無限重啟、疑似 driver 問題、INACCESSIBLE_BOOT_DEVICE | [11 驅動與更新](references/11-driver-and-update-issues.md)，依證據選擇修復 |
| 暫存設定檔、使用者設定檔服務登入失敗 | [12 設定檔修復](references/12-profile-corruption.md) |
| 系統組件損壞或遺失、有 ISO／WIM／ESD／SWM 或備份映像可取檔 | [15 映像檔案替換](references/15-image-file-replacement.md)，辨識來源、提取個別檔案並驗證替換 |
| 需要 SFC、DISM、正式安裝 driver、重建 BCD 或重設系統 | [13 Windows 修復工具交接](references/13-when-linux-cannot-fix.md) |

修復前依 [01 安全準則](references/01-safety-principles.md) 保存重要資料及受影響檔案／結構。說明確切修改與還原方式，沿用已授權範圍，不逐個 `sudo` 或同一操作重複確認。

映像來源優先選與目標相符的版本。版本不符或無法完整確認時，也可說明差異、可能無效或引入新故障，讓使用者選擇備份後嘗試。依 [15](references/15-image-file-replacement.md) 保留可還原的替換路徑，不承諾一定能開機。

### 4. 驗證與交付

按改動檢查結果：檔案替換比對內容、hive 修改核對目標值與其他值、EFI 修復核對檔案與開機項、備份核對命令結果及可讀性。`ntfsfix` 寫入屬於修復，不是通用驗證。修檔案系統前先卸載。

完成寫入後正常卸載，再測試 Windows 開機與原故障。無法現場開機時明確列為待驗證。測試失敗先還原本次試改、重新診斷，不重複相同修法或接連換多個版本。

## Scripts

在 skill 資料夾執行，先看腳本的參數與輸出位置。腳本只協助操作，不能代替本案診斷。

| 腳本 | 用途 |
|---|---|
| [bootstrap-check.sh](scripts/bootstrap-check.sh) | 盤點環境與工具，不安裝 |
| [install-rescue-tools.sh](scripts/install-rescue-tools.sh) | 依選定範圍安裝工具，準備救援碟時使用 |
| [identify-windows-volumes.sh](scripts/identify-windows-volumes.sh) | 找 Windows、EFI、Recovery 候選分割區 |
| [mount-windows-safe.sh](scripts/mount-windows-safe.sh) | 唯讀掛載 Windows 分割區 |
| [backup-user-data.sh](scripts/backup-user-data.sh) | 把指定掛載點的使用者資料備份到另一個目的地 |
| [disk-health-report.sh](scripts/disk-health-report.sh) | 讀取磁碟健康資訊與檢查限制 |
| [boot-diagnostic.sh](scripts/boot-diagnostic.sh) | 收集開機檔案、EFI、registry 與日誌線索 |
| [malware-quick-scan.sh](scripts/malware-quick-scan.sh) | 掃描常見位置並報告偵測結果，預設不移動檔案 |

## Output Contract

回報診斷依據、實際修改、備份／還原位置、驗證結果及尚未解決的問題。救援紀錄保存在使用者指定的外接碟或其他可持續保存的位置，供使用者或接手技師閱讀。腳本暫存在 `/tmp` 的報告須於重開前轉存；不把金鑰或密碼寫進紀錄。

## Quality Rules

- 先唯讀，壞碟先映像，無法解鎖的 BitLocker 不當一般 NTFS 修。
- 從症狀判斷原因，檔名、時間、錯誤代碼與掃描命中都需要上下文。
- 映像提取成功、檔案複製成功與恢復開機分別驗證，不互相代替。
- `tmux` 能維持 SSH 斷線後的程序；不能防止斷電或 Live USB 當機。映像續作靠持續保存的 mapfile。
