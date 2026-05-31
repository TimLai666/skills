#!/usr/bin/env bash
# install-rescue-tools.sh
# 在 Ubuntu Live USB 上一次裝完 Windows 救援需要的所有工具
#
# 預設行為：互動式詢問每一個區塊要不要裝
# 自動模式：sudo bash install-rescue-tools.sh --auto
# 只裝核心：sudo bash install-rescue-tools.sh --core
# 含 Node：sudo bash install-rescue-tools.sh --with-node
# 全裝：  sudo bash install-rescue-tools.sh --full

set -e

if [[ $EUID -ne 0 ]]; then
    echo "請用 sudo 跑" >&2
    exit 1
fi

# 處理參數
MODE="interactive"
for arg in "$@"; do
    case "$arg" in
        --auto)      MODE="auto" ;;
        --core)      MODE="core" ;;
        --with-node) MODE="with-node" ;;
        --full)      MODE="full" ;;
        --help|-h)
            cat <<'EOF'
用法：
  sudo bash install-rescue-tools.sh             # 互動式（每一塊問一次）
  sudo bash install-rescue-tools.sh --core      # 只裝核心救援工具
  sudo bash install-rescue-tools.sh --with-node # 核心 + Node.js + Claude Code
  sudo bash install-rescue-tools.sh --full      # 全部都裝
  sudo bash install-rescue-tools.sh --auto      # 不問，預設全部裝
EOF
            exit 0
            ;;
    esac
done

LOG="/tmp/rescue-tools-install-$(date +%Y%m%d-%H%M%S).log"
echo "安裝日誌：$LOG"
exec > >(tee -a "$LOG") 2>&1

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[0;33m'; BOLD='\033[1m'; NC='\033[0m'

echo -e "${BOLD}============================================"
echo "  Windows 救援工具 + AI Agent 環境安裝"
echo "  $(date)"
echo -e "  模式: $MODE${NC}"
echo "============================================"

# 詢問函數
ask() {
    local prompt="$1"
    local default="${2:-y}"
    case "$MODE" in
        auto|full) return 0 ;;
        core)
            [[ "$prompt" == *"核心"* ]] && return 0 || return 1 ;;
        with-node)
            [[ "$prompt" == *"核心"* || "$prompt" == *"Node"* || "$prompt" == *"Claude"* ]] && return 0 || return 1 ;;
    esac
    # interactive
    read -rp "$prompt [Y/n] " ans
    ans="${ans:-$default}"
    [[ "$ans" =~ ^[Yy]$ ]]
}

# ============================================
# 1. 檢查網路
# ============================================
echo ""
echo -e "${BOLD}[檢查] 網路連線${NC}"
if ! ping -c 1 -W 3 archive.ubuntu.com >/dev/null 2>&1; then
    echo -e "  ${RED}✗ 連不到 Ubuntu 套件庫${NC}"
    echo "  請確認網路後再試（手機熱點 / 網路線都行）"
    echo ""
    echo "  離線安裝指引見 references/00-rescue-usb-preparation.md §9"
    exit 1
fi
echo -e "  ${GREEN}✓ 網路 OK${NC}"

echo ""
echo -e "${BOLD}[檢查] 更新套件索引${NC}"
apt-get update -qq

# ============================================
# 2. 核心救援工具（必裝）
# ============================================
if ask "[1/5] 安裝核心救援工具（NTFS / chntpw / testdisk / ddrescue / smartctl ...）？"; then
    echo ""
    echo -e "${BOLD}[1/5] 核心救援工具${NC}"

    CORE_PACKAGES=(
        # NTFS
        ntfs-3g

        # Registry / SAM
        chntpw
        libhivex-bin
        libhivex0

        # 分割表 / 檔案系統
        testdisk           # 含 photorec
        gddrescue          # ddrescue 執行檔
        gdisk
        parted
        dosfstools
        mtools
        partclone

        # 開機修復
        efibootmgr
        grub-efi-amd64-bin
        grub-common
        os-prober

        # 磁碟健康
        smartmontools
        nvme-cli
        hdparm

        # 防毒
        clamav
        clamav-freshclam

        # 加密磁碟
        dislocker
        fuse3
        cryptsetup

        # 檔案救援
        foremost
        p7zip-full

        # Windows 鑑識
        python3-evtx
        cabextract

        # 系統工具
        rsync
        pv
        pigz
        tmux
        screen
        mc
        htop
        iotop

        # 硬體偵測
        lshw
        hwinfo
        dmidecode
        pciutils
        usbutils
        inxi
        lm-sensors

        # 記憶體 / CPU 測試
        memtester
        stress-ng

        # 網路
        curl
        wget
        openssh-client
        net-tools
        iproute2

        # 文字工具
        vim
        nano
        less
        tree
        file
        binutils

        # 開發/補裝用
        python3-pip
        git
        build-essential
    )

    DEBIAN_FRONTEND=noninteractive apt-get install -y "${CORE_PACKAGES[@]}" || {
        echo -e "${YELLOW}⚠ 部分套件失敗，繼續...${NC}"
    }
    echo -e "${GREEN}✓ 核心工具裝完${NC}"
