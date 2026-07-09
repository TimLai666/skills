#!/usr/bin/env bash
# backup-user-data.sh
# 從掛載中的 Windows 系統碟備份使用者資料到外接碟
# 用法：sudo bash backup-user-data.sh [windows_mount] [backup_target]
# 範例：sudo bash backup-user-data.sh /mnt/win /mnt/external/rescue-$(date +%Y%m%d)

set -u

if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

# 顏色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m'

WIN_MNT="${1:-/mnt/win}"
TARGET="${2:-}"

# 1. 確認 Windows 已掛載
if ! mountpoint -q "$WIN_MNT" 2>/dev/null; then
    echo -e "${RED}✗ $WIN_MNT 沒有掛載 Windows${NC}" >&2
    echo "請先用 mount-windows-safe.sh 掛載"
    exit 1
fi

if [[ ! -d "$WIN_MNT/Users" ]]; then
    echo -e "${RED}✗ $WIN_MNT/Users 不存在 —— 不是 Windows 系統碟${NC}" >&2
    exit 1
fi

# 2. 互動式選目標
if [[ -z "$TARGET" ]]; then
    echo "目前可寫入的外接碟："
    lsblk -o NAME,SIZE,LABEL,MOUNTPOINT,FSTYPE -e 7,11 | grep -E "(NAME|/media/|/mnt/)" | grep -v "$WIN_MNT"
    echo ""
    read -rp "輸入備份目標路徑（例如 /mnt/external/rescue-$(date +%Y%m%d)）：" TARGET
fi

if [[ -z "$TARGET" ]]; then
    echo -e "${RED}✗ 沒指定目標${NC}"
    exit 1
fi

# 3. 確認目標不是同顆 Windows 碟
TARGET_PARENT=$(df --output=source "$(dirname "$TARGET")" 2>/dev/null | tail -1)
WIN_SOURCE=$(df --output=source "$WIN_MNT" 2>/dev/null | tail -1)
if [[ "$TARGET_PARENT" == "$WIN_SOURCE" ]]; then
    echo -e "${RED}✗ 備份目標跟來源在同一顆碟！${NC}"
    echo "  Windows 碟：$WIN_SOURCE"
    echo "  目標所在：$TARGET_PARENT"
    echo "請插外接碟或網路儲存後再試"
    exit 1
fi

# 4. 確認空間夠
USERS_SIZE_KB=$(du -sk "$WIN_MNT/Users" 2>/dev/null | awk '{print $1}' || echo 0)
USERS_SIZE_HUMAN=$(numfmt --to=iec --from-unit=Ki --suffix=B "$USERS_SIZE_KB" 2>/dev/null || echo "?")
mkdir -p "$TARGET"
AVAIL_KB=$(df --output=avail "$TARGET" 2>/dev/null | tail -1 || echo 0)
AVAIL_HUMAN=$(numfmt --to=iec --from-unit=Ki --suffix=B "$AVAIL_KB" 2>/dev/null || echo "?")

echo ""
echo -e "${BOLD}空間檢查${NC}"
echo "  Windows Users 總大小（含 AppData）：~$USERS_SIZE_HUMAN"
echo "  備份目標可用空間：$AVAIL_HUMAN"
if [[ "$AVAIL_KB" -lt "$USERS_SIZE_KB" ]]; then
    echo -e "  ${YELLOW}⚠ 目標空間不足！${NC}"
    echo "    可以挑選性備份，或換顆大碟"
    read -rp "繼續嗎？[y/N] " ans
    [[ "$ans" =~ ^[Yy]$ ]] || exit 0
fi

# 5. 列出使用者帳號
echo ""
echo -e "${BOLD}偵測到的使用者帳號${NC}"
USERS=()
while IFS= read -r U; do
    USERS+=("$U")
done < <(find "$WIN_MNT/Users" -maxdepth 1 -mindepth 1 -type d \
    ! -name "Default*" ! -name "Public" ! -name "All Users" ! -name "WDAGUtilityAccount" \
    -printf "%f\n" 2>/dev/null | sort)

