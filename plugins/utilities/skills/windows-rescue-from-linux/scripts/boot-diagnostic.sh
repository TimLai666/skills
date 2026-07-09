#!/usr/bin/env bash
# boot-diagnostic.sh
# 收集 Windows 開機相關資訊：EFI 分割區內容、BCD、開機 driver、相關事件日誌
# 用法：sudo bash boot-diagnostic.sh [windows_mount] [efi_mount]
# 範例：sudo bash boot-diagnostic.sh /mnt/win /mnt/efi

set -u

if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

WIN_MNT="${1:-/mnt/win}"
EFI_MNT="${2:-/mnt/efi}"

REPORT_DIR="/tmp/boot-diagnostic-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$REPORT_DIR"
REPORT="$REPORT_DIR/report.md"

# 開頭
{
    echo "# Windows 開機問題診斷報告"
    echo ""
    echo "生成時間：$(date)"
    echo ""
} > "$REPORT"

echo -e "${BOLD}==== Windows 開機問題診斷 ====${NC}"
echo "報告位置：$REPORT_DIR"
echo ""

# ============================================
# 1. UEFI vs Legacy
# ============================================
echo -e "${BOLD}[1] 韌體模式檢查${NC}"
{
    echo "## 1. 韌體模式"
    echo ""
    if [[ -d /sys/firmware/efi ]]; then
        echo "目前 Linux 開機是 **UEFI** 模式"
        echo ""
        echo "**這顆 Live USB 是用 UEFI 開機**，但要修的 Windows 系統可能是 UEFI 也可能是 Legacy，"
        echo "後面看分割表會知道。"
    else
        echo "目前 Linux 開機是 **Legacy/BIOS** 模式"
        echo ""
        echo "如果要修的 Windows 是 UEFI 系統，efibootmgr 可能用不了，建議：" 
        echo "1. 重開機，BIOS 切到 UEFI 模式再開 Live USB"
        echo "2. 或從 Windows 安裝媒體進 WinRE 處理"
    fi
    echo ""
} | tee -a "$REPORT"
echo ""

# ============================================
# 2. 分割表類型
# ============================================
echo -e "${BOLD}[2] 偵測 Windows 系統碟與分割表${NC}"
{
    echo "## 2. 磁碟分割表"
    echo ""
    echo '```'
    fdisk -l 2>/dev/null | grep -E "^Disk /dev/|^Disklabel type:|^Device " | head -40
    echo '```'
    echo ""
    echo "**Disklabel type** = `gpt` 代表 UEFI 系統；`dos` 代表 Legacy/MBR 系統。"
    echo ""
} | tee -a "$REPORT"
echo ""

# 找 EFI 分割區
EFI_PART=""
for P in $(lsblk -nrpo NAME,FSTYPE | awk '$2=="vfat" {print $1}'); do
    TMP=$(mktemp -d)
    if mount -t vfat -o ro "$P" "$TMP" 2>/dev/null; then
        if [[ -d "$TMP/EFI" ]]; then
            EFI_PART="$P"
            umount "$TMP"
            rmdir "$TMP"
            break
        fi
        umount "$TMP"
    fi
    rmdir "$TMP"
done

# ============================================
# 3. efibootmgr 輸出
# ============================================
echo -e "${BOLD}[3] UEFI 開機項清單${NC}"
{
    echo "## 3. UEFI 開機項（efibootmgr）"
    echo ""
    if command -v efibootmgr >/dev/null && [[ -d /sys/firmware/efi/efivars ]]; then
        echo '```'
        efibootmgr -v 2>&1 || echo "efibootmgr 執行失敗"
        echo '```'
        echo ""
        # 解析
        if efibootmgr -v 2>/dev/null | grep -qi "Windows Boot Manager"; then
            echo "✓ 找到 **Windows Boot Manager** 項目"
        else
            echo "✗ **沒找到 Windows Boot Manager！** 這就是開不了機的原因之一。"
            echo ""
            echo "修法（要先確認 EFI 分割區與 Windows 系統碟）："
            echo '```bash'
            echo "# 1. 找到 bootmgfw.efi"
            echo "find /mnt/efi -iname bootmgfw.efi"
            echo ""
            echo "# 2. 註冊回去（假設 EFI 在 /dev/sda1）"
            echo "sudo efibootmgr -c -d /dev/sda -p 1 \\"
            echo "    -L 'Windows Boot Manager' \\"
            echo "    -l '\\EFI\\Microsoft\\Boot\\bootmgfw.efi'"
            echo '```'
        fi
        echo ""

        # BootOrder
        BOOTORDER=$(efibootmgr 2>/dev/null | grep BootOrder | awk '{print $2}')
        if [[ -n "$BOOTORDER" ]]; then
            echo "**目前 BootOrder：** $BOOTORDER"
        fi
    else
        echo "efibootmgr 不能用（沒裝或不是 UEFI 開機）"
    fi
    echo ""
} | tee -a "$REPORT" >/dev/null
echo ""

