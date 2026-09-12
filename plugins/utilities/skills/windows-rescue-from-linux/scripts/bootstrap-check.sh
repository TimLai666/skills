#!/usr/bin/env bash
# bootstrap-check.sh
# 給 AI agent（Claude Code / Codex）進入這個 skill 時跑的環境體檢
# 不安裝任何東西，只回報狀態
# 用法：bash bootstrap-check.sh

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[0;33m'; BOLD='\033[1m'; NC='\033[0m'

ok=0; warn=0; fail=0

check() {
    local cmd="$1"
    local label="${2:-$cmd}"
    local hint="${3:-}"
    if command -v "$cmd" >/dev/null 2>&1; then
        local ver
        ver=$($cmd --version 2>/dev/null | head -1 | cut -c1-60 || echo "")
        printf "  ${GREEN}✓${NC} %-15s %s\n" "$label" "$ver"
        ((ok++))
    else
        printf "  ${RED}✗${NC} %-15s 缺失" "$label"
        [[ -n "$hint" ]] && printf "  ${YELLOW}→ %s${NC}" "$hint"
        echo ""
        ((fail++))
    fi
}

echo -e "${BOLD}======================================"
echo "  Windows 救援環境體檢"
echo "  $(date)"
echo -e "======================================${NC}"

# ---- 環境 ----
echo ""
echo -e "${BOLD}[環境]${NC}"
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    printf "  Distro:        %s %s\n" "$NAME" "$VERSION"
else
    echo "  ⚠ 無法判斷 distro"
fi
[[ -d /sys/firmware/efi ]] && BOOT_MODE="UEFI" || BOOT_MODE="Legacy/BIOS"
printf "  Boot Mode:     %s\n" "$BOOT_MODE"
printf "  Hostname:      %s\n" "$(hostname)"
printf "  User:          %s (uid=%s)\n" "$USER" "$(id -u)"

# 在 Live USB？
if grep -q "boot=live\|boot=casper" /proc/cmdline 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} 看起來在 Live USB 環境"
fi

# 離線不妨礙已備妥工具的救援；下載時再以實際服務確認連線。
echo "網路需求依本次操作判斷，未進行連線測試。"

# ---- 核心救援工具（5 大金剛）----
echo ""
echo -e "${BOLD}[常用救援工具，依本案需求選用]${NC}"
check ntfsfix   "ntfsfix"   "sudo apt install ntfs-3g"
check chntpw    "chntpw"    "sudo apt install chntpw"
check testdisk  "testdisk"  "sudo apt install testdisk"
check photorec  "photorec"  "sudo apt install testdisk"
check ddrescue  "ddrescue"  "sudo apt install gddrescue"

# ---- 其他關鍵 ----
echo ""
echo -e "${BOLD}[其他關鍵工具]${NC}"
check hivexsh    "hivexsh"    "sudo apt install libhivex-bin"
check smartctl   "smartctl"   "sudo apt install smartmontools"
check clamscan   "clamscan"   "sudo apt install clamav"
check dislocker  "dislocker"  "sudo apt install dislocker"
check efibootmgr "efibootmgr" "sudo apt install efibootmgr"
check rsync      "rsync"      "sudo apt install rsync"
check tmux       "tmux"       "sudo apt install tmux"

# ---- AI agent 環境 ----
echo ""
echo -e "${BOLD}[AI Agent 環境]${NC}"

echo "AI 工具是選用項目；已有可用代理程式時不必另裝。"
for cmd in node npm claude codex; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "  $cmd: $(command -v "$cmd")"
    else
        echo "  $cmd: 未安裝（選用）"
    fi
done

# Skill 在不在
echo ""
echo -e "${BOLD}[Skill 安裝狀態]${NC}"
SKILL_PATHS=(
    "$HOME/.claude/skills/windows-rescue-from-linux"
    "$HOME/.codex/skills/windows-rescue-from-linux"
    "$HOME/.agents/skills/windows-rescue-from-linux"
    "$(cd "$(dirname "$0")/.." && pwd)"
    "./windows-rescue-from-linux"
)
SKILL_FOUND=false
for P in "${SKILL_PATHS[@]}"; do
    if [[ -f "$P/SKILL.md" ]]; then
        echo -e "  ${GREEN}✓${NC} 找到 skill：$P"
        SKILL_FOUND=true
        break
    fi
done
if ! $SKILL_FOUND; then
    echo -e "  ${YELLOW}⚠${NC} 沒找到 SKILL.md 在 ~/.claude/skills/，記得 symlink 過去"
    ((warn++))
fi

# ---- 結論 ----
echo ""
echo -e "${BOLD}======================================"
echo -e "  結論：${GREEN}$ok 通過${NC} / ${YELLOW}$warn 警告${NC} / ${RED}$fail 缺失${NC}"
echo -e "======================================${NC}"

echo "缺少工具不代表無法救援。依症狀分流，只安裝本次需要的工具。"
echo "安裝方式見 references/00-rescue-usb-preparation.md。"
exit 0
