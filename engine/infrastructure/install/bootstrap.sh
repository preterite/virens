#!/usr/bin/env bash
# VIRENS Bootstrap Script
# First-run system setup

set -e

FRAMEWORK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../.." && pwd )"

echo "═══════════════════════════════════════════════════════════"
echo "              VIRENS BOOTSTRAP"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found"
    echo "Install from: https://brew.sh"
    exit 1
fi
echo "✅ Homebrew installed"

# Check for Git
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    brew install git
fi
echo "✅ Git available"

# Check for fd (modern find)
if ! command -v fd &> /dev/null; then
    echo "Installing fd..."
    brew install fd
fi
echo "✅ fd available"

# Check for ripgrep
if ! command -v rg &> /dev/null; then
    echo "Installing ripgrep..."
    brew install ripgrep
fi
echo "✅ ripgrep available"

# Check for Python 3.13+
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    brew install python@3.13
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}' | cut -d. -f1,2)
echo "✅ Python $PYTHON_VERSION available"

# Check for pandoc
if ! command -v pandoc &> /dev/null; then
    echo "Installing pandoc..."
    brew install pandoc pandoc-citeproc
fi
echo "✅ Pandoc available"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Bootstrap complete! Ready for installation."
echo "═══════════════════════════════════════════════════════════"