if [[ ${#USERS[@]} -eq 0 ]]; then
    echo "  （沒有可備份的使用者帳號）"
    exit 0
fi

for i in "${!USERS[@]}"; do
    U="${USERS[$i]}"
    USIZE=$(du -sh "$WIN_MNT/Users/$U" 2>/dev/null | awk '{print $1}')
    echo "  [$((i+1))] $U  ($USIZE)"
done

echo ""
read -rp "備份哪些使用者？輸入編號用空格分隔，或 'all'：" SELECT

SELECTED_USERS=()
if [[ "$SELECT" == "all" ]]; then
    SELECTED_USERS=("${USERS[@]}")
else
    for n in $SELECT; do
        idx=$((n-1))
        if [[ $idx -ge 0 && $idx -lt ${#USERS[@]} ]]; then
            SELECTED_USERS+=("${USERS[$idx]}")
        fi
    done
fi

if [[ ${#SELECTED_USERS[@]} -eq 0 ]]; then
    echo -e "${RED}✗ 沒選任何使用者${NC}"
    exit 1
fi

# 6. 備份模式
echo ""
echo -e "${BOLD}備份模式${NC}"
echo "  [1] 精簡模式：只備份 Desktop / Documents / Downloads / Pictures / Videos / Music / Favorites"
echo "  [2] 標準模式：精簡 + 瀏覽器（Chrome/Edge/Firefox）+ Outlook"
echo "  [3] 完整模式：整個 Users\\<名字>\\ 全備（排除 Temp 暫存類）"
echo ""
read -rp "選擇模式 [1/2/3]（預設 2）：" MODE
MODE="${MODE:-2}"

# 7. 設定 rsync excludes
COMMON_EXCLUDES=(
    --exclude='AppData/Local/Temp'
    --exclude='AppData/Local/Microsoft/Windows/INetCache'
    --exclude='AppData/Local/Microsoft/Windows/WebCache'
    --exclude='AppData/Local/Microsoft/Windows/Explorer'
    --exclude='AppData/Local/Microsoft/Windows/WER'
    --exclude='AppData/Local/CrashDumps'
    --exclude='AppData/LocalLow/Temp'
    --exclude='AppData/Local/Microsoft/Edge/User Data/*/Cache'
    --exclude='AppData/Local/Google/Chrome/User Data/*/Cache'
    --exclude='AppData/Local/Mozilla/Firefox/Profiles/*/cache2'
    --exclude='NTUSER.DAT.LOG*'
    --exclude='ntuser.dat.LOG*'
    --exclude='*.tmp'
)

# 8. 開始備份
echo ""
echo -e "${BOLD}開始備份${NC}"
echo "  來源：$WIN_MNT/Users/"
echo "  目標：$TARGET/"
echo "  模式：$MODE"
echo ""

LOG="$TARGET/backup-log-$(date +%Y%m%d-%H%M%S).txt"
mkdir -p "$TARGET"

{
    echo "=== Windows User Data Backup ==="
    echo "Started: $(date)"
    echo "Source:  $WIN_MNT/Users/"
    echo "Target:  $TARGET/"
    echo "Mode:    $MODE"
    echo "Users:   ${SELECTED_USERS[*]}"
    echo ""
} > "$LOG"

for USER in "${SELECTED_USERS[@]}"; do
    SRC="$WIN_MNT/Users/$USER"
    DST="$TARGET/$USER"

    echo ""
    echo -e "${YELLOW}[$USER]${NC}"
    mkdir -p "$DST"

    case "$MODE" in
        1)
            # 精簡：固定資料夾白名單
            for FOLDER in Desktop Documents Downloads Pictures Videos Music Favorites; do
                if [[ -d "$SRC/$FOLDER" ]]; then
                    echo "  → $FOLDER"
                    rsync -aH --info=progress2 --no-i-r \
                        "${COMMON_EXCLUDES[@]}" \
                        "$SRC/$FOLDER/" "$DST/$FOLDER/" 2>&1 | tee -a "$LOG"
                fi
            done
            ;;

        2)
            # 標準：精簡 + 瀏覽器 + Outlook
            for FOLDER in Desktop Documents Downloads Pictures Videos Music Favorites Links Contacts; do
                if [[ -d "$SRC/$FOLDER" ]]; then
                    echo "  → $FOLDER"
                    rsync -aH --info=progress2 --no-i-r \
                        "${COMMON_EXCLUDES[@]}" \
                        "$SRC/$FOLDER/" "$DST/$FOLDER/" 2>&1 | tee -a "$LOG"
                fi
            done

            # 瀏覽器
            for BROWSER in \
                "AppData/Local/Google/Chrome/User Data" \
                "AppData/Local/Microsoft/Edge/User Data" \
                "AppData/Roaming/Mozilla/Firefox" \
                "AppData/Local/BraveSoftware/Brave-Browser/User Data" \
                "AppData/Local/Vivaldi/User Data"
            do
                if [[ -d "$SRC/$BROWSER" ]]; then
                    BROWSER_NAME=$(echo "$BROWSER" | awk -F/ '{print $(NF-1)}')
                    echo "  → 瀏覽器: $BROWSER_NAME"
                    rsync -aH --info=progress2 --no-i-r \
                        "${COMMON_EXCLUDES[@]}" \
                        "$SRC/$BROWSER/" "$DST/AppData-browser-$BROWSER_NAME/" 2>&1 | tee -a "$LOG"
                fi
            done

            # Outlook
            if [[ -d "$SRC/AppData/Local/Microsoft/Outlook" ]]; then
                echo "  → Outlook 資料"
                rsync -aH --info=progress2 --no-i-r \
                    "$SRC/AppData/Local/Microsoft/Outlook/" "$DST/Outlook/" 2>&1 | tee -a "$LOG"
            fi
            if [[ -d "$SRC/AppData/Roaming/Microsoft/Outlook" ]]; then
                rsync -aH --info=progress2 --no-i-r \
                    "$SRC/AppData/Roaming/Microsoft/Outlook/" "$DST/Outlook-roaming/" 2>&1 | tee -a "$LOG"
            fi
            if [[ -d "$SRC/AppData/Roaming/Microsoft/Signatures" ]]; then
                echo "  → Outlook 簽名"
                rsync -aH --info=progress2 --no-i-r \
                    "$SRC/AppData/Roaming/Microsoft/Signatures/" "$DST/Outlook-signatures/" 2>&1 | tee -a "$LOG"
            fi
            ;;

        3)
            # 完整模式
            echo "  → 整個 Users\\$USER\\ 備份（排除 Temp/Cache）"
            rsync -aH --info=progress2 --no-i-r \
                "${COMMON_EXCLUDES[@]}" \
                "$SRC/" "$DST/" 2>&1 | tee -a "$LOG"
            ;;
    esac
done

# 9. 額外重要資料夾（不分使用者）
echo ""
echo -e "${YELLOW}[ProgramData / 系統共用]${NC}"

# ProgramData 裡常有重要 App 資料
if [[ -d "$WIN_MNT/ProgramData" ]]; then
    echo "  → 重要 ProgramData 項目"
    mkdir -p "$TARGET/ProgramData"
    for ITEM in "Microsoft Office" "Adobe" "LINE" "obs-studio" "Steam" "Origin" "Epic"; do
        if [[ -d "$WIN_MNT/ProgramData/$ITEM" ]]; then
            rsync -aH --info=progress2 --no-i-r \
                "$WIN_MNT/ProgramData/$ITEM/" "$TARGET/ProgramData/$ITEM/" 2>&1 | tee -a "$LOG"
        fi
    done
fi

# 10. 摘要
echo ""
echo -e "${GREEN}${BOLD}=========================================="
echo "  備份完成"
echo "==========================================${NC}"
echo ""

BACKUP_SIZE=$(du -sh "$TARGET" 2>/dev/null | awk '{print $1}')
echo "  備份位置：$TARGET"
echo "  備份大小：$BACKUP_SIZE"
echo "  日誌：    $LOG"
echo ""

{
    echo ""
    echo "=== Finished: $(date) ==="
    echo "Total size: $BACKUP_SIZE"
} >> "$LOG"

# 11. 完整性建議
echo "建議下一步："
echo "  • 立即驗證備份：cd $TARGET && ls -la"
echo "  • 把備份再複製到另一顆碟（3-2-1 原則）"
echo "  • 重灌前再做一次完整檢查"
