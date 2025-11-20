#!/usr/bin/env zsh
# VIRENS Framework Core Shell Functions
# These functions are sourced by user dotfiles

# Logging functions
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $*" >&2
}

log_success() {
    echo "[SUCCESS] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

log_warning() {
    echo "[WARNING] $(date '+%Y-%m-%d %H:%M:%S') - $*"
}

# Path helpers (updated for Option B structure)
virens_framework() {
    # .virens points to user instance (e.g., ~/Local/virens/user1)
    # Framework is sibling: ~/Local/virens/virens
    if [ -f "$HOME/.virens" ]; then
        local user_instance=$(cat "$HOME/.virens")
        local virens_container=$(dirname "$user_instance")
        echo "$virens_container/virens"
    else
        echo "$HOME/Local/virens/virens"
    fi
}

virens_user() {
    # Returns user instance directory
    if [ -f "$HOME/.virens" ]; then
        cat "$HOME/.virens"
    else
        echo "$HOME/Local/virens/user1"
    fi
}

# Module helpers
virens_module_enabled() {
    # Check if a module is enabled
    local module=$1
    local user_dir=$(virens_user)
    
    if [ -f "$user_dir/config/modules.yaml" ]; then
        grep -q "^  - $module$" "$user_dir/config/modules.yaml"
        return $?
    fi
    return 1
}

# Observatory helpers
observatory_db() {
    # Returns path to Observatory database
    local user_dir=$(virens_user)
    echo "$user_dir/observatory/data/observatory.db"
}

# Quick navigation
alias cdv='cd $(virens_framework)'
alias cdu='cd $(virens_user)'
alias cdo='cd $(virens_user)/obsidian-vault'

# Framework updates
virens_update() {
    local framework_dir=$(virens_framework)
    cd "$framework_dir" || return 1
    
    log_info "Updating VIRENS framework..."
    git pull origin main
    log_success "Framework updated to $(cat VERSION)"
}

# Module management
virens_list_modules() {
    local user_dir=$(virens_user)
    
    if [ -f "$user_dir/config/modules.yaml" ]; then
        echo "Enabled modules:"
        grep "^  - " "$user_dir/config/modules.yaml" | sed 's/^  - /  ✓ /'
    else
        log_error "No modules.yaml found"
    fi
}