# ============================================
# 4. EFI 分割區內容
# ============================================
echo -e "${BOLD}[4] EFI 分割區內容${NC}"
{
    echo "## 4. EFI 分割區內容"
    echo ""

    if [[ -z "$EFI_PART" ]] && [[ ! -d "$EFI_MNT/EFI" ]]; then
        # 試掛 EFI_MNT
        if [[ -n "$EFI_PART" ]]; then
            mkdir -p "$EFI_MNT"
            mount -t vfat -o ro "$EFI_PART" "$EFI_MNT" 2>/dev/null && MOUNTED_EFI=1
        fi
    fi

    if [[ -d "$EFI_MNT/EFI" ]]; then
        echo "EFI 分割區掛載於：$EFI_MNT"
        echo ""
        echo '```'
        tree -L 3 "$EFI_MNT/EFI" 2>/dev/null || find "$EFI_MNT/EFI" -maxdepth 3 -type d
        echo '```'
        echo ""

        # 重要檔案存在性檢查
        echo "### 關鍵檔案檢查"
        echo ""
        for F in \
            "$EFI_MNT/EFI/Microsoft/Boot/bootmgfw.efi" \
            "$EFI_MNT/EFI/Microsoft/Boot/BCD" \
            "$EFI_MNT/EFI/Boot/bootx64.efi"
        do
            if [[ -f "$F" ]]; then
                SIZE=$(stat -c%s "$F")
                echo "✓ \`$F\` ($SIZE bytes)"
            else
                echo "✗ **\`$F\` 缺失**"
            fi
        done
        echo ""
    elif [[ -n "$EFI_PART" ]]; then
        echo "找到 EFI 分割區 $EFI_PART，但沒掛起來。"
        echo ""
        echo "掛載指令："
        echo '```bash'
        echo "sudo mkdir -p $EFI_MNT"
        echo "sudo mount -t vfat -o ro $EFI_PART $EFI_MNT"
        echo '```'
    else
        echo "沒偵測到 EFI 分割區 —— 可能是 Legacy/MBR 系統。"
    fi
    echo ""
} | tee -a "$REPORT" >/dev/null
echo ""

# ============================================
# 5. Windows 系統碟內容
# ============================================
echo -e "${BOLD}[5] Windows 系統碟檢查${NC}"
{
    echo "## 5. Windows 系統碟"
    echo ""

    if ! mountpoint -q "$WIN_MNT" 2>/dev/null; then
        echo "⚠ \`$WIN_MNT\` 沒掛載。請先用 mount-windows-safe.sh 掛上去再跑。"
        echo ""
    elif [[ ! -d "$WIN_MNT/Windows" ]]; then
        echo "⚠ \`$WIN_MNT\` 看不到 Windows 資料夾。"
        echo ""
    else
        echo "Windows 系統碟掛載於：\`$WIN_MNT\`"
        echo ""

        # 關鍵開機檔案
        echo "### 核心開機檔案"
        echo ""
        for F in \
            "Windows/System32/winload.efi" \
            "Windows/System32/winload.exe" \
            "Windows/Boot/EFI/bootmgfw.efi" \
            "Windows/Boot/PCAT/bootmgr" \
            "Windows/System32/config/SYSTEM" \
            "Windows/System32/config/SOFTWARE" \
            "Windows/System32/drivers"
        do
            P="$WIN_MNT/$F"
            if [[ -e "$P" ]]; then
                if [[ -d "$P" ]]; then
                    COUNT=$(ls "$P" 2>/dev/null | wc -l)
                    echo "✓ \`$F\` ($COUNT 個項目)"
                else
                    SIZE=$(stat -c%s "$P")
                    echo "✓ \`$F\` ($SIZE bytes)"
                fi
            else
                echo "✗ **\`$F\` 缺失**"
            fi
        done
        echo ""

        # 上次啟動時間
        if [[ -d "$WIN_MNT/Windows/Prefetch" ]]; then
            LAST_BOOT=$(stat -c%y "$WIN_MNT/Windows/Prefetch/NTOSBOOT-B00DFAAD.pf" 2>/dev/null | cut -d. -f1)
            if [[ -n "$LAST_BOOT" ]]; then
                echo "### 上次成功開機時間"
                echo ""
                echo "**$LAST_BOOT**"
                echo ""
                echo "（從 \`Prefetch/NTOSBOOT.pf\` 的 mtime 推算）"
                echo ""
            fi
        fi

        # Hibernation
        if [[ -f "$WIN_MNT/hiberfil.sys" ]]; then
            HSIZE=$(stat -c%s "$WIN_MNT/hiberfil.sys")
            if [[ "$HSIZE" -gt 1048576 ]]; then
                HSIZE_HUMAN=$(numfmt --to=iec --suffix=B "$HSIZE")
                echo "### Hibernation 狀態"
                echo ""
                echo "⚠ \`hiberfil.sys\` 存在（$HSIZE_HUMAN）—— 系統處於 hibernation 或 Fast Startup 狀態"
                echo ""
                echo "rw 掛載時要加 \`remove_hiberfile\` 參數。"
                echo ""
            fi
        fi

        # pending.xml
        if [[ -f "$WIN_MNT/Windows/WinSxS/pending.xml" ]]; then
            PSIZE=$(stat -c%s "$WIN_MNT/Windows/WinSxS/pending.xml")
            echo "### ⚠ pending.xml 存在"
            echo ""
            echo "\`Windows/WinSxS/pending.xml\` ($PSIZE bytes) —— Windows 卡在 update 中"
            echo ""
            echo "如果開機卡「Working on updates / 正在處理更新」，這就是原因。處理："
            echo '```bash'
            echo "sudo mv $WIN_MNT/Windows/WinSxS/pending.xml \\"
            echo "        $WIN_MNT/Windows/WinSxS/pending.xml.bak"
            echo '```'
            echo "詳見 references/11-driver-and-update-issues.md"
            echo ""
        fi
    fi
} | tee -a "$REPORT" >/dev/null
echo ""

