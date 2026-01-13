#!/usr/bin/env zsh
# ============================================================================
# VIRENS - ZSH PROFILE (FRAMEWORK BASE)
# ============================================================================
# This file is sourced for login shells before .zshrc
# Use this for:
#   - Setting up $PATH
#   - Environment variables needed by GUI apps
#   - One-time login shell initialization
#
# Keep this file minimal and fast - it runs before .zshrc
# ============================================================================

# ============================================================================
# PYTHON 3.13 PATH (For ML/AI Libraries)
# ============================================================================
# Python 3.13 required for: PyTorch, TensorFlow, transformers
# Python 3.14 has compatibility issues with ML libraries on macOS
if [[ -d "/Library/Frameworks/Python.framework/Versions/3.13" ]]; then
  export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"
fi

# ============================================================================
# HOMEBREW (Early initialization for PATH)
# ============================================================================
# Detect architecture and set Homebrew prefix
if [[ $(uname -m) == "arm64" ]]; then
  export HOMEBREW_PREFIX="/opt/homebrew"
else
  export HOMEBREW_PREFIX="/usr/local"
fi

# Add Homebrew to PATH early
export PATH="$HOMEBREW_PREFIX/bin:$HOMEBREW_PREFIX/sbin:$PATH"

# ============================================================================
# VIRENS PATHS (Early setup)
# ============================================================================
export VIRENS_HOME="$HOME/Local/virens"
export VIRENS_FRAMEWORK="$VIRENS_HOME/virens"

# Detect user instance
if [[ -f "$HOME/.virens" ]]; then
  export VIRENS_USER=$(cat "$HOME/.virens")
else
  export VIRENS_USER="$VIRENS_HOME/user1"
fi

# Add VIRENS binaries to PATH
export PATH="$VIRENS_FRAMEWORK/bin:$VIRENS_USER/bin:$PATH"

# ============================================================================
# GUI APPLICATION ENVIRONMENT
# ============================================================================
# These variables are inherited by GUI applications launched from Finder

# Default editor for GUI apps
export EDITOR='micro'
export VISUAL='micro'

# Language settings
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# ============================================================================
# LOCAL PROFILE OVERRIDES
# ============================================================================
# Source user-specific profile additions
if [[ -f "$HOME/.zprofile.local" ]]; then
  source "$HOME/.zprofile.local"
fi

# ============================================================================
# END OF FRAMEWORK PROFILE
# ============================================================================
