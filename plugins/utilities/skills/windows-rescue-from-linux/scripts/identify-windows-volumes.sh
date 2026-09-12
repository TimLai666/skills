#!/usr/bin/env bash
# identify-windows-volumes.sh
# 掃描所有磁碟，找出 Windows 系統碟、EFI 分割區、Recovery 分割區
# 並輸出建議的掛載指令
# 用法：sudo bash identify-windows-volumes.sh

set -u
PROBE=false
case "${1:-}" in
    "") ;;
    --probe) PROBE=true ;;
    *) echo "用法：sudo bash $0 [--probe]（確認磁碟適合讀取後才探查內容）"; exit 2 ;;
esac


if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BOLD}==== Windows 磁碟與分割區盤點 ====${NC}"
echo "時間：$(date)"
echo ""

# 1. 列出所有實體磁碟
echo -e "${BOLD}[1] 偵測到的儲存裝置${NC}"
lsblk -d -o NAME,SIZE,MODEL,SERIAL,TRAN -e 7,11 | grep -v loop
echo ""

# 2. 掃所有分割區
echo -e "${BOLD}[2] 所有分割區${NC}"
lsblk -f -o NAME,FSTYPE,LABEL,UUID,SIZE,MOUNTPOINT -e 7,11
echo ""

# 3. 分類找出特殊用途分割區
echo -e "${BOLD}[3] 分割區用途分析${NC}"
echo ""

declare -A WIN_PARTS EFI_PARTS RECOVERY_PARTS BITLOCKER_PARTS DYNAMIC_PARTS
declare -a ALL_PARTS

# 取得所有可能的分割區
while read -r DEV; do
    [[ -z "$DEV" ]] && continue
    [[ ! -b "/dev/$DEV" ]] && continue
    ALL_PARTS+=("$DEV")
done < <(lsblk -nrpo NAME,TYPE | awk '$2=="part" {print $1}' | sed 's|/dev/||')

# 對每個分割區做判斷
for PART in "${ALL_PARTS[@]}"; do
    DEV="/dev/$PART"
    FSTYPE=$(blkid -o value -s TYPE "$DEV" 2>/dev/null || echo "")
    LABEL=$(blkid -o value -s LABEL "$DEV" 2>/dev/null || echo "")
    PARTLABEL=$(blkid -o value -s PARTLABEL "$DEV" 2>/dev/null || echo "")
    SIZE=$(lsblk -nbo SIZE "$DEV" 2>/dev/null | head -1)
    SIZE_HUMAN=$(numfmt --to=iec --suffix=B --format="%.1f" "$SIZE" 2>/dev/null || echo "?")

    if ! $PROBE; then
        printf '%s  type=%s label=%s partlabel=%s size=%s\n' "$DEV" "$FSTYPE" "$LABEL" "$PARTLABEL" "$SIZE_HUMAN"
        continue
    fi

    # BitLocker
    if [[ "$FSTYPE" == "BitLocker" ]] || dd if="$DEV" bs=8 count=1 2>/dev/null | grep -q "FVE-FS"; then
        BITLOCKER_PARTS[$DEV]="$SIZE_HUMAN, label=$LABEL"
        continue
    fi

    # Dynamic Disk
    if [[ "$FSTYPE" == "LDM_data" ]] || [[ "$FSTYPE" == "LDM_metadata" ]]; then
        DYNAMIC_PARTS[$DEV]="$SIZE_HUMAN"
        continue
    fi

    # EFI 分割區（FAT32 + 標籤含 EFI/SYSTEM 或 PARTLABEL 含 EFI）
    if [[ "$FSTYPE" == "vfat" ]]; then
        if [[ "$PARTLABEL" =~ [Ee][Ff][Ii] ]] || \
           [[ "$LABEL" =~ ^([Ee][Ff][Ii]|SYSTEM)$ ]] || \
           [[ "$SIZE" -lt 1073741824 ]]; then  # <1GB
            # 進一步確認 - 掛上去看有沒有 EFI 資料夾
            TMPMOUNT=$(mktemp -d)
            if mount -t vfat -o ro "$DEV" "$TMPMOUNT" 2>/dev/null; then
                if [[ -d "$TMPMOUNT/EFI" ]] || [[ -d "$TMPMOUNT/efi" ]]; then
                    EFI_PARTS[$DEV]="$SIZE_HUMAN, label=$LABEL"
                    umount "$TMPMOUNT" 2>/dev/null || { echo "卸載失敗：$TMPMOUNT" >&2; exit 1; }
                    rmdir "$TMPMOUNT"
                    continue
                fi
                umount "$TMPMOUNT" 2>/dev/null || { echo "卸載失敗：$TMPMOUNT" >&2; exit 1; }
            fi
            rmdir "$TMPMOUNT"
        fi
    fi

    # Recovery 分割區（NTFS + 標籤含 Recovery，或內含 Winre.wim）
    if [[ "$FSTYPE" == "ntfs" ]]; then
        if [[ "$LABEL" =~ [Rr]ecovery ]] || [[ "$PARTLABEL" =~ [Rr]ecovery ]]; then
            RECOVERY_PARTS[$DEV]="$SIZE_HUMAN, label=$LABEL"
            continue
        fi
        # 通常 Recovery 很小（<2GB）
        if [[ "$SIZE" -lt 2147483648 ]]; then
            TMPMOUNT=$(mktemp -d)
            if mount -t ntfs-3g -o ro "$DEV" "$TMPMOUNT" 2>/dev/null; then
                if [[ -f "$TMPMOUNT/Recovery/WindowsRE/Winre.wim" ]] || \
                   find "$TMPMOUNT" -maxdepth 3 -name "Winre.wim" -print -quit 2>/dev/null | grep -q .; then
                    RECOVERY_PARTS[$DEV]="$SIZE_HUMAN, label=$LABEL"
                    umount "$TMPMOUNT" 2>/dev/null || { echo "卸載失敗：$TMPMOUNT" >&2; exit 1; }
                    rmdir "$TMPMOUNT"
                    continue
                fi
                umount "$TMPMOUNT" 2>/dev/null || { echo "卸載失敗：$TMPMOUNT" >&2; exit 1; }
            fi
            rmdir "$TMPMOUNT"
        fi

        # 系統碟（NTFS 大碟 + 有 Windows 資料夾）
        TMPMOUNT=$(mktemp -d)
        if mount -t ntfs-3g -o ro "$DEV" "$TMPMOUNT" 2>/dev/null; then
            if [[ -d "$TMPMOUNT/Windows/System32" ]]; then
                BUILD=""
                if [[ -f "$TMPMOUNT/Windows/System32/license.rtf" ]] || \
                   [[ -d "$TMPMOUNT/Windows/System32/config" ]]; then
                    # 試讀 build number
                    if [[ -f "$TMPMOUNT/Windows/System32/config/SOFTWARE" ]]; then
                        BUILD=" (Windows 系統碟)"
                    fi
                fi
                WIN_PARTS[$DEV]="$SIZE_HUMAN, label=$LABEL$BUILD"
            fi
            umount "$TMPMOUNT" 2>/dev/null || { echo "卸載失敗：$TMPMOUNT" >&2; exit 1; }
        fi
        rmdir "$TMPMOUNT"
    fi