# ============================================
# 6. 開機相關 driver（從 SYSTEM hive）
# ============================================
echo -e "${BOLD}[6] 開機 driver 與服務狀態${NC}"
{
    echo "## 6. 開機關鍵 driver"
    echo ""

    if [[ -f "$WIN_MNT/Windows/System32/config/SYSTEM" ]]; then
        # 找出哪個是 Current ControlSet
        CURRENT=$(hivexsh "$WIN_MNT/Windows/System32/config/SYSTEM" <<'EOF' 2>/dev/null
cd Select
lsval
EOF
)
        echo '```'
        echo "$CURRENT" | head -10
        echo '```'
        echo ""

        echo "### Start=0 (boot driver) 的服務"
        echo ""
        echo "這些 driver 在 Windows 啟動最早期 load。任何一個壞了都會 BSOD。"
        echo ""

        # 暫存腳本
        TMPCMD=$(mktemp)
        cat > "$TMPCMD" <<'EOSH'
cd ControlSet001\Services
ls
EOSH

        # 取得所有 services
        SVC_LIST=$(hivexsh "$WIN_MNT/Windows/System32/config/SYSTEM" < "$TMPCMD" 2>/dev/null | tail -n +2)
        rm "$TMPCMD"

        echo '```'
        # 對每個 service 查 Start value
        BOOT_DRIVERS=()
        for SVC in $SVC_LIST; do
            START=$(hivexsh "$WIN_MNT/Windows/System32/config/SYSTEM" <<EOF 2>/dev/null | grep -i "^Start" | head -1
cd ControlSet001\\Services\\$SVC
lsval
EOF
)
            if echo "$START" | grep -q "dword:0x0\b\|dword:0x00000000"; then
                BOOT_DRIVERS+=("$SVC")
            fi
        done

        printf '  %s\n' "${BOOT_DRIVERS[@]}" 2>/dev/null | head -30 || echo "(取不到清單)"
        echo '```'
        echo ""

        echo "如果系統開機卡在 logo 或 BSOD INACCESSIBLE_BOOT_DEVICE，"
        echo "通常是其中某個 boot driver（特別是儲存控制器類）出問題。"
        echo ""
        echo "處理方式見 references/11-driver-and-update-issues.md"
        echo ""
    else
        echo "找不到 SYSTEM hive。"
        echo ""
    fi
} | tee -a "$REPORT" >/dev/null
echo ""

