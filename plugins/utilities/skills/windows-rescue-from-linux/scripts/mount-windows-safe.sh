#!/usr/bin/env bash
# mount-windows-safe.sh
# 互動式安全掛載 Windows 系統碟
# 1. 預設 ro，確認看得到才考慮 rw
# 2. 回報休眠掛載錯誤，不清除休眠資料
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
    echo "  3. sudo dislocker -r -V $DEV -p -- /mnt/bitlocker  # 依提示輸入復原密碼"
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
mountpoint -q "$MNT" && { err "掛載點已被使用"; exit 1; }
mkdir -p "$MNT" || exit 1
ERR_FILE=$(mktemp) || exit 1
trap 'rm -f "$ERR_FILE"' EXIT

# 8. 永遠先 ro 掛
echo ""
echo "[第一階段] 唯讀掛載..."
if mount -t ntfs-3g -o ro "$DEV" "$MNT" 2>"$ERR_FILE"; then
    OPTIONS=$(findmnt -nro OPTIONS --target "$MNT") || { err "無法確認掛載選項"; exit 1; }
    if [[ ",$OPTIONS," != *,ro,* ]]; then
        err "實際掛載未確認為唯讀，停止後續讀取，請檢查掛載狀態"
        exit 1
    fi
    ok "ro 掛載成功：$DEV → $MNT"
else
    ERR_MSG=$(cat "$ERR_FILE")
    err "ro 掛載失敗：$ERR_MSG"
    echo ""
    echo "先依 references/03-mount-windows.md 判斷掛載錯誤。"
    echo "若有 I/O 錯誤或硬體故障，先做映像；需要寫入修復時先備份。"
    exit 1
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

# 10. 檔案存在不足以判定正在休眠
if [[ -f "$MNT/hiberfil.sys" ]]; then
    echo "hiberfil.sys 存在；休眠狀態須依掛載診斷判斷。"
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
echo "     sudo bash \"$(dirname "$0")/backup-user-data.sh\" \"$MNT\" /mnt/external/backup"
echo ""
echo "  🔬 看 registry / 事件日誌（ro 也能讀）："
echo "     sudo hivexsh $MNT/Windows/System32/config/SOFTWARE"
echo "     事件日誌解析見 boot-diagnostic.sh"
echo ""
echo "  需要修改時，先確認備份與修復目標，再依 references/03-mount-windows.md 切換掛載模式。"
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