done

if ! $PROBE; then
    echo "目前僅列出分割區資料，尚未檢查 Windows 或 EFI 內容。"
    echo "有異音、讀取錯誤或掉線時先做映像救援。確認適合探查後，再加 --probe 辨識內容。"
    exit 0
fi

# 4. 輸出分類結果
print_section() {
    local title="$1"
    local color="$2"
    local -n arr=$3

    echo -e "${color}${BOLD}${title}${NC}"
    if [[ ${#arr[@]} -eq 0 ]]; then
        echo "  （沒找到）"
    else
        for k in "${!arr[@]}"; do
            echo -e "  ${color}$k${NC}  -  ${arr[$k]}"
        done
    fi
    echo ""
}

print_section "Windows 系統碟（含 Windows\\System32）" "$GREEN" WIN_PARTS
print_section "EFI 系統分割區（含 EFI 資料夾）" "$BLUE" EFI_PARTS
print_section "Windows Recovery 分割區（含 Winre.wim）" "$YELLOW" RECOVERY_PARTS
print_section "BitLocker 加密分割區（需 recovery key 解密）" "$RED" BITLOCKER_PARTS
print_section "Windows Dynamic Disk（需 ldmtool 處理）" "$RED" DYNAMIC_PARTS

# 5. 多個候選須對照磁碟、分割區 UUID 與安裝內容，不自行選第一個。
echo "對照上面的裝置型號、序號、分割區與 Windows 內容，確認目標後執行："
echo 'sudo bash scripts/mount-windows-safe.sh /dev/已確認的分割區 /mnt/win'


# 6. 警告與提醒
echo -e "${BOLD}==== 警告與提醒 ====${NC}"

# SMART 警告
echo ""
echo "SMART 健康快速檢查："
for DISK in $(lsblk -d -nro NAME -e 7,11 | grep -v loop); do
    DEV="/dev/$DISK"
    if [[ -b "$DEV" ]]; then
        HEALTH=$(smartctl -H "$DEV" 2>/dev/null | grep -i "health\|self-assessment" | head -1 | sed 's/^[[:space:]]*//')
        if [[ -n "$HEALTH" ]]; then
            if echo "$HEALTH" | grep -q "PASSED\|OK"; then
                echo -e "  $DEV: ${GREEN}$HEALTH${NC}"
            else
                echo -e "  $DEV: ${RED}$HEALTH${NC}  ⚠ 先 ddrescue 再說，不要直接修檔系統"
            fi
        else
            echo "  $DEV: 無 SMART 資訊（可能是 USB 或虛擬碟）"
        fi
    fi
done

echo ""
echo -e "${BOLD}盤點完成${NC}"
echo ""
echo "下一步建議："
echo "  • 看 references/02-symptom-triage.md 確認故障類型"
echo "  • 看 references/03-mount-windows.md 安全掛載"
echo "  • 有硬體故障跡象時，先映像救援，再檢查副本"
