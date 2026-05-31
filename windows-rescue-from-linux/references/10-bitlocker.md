# 10 · BitLocker 加密磁碟的處理

> **核心觀念**：BitLocker 是 Windows 的全碟加密，從 Linux 看到的會是一團亂碼。在 Linux 端**沒有金鑰就完全無法存取**，這不是 bug，是設計。先弄到金鑰，再用 `dislocker` 解開來掛載。

---

## 1. 先確認是不是 BitLocker

```bash
# 方法 1：blkid
sudo blkid /dev/sda3
# 看到 TYPE="BitLocker" 就是了

# 方法 2：file -s
sudo file -s /dev/sda3
# 開頭會有 "-FVE-FS-" 字串

# 方法 3：直接看開頭 bytes
sudo dd if=/dev/sda3 bs=512 count=1 2>/dev/null | hexdump -C | head -2
# BitLocker 簽章：-FVE-FS- (2D 46 56 45 2D 46 53 2D)
```

| 開頭簽章 | 加密狀態 |
|---|---|
| `EB 52 90 4E 54 46 53` | 一般 NTFS（沒加密） |
| `2D 46 56 45 2D 46 53 2D` | BitLocker（傳統） |
| `EB 58 90 2D 46 56 45 2D` | BitLocker To Go / Win8+ |

---

## 2. 取得 Recovery Key 的四條路徑

**沒有金鑰 = 沒辦法解。不要白費力氣去試暴力破解，48 位數字組合穩穩破不完。**

| 來源 | 步驟 |
|---|---|
| **Microsoft 帳號** | 在另一台電腦或手機開 https://account.microsoft.com/devices/recoverykey 用同一個 MS 帳號登入 |
| **公司 AD/Entra** | 公司電腦多半同步到 AD，找 IT 取得；或登入 https://myaccount.microsoft.com 看 Devices |
| **列印備份** | 啟用時 Windows 強制要備份，可能存在 USB / 雲端 / 印出來的紙上 |
| **網域 MBAM** | 企業環境的 BitLocker 管理伺服器，找 IT |

**Recovery key 長相**：`123456-234567-345678-456789-567890-678901-789012-890123`（8 組 6 位數字，總共 48 位）

> **TPM-only BitLocker 的特殊狀況**：如果加密時只綁 TPM 沒設密碼，沒有 recovery key 純粹靠 TPM。這種情況**只能回原機開機**，從 Linux 真的解不開。Windows 啟用 BitLocker 時其實還是會強制備份 recovery key，使用者只是忘記在哪。

---

## 3. dislocker 解密掛載

### 安裝

```bash
sudo apt install dislocker fuse3
```

### 標準流程

```bash
# 1. 建立兩個掛載點
sudo mkdir -p /mnt/bitlocker /mnt/win

# 2. 用 recovery key 解開（推薦做法，最不會出包）
sudo dislocker -V /dev/sda3 \
    -p123456-234567-345678-456789-567890-678901-789012-890123 \
    -- /mnt/bitlocker
# 注意：-p 後面**直接接 recovery key 不要加空格**
# 解開後 /mnt/bitlocker/ 會出現 dislocker-file（這是虛擬的 NTFS 映像）

# 3. 把 dislocker-file 當 loopback 掛起來
sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file /mnt/win

# 4. 確認
ls /mnt/win
# 應該看到 Windows/ Users/ Program Files/ 等資料夾
```

### 其它解鎖選項

```bash
# 用 User Password（使用者每次開機輸入的密碼，不是登入密碼）
sudo dislocker -V /dev/sda3 -u -- /mnt/bitlocker
# 互動式詢問密碼

# 用 .BEK 檔（USB 啟動金鑰，少見）
sudo dislocker -V /dev/sda3 -f /path/to/key.bek -- /mnt/bitlocker

# 用 FVEK（Full Volume Encryption Key，從 memory dump 救出來的，超罕見）
sudo dislocker -V /dev/sda3 -K /path/to/fvek.bin -- /mnt/bitlocker
```

---

## 4. 寫入模式（高風險）

預設 dislocker 是讀寫，但**寫入 BitLocker 容器很容易出包**。如果只是要救資料，永遠用 `ro`：

```bash
sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file /mnt/win
```

如果非寫不可（例如要修 registry、要 chntpw）：