fi

# ============================================
# 3. 進階救援工具（可選）
# ============================================
if ask "[2/5] 安裝進階救援工具（rkhunter / yara / wimtools / magic-wormhole ...）？"; then
    echo ""
    echo -e "${BOLD}[2/5] 進階救援工具${NC}"

    EXTRA_PACKAGES=(
        # 進階防毒
        rkhunter
        chkrootkit
        yara

        # 檔案救援
        scalpel
        bulk-extractor

        # Windows 鑑識
        libwin-hivex-perl
        libpff-utils       # Outlook PST 處理

        # Windows 映像
        wimtools

        # 從 Linux 燒 Windows ISO
        woeusb-ng

        # 跨機傳檔
        magic-wormhole
        rclone

        # 監控
        nethogs

        # PE 檔案分析
        pev

        # 進階 registry
        samdump2
        registry-tools

        # 對話框（給 script 用）
        zenity
        whiptail
        dialog
    )

    DEBIAN_FRONTEND=noninteractive apt-get install -y "${EXTRA_PACKAGES[@]}" 2>/dev/null || {
        echo -e "${YELLOW}⚠ 部分進階套件不存在於本版 Ubuntu，跳過${NC}"
    }
    echo -e "${GREEN}✓ 進階工具裝完${NC}"
fi

# ============================================
# 4. Node.js + npm（給 Claude Code / Codex 用）
# ============================================
NODE_INSTALLED=false
if command -v node >/dev/null && [[ $(node -v | sed 's/v//; s/\..*//') -ge 18 ]]; then
    echo ""
    echo -e "${BOLD}[3/5] Node.js 已裝（$(node -v)），跳過${NC}"
    NODE_INSTALLED=true
elif ask "[3/5] 安裝 Node.js 20 LTS（Claude Code / Codex CLI 需要）？"; then
    echo ""
    echo -e "${BOLD}[3/5] 裝 Node.js 20 LTS（NodeSource）${NC}"

    # NodeSource repo
    if curl -fsSL https://deb.nodesource.com/setup_20.x | bash - ; then
        apt-get install -y nodejs
        echo -e "${GREEN}✓ Node.js 裝完：$(node --version)${NC}"
        NODE_INSTALLED=true
    else
        echo -e "${YELLOW}⚠ NodeSource 失敗，改用 apt 預設${NC}"
        apt-get install -y nodejs npm
        if command -v node >/dev/null; then
            echo -e "${GREEN}✓ Node.js 裝完：$(node --version)${NC}"
            NODE_INSTALLED=true
        else
            echo -e "${RED}✗ Node.js 安裝失敗${NC}"
            echo "  手動裝法見 references/00-rescue-usb-preparation.md §4"
        fi
    fi

    # 給「正常使用者」設定 npm 全域目錄到家目錄（避免 sudo 才能裝）
    REAL_USER="${SUDO_USER:-$USER}"
    REAL_HOME=$(eval echo "~$REAL_USER")
    if [[ -d "$REAL_HOME" && "$REAL_USER" != "root" ]]; then
        sudo -u "$REAL_USER" bash -c "
            mkdir -p '$REAL_HOME/.npm-global'
            npm config set prefix '$REAL_HOME/.npm-global'
            if ! grep -q '.npm-global/bin' '$REAL_HOME/.bashrc' 2>/dev/null; then
                echo 'export PATH=\"\$HOME/.npm-global/bin:\$PATH\"' >> '$REAL_HOME/.bashrc'
            fi
        "
        echo "  ✓ 設定 npm 全域目錄 = $REAL_HOME/.npm-global"
        echo "    請執行 'source ~/.bashrc' 或開新 terminal 套用"
    fi
fi

# ============================================
# 5. Claude Code
# ============================================
CLAUDE_INSTALLED=false
if command -v claude >/dev/null; then
    echo ""
    echo -e "${BOLD}[4/5] Claude Code 已裝（$(claude --version 2>/dev/null | head -1)），跳過${NC}"
    CLAUDE_INSTALLED=true
elif $NODE_INSTALLED && ask "[4/5] 安裝 Claude Code（Anthropic 官方 CLI）？"; then
    echo ""
    echo -e "${BOLD}[4/5] 裝 Claude Code${NC}"

    REAL_USER="${SUDO_USER:-$USER}"
    if [[ "$REAL_USER" != "root" ]]; then
        # 以正常使用者安裝（不用 sudo，裝到 ~/.npm-global）
        sudo -u "$REAL_USER" bash -c '
            export PATH="$HOME/.npm-global/bin:$PATH"
            npm install -g @anthropic-ai/claude-code
        ' && {
            echo -e "${GREEN}✓ Claude Code 裝完${NC}"
            echo "  執行檔：$(eval echo "~$REAL_USER")/.npm-global/bin/claude"
            echo "  首次跑：claude  ← 會引導登入或設 API key"
            CLAUDE_INSTALLED=true
        } || {
            echo -e "${YELLOW}⚠ Claude Code 安裝失敗，可以手動：npm install -g @anthropic-ai/claude-code${NC}"
        }
    else
        npm install -g @anthropic-ai/claude-code && CLAUDE_INSTALLED=true
    fi
