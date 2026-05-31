# 04 — 開機修復（UEFI / BCD / MBR / EFI）

Windows 開不了機最常見的原因之一是 bootloader 損壞。這份涵蓋：

- UEFI 開機項損壞 / 不見
- BCD（Boot Configuration Data）損壞
- EFI 分割區檔案損壞
- 舊的 Legacy BIOS + MBR
- 雙系統（裝完 Linux 後 Windows 不見了 / 反之）

## 開機階段釐清

Windows 開機鏈：

```
電源 → POST → BIOS/UEFI 找 boot device
              ↓
        UEFI: 讀 ESP → /EFI/Microsoft/Boot/bootmgfw.efi
        Legacy: 讀 MBR → boot sector → bootmgr
              ↓
        bootmgr 讀 BCD（在 EFI 分割區或系統碟的 \Boot\BCD）
              ↓
        BCD 指向 winload.efi（或 winload.exe）
              ↓
        winload 載入 kernel（ntoskrnl.exe）+ HAL + boot driver
              ↓
        Windows 啟動
```

問題出在哪一段，修法不同。

## 先診斷在 UEFI 還是 Legacy

```bash
# 在 Linux 救援碟內
[ -d /sys/firmware/efi ] && echo "UEFI mode" || echo "Legacy BIOS mode"

# 從磁碟結構判斷 Windows 是用哪個
sudo fdisk -l /dev/sda
# GPT + 含 EFI System Partition → UEFI
# MBR + 含 active 分割區 → Legacy
```

如果 Linux 是 UEFI 開機但 Windows 之前是 Legacy 開機（或反之）——這也會造成「看不到 Windows」。BIOS 設定改回對應的模式才會看到。

## UEFI 路徑：用 efibootmgr 修

### 看現有開機項

```bash
sudo efibootmgr -v
```

健康的範例：

```
BootCurrent: 0001
Timeout: 0 seconds
BootOrder: 0000,0001,0002
Boot0000* Windows Boot Manager    HD(1,GPT,xxx,0x800,0x32000)/File(\EFI\Microsoft\Boot\bootmgfw.efi)
Boot0001* ubuntu                  HD(1,GPT,xxx,0x800,0x32000)/File(\EFI\ubuntu\shimx64.efi)
Boot0002* UEFI: USB...
```

問題狀況：

- **沒有 Windows Boot Manager 那行**：UEFI 不認得 Windows 開機項
- **有但 BootOrder 把它排在不能開機的項後面**：開機進不了 Windows
- **有但 File() 後面的路徑壞掉**：指錯位置

### 修復場景 1：Windows Boot Manager 項目不見

先確認 EFI 分割區裡的檔案還在：

```bash
sudo mkdir -p /mnt/efi
sudo mount /dev/sda1 /mnt/efi    # sda1 = ESP
ls /mnt/efi/EFI/Microsoft/Boot/bootmgfw.efi
# 應該要有
```

檔案還在但 UEFI 不認得它——重新加：

```bash
# 找出 ESP 的磁碟和分割區編號
# 假設 ESP 是 /dev/sda1，下面參數要對應
sudo efibootmgr -c -d /dev/sda -p 1 \
    -L "Windows Boot Manager" \
    -l "\EFI\Microsoft\Boot\bootmgfw.efi"

# 確認加進去了
sudo efibootmgr -v
```

`-c` create, `-d` disk, `-p` partition number, `-L` label, `-l` loader path（注意是反斜線，UEFI 規格）。

### 修復場景 2：BootOrder 順序不對

```bash
# 把 Windows Boot Manager 排第一
sudo efibootmgr -o 0000,0001,0002    # 數字換成實際的
```

### 修復場景 3：EFI 分割區裡 bootmgfw.efi 不見了

```bash
ls /mnt/efi/EFI/Microsoft/Boot/
# 結果：空的，或只有 BCD 沒有 bootmgfw.efi
```

從 Windows 系統碟的備份位置複製：

