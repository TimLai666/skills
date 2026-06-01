# 03 — 掛載 Windows 磁碟

掛載是所有後續操作的前置。掛得不好後面什麼都做不了。

## 先看清楚有什麼

```bash
lsblk -f -o NAME,FSTYPE,LABEL,SIZE,MOUNTPOINT,UUID
sudo blkid
```

範例輸出解讀：

```
NAME    FSTYPE   LABEL    SIZE   MOUNTPOINT
sda
├─sda1  vfat     SYSTEM   100M           ← EFI 分割區
├─sda2                    16M            ← Microsoft Reserved (MSR)，不用掛
├─sda3  ntfs     OS       500G           ← Windows 系統碟
├─sda4  ntfs     Data     200G           ← 使用者資料碟
└─sda5  ntfs     Recovery 600M           ← Recovery 分割區
```

要識別的關鍵：

| 分割區 | 特徵 |
|---|---|
| Windows 系統 | NTFS、最大、LABEL 常為 OS/Windows/SYSTEM、含 `/Windows/System32/` |
| EFI System Partition (ESP) | FAT32、100-500MB、含 `/EFI/Microsoft/Boot/` |
| Microsoft Reserved (MSR) | 16MB、無檔案系統，不用掛 |
| Recovery | NTFS、500MB-1GB、LABEL Recovery/WinRE、含 `Recovery/WindowsRE/Winre.wim` |
| BitLocker | `blkid` 會顯示 `TYPE="BitLocker"` |

## 第一次掛載永遠 read-only

```bash
sudo mkdir -p /mnt/win
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 確認對了
ls /mnt/win
# 應該看到：'Program Files'  'Program Files (x86)'  'ProgramData'  Users  Windows ...
```

掛錯了（其實是 Data 不是 OS）會看到完全不同的內容，這時 `umount` 換一個試。

## 處理 Hibernation / Fast Startup

最常見的錯誤：

```
The disk contains an unclean file system (0, 0).
Metadata kept in Windows cache, refused to mount.
Failed to mount '/dev/sda3': Operation not permitted
The NTFS partition is in an unsafe state. Please resume and shutdown
Windows fully (no hibernation or fast restarting), or mount the volume
read-only with the 'ro' mount option.
```

選一：

### 選項 A：唯讀讀就好（救資料時用）

```bash
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
```

可以讀但不能寫。對於只想 rsync 出資料的情境，這樣最安全。

### 選項 B：強制清掉 hibernation state（要寫入時用）

```bash
sudo mount -t ntfs-3g -o remove_hiberfile /dev/sda3 /mnt/win
```

`remove_hiberfile` 會把 `hiberfil.sys` 砍掉。**後果**：使用者上次的 hibernation/fast startup 狀態整個丟失。如果 Windows 之前是「快速啟動」關機而不是真關機，這次掛載完之後，下次回 Windows 會「冷開機」——比較慢但乾淨。

執行前一定要跟使用者確認：「你電腦現在的狀態相當於休眠中，未存的工作會丟失。確定要繼續嗎？」

### 選項 C：在 Windows 端徹底關機

如果使用者還能進 Windows（例如安全模式），叫他跑：

```cmd
shutdown /s /f /t 0
```

或關掉「快速啟動」：控制台 → 電源選項 → 選擇按下電源按鈕的行為 → 變更目前無法使用的設定 → 取消勾選「啟用快速啟動」。

然後重開機進 Linux 救援碟，磁碟就會是 clean 狀態。

## BitLocker 偵測

```bash
sudo blkid /dev/sda3
# /dev/sda3: TYPE="BitLocker"
```

或

```bash
sudo file -s /dev/sda3
# 顯示 -FVE-FS- 或 BitLocker
```

或

```bash
sudo dd if=/dev/sda3 bs=512 count=1 2>/dev/null | hexdump -C | head -2
# 前幾個 byte 看到 "-FVE-FS-" 就是 BitLocker
```

確認是 BitLocker 後**不要繼續硬掛**，跳去 `10-bitlocker.md`。

## 唯讀掛載 EFI 分割區看 boot 設定

