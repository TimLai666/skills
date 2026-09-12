#!/usr/bin/env bash
# disk-health-report.sh
# 對所有偵測到的儲存裝置做 SMART 健康檢查
# 輸出彩色摘要 + 詳細報告
# 用法：sudo bash disk-health-report.sh [/dev/sdX]

set -u

if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m'

REPORT_DIR="/tmp/disk-health-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$REPORT_DIR" || exit 2

echo -e "${BOLD}==== 磁碟健康總檢 ====${NC}"
echo "時間：$(date)"
echo "報告位置：$REPORT_DIR"
echo ""

# 1. 列出要檢查的裝置
if [[ $# -gt 0 ]]; then
    DEVICES=("$@")
else
    DEVICES=()
    while read -r DEV; do
        [[ -b "$DEV" ]] && DEVICES+=("$DEV")
    done < <(lsblk -d -nro NAME -e 7,11 | grep -v loop | sed 's|^|/dev/|')
fi

if [[ ${#DEVICES[@]} -eq 0 ]]; then
    echo -e "${RED}沒偵測到磁碟${NC}"
    exit 1
fi

# 2. 對每顆裝置做檢查
declare -A HEALTH_SUMMARY

for DEV in "${DEVICES[@]}"; do
    DEV_NAME=$(basename "$DEV")
    OUT="$REPORT_DIR/$DEV_NAME.txt"

    echo -e "${BOLD}=== $DEV ===${NC}" | tee "$OUT"

    # 基本資訊
    MODEL=$(lsblk -dno MODEL "$DEV" 2>/dev/null | xargs)
    SERIAL=$(lsblk -dno SERIAL "$DEV" 2>/dev/null | xargs)
    SIZE=$(lsblk -dno SIZE "$DEV" 2>/dev/null | xargs)
    ROTA=$(lsblk -dno ROTA "$DEV" 2>/dev/null | xargs)
    TRAN=$(lsblk -dno TRAN "$DEV" 2>/dev/null | xargs)
    {
        echo "Model:     $MODEL"
        echo "Serial:    $SERIAL"
        echo "Size:      $SIZE"
        echo "Rotation:  $([[ "$ROTA" == "1" ]] && echo HDD || echo SSD/NVMe)"
        echo "Transport: $TRAN"
        echo ""
    } | tee -a "$OUT"

    # 一次唯讀收集，保留 smartctl 位元狀態碼；NVMe 不使用 ATA 支援字串判定。
    SMART_DATA=$(smartctl -a "$DEV" 2>&1)
    SMART_STATUS=$?
    printf '%s\n' "$SMART_DATA" >> "$OUT"
    if (( SMART_STATUS & 7 )); then
        echo "⚠ SMART 資料不完整或無法讀取，不能判定健康" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="UNKNOWN"
        continue
    fi

    # 健康狀態
    HEALTH=$(printf '%s\n' "$SMART_DATA" | grep -i "overall-health\|test result" | tail -1)
    echo "" | tee -a "$OUT"
    echo "[健康狀態]" | tee -a "$OUT"
    if (( SMART_STATUS & 24 )); then
        echo "⚠ SMART 回報整體失敗或目前屬性低於臨界值（狀態碼 ${SMART_STATUS}）。" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="FAILING"
    elif (( SMART_STATUS & 224 )); then
        echo "⚠ SMART 回報歷史臨界值、錯誤日誌或自我測試紀錄（狀態碼 ${SMART_STATUS}），須對照完整報告。" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="WARN"
    elif echo "$HEALTH" | grep -qi "PASSED\|OK"; then
        echo -e "  ${GREEN}$HEALTH${NC}" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="OK"
    elif echo "$HEALTH" | grep -qi "FAILED"; then
        echo -e "  ${RED}${BOLD}$HEALTH${NC}" | tee -a "$OUT"
        echo -e "  ${RED}${BOLD}⚠ 這顆碟即將失效。立刻 ddrescue 把資料弄出來，然後換新碟。${NC}" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="FAILING"
    else
        echo "  $HEALTH" | tee -a "$OUT"
        HEALTH_SUMMARY[$DEV]="UNKNOWN"
    fi

    # SMART 完整資訊
    echo "" >> "$OUT"
    echo "[完整 SMART 資訊]" >> "$OUT"
    : # 原始資料已保存

    # 關鍵屬性分析
    echo "" | tee -a "$OUT"
    echo "[關鍵屬性檢查]" | tee -a "$OUT"

    declare -A CRITICAL=(
        [5]="Reallocated_Sector_Ct"
        [10]="Spin_Retry_Count"
        [184]="End-to-End_Error"
        [187]="Reported_Uncorrect"
        [188]="Command_Timeout"
        [196]="Reallocated_Event_Count"
        [197]="Current_Pending_Sector"
        [198]="Offline_Uncorrectable"
        [199]="UDMA_CRC_Error_Count"
    )

    PROBLEMS=0
    for ID in 5 10 184 187 188 196 197 198 199; do
        NAME="${CRITICAL[$ID]}"
        # 找這個屬性的 RAW value
        LINE=$(printf '%s\n' "$SMART_DATA" | awk -v id="$ID" '$1==id {print}')
        if [[ -n "$LINE" ]]; then
            RAW=$(echo "$LINE" | awk '{print $NF}' | sed 's/[^0-9].*//')
            if [[ ! "$RAW" =~ ^[0-9]+$ ]]; then
                printf '  ? %-30s 原始值無法解析，請看完整報告\n' "$NAME" | tee -a "$OUT"
                ((PROBLEMS++))
                continue
            fi
            if [[ "$RAW" -eq 0 ]]; then
                printf "  ${GREEN}✓${NC} %-30s = %s\n" "$NAME" "$RAW" | tee -a "$OUT"
            elif [[ "$ID" -eq 199 ]]; then
                # UDMA_CRC_Error 通常代表線材，不是碟本身
                printf "  ${YELLOW}⚠${NC} %-30s = %s  ${YELLOW}(可能與傳輸連線有關，須對照趨勢)${NC}\n" "$NAME" "$RAW" | tee -a "$OUT"
                ((PROBLEMS++))
            else
                printf "  ${RED}✗${NC} %-30s = %s  ${RED}(需依廠商定義與變化判讀)${NC}\n" "$NAME" "$RAW" | tee -a "$OUT"
                ((PROBLEMS++))
            fi
        fi
    done

    # SSD 特殊屬性
    if [[ "$ROTA" == "0" ]]; then
        echo "" | tee -a "$OUT"
        echo "[SSD 特殊屬性]" | tee -a "$OUT"

        for ID in 173 177 233 241; do
            LINE=$(printf '%s\n' "$SMART_DATA" | awk -v id="$ID" '$1==id {print}')
            if [[ -n "$LINE" ]]; then
                NAME=$(echo "$LINE" | awk '{print $2}')
                RAW=$(echo "$LINE" | awk '{print $NF}' | sed 's/[^0-9].*//')
                VALUE=$(echo "$LINE" | awk '{print $4}')
                printf "  %-30s value=%s raw=%s\n" "$NAME" "$VALUE" "$RAW" | tee -a "$OUT"
            fi
        done

        # 健康百分比（NVMe）
        if [[ "$DEV" =~ nvme ]]; then
            HEALTH_USED=$(printf '%s\n' "$SMART_DATA" | grep -i "Percentage Used" | awk '{print $NF}' | tr -d '%')
            if [[ "$HEALTH_USED" =~ ^[0-9]+$ ]]; then
                if [[ "$HEALTH_USED" -lt 50 ]]; then
                    printf "  ${GREEN}NVMe 使用量: %s%%${NC}\n" "$HEALTH_USED" | tee -a "$OUT"
                elif [[ "$HEALTH_USED" -lt 80 ]]; then
                    printf "  ${YELLOW}NVMe 使用量: %s%%${NC}\n" "$HEALTH_USED" | tee -a "$OUT"
                else
                    printf "  ${RED}NVMe 使用量: %s%% (耐久度估計，非剩餘壽命保證)${NC}\n" "$HEALTH_USED" | tee -a "$OUT"
                fi
            fi
        fi
    fi

    # 使用時數
    POH=$(printf '%s\n' "$SMART_DATA" | awk '$1==9 {print $NF}' | sed 's/[^0-9].*//')
    if [[ -n "$POH" && "$POH" -gt 0 ]]; then
        DAYS=$((POH / 24))
        YEARS=$(echo "scale=1; $POH/8760" | bc 2>/dev/null || echo "?")
        echo "" | tee -a "$OUT"
        echo "[使用時間] ${POH} 小時 = ${DAYS} 天 ≈ ${YEARS} 年" | tee -a "$OUT"
    fi

    # 上次自我測試
    echo "" | tee -a "$OUT"
    echo "[最近的自我測試]" | tee -a "$OUT"
    printf '%s\n' "$SMART_DATA" | tail -10 | head -7 | tee -a "$OUT"

    # 結論
    echo "" | tee -a "$OUT"
    case "${HEALTH_SUMMARY[$DEV]}" in
        OK)
            if [[ $PROBLEMS -eq 0 ]]; then
                echo -e "${GREEN}結論：本次 SMART 未回報警告，仍須對照症狀${NC}" | tee -a "$OUT"
            else
                echo -e "${YELLOW}結論：通過 SMART 整體判斷，但有 $PROBLEMS 項警告值${NC}" | tee -a "$OUT"
                HEALTH_SUMMARY[$DEV]="WARN"
            fi
            ;;
        WARN)
            echo "結論：SMART 有警告紀錄，不能只以 PASSED 判定健康。" | tee -a "$OUT"
            ;;
        FAILING)
            echo -e "${RED}結論：磁碟即將失效，立刻備份！${NC}" | tee -a "$OUT"
            ;;
        *)
            echo "結論：狀態不明" | tee -a "$OUT"
            ;;
    esac

    echo ""
done

# 3. 全部摘要
echo ""
echo -e "${BOLD}=========================================="
echo "  全體磁碟健康摘要"
echo "==========================================${NC}"
echo ""
for DEV in "${!HEALTH_SUMMARY[@]}"; do
    case "${HEALTH_SUMMARY[$DEV]}" in
        OK)      echo -e "  ${GREEN}✓${NC} $DEV  SMART 未回報警告" ;;
        WARN)    echo -e "  ${YELLOW}⚠${NC} $DEV  有警告值，建議盡早備份" ;;
        FAILING) echo -e "  ${RED}✗${NC} $DEV  即將失效，立刻 ddrescue" ;;
        *)       echo -e "  ${YELLOW}?${NC} $DEV  狀態不明" ;;
    esac