```bash
# 系統碟也要掛起來
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win

# Windows 安裝後會在這裡留一份
ls /mnt/win/Windows/Boot/EFI/
# bootmgfw.efi, bootmgr.efi, memtest.efi, ...

# 複製回 EFI 分割區（需要可寫掛載）
sudo umount /mnt/efi
sudo mount -o rw /dev/sda1 /mnt/efi
sudo mkdir -p /mnt/efi/EFI/Microsoft/Boot/
sudo cp /mnt/win/Windows/Boot/EFI/bootmgfw.efi /mnt/efi/EFI/Microsoft/Boot/
sudo cp /mnt/win/Windows/Boot/EFI/bootmgr.efi /mnt/efi/EFI/Microsoft/Boot/
sudo cp -r /mnt/win/Windows/Boot/EFI/* /mnt/efi/EFI/Microsoft/Boot/
sudo cp -r /mnt/win/Windows/Boot/Fonts /mnt/efi/EFI/Microsoft/Boot/
sudo cp -r /mnt/win/Windows/Boot/Resources /mnt/efi/EFI/Microsoft/Boot/
```

### 修復場景 4：BCD 不見 / 損壞

BCD 在 `/mnt/efi/EFI/Microsoft/Boot/BCD`。它是一個 registry hive 格式。

Linux 上沒辦法像 Windows `bcdedit` 那樣方便地重建 BCD。可以做的：

**A. 用 hivex 看 BCD 內容**

```bash
sudo apt install libhivex-bin
sudo hivexsh /mnt/efi/EFI/Microsoft/Boot/BCD

# 在 hivexsh 內：
> ls
> cd Objects
> ls
> exit
```

至少能看 BCD 有沒有結構毀掉。

**B. 從備份還原**

如果之前 cp 出過 BCD.bak：

```bash
sudo cp /backup/BCD.bak /mnt/efi/EFI/Microsoft/Boot/BCD
```

**C. 重建 BCD（需要 Windows 安裝媒體）**

最可靠的辦法。Linux 端做完前置（檢查 EFI 結構），告訴使用者：

> 拿 Windows 11/10 安裝隨身碟開機 → 修復電腦 → 疑難排解 → 命令提示字元，跑：
> ```cmd
> bootrec /scanos
> bootrec /rebuildbcd
> bcdboot C:\Windows /s X: /f UEFI
> ```
> （X: 是 EFI 分割區掛載字母，用 diskpart 給）

詳見 `13-when-linux-cannot-fix.md`。

**D. Linux 端最小重建**

如果連 Windows 安裝媒體都沒有，可以試這個 hack：用 `chntpw` 或 `hivexsh` 從一個健康的 Windows 抓 BCD 範本，改成這台機器的路徑——不建議，太容易出錯。

## Legacy BIOS / MBR 路徑

老電腦或刻意設 Legacy 模式的：

```bash
# 看 MBR
sudo dd if=/dev/sda bs=512 count=1 2>/dev/null | xxd | tail
# 最後兩個 byte 要是 55 aa
```

### MBR 損壞修復

```bash
# 確認 ms-sys 工具有裝
sudo apt install mbr ms-sys

# Windows 7 / 8 / 10 / 11 用通用 MBR
sudo ms-sys -m /dev/sda

# 或更指定
sudo ms-sys --mbr7 /dev/sda    # Windows 7+
```

但要注意：純寫 MBR 不會復活 BCD。如果 BCD 也掛了，要連 BCD 一起救（同 UEFI 路徑的 BCD 章節）。

### Active 分割區旗標

Legacy BIOS 找的是 MBR 上「active」那個分割區。如果這個 flag 不見了：

```bash
sudo fdisk /dev/sda
# 進到互動界面
# 按 a 切換 active flag
# 數字選 Windows 系統分割區
# 按 w 寫入
```

或用 sfdisk：

```bash
# 看當前
sudo sfdisk -A /dev/sda
# 設成 sda1 是 active
sudo sfdisk -A /dev/sda 1
```

## 雙系統修復

### 場景：裝完 Linux 後 Windows 不見了

通常是 GRUB 沒偵測到 Windows。

```bash
sudo apt install os-prober grub-common
sudo os-prober
# 應該回 /dev/sda1:Windows Boot Manager:Windows:efi 或類似
```

如果 os-prober 找到了但 GRUB menu 沒顯示，編輯 `/etc/default/grub`：

```bash
sudo nano /etc/default/grub
# 確認有：
#   GRUB_DISABLE_OS_PROBER=false

sudo update-grub
```