```bash
sudo mkdir -p /mnt/efi
sudo mount /dev/sda1 /mnt/efi   # FAT32 不用 ntfs-3g

# 看結構
ls /mnt/efi/EFI/
# 健康的 Windows 系統會看到：
#   Boot/        ← Windows boot files
#   Microsoft/   ← Microsoft Boot Manager
# Linux 進來後可能多：
#   ubuntu/  debian/  GRUB/  等

ls /mnt/efi/EFI/Microsoft/Boot/
# 應該有 bootmgfw.efi, BCD, BCD.LOG*, en-US/, zh-TW/, ...
# 沒有 → bootloader 真的不見了
```

## 掛載 Recovery 分割區

通常你不需要動它，但偶爾要從裡面拉 Winre.wim 出來研究：

```bash
sudo mkdir -p /mnt/recovery
sudo mount -t ntfs-3g -o ro /dev/sda5 /mnt/recovery
ls /mnt/recovery/Recovery/WindowsRE/
# Winre.wim, ReAgent.xml, boot.sdi, ...
```

`Winre.wim` 是 Windows Recovery Environment 的映像檔，內含 sfc/DISM/chkdsk 等工具。Linux 解不開 .wim 但可以用 `wimlib`：

```bash
sudo apt install wimtools
sudo wiminfo /mnt/recovery/Recovery/WindowsRE/Winre.wim
```

不過要實際跑 WinRE 還是要從這個 wim 開機（用 Ventoy 加 winpe 工具）或用 Windows 安裝媒體。

## 處理 Dynamic Disk / Storage Spaces

Windows 的「動態磁碟」或「Storage Spaces」（Microsoft 的 software RAID）在 Linux 端是個麻煩。常見訊息：

```
$ sudo mount -t ntfs-3g /dev/sda3 /mnt/win
NTFS signature is missing.
Failed to mount '/dev/sda3': Invalid argument
```

但 `blkid` 顯示是 `LVM2_member` 或 `LDM_data_partition`。

解法：
- 動態磁碟：用 `ldmtool`（在 Ubuntu repo 中）
  ```bash
  sudo apt install ldmtool
  sudo ldmtool scan
  sudo ldmtool create all
  # 之後 /dev/mapper/ldm_vol_* 就能掛
  ```
- Storage Spaces：Linux 沒有官方支援，最好的辦法是把該系統移回 Windows 環境操作

## 常用掛載組合

```bash
# 救資料（最安全）
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# 要寫入（registry 修改、檔案修改）
sudo mount -t ntfs-3g -o remove_hiberfile,rw /dev/sda3 /mnt/win

# 看 EFI
sudo mount /dev/sda1 /mnt/efi

# uid/gid 比較順手（讓 ntfs 上的檔案看起來像本機使用者擁有）
sudo mount -t ntfs-3g -o ro,uid=$(id -u),gid=$(id -g) /dev/sda3 /mnt/win
```

## 卸載

完成後永遠記得 umount，特別是動完 registry 或檔案後：

```bash
sudo umount /mnt/win
# 卸不掉看誰在用
sudo fuser -vm /mnt/win
sudo lsof /mnt/win
# 確定沒人後再強制
sudo umount -l /mnt/win    # lazy umount
```

`umount` 成功才算真的「寫回去」了。沒卸就直接拔碟或重開——資料會 corrupt。

## 故障排除

### 「Cannot allocate memory」

NTFS 結構毀損嚴重，ntfs-3g 連結構都讀不出來。流程：

1. 立刻 `umount`
2. `sudo ntfsfix /dev/sda3`（會嘗試修小毛病）
3. 還不行→ `08-data-recovery.md` 的 ddrescue 章節，先做映像再說

### 「Invalid argument」

可能是：
- 不是 NTFS（看錯分割區）
- BitLocker
- 動態磁碟
- 分割表有問題（partition 起始/結束 LBA 錯）

依序 `blkid` / `sudo fdisk -l` 確認。

### 掛得起來但讀檔案 I/O error

```
ls: reading directory '/mnt/win/Users': Input/output error
```

`dmesg` 看實際磁碟 I/O 錯誤。幾乎一定是壞磁區。立刻 `umount` 並切到 ddrescue 流程。

```bash
sudo umount /mnt/win
dmesg | tail -50
sudo smartctl -a /dev/sda
```