done
echo ""

# 4. 給建議
HAS_FAILING=false
HAS_WARN=false
HAS_UNKNOWN=false
for STATUS in "${HEALTH_SUMMARY[@]}"; do
    [[ "$STATUS" == "FAILING" ]] && HAS_FAILING=true
    [[ "$STATUS" == "WARN" ]] && HAS_WARN=true
    [[ "$STATUS" == "UNKNOWN" ]] && HAS_UNKNOWN=true
done

if $HAS_FAILING; then
    echo -e "${RED}${BOLD}建議：立刻把所有重要資料從失效磁碟救出來${NC}"
    echo "  sudo ddrescue -f -n /dev/<failing_disk> /mnt/external/disk-image.img /mnt/external/disk.log"
    echo "  詳見 references/08-data-recovery.md"
elif $HAS_WARN; then
    echo -e "${YELLOW}建議：先備份，再對照警告的時間、類型與症狀，判斷是否需更換${NC}"
    echo "  • 在下次大型工作前完整備份"
    echo "  • 若有讀取錯誤、異音或掉線，先做映像救援，不加跑長測試"
elif $HAS_UNKNOWN; then
    echo "部分磁碟狀態不明；確認工具、介面與讀取錯誤後再判斷。"
else
    echo -e "${GREEN}建議：SMART 未回報警告；這不排除硬體故障${NC}"
fi

echo ""
echo "完整報告：$REPORT_DIR/"

$HAS_FAILING && exit 1
$HAS_UNKNOWN && exit 2
$HAS_WARN && exit 1
exit 0
