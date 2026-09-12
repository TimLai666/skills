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

簽章位於磁區內，不能把表面十六進位片段當成版本分類。結合 `blkid`、分割區位置與 dislocker 的中繼資料判讀。

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

> **TPM-only BitLocker 的特殊狀況**：如果加密時只綁 TPM 沒設密碼，沒有 recovery key 純粹靠 TPM。這種情況**只能回原機開機**，從 Linux 真的解不開。先查帳號、組織與既有備份紀錄，不能假定金鑰一定已保存。

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
sudo dislocker -r -V /dev/sda3 -p -- /mnt/bitlocker
# -p 不帶值，依提示輸入，避免金鑰出現在命令列、shell history 或報告
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
sudo dislocker -r -V /dev/sda3 -u -- /mnt/bitlocker
# 互動式詢問密碼

# 用 .BEK 檔（USB 啟動金鑰，少見）
sudo dislocker -r -V /dev/sda3 -f /path/to/key.bek -- /mnt/bitlocker

# 用 FVEK（Full Volume Encryption Key，從 memory dump 救出來的，超罕見）
sudo dislocker -r -V /dev/sda3 -k /path/to/fvek.bin -- /mnt/bitlocker
```

---

## 4. 在映像副本上修復

資料讀取同時使用 dislocker `-r` 與 NTFS 掛載 `ro`。dislocker 的虛擬 NTFS 寫入會回寫底層 BitLocker 容器；要修復時先依 [08 的映像流程](08-data-recovery.md) 保留原始映像與 mapfile，另建工作副本。

確認工作副本來源、類型與需要修復的項目後，先卸載唯讀檢查時的兩層掛載。以下假設副本是**單一 BitLocker 分割區的原始映像**，可直接交給 dislocker：

```bash
sudo umount /mnt/win
sudo umount /mnt/bitlocker
# 工作副本已依 08 建立；這次允許回寫副本
sudo dislocker -V /mnt/external/bitlocker-work.img -p -- /mnt/bitlocker
sudo mount -t ntfs-3g -o loop,rw /mnt/bitlocker/dislocker-file /mnt/win
# 只執行已選定的修復；完成後依序卸載
sudo umount /mnt/win
sudo umount /mnt/bitlocker
```

若是**整碟原始映像**，先以 `losetup --find --partscan --show` 連接工作副本，從 `lsblk` 確認加密分割區，再把該 `/dev/loopXpY` 傳給 `-V`；最後另行解除 loop 裝置。唯讀檢查原始映像時，losetup 也加 `--read-only`。

遇到休眠或不乾淨狀態造成拒寫，接 [03 掛載排錯](03-mount-windows.md) 判斷；不為了掛載成功直接丟棄休眠資料。副本上修改成功不代表原機已修好，需交代結果要如何使用或還原；還原回原裝置須另確認來源、目標及備份。

---

## 5. 解開後接什麼

BitLocker 解開只是把加密的 NTFS 變成可讀的 NTFS。後續的修復一樣走原本流程：

- 檔案系統有問題 → 走 [05-filesystem-repair.md](05-filesystem-repair.md)，先卸載 NTFS，再對可寫工作副本的 `dislocker-file` 建立 loop 裝置，確認它未掛載後處理；不能對加密的原始裝置直接執行 NTFS 工具
- 改 registry → 走 [06-registry-edit.md](06-registry-edit.md)
- 救資料 → 走 [08-data-recovery.md](08-data-recovery.md)
- 修 boot → 走 [04-boot-repair.md](04-boot-repair.md)（EFI 分割區通常未加密，仍須確認所屬 Windows 磁碟並備份）

---

## 6. 常見錯誤

### `dislocker: cannot find BitLocker metadata`
- 確認分割區真的是 BitLocker（`blkid`）
- 整碟映像先依分割表找對分割區；`-O` 是以位元組表示的實際分割區偏移，只在已確認偏移時使用，不套固定數字
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
- 依實際 FUSE 錯誤檢查權限與套件版本；沒有使用 `allow_other` 時不必為此修改全域設定

---

## 7. 資料救援的交接

解開並唯讀掛載後，依 [08 的 rsync 與驗證步驟](08-data-recovery.md) 選取需要的資料。磁碟異常時先映像再解密；只需要資料時，驗證備份後即可停止。結束時先卸載 `/mnt/win`，再卸載 `/mnt/bitlocker`，最後解除本案建立的 loop 裝置。

---

## 8. 提醒使用者

- 修復後確認 BitLocker 保護狀態與復原金鑰備份
- Recovery key 存放在能於原機故障時取得的安全位置
- 確認這台裝置的金鑰是否已備份至個人帳號或組織，不把使用帳號登入視為備份成功證據
- 公司電腦不要自己關 BitLocker，會違反公司政策

參數依據：[dislocker 官方手冊](https://github.com/Aorimn/dislocker/blob/master/man/linux/dislocker-fuse.1)。