### 場景：裝完 Windows 後 Linux 不見了（Windows 把 ESP 的東西蓋掉）

Windows 安裝會把 EFI 中其他項目都關掉，只留自己。Linux 救援碟開機後：

```bash
# 確認 ubuntu 的 EFI 還在
ls /mnt/efi/EFI/ubuntu/
# 應該有 shimx64.efi 或 grubx64.efi

# 重新註冊到 UEFI
sudo efibootmgr -c -d /dev/sda -p 1 \
    -L "ubuntu" \
    -l "\EFI\ubuntu\shimx64.efi"

# 把它排前面
sudo efibootmgr -o 0002,0000,0001    # 看實際編號
```

如果 ubuntu 的 EFI 也被刪了，要從 ubuntu 系統 chroot 重灌 grub：

```bash
sudo mount /dev/sda5 /mnt/ubuntu    # ubuntu 根目錄
sudo mount --bind /dev /mnt/ubuntu/dev
sudo mount --bind /proc /mnt/ubuntu/proc
sudo mount --bind /sys /mnt/ubuntu/sys
sudo mount /dev/sda1 /mnt/ubuntu/boot/efi
sudo chroot /mnt/ubuntu

# chroot 內
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu
update-grub
exit
```

## 完整修復流程範例

「Windows 11 開機顯示 BOOTMGR is missing」：

```bash
# 1. 識別磁碟
sudo blkid
# 假設 /dev/sda1 是 ESP, /dev/sda3 是 Windows

# 2. SMART 確認硬體 OK
sudo smartctl -H /dev/sda

# 3. 唯讀掛載確認資料還在
sudo mkdir -p /mnt/win /mnt/efi
sudo mount -t ntfs-3g -o ro /dev/sda3 /mnt/win
sudo mount /dev/sda1 /mnt/efi
ls /mnt/win/Users/

# 4. 備份使用者資料（保險）
sudo rsync -avh --info=progress2 /mnt/win/Users/USERNAME/ /media/external/backup/

# 5. 檢查 EFI 結構
ls /mnt/efi/EFI/Microsoft/Boot/
# 缺 bootmgfw.efi → 場景 3

# 6. 卸載 EFI，可寫重掛
sudo umount /mnt/efi
sudo mount -o rw /dev/sda1 /mnt/efi
sudo mkdir -p /mnt/efi/EFI/Microsoft/Boot/
sudo cp /mnt/win/Windows/Boot/EFI/bootmgfw.efi /mnt/efi/EFI/Microsoft/Boot/
sudo cp -r /mnt/win/Windows/Boot/EFI/* /mnt/efi/EFI/Microsoft/Boot/
sudo cp -r /mnt/win/Windows/Boot/Fonts /mnt/efi/EFI/Microsoft/Boot/

# 7. 補 UEFI 開機項
sudo efibootmgr -c -d /dev/sda -p 1 \
    -L "Windows Boot Manager" \
    -l "\EFI\Microsoft\Boot\bootmgfw.efi"

# 8. 同步 + 卸載
sudo sync
sudo umount /mnt/efi /mnt/win

# 9. 跟使用者說可以重開機試
```

## 常見錯誤

### 「modprobe: ERROR: could not insert 'efivars'」

Linux 是 Legacy 模式開機進來的，efibootmgr 跑不了。重開機進 BIOS 把 USB 開機改成 UEFI 模式。

### 「efibootmgr: cannot open /sys/firmware/efi/...」

同上。確認 `/sys/firmware/efi` 存在。

### 改完還是不開

- BIOS 裡的 Secure Boot：開啟狀態會檢查 signed bootloader。Windows 系統用 signed，沒問題。但如果你動了什麼，可能要暫時關 Secure Boot 測。
- Fast Boot：BIOS 的 Fast Boot 會跳過完整初始化，可能跳過你的 USB。關掉。
- CSM (Compatibility Support Module)：開啟會讓 UEFI 模擬 BIOS。Windows 是 UEFI 裝的話 CSM 要關。

### `efibootmgr -c` 出現「Could not create variable」

NVRAM 空間不足或主機板的怪毛病。可以先 `efibootmgr -B -b XXXX` 刪掉沒用的舊項目，騰出空間再 -c。