```bash
# 1. 先把整顆 BitLocker 區段做 ddrescue 映像（強烈建議）
sudo ddrescue -f -n /dev/sda3 /mnt/external/bitlocker.img /mnt/external/bitlocker.log

# 2. 在映像上跑 dislocker
sudo losetup -fP --show /mnt/external/bitlocker.img
# 假設回 /dev/loop0
sudo dislocker -V /dev/loop0 -p<key> -- /mnt/bitlocker
sudo mount -t ntfs-3g -o loop,rw,remove_hiberfile /mnt/bitlocker/dislocker-file /mnt/win

# 3. 改完之後完全卸載
sudo umount /mnt/win
sudo umount /mnt/bitlocker
sudo losetup -d /dev/loop0
```

**為什麼這麼麻煩？**：BitLocker 寫入時若中斷（拔線、藍屏、kernel panic），整個磁碟可能直接 unrecoverable。在映像上操作壞了大不了重來。

---

## 5. 解開後接什麼

BitLocker 解開只是把加密的 NTFS 變成可讀的 NTFS。後續的修復一樣走原本流程：

- 檔案系統有問題 → 走 [05-filesystem-repair.md](05-filesystem-repair.md)，但 `ntfsfix` 跑在 `/mnt/bitlocker/dislocker-file` 這個 loopback 上而不是真實裝置
- 改 registry → 走 [06-registry-edit.md](06-registry-edit.md)
- 救資料 → 走 [08-data-recovery.md](08-data-recovery.md)
- 修 boot → 走 [04-boot-repair.md](04-boot-repair.md)（但 EFI 分割區通常沒加密，可以直接動）

---

## 6. 常見錯誤

### `dislocker: cannot find BitLocker metadata`
- 確認分割區真的是 BitLocker（`blkid`）
- BitLocker To Go（USB 隨身碟）用 `dislocker-fuse` 或加 `-O 65536` 偏移
- 磁碟有實體損壞 → 先 ddrescue 出來再說

### `Cannot mount: invalid argument`
- 確定 dislocker-file 跑出來了（`ls /mnt/bitlocker/`）
- 試 `-o loop,ro` 而不是只 `-o ro`
- 試 `mount -t ntfs-3g` 明確指定檔案系統

### `Cannot decrypt: wrong key`
- 重新確認 recovery key 沒打錯（48 位數字，8 組 6 位）
- key 是給這顆碟的，不是其他電腦的（一個 MS 帳號可能有多顆 BitLocker 碟）
- 拿到的可能是「User Password」不是「Recovery Key」，要用 `-u` 不是 `-p`

### `cannot mount file system; Operation not permitted`
- 確認你是 root（`sudo`）
- FUSE 沒裝起來：`sudo apt install fuse3`
- 確認 /etc/fuse.conf 有 `user_allow_other`（多半預設就有）

---

## 7. 完整流程範例：救一台 BitLocker 加密的當機 Windows

```bash
# 場景：使用者公司電腦藍屏起不來，BitLocker 開著，IT 給了 recovery key

# 1. 識別磁碟
sudo lsblk -f
# /dev/nvme0n1p1 vfat       EFI
# /dev/nvme0n1p2            (Microsoft reserved)
# /dev/nvme0n1p3 BitLocker  (Windows)
# /dev/nvme0n1p4 ntfs       Recovery

# 2. 先做完整 image（救命的時候 5 分鐘也要花）
sudo ddrescue -f -n /dev/nvme0n1p3 /mnt/external/win-bitlocker.img \
    /mnt/external/win-bitlocker.log

# 3. 解開
sudo mkdir -p /mnt/bitlocker /mnt/win
sudo losetup -fP --show /mnt/external/win-bitlocker.img
# 假設 /dev/loop0
sudo dislocker -V /dev/loop0 \
    -p<48-digit-recovery-key> -- /mnt/bitlocker

# 4. 唯讀掛載先確認看得到東西
sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file /mnt/win
ls /mnt/win/Users
# OK，看到使用者資料夾了

# 5. 救資料（不修系統的話到這就夠了）
sudo rsync -aHv --info=progress2 \
    /mnt/win/Users/Alice/Documents/ \
    /mnt/external/Alice-Documents/

# 6. 如果要修系統，重掛 rw
sudo umount /mnt/win
sudo mount -t ntfs-3g -o loop,rw,remove_hiberfile \
    /mnt/bitlocker/dislocker-file /mnt/win

# 7. 收尾
sudo umount /mnt/win
sudo umount /mnt/bitlocker
sudo losetup -d /dev/loop0
```

---

## 8. 提醒使用者

- BitLocker 不是壞東西，**沒它你資料早被拿走了**。修好後鼓勵繼續開著
- Recovery key 一定要備份到**手機 + 雲端 + 列印**至少兩種以上
- 如果用 Microsoft 帳號登入 Windows，BitLocker 預設會自動上傳金鑰到該帳號，這是預設行為不是被盜
- 公司電腦不要自己關 BitLocker，會違反公司政策