fi

# ============================================
# 6. Codex CLI（可選）
# ============================================
if command -v codex >/dev/null; then
    echo ""
    echo -e "${BOLD}[5/5] Codex CLI 已裝，跳過${NC}"
elif $NODE_INSTALLED && ask "[5/5] 安裝 Codex CLI（OpenAI 官方 CLI，可選）？"; then
    echo ""
    echo -e "${BOLD}[5/5] 裝 Codex CLI${NC}"

    REAL_USER="${SUDO_USER:-$USER}"
    if [[ "$REAL_USER" != "root" ]]; then
        sudo -u "$REAL_USER" bash -c '
            export PATH="$HOME/.npm-global/bin:$PATH"
            npm install -g @openai/codex
        ' && {
            echo -e "${GREEN}✓ Codex CLI 裝完${NC}"
            echo "  首次跑：codex  ← 會引導設 OpenAI API key"
        } || {
            echo -e "${YELLOW}⚠ Codex 安裝失敗${NC}"
        }
    else
        npm install -g @openai/codex
    fi
fi

# ============================================
# 7. 初始化 ClamAV 病毒碼
# ============================================
echo ""
echo -e "${BOLD}[後續] 初始化 ClamAV 病毒碼${NC}"
systemctl stop clamav-freshclam 2>/dev/null || true
freshclam --quiet 2>&1 | tail -3 || echo "  ⚠ freshclam 失敗，之後手動 sudo freshclam"

# ============================================
# 8. 偵測溫度感應器（給 lm-sensors 用）
# ============================================
echo ""
echo -e "${BOLD}[後續] 偵測溫度感應器${NC}"
yes "" | sensors-detect --auto >/dev/null 2>&1 || true
echo "  完成"

# ============================================
# 9. 把 skill 連結到 ~/.claude/skills
# ============================================
SKILL_DIR=$(dirname "$(realpath "$0")")
SKILL_DIR=$(dirname "$SKILL_DIR")  # 跳到 skill 根目錄
if [[ -f "$SKILL_DIR/SKILL.md" && $CLAUDE_INSTALLED == true ]]; then
    REAL_USER="${SUDO_USER:-$USER}"
    REAL_HOME=$(eval echo "~$REAL_USER")
    if ask "[後續] 把這個 skill 安裝到 $REAL_HOME/.claude/skills/？"; then
        TARGET="$REAL_HOME/.claude/skills/windows-rescue-from-linux"
        sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/.claude/skills"
        if [[ -e "$TARGET" ]]; then
            echo "  $TARGET 已存在，跳過（用 rm -rf 後重跑可覆蓋）"
        else
            sudo -u "$REAL_USER" ln -s "$SKILL_DIR" "$TARGET"
            echo -e "  ${GREEN}✓ 已建立 symlink：$TARGET → $SKILL_DIR${NC}"
        fi
    fi
fi

# ============================================
# 10. 最終驗證
# ============================================
echo ""
echo -e "${BOLD}============================================"
echo "  安裝完成 - 工具驗證"
echo -e "============================================${NC}"

echo ""
echo "救援核心工具："
for cmd in ntfsfix chntpw hivexsh testdisk photorec ddrescue \
           smartctl clamscan dislocker efibootmgr rsync; do
    if command -v "$cmd" >/dev/null 2>&1; then
        printf "  ${GREEN}✓${NC} %-15s  %s\n" "$cmd" "$(command -v "$cmd")"
    else
        printf "  ${RED}✗${NC} %-15s  缺失\n" "$cmd"
    fi
done

echo ""
echo "AI agent 環境："
for cmd in node npm claude codex; do
    if command -v "$cmd" >/dev/null 2>&1; then
        VER=$($cmd --version 2>/dev/null | head -1 || echo "?")
        printf "  ${GREEN}✓${NC} %-10s  %s\n" "$cmd" "$VER"
    else
        printf "  ${YELLOW}○${NC} %-10s  未裝（可選）\n" "$cmd"
    fi
done

echo ""
echo "便利工具："
for cmd in tmux mc pv pigz htop magic-wormhole; do
    if command -v "$cmd" >/dev/null 2>&1; then
        printf "  ${GREEN}✓${NC} %s\n" "$cmd"
    fi
done

echo ""
echo -e "${BOLD}下一步：${NC}"
echo "  1. source ~/.bashrc      # 套用 PATH 改動"
echo "  2. claude                # 首次設定 Claude Code（要 API key）"
echo "  3. 跟 Claude 說『幫我救 Windows』，它會自動載入這個 skill"
echo ""
echo "詳細指南：references/00-rescue-usb-preparation.md"
echo "安裝日誌：$LOG"
