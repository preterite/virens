#!/usr/bin/env zsh
# ============================================================================
# VIRENS - ZSH CONFIGURATION (FRAMEWORK BASE)
# ============================================================================
# Version: 3.0
# Purpose: Academic research shell environment with intelligent multi-machine
#          support, modern tooling, and teaching-quality documentation
# Author: VIRENS Project
# License: AGPL-3.0 (code), CC-BY-SA-4.0 (documentation)
# Repository: https://github.com/preterite/virens
#
# This configuration is designed to be:
#   - Fully shareable without exposing personal data
#   - Self-documenting for teaching purposes
#   - Modular and maintainable
#   - Portable across multiple machines
#
# Architecture:
#   ~/.zshrc                         - This file (framework, version controlled)
#   ~/.zshrc.local                   - Personal overrides (gitignored)
#   ~/Local/virens/user1/config/     - User-specific configs
#   ~/Local/virens/virens/           - Framework code
#
# Quick Start:
#   1. Install: Run framework install.sh to create user instance
#   2. Configure: Edit ~/Local/virens/user1/config/*.yaml
#   3. Reload: Run `reload` or restart your shell
# ============================================================================

# ============================================================================
# PERFORMANCE: INSTANT PROMPT
# ============================================================================
# Powerlevel10k instant prompt - must be at the very top
# This enables fast shell startup by showing prompt before full initialization
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# ============================================================================
# ARCHITECTURE DETECTION
# ============================================================================
# Detect CPU architecture for appropriate tool paths (Apple Silicon vs Intel)
export MACHINE_ARCH=$(uname -m)
export IS_ARM=$([[ "$MACHINE_ARCH" == "arm64" ]] && echo "true" || echo "false")

# ============================================================================
# HOMEBREW SETUP
# ============================================================================
# Configure Homebrew based on architecture
if [[ "$IS_ARM" == "true" ]]; then
  # Apple Silicon (M1/M2/M3/M4) - /opt/homebrew
  export HOMEBREW_PREFIX="/opt/homebrew"
else
  # Intel Macs - /usr/local
  export HOMEBREW_PREFIX="/usr/local"
fi

# Add Homebrew to PATH and initialize environment
export PATH="$HOMEBREW_PREFIX/bin:$HOMEBREW_PREFIX/sbin:$PATH"
eval "$(brew shellenv 2>/dev/null)"

# ============================================================================
# VIRENS DIRECTORY STRUCTURE
# ============================================================================
# VIRENS container and framework paths
export VIRENS_HOME="$HOME/Local/virens"
export VIRENS_FRAMEWORK="$VIRENS_HOME/virens"
export VIRENS_ENGINE="$VIRENS_FRAMEWORK/engine"

# Detect user instance (default to user1, or read from ~/.virens pointer)
if [[ -f "$HOME/.virens" ]]; then
  export VIRENS_USER=$(cat "$HOME/.virens")
else
  export VIRENS_USER="$VIRENS_HOME/user1"
fi

# Legacy compatibility (for migration period)
export SRE_HOME="$VIRENS_FRAMEWORK"  # Backward compatibility

# ============================================================================
# PATH CONFIGURATION
# ============================================================================
# Base system paths
export PATH="$HOME/bin:/usr/local/bin:$PATH"

# VIRENS framework binaries
export PATH="$VIRENS_FRAMEWORK/bin:$PATH"

# User instance binaries (custom scripts)
export PATH="$VIRENS_USER/bin:$PATH"

# Development tools
export PATH="/Applications/Sublime Text.app/Contents/SharedSupport/bin:$PATH"

# ============================================================================
# USER CONFIGURATION DIRECTORY
# ============================================================================
# User-specific configuration from VIRENS instance
export VIRENS_CONFIG="$VIRENS_USER/config"

# Create config directory if it doesn't exist (silent, won't break p10k)
[[ -d "$VIRENS_CONFIG" ]] || mkdir -p "$VIRENS_CONFIG" 2>/dev/null

# ============================================================================
# MACHINE IDENTITY & ROLE
# ============================================================================
# Load machine configuration from user instance
if [[ -f "$VIRENS_CONFIG/machine.yaml" ]]; then
  # Parse YAML for machine name and role (simplified parsing)
  export MACHINE_NAME=$(grep '^name:' "$VIRENS_CONFIG/machine.yaml" | sed 's/name: *//' | tr -d '"' 2>/dev/null)
  export MACHINE_ROLE=$(grep '^role:' "$VIRENS_CONFIG/machine.yaml" | sed 's/role: *//' | tr -d '"' 2>/dev/null)
else
  # Auto-detect machine name from system
  export MACHINE_NAME=$(scutil --get ComputerName 2>/dev/null | tr ' ' '-' | tr '[:upper:]' '[:lower:]' || hostname)
  export MACHINE_ROLE="workstation"  # Default role
