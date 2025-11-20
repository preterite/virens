#!/usr/bin/env zsh
# VIRENS Logging System

# Log directory
VIRENS_LOG_DIR="${VIRENS_LOG_DIR:-$HOME/.local/share/virens/logs}"
mkdir -p "$VIRENS_LOG_DIR"

# Current log file
VIRENS_LOG_FILE="$VIRENS_LOG_DIR/virens-$(date +%Y%m%d).log"

# Logging function with file output
log_to_file() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >> "$VIRENS_LOG_FILE"
}

# Enhanced logging functions
log_info() {
    echo "[INFO] $*"
    log_to_file "INFO" "$*"
}

log_error() {
    echo "[ERROR] $*" >&2
    log_to_file "ERROR" "$*"
}

log_success() {
    echo "[SUCCESS] $*"
    log_to_file "SUCCESS" "$*"
}

log_warning() {
    echo "[WARNING] $*"
    log_to_file "WARNING" "$*"
}

# Log rotation (keep last 30 days)
cleanup_old_logs() {
    find "$VIRENS_LOG_DIR" -name "virens-*.log" -mtime +30 -delete 2>/dev/null
}

cleanup_old_logs
