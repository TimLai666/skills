#!/usr/bin/env bash
# mount-windows-safe.sh
# 互動式安全掛載 Windows 系統碟
# 1. 預設 ro，確認看得到才考慮 rw
# 2. 自動處理 hibernation
# 3. 偵測 BitLocker
# 用法：sudo bash mount-windows-safe.sh [/dev/sdXN] [/mnt/win]

set -u

if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

DEV="${1:-}"
MNT="${2:-/mnt/win}"

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

err() { echo -e "${RED}✗ $1${NC}" >&2; }
ok() { echo -e "${GREEN}✓ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }

# 1. 沒帶參數時互動式選
if [[ -z "$DEV" ]]; then
    echo "目前 NTFS 分割區："
    lsblk -f -e 7,11 | grep -E "(NAME|ntfs|BitLocker)"
    echo ""
    read -rp "輸入要掛載的分割區（例如 /dev/sda3）：" DEV
fi

# 2. 檢查裝置存在
if [[ ! -b "$DEV" ]]; then
    err "$DEV 不是區塊裝置"
    exit 1
fi

# 3. 檢查是不是已經 mount 在別處
EXISTING_MOUNT=$(findmnt -nro TARGET "$DEV" 2>/dev/null | head -1 || true)
if [[ -n "$EXISTING_MOUNT" ]]; then
    warn "$DEV 已經掛在 $EXISTING_MOUNT"
    read -rp "要先卸載再重掛嗎？[y/N] " ans
    if [[ "$ans" =~ ^[Yy]$ ]]; then
        umount "$EXISTING_MOUNT" || { err "卸載失敗，可能有檔案開啟中"; exit 1; }
    else
        exit 0
    fi
fi

# 4. 偵測檔案系統
FSTYPE=$(blkid -o value -s TYPE "$DEV" 2>/dev/null || echo "")
echo ""
echo "裝置：$DEV"
echo "檔案系統：$FSTYPE"

# 5. BitLocker 特例
if [[ "$FSTYPE" == "BitLocker" ]] || dd if="$DEV" bs=8 count=1 2>/dev/null | grep -q "FVE-FS"; then
    err "這是 BitLocker 加密碟，需要 recovery key"
    echo ""
    echo "解開步驟："
    echo "  1. 取得 48 位 recovery key（從 account.microsoft.com 等）"
    echo "  2. sudo mkdir -p /mnt/bitlocker $MNT"
    echo "  3. sudo dislocker -V $DEV -p<recovery-key> -- /mnt/bitlocker"
    echo "  4. sudo mount -t ntfs-3g -o loop,ro /mnt/bitlocker/dislocker-file $MNT"
    echo ""
    echo "詳見 references/10-bitlocker.md"
    exit 1
fi

# 6. 不是 NTFS 警告
if [[ "$FSTYPE" != "ntfs" ]]; then
    warn "不是 NTFS 檔案系統（$FSTYPE）"
    read -rp "還是要繼續？[y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || exit 0
fi

# 7. 建立掛載點
mkdir -p "$MNT"

# 8. 永遠先 ro 掛
echo ""
echo "[第一階段] 唯讀掛載..."
if mount -t ntfs-3g -o ro "$DEV" "$MNT" 2>/tmp/mount-err; then
    ok "ro 掛載成功：$DEV → $MNT"
else
    ERR_MSG=$(cat /tmp/mount-err)
    err "ro 掛載失敗：$ERR_MSG"
    echo ""
    if echo "$ERR_MSG" | grep -q "hibernated\|hiberfile"; then
        warn "系統處於 hibernation 狀態"
        echo "可以用 ro 強制掛（資料看得到，但要記得這是 hibernation 時的快照）"
        read -rp "用 -o ro,force 強制 ro 掛載？[y/N] " ans
        if [[ "$ans" =~ ^[Yy]$ ]]; then
            mount -t ntfs-3g -o ro,force "$DEV" "$MNT" || { err "還是失敗"; exit 1; }
            ok "強制 ro 掛載成功"
        else
            echo "其他選項："
            echo "  • 開回 Windows 跑 shutdown /s /f 完整關機，再來試"
            echo "  • sudo mount -t ntfs-3g -o remove_hiberfile $DEV $MNT  ← 寫入，會丟 hibernation 內未存的資料"
            exit 1
        fi
    elif echo "$ERR_MSG" | grep -q "unclean\|dirty"; then
        warn "NTFS 是 dirty 狀態（沒乾淨卸載過）"
        echo "可以試 ntfsfix 處理（會寫入！），或先 ro 看狀況："
        echo "  sudo ntfsfix --no-action $DEV    # dry run，不會寫"
        echo "  sudo ntfsfix $DEV                # 實際修"
        exit 1
    else
        echo "其他錯誤，看完整訊息：cat /tmp/mount-err"
        exit 1
    fi
fi

# 9. 確認看得到 Windows
echo ""
echo "[檢查] 確認看得到 Windows 目錄結構..."
WIN_OK=false
if [[ -d "$MNT/Windows/System32" ]]; then
    ok "看到 Windows\\System32"
    WIN_OK=true
fi
if [[ -d "$MNT/Users" ]]; then
    USERS=$(ls "$MNT/Users" 2>/dev/null | grep -v -E "^(Default|Public|All Users)$" || true)
    ok "看到 Users，使用者帳號：$(echo $USERS | tr '\n' ' ')"
fi
if [[ -d "$MNT/Program Files" ]]; then
    ok "看到 Program Files"
fi

if ! $WIN_OK; then
    warn "看不到 Windows\\System32 —— 可能不是系統碟，或檔案系統毀損"
    echo ""
    ls "$MNT" | head -20
fi

# 10. 偵測 hibernation
if [[ -f "$MNT/hiberfil.sys" ]]; then
    HSIZE=$(stat -c%s "$MNT/hiberfil.sys" 2>/dev/null || echo 0)
    HSIZE_HUMAN=$(numfmt --to=iec --suffix=B "$HSIZE" 2>/dev/null || echo "?")
    if [[ "$HSIZE" -gt 1048576 ]]; then
        warn "hiberfil.sys 存在（$HSIZE_HUMAN），系統可能是 hibernation/fast startup 狀態"
        echo "   如果之後要 rw 掛載，要加 remove_hiberfile 參數"
    fi
fi

# 11. 提示下一步
echo ""
echo "=========================================="
echo "  目前狀態：ro 掛載於 $MNT"
echo "=========================================="
echo ""
echo "下一步可以做的："
echo ""
echo "  📁 看資料："
echo "     ls $MNT/Users/"
echo ""
echo "  💾 備份資料（推薦先做）："
echo "     bash $(dirname "$0")/backup-user-data.sh /dev/EXT_DISK"
echo ""
echo "  🔬 看 registry / 事件日誌（ro 也能讀）："
echo "     sudo hivexsh $MNT/Windows/System32/config/SOFTWARE"
echo "     python3 -m Evtx.Evtx $MNT/Windows/System32/winevt/Logs/System.evtx"
echo ""
echo "  ✏  如果之後需要修改（寫入）："
echo "     sudo umount $MNT"
read -p "" -t 0 && true  # 補空行
if [[ -f "$MNT/hiberfil.sys" ]]; then
    echo "     sudo mount -t ntfs-3g -o rw,remove_hiberfile $DEV $MNT"
else
    echo "     sudo mount -t ntfs-3g -o rw $DEV $MNT"
fi
echo ""
echo "  ⏏  卸載："
echo "     sudo umount $MNT"
echo ""

# 12. 留下日誌
LOG_DIR="/tmp/rescue-log"
mkdir -p "$LOG_DIR"
{
    echo "=== mount log $(date) ==="
    echo "Device: $DEV"
    echo "FSType: $FSTYPE"
    echo "MountPoint: $MNT"
    echo "Mode: ro"
    blkid "$DEV"
} >> "$LOG_DIR/mount.log"