fi

# ============================================================================
# VIRENS PATHS - FROM USER CONFIG
# ============================================================================
# Load user-specific paths from config
if [[ -f "$VIRENS_CONFIG/paths.yaml" ]]; then
  # Parse paths.yaml for key directories
  # This is basic parsing - proper YAML parser would be better but adds dependency
  export OBSIDIAN_VAULT=$(grep '^obsidian_vault:' "$VIRENS_CONFIG/paths.yaml" | sed 's/obsidian_vault: *//' | tr -d '"' 2>/dev/null)
  export DEVONTHINK_DB=$(grep '^devonthink_database:' "$VIRENS_CONFIG/paths.yaml" | sed 's/devonthink_database: *//' | tr -d '"' 2>/dev/null)
else
  # Set defaults if config doesn't exist
  export OBSIDIAN_VAULT="$VIRENS_USER/obsidian-vault"
  export DEVONTHINK_DB="$HOME/Databases/DEVONthink Local/Resources.dtBase2"
fi

# Convenience aliases for common paths
export ZETTELKASTEN="$OBSIDIAN_VAULT"
export SCHOLAR_VAULT="$OBSIDIAN_VAULT"
export SCHOLAR_INBOX="$OBSIDIAN_VAULT/000_inbox"
export ACADEMIC_HOME="$VIRENS_USER"

# Observatory data paths
export OBSERVATORY_HOME="$VIRENS_USER/observatory"
export OBSERVATORY_DATA="$OBSERVATORY_HOME/data"

# ============================================================================
# FEATURE FLAGS
# ============================================================================
# Load feature configuration from user instance
if [[ -f "$VIRENS_CONFIG/modules.yaml" ]]; then
  # Parse enabled modules (basic parsing)
  export ENABLE_OBSERVATORY=$(grep 'observatory:' "$VIRENS_CONFIG/modules.yaml" | grep 'enabled: true' >/dev/null && echo "true" || echo "false")
else
  # Set sensible defaults
  export ENABLE_LOGGING="true"
  export LOG_LEVEL="info"
  export ENABLE_OBSERVATORY=$([[ "$MACHINE_ROLE" == "hub" ]] && echo "true" || echo "false")
  export ENABLE_COMMAND_TRACKING=$([[ "$MACHINE_ROLE" == "hub" ]] && echo "true" || echo "false")
  export ALERT_MODE=$([[ "$MACHINE_ROLE" == "hub" ]] && echo "comprehensive" || echo "critical_only")
  export AUTO_ACTIVATE_VENV="true"
fi

# ============================================================================
# LOGGING INFRASTRUCTURE (P10K-SAFE)
# ============================================================================
# Initialize logging system if enabled (all silent, won't break p10k)
if [[ "$ENABLE_LOGGING" == "true" ]]; then
  export LOG_DIR="$VIRENS_USER/logs"
  mkdir -p "$LOG_DIR" 2>/dev/null
  
  export ERROR_LOG="$LOG_DIR/error.log"
  export INFO_LOG="$LOG_DIR/info.log"
  export SYNC_LOG="$LOG_DIR/sync.log"
  export COMMAND_LOG="$LOG_DIR/command_history.log"
  
  # Logging functions (safe - no output during definition)
  log_info() {
    [[ -n "$INFO_LOG" ]] && echo "[$(date -Iseconds)] INFO: $*" >> "$INFO_LOG"
  }
  
  log_error() {
    [[ -n "$ERROR_LOG" ]] && echo "[$(date -Iseconds)] ERROR: $*" >> "$ERROR_LOG"
  }
  
  log_sync() {
    [[ -n "$SYNC_LOG" ]] && echo "[$(date -Iseconds)] SYNC: $*" >> "$SYNC_LOG"
  }
fi

# ============================================================================
# OH-MY-ZSH CONFIGURATION
# ============================================================================
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"

# Oh-My-Zsh behavior settings
CASE_SENSITIVE="true"                      # Case-sensitive completion
HYPHEN_INSENSITIVE="true"                  # Treat hyphens and underscores as equivalent
COMPLETION_WAITING_DOTS="true"             # Show dots while waiting for completion
DISABLE_UNTRACKED_FILES_DIRTY="true"       # Faster git status in large repos
HIST_STAMPS="yyyy-mm-dd"                   # History timestamp format

# Plugin configuration
# Note: zsh-syntax-highlighting must be last in the plugins array
plugins=(
    git
    brew
    macos
    python
    pip
    direnv
    fnm
    gh
    colored-man-pages
    extract
    command-not-found
    zsh-autosuggestions
    zsh-syntax-highlighting
)

