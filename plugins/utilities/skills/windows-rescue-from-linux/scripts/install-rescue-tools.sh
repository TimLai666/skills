#!/usr/bin/env bash
# Ubuntu/Debian 救援工具安裝；只安裝選定群組，不修改 AI 設定或啟動硬體測試。
set -o pipefail
usage() {
    echo "用法：sudo bash $0 [--core|--full|--auto|--group NAME]"
    echo "群組：core registry recovery boot malware bitlocker image diagnostics"
    echo "無參數會詢問群組；--full/--auto 選全部救援群組。AI CLI 請依準備指南另裝。"
}
GROUPS_SELECTED=()
while (( $# )); do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        --core) GROUPS_SELECTED+=(core) ;;
        --full|--auto) GROUPS_SELECTED+=(core registry recovery boot malware bitlocker image diagnostics) ;;
        --group) shift; [[ $# -gt 0 ]] || { usage; exit 2; }; GROUPS_SELECTED+=("$1") ;;
        --with-node) echo "--with-node 不再安裝全域 AI 環境；依 references/00-rescue-usb-preparation.md 選擇 CLI。" >&2; exit 2 ;;
        *) usage; exit 2 ;;
    esac
    shift
done
if [[ ${#GROUPS_SELECTED[@]} -eq 0 ]]; then
    for group in core registry recovery boot malware bitlocker image diagnostics; do
        read -rp "安裝 $group 工具？[y/N] " answer || answer=n
        [[ "$answer" =~ ^[Yy]$ ]] && GROUPS_SELECTED+=("$group")
    done
fi
PACKAGES=()
COMMANDS=()
for group in "${GROUPS_SELECTED[@]}"; do
    case "$group" in
        core) PACKAGES+=(ntfs-3g rsync smartmontools tmux); COMMANDS+=(ntfsfix rsync smartctl tmux) ;;
        registry) PACKAGES+=(chntpw libhivex-bin libwin-hivex-perl); COMMANDS+=(chntpw hivexsh hivexregedit) ;;
        recovery) PACKAGES+=(gddrescue testdisk partclone); COMMANDS+=(ddrescue testdisk photorec) ;;
        boot) PACKAGES+=(efibootmgr gdisk dosfstools mtools); COMMANDS+=(efibootmgr sgdisk fsck.fat) ;;
        malware) PACKAGES+=(clamav clamav-freshclam yara); COMMANDS+=(clamscan freshclam yara) ;;
        bitlocker) PACKAGES+=(dislocker cryptsetup); COMMANDS+=(dislocker cryptsetup) ;;
        image) PACKAGES+=(wimtools cabextract); COMMANDS+=(wimlib-imagex cabextract) ;;
        diagnostics) PACKAGES+=(nvme-cli python3-evtx pciutils usbutils dmidecode); COMMANDS+=(nvme lspci lsusb dmidecode) ;;
        *) echo "未知群組：$group" >&2; exit 2 ;;
    esac
done
if [[ ${#PACKAGES[@]} -eq 0 ]]; then echo "未選取套件，未進行安裝。"; exit 0; fi
[[ $EUID -eq 0 ]] || { echo "請用 sudo 執行安裝" >&2; exit 1; }
command -v apt-get >/dev/null || { echo "此腳本需要 apt-get；其他發行版請依工具目錄安裝。" >&2; exit 1; }
LOG=$(mktemp /tmp/rescue-tools-install.XXXXXX) || exit 1
FAILED=0
echo "安裝日誌：$LOG"
echo "選取套件：${PACKAGES[*]}"
if ! apt-get update 2>&1 | tee -a "$LOG"; then
    echo "套件索引更新失敗，未繼續安裝。" >&2
    exit 1
fi
# 逐一安裝，單一套件缺少不阻擋其他已選套件；最後統一回報失敗。
for package in "${PACKAGES[@]}"; do
    if ! DEBIAN_FRONTEND=noninteractive apt-get install -y "$package" 2>&1 | tee -a "$LOG"; then
        echo "安裝失敗：$package" >&2
        FAILED=1
    fi
done
for cmd in "${COMMANDS[@]}"; do
    if command -v "$cmd" >/dev/null; then
        echo "可用：$cmd"
    else
        echo "驗證失敗：找不到 $cmd" >&2
        FAILED=1
    fi
done
if (( FAILED )); then echo "安裝未全部完成，請查看日誌。" >&2; exit 1; fi
echo "選取工具安裝與執行檔檢查完成。病毒碼更新另依掃描需求執行。"