# ============================================
# 7. 事件日誌（最近的開機失敗）
# ============================================
echo -e "${BOLD}[7] Windows 事件日誌（最近 BSOD / 開機失敗）${NC}"
{
    echo "## 7. 最近的 BSOD / 開機失敗事件"
    echo ""

    if command -v python3 >/dev/null && python3 -c "import Evtx" 2>/dev/null; then
        EVTX="$WIN_MNT/Windows/System32/winevt/Logs/System.evtx"
        if [[ -f "$EVTX" ]]; then
            echo "從 System.evtx 撈出最近的關鍵事件（Event ID 41 / 1001 / 6008 / 219）..."
            echo ""
            echo '```'
            # 撈關鍵 ID
            python3 -m Evtx.Evtx "$EVTX" 2>/dev/null | \
                grep -B 2 -A 10 -E "EventID.*>(41|1001|6008|219|7000|7026)<" | \
                tail -150 | head -100 || echo "(沒抓到關鍵事件)"
            echo '```'
            echo ""
            echo "**事件 ID 解讀：**"
            echo "- 41: kernel power（不正常重開機，例如斷電或藍屏）"
            echo "- 1001: BugCheck（BSOD，裡面會有 STOP code 例如 0x0000007E）"
            echo "- 6008: unexpected shutdown"
            echo "- 219: driver load failure（含失敗 driver 名稱）"
            echo "- 7000/7026: 服務啟動失敗（多半 driver）"
            echo ""
        else
            echo "找不到 System.evtx"
            echo ""
        fi
    else
        echo "python3 + python-evtx 沒裝。安裝後重跑："
        echo '```bash'
        echo "sudo apt install python3-evtx"
        echo '```'
        echo ""
    fi

    # Minidump 清單
    if [[ -d "$WIN_MNT/Windows/Minidump" ]]; then
        DUMPS=$(ls "$WIN_MNT/Windows/Minidump"/*.dmp 2>/dev/null | wc -l)
        if [[ "$DUMPS" -gt 0 ]]; then
            echo "### Minidump 檔案（$DUMPS 個）"
            echo ""
            echo '```'
            ls -lat "$WIN_MNT/Windows/Minidump"/*.dmp 2>/dev/null | head -10
            echo '```'
            echo ""
            echo "Linux 端不能完整解析 minidump，但檔名格式 MMDDYY-XXXXX-XX.dmp 可以看出 BSOD 時間。"
            echo "想分析內容，把這些檔複製到外接碟，事後用 WinDbg 或 BlueScreenView 開。"
            echo ""
        fi
    fi
} | tee -a "$REPORT" >/dev/null
echo ""

# ============================================
# 8. 推測診斷結論
# ============================================
echo -e "${BOLD}[8] 自動診斷推測${NC}"
{
    echo "## 8. 自動診斷推測"
    echo ""

    POSSIBLE=()

    # 用前面收集的資訊推測
    if ! efibootmgr -v 2>/dev/null | grep -qi "Windows Boot Manager"; then
        POSSIBLE+=("UEFI 開機項裡沒有 Windows Boot Manager → 用 efibootmgr 重新註冊（references/04-boot-repair.md 場景 1）")
    fi

    if [[ -d "$EFI_MNT/EFI" ]] && [[ ! -f "$EFI_MNT/EFI/Microsoft/Boot/bootmgfw.efi" ]]; then
        POSSIBLE+=("EFI 分割區裡的 bootmgfw.efi 不見了 → 從 Windows 系統碟複製回來（references/04-boot-repair.md 場景 3）")
    fi

    if [[ -f "$WIN_MNT/Windows/WinSxS/pending.xml" ]]; then
        POSSIBLE+=("pending.xml 存在 → Windows Update 卡住，移除它（references/11-driver-and-update-issues.md）")
    fi

    if [[ -f "$WIN_MNT/hiberfil.sys" ]]; then
        HSIZE=$(stat -c%s "$WIN_MNT/hiberfil.sys" 2>/dev/null || echo 0)
        if [[ "$HSIZE" -gt 1048576 ]]; then
            POSSIBLE+=("hiberfil.sys 大檔存在 → Fast Startup 卡住，rw 掛時加 remove_hiberfile")
        fi
    fi

    if [[ ${#POSSIBLE[@]} -gt 0 ]]; then
        echo "**根據收集到的資訊，最有可能的問題：**"
        echo ""
        for P in "${POSSIBLE[@]}"; do
            echo "- $P"
        done
    else
        echo "沒偵測到明顯的開機問題訊號。"
        echo ""
        echo "**可能的方向：**"
        echo "- 開機後黑屏：看 driver 載入失敗（references/02-symptom-triage.md）"
        echo "- 卡 Windows logo：跑 ntfsfix（references/05-filesystem-repair.md）"
        echo "- 隨機 BSOD：跑 SMART + memtest86+ 排查硬體（references/09-hardware-diagnostics.md）"
    fi
    echo ""
    echo "**永遠的安全提醒：動手修之前先 ddrescue/rsync 救資料！**"
} | tee -a "$REPORT" >/dev/null

# ============================================
# 結尾
# ============================================
echo ""
echo -e "${GREEN}${BOLD}=========================================="
echo "  診斷完成"
echo "==========================================${NC}"
echo ""
echo "完整報告：$REPORT"
echo ""
echo "用 less 或編輯器看："
echo "  less $REPORT"

# 清理暫時掛的 EFI
if [[ "${MOUNTED_EFI:-0}" == "1" ]]; then
    umount "$EFI_MNT" 2>/dev/null
fi
