#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# unlock.sh — Samsung FRP Bypass via ADB
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

RED='\033[0;31m'
GRN='\033[0;32m'
CYN='\033[0;36m'
YLW='\033[0;33m'
RST='\033[0m'

log()  { echo -e "${CYN}[*]${RST} $1"; }
ok()   { echo -e "${GRN}[✓]${RST} $1"; }
warn() { echo -e "${YLW}[!]${RST} $1"; }
die()  { echo -e "${RED}[✗]${RST} $1" >&2; exit 1; }

# ── Preflight ────────────────────────────────────────────────────────────────

command -v adb &>/dev/null || die "adb not found. Install Android platform-tools and add to PATH."

log "Waiting for ADB device..."
adb wait-for-device || die "No device detected."

DEVICE=$(adb get-serialno 2>/dev/null || echo "unknown")
ok "Device connected: ${DEVICE}"

# ── Helper ───────────────────────────────────────────────────────────────────

execute_adb_command() {
    local cmd="$1"
    local desc="${2:-$1}"
    log "Running: ${desc}"
    if adb shell "$cmd"; then
        ok "Done: ${desc}"
    else
        warn "Command may have failed (non-zero exit): ${desc}"
    fi
}

# ── FRP Bypass Sequence ──────────────────────────────────────────────────────

echo ""
echo -e "${CYN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
echo -e "${CYN}  Samsung FRP Bypass                              ${RST}"
echo -e "${CYN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}"
echo ""

execute_adb_command \
    "settings put global setup_wizard_has_run 1" \
    "Mark setup wizard as complete"

execute_adb_command \
    "settings put secure user_setup_complete 1" \
    "Mark user setup as complete"

execute_adb_command \
    "content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1" \
    "Set DEVICE_PROVISIONED"

execute_adb_command \
    "content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1" \
    "Set user_setup_complete (secure)"

execute_adb_command \
    "content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1" \
    "Allow non-market app installs"

execute_adb_command \
    "am start -c android.intent.category.HOME -a android.intent.action.MAIN" \
    "Return to home screen"

log "Waiting 5 seconds for home screen to settle..."
sleep 5

execute_adb_command \
    "am start -n com.android.settings/com.android.settings.Settings" \
    "Open Android Settings"

log "Waiting 5 seconds for Settings to load..."
sleep 5

echo ""
warn "In Settings, navigate to:  Backup and reset → Factory data reset"
warn "Complete the factory reset, then the device will reboot unlocked."
echo ""

read -r -p "$(echo -e "${YLW}Press Enter to reboot the device now, or Ctrl+C to cancel...${RST}")"

execute_adb_command "reboot" "Reboot device"

echo ""
ok "FRP bypass sequence complete."