# Initialize Oh-My-Zsh
source $ZSH/oh-my-zsh.sh

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================
# System locale and editor
export LANG=en_US.UTF-8
export EDITOR='micro'
export VISUAL='micro'
export ARCHFLAGS="-arch $MACHINE_ARCH"

# Git configuration
export GIT_CONFIG_GLOBAL="$HOME/.gitconfig"

# VIRENS environment metadata
export VIRENS_VERSION="3.1"

# ============================================================================
# EZA CONFIGURATION (Modern ls replacement)
# ============================================================================
# Eza is a modern replacement for ls with colors and git integration
if command -v eza >/dev/null; then
  # Basic listing
  alias ls='eza --icons --group-directories-first'
  alias ll='eza --icons --long --header --group-directories-first'
  alias la='eza --icons --long --header --group-directories-first --all'
  
  # Tree views
  alias lt='eza --icons --tree --level=2 --group-directories-first'
  alias lt3='eza --icons --tree --level=3 --group-directories-first'
  alias lta='eza --icons --tree --level=2 --group-directories-first --all'
  
  # With git status
  alias llg='eza --icons --long --header --group-directories-first --git'
  alias lag='eza --icons --long --header --group-directories-first --all --git'
  
  # Detailed file info
  alias lld='eza --icons --long --header --group-directories-first --extended'
fi

# ============================================================================
# BAT CONFIGURATION (Modern cat replacement)
# ============================================================================
# Bat is a cat clone with syntax highlighting and git integration
if command -v bat >/dev/null; then
  export BAT_THEME="Monokai Extended"
  alias cat='bat --style=auto'
  alias catp='bat --style=plain'  # Plain output without line numbers
  alias bathelp='bat --list-themes'
fi

# ============================================================================
# RIPGREP CONFIGURATION (Modern grep replacement)
# ============================================================================
if command -v rg >/dev/null; then
  # Use .gitignore by default
  export RIPGREP_CONFIG_PATH="$HOME/.ripgreprc"
  
  # Create ripgrep config if it doesn't exist (silent)
  if [[ ! -f "$RIPGREP_CONFIG_PATH" ]]; then
    cat > "$RIPGREP_CONFIG_PATH" 2>/dev/null <<'EOF'
# Always show line numbers
--line-number

# Smart case (case-insensitive unless uppercase present)
--smart-case

# Show hidden files
--hidden

