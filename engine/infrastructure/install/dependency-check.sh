#!/usr/bin/env bash
# VIRENS Dependency Checker
# Verifies all required tools are installed

set -e

echo "═══════════════════════════════════════════════════════════"
echo "          VIRENS DEPENDENCY CHECK"
echo "═══════════════════════════════════════════════════════════"
echo ""

MISSING_DEPS=()

# Check each dependency
check_command() {
    if command -v "$1" &> /dev/null; then
        echo "✅ $1"
    else
        echo "❌ $1 (missing)"
        MISSING_DEPS+=("$1")
    fi
}

echo "Core Tools:"
check_command brew
check_command git
check_command zsh
check_command fd
check_command rg
check_command tree
check_command python3
check_command pandoc

echo ""
echo "Optional Tools:"
if command -v gh &> /dev/null; then
    echo "✅ gh (GitHub CLI)"
else
    echo "⚪ gh (GitHub CLI - optional, install with: brew install gh)"
fi

# Summary
echo ""
if [ ${#MISSING_DEPS[@]} -eq 0 ]; then
    echo "✅ All required dependencies installed"
    exit 0
else
    echo "❌ Missing dependencies: ${MISSING_DEPS[*]}"
    echo ""
    echo "Install with:"
    echo "  brew install ${MISSING_DEPS[*]}"
    exit 1
fi
