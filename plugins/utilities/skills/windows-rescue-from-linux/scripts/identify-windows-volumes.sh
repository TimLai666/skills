#!/usr/bin/env bash
# identify-windows-volumes.sh
# 掃描所有磁碟，找出 Windows 系統碟、EFI 分割區、Recovery 分割區
# 並輸出建議的掛載指令
# 用法：sudo bash identify-windows-volumes.sh

set -u

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
                    umount "$TMPMOUNT" 2>/dev/null
                    rmdir "$TMPMOUNT"
                    continue
                fi
                umount "$TMPMOUNT" 2>/dev/null
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
                    umount "$TMPMOUNT" 2>/dev/null
                    rmdir "$TMPMOUNT"
                    continue
                fi
                umount "$TMPMOUNT" 2>/dev/null
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
            umount "$TMPMOUNT" 2>/dev/null
        fi
        rmdir "$TMPMOUNT"
    fi
done

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

# 5. 提供建議的掛載指令
echo -e "${BOLD}==== 建議的掛載指令 ====${NC}"
echo ""

if [[ ${#WIN_PARTS[@]} -gt 0 ]]; then
    echo -e "${GREEN}# 建議第一步：唯讀掛載 Windows 系統碟${NC}"
    echo "sudo mkdir -p /mnt/win"
    for k in "${!WIN_PARTS[@]}"; do
        echo "sudo mount -t ntfs-3g -o ro $k /mnt/win   # 唯讀，安全"
        echo ""
        echo -e "${YELLOW}# 確認看得到 Windows 後，如果要修改：${NC}"
        echo "# sudo umount /mnt/win"
        echo "# sudo mount -t ntfs-3g -o rw,remove_hiberfile $k /mnt/win"
        break
    done
    echo ""
fi

if [[ ${#EFI_PARTS[@]} -gt 0 ]]; then
    echo -e "${BLUE}# 修開機問題時需要掛 EFI 分割區${NC}"
    echo "sudo mkdir -p /mnt/efi"
    for k in "${!EFI_PARTS[@]}"; do
        echo "sudo mount -t vfat -o ro $k /mnt/efi"
        break
    done
    echo ""
fi

if [[ ${#BITLOCKER_PARTS[@]} -gt 0 ]]; then
    echo -e "${RED}# 偵測到 BitLocker 加密碟，先弄到 recovery key${NC}"
    echo "# 取得 key 後："
    echo "sudo mkdir -p /mnt/bitlocker /mnt/win"
    for k in "${!BITLOCKER_PARTS[@]}"; do
        echo "sudo dislocker -V $k -p<48-digit-recovery-key> -- /mnt/bitlocker"
        echo "sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file /mnt/win"
        break
    done
    echo ""
fi

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
echo "Hibernation 檢查："
for k in "${!WIN_PARTS[@]}"; do
    TMPMOUNT=$(mktemp -d)
    if mount -t ntfs-3g -o ro "$k" "$TMPMOUNT" 2>/dev/null; then
        if [[ -f "$TMPMOUNT/hiberfil.sys" ]]; then
            HSIZE=$(stat -c%s "$TMPMOUNT/hiberfil.sys" 2>/dev/null || echo 0)
            if [[ "$HSIZE" -gt 1048576 ]]; then
                echo -e "  $k: ${YELLOW}hiberfil.sys 存在（$(numfmt --to=iec --suffix=B "$HSIZE")），rw 掛載時要加 remove_hiberfile${NC}"
            fi
        fi
        umount "$TMPMOUNT" 2>/dev/null
    fi
    rmdir "$TMPMOUNT"
done

echo ""
echo -e "${BOLD}盤點完成${NC}"
echo ""
echo "下一步建議："
echo "  • 看 references/02-symptom-triage.md 確認故障類型"
echo "  • 看 references/03-mount-windows.md 安全掛載"
echo "  • 不確定狀況時，先 ro 掛載 + rsync 救資料到外接碟"