# Don't search in .git directories
--glob=!.git/*

# Don't search in node_modules
--glob=!node_modules/*

# Don't search in build artifacts
--glob=!*.pyc
--glob=!__pycache__/*
EOF
  fi
fi

# ============================================================================
# MODERN TOOL INITIALIZATION
# ============================================================================

# ----------------------------------------------------------------------------
# ZOXIDE - Smarter cd command (learns from your navigation patterns)
# ----------------------------------------------------------------------------
if command -v zoxide >/dev/null; then
  eval "$(zoxide init zsh)"
  alias cd='z'      # Replace cd with zoxide
  alias cdi='zi'    # Interactive directory selection
fi

# ----------------------------------------------------------------------------
# FZF - Fuzzy finder for files, history, and more
# ----------------------------------------------------------------------------
if [[ -f ~/.fzf.zsh ]]; then
  source ~/.fzf.zsh
  
  # Use fd for file discovery (respects .gitignore)
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
  
  # Enhanced preview with bat
  export FZF_DEFAULT_OPTS='
    --height 40% 
    --layout=reverse 
    --border=rounded
    --preview "bat --style=numbers --color=always --line-range :500 {}"
    --preview-window=right:60%:wrap
  '
  
  # Use fd for path completion
  _fzf_compgen_path() {
    fd --hidden --follow --exclude ".git" . "$1"
  }
  
  # Use fd for directory completion
  _fzf_compgen_dir() {
    fd --type d --hidden --follow --exclude ".git" . "$1"
  }
fi

# ----------------------------------------------------------------------------
# PYTHON ENVIRONMENT - pyenv
# ----------------------------------------------------------------------------
if [[ -d "$HOME/.pyenv" ]]; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
fi

# Auto-activate VIRENS virtual environment (silent)
if [[ "$AUTO_ACTIVATE_VENV" == "true" ]] && [[ -d "$VIRENS_FRAMEWORK/venv" ]] && [[ -z "$VIRTUAL_ENV" ]]; then
  source "$VIRENS_FRAMEWORK/venv/bin/activate" 2>/dev/null
fi

# ----------------------------------------------------------------------------
# NODE.JS ENVIRONMENT - fnm (Fast Node Manager)
# ----------------------------------------------------------------------------
if command -v fnm >/dev/null; then
  eval "$(fnm env --use-on-cd)"
fi

# ============================================================================
# COMPLETION SYSTEM
# ============================================================================
autoload -Uz compinit && compinit

# Completion styling
zstyle ':completion:*' menu select                          # Interactive menu
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'        # Case-insensitive matching
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"    # Colored completion

# ============================================================================
# HISTORY CONFIGURATION
# ============================================================================
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

# History behavior
setopt SHARE_HISTORY              # Share history between sessions
setopt HIST_IGNORE_DUPS          # Don't record duplicates
setopt HIST_IGNORE_SPACE         # Don't record commands starting with space
setopt HIST_REDUCE_BLANKS        # Remove unnecessary blanks
setopt HIST_VERIFY               # Show command before executing from history

# ============================================================================
# KEY BINDINGS
# ============================================================================
# Arrow keys for history search
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# ============================================================================
# VIRENS CONVENIENCE ALIASES
# ============================================================================
# Quick navigation
alias virens='cd $VIRENS_HOME'
alias vf='cd $VIRENS_FRAMEWORK'
alias vu='cd $VIRENS_USER'
alias vo='cd $OBSIDIAN_VAULT'
alias vobs='cd $OBSERVATORY_HOME'

# Configuration
alias vconf='cd $VIRENS_CONFIG && ll'
alias vedit='micro $VIRENS_CONFIG'

# Logs
alias vlogs='cd $LOG_DIR && ll'
alias vlog='tail -f $INFO_LOG'
alias verr='tail -f $ERROR_LOG'

# System management
alias reload='source ~/.zshrc'
alias vzsh='micro ~/.zshrc'
alias vzlocal='micro ~/.zshrc.local'

# ============================================================================
# COMMAND TRACKING (Documentation & Analytics)
# ============================================================================
# Track command usage for documentation generation (P10K-SAFE)
if [[ "$ENABLE_COMMAND_TRACKING" == "true" ]] && [[ -z "$SANDBOX_MODE" ]]; then
  preexec() {
    if [[ -n "$COMMAND_LOG" ]]; then
      echo "$(date -Iseconds)|$1" >> "$COMMAND_LOG" 2>/dev/null
    fi
  }
fi

# ============================================================================
# SANDBOX MODE (Safe Demo/Teaching Environment)
# ============================================================================
# Enable sandbox mode by setting SANDBOX_MODE=1 before starting shell
# Useful for demonstrations and teaching without risk of data modification
if [[ -n "$SANDBOX_MODE" ]]; then
  export PS1="[SANDBOX] $PS1"
  
  # Override destructive commands
  alias rm='echo "⚠️  rm disabled in sandbox mode"'
  alias mv='echo "⚠️  mv disabled in sandbox mode"'
  alias rmdir='echo "⚠️  rmdir disabled in sandbox mode"'
  
  # Use sandbox directory for VIRENS
  export VIRENS_USER="$VIRENS_HOME/sandbox"
  mkdir -p "$VIRENS_USER" 2>/dev/null
  
  # This output is AFTER instant prompt completes (via precmd)
  _sandbox_warn() {
    if [[ -z "$_SANDBOX_WARNED" ]]; then
      echo ""
      echo "⚠️  SANDBOX MODE ACTIVE - Safe for demonstrations"
      echo ""
      export _SANDBOX_WARNED=1
    fi
  }
  precmd_functions+=(_sandbox_warn)
fi

# ============================================================================
# ITERM2 INTEGRATION
# ============================================================================
if [[ -f "${HOME}/.iterm2_shell_integration.zsh" ]]; then
  source "${HOME}/.iterm2_shell_integration.zsh"
fi

# ============================================================================
# POWERLEVEL10K THEME
# ============================================================================
# Disable configuration wizard (we manage config in .p10k.zsh)
POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true

# Load Powerlevel10k configuration
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# ============================================================================
# LOCAL OVERRIDES (USER-SPECIFIC)
# ============================================================================
# Source personal overrides last (gitignored, machine-specific customizations)
# Use this file for:
#   - Personal aliases
#   - Experimental configurations
#   - Machine-specific tweaks
#   - Sensitive data that shouldn't be in version control
#
# IMPORTANT: ~/.zshrc.local must NOT output anything during sourcing!
# All functions are safe - they only output when CALLED.
if [[ -f "$HOME/.zshrc.local" ]]; then
  source "$HOME/.zshrc.local"
fi

# ============================================================================
# POST-INITIALIZATION DISPLAY
# ============================================================================
# Welcome message moved to ~/.zshrc.local for user customization
# This keeps the framework completely silent for p10k instant prompt

# ============================================================================
# END OF FRAMEWORK CONFIGURATION
# ============================================================================
# VIRENS initialized successfully
# For help: scholar-status
# For configuration: cd $VIRENS_CONFIG
# ============================================================================
