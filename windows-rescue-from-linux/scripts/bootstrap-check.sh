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

# 網路
echo ""
echo -e "${BOLD}[網路]${NC}"
if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} 網際網路可達"
    ((ok++))
else
    echo -e "  ${RED}✗${NC} 沒網路（會擋下載病毒碼、安裝套件、AI 對話）"
    ((fail++))
fi

# ---- 核心救援工具（5 大金剛）----
echo ""
echo -e "${BOLD}[核心救援工具 - 必裝]${NC}"
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
check tmux       "tmux"       "sudo apt install tmux  ← 長時間任務必裝"

# ---- AI agent 環境 ----
echo ""
echo -e "${BOLD}[AI Agent 環境]${NC}"

# Node.js
if command -v node >/dev/null 2>&1; then
    NODE_VER=$(node -v | sed 's/v//')
    NODE_MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
    if [[ "$NODE_MAJOR" -ge 18 ]]; then
        printf "  ${GREEN}✓${NC} %-15s v%s\n" "node" "$NODE_VER"
        ((ok++))
    else
        printf "  ${YELLOW}⚠${NC} %-15s v%s (太舊，需要 >= 18)\n" "node" "$NODE_VER"
        ((warn++))
    fi
else
    printf "  ${RED}✗${NC} %-15s 缺失  ${YELLOW}→ 見 references/00-rescue-usb-preparation.md §4${NC}\n" "node"
    ((fail++))
fi

check npm    "npm"    "Node.js 內建，裝 Node 就有"
check claude "claude" "npm install -g @anthropic-ai/claude-code"
check codex  "codex"  "npm install -g @openai/codex (可選)"

# Skill 在不在
echo ""
echo -e "${BOLD}[Skill 安裝狀態]${NC}"
SKILL_PATHS=(
    "$HOME/.claude/skills/windows-rescue-from-linux"
    "$HOME/.config/codex/skills/windows-rescue-from-linux"
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

# 建議
echo ""
if [[ $fail -eq 0 && $warn -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}✓ 環境完整，可以開始救援${NC}"
    echo ""
    echo "下一步：跟 Claude 講使用者的狀況，照 SKILL.md「症狀分流」流程走"
elif [[ $fail -gt 0 ]]; then
    echo -e "${YELLOW}${BOLD}⚠ 有 $fail 個工具缺失${NC}"
    echo ""
    echo "建議跑安裝腳本（會問每一塊要不要裝）："
    echo ""
    echo "  sudo bash scripts/install-rescue-tools.sh"
    echo ""
    echo "或一次裝完："
    echo ""
    echo "  sudo bash scripts/install-rescue-tools.sh --full"
else
    echo -e "${YELLOW}有 $warn 個警告，但可以開始救援${NC}"
fi

# 給 agent 的 hint
if [[ -n "${CLAUDECODE:-}${CODEX:-}" ]]; then
    echo ""
    echo "---"
    echo "AGENT HINT:"
    if [[ $fail -gt 0 ]]; then
        echo "  - 主動詢問使用者是否要跑 install-rescue-tools.sh"
        echo "  - 不要在沒得到使用者明確 yes 之前 sudo apt install"
    fi
    if ! $SKILL_FOUND; then
        echo "  - 提醒使用者把 skill symlink 到 ~/.claude/skills/"
    fi
fi
