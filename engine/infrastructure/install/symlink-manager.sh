#!/usr/bin/env bash
# VIRENS Symlink Manager
# Creates symlinks from home directory to user instance dotfiles

set -e

USER_INSTANCE=${1:-"$HOME/Local/virens/user1"}
DOTFILES_DIR="$USER_INSTANCE/dotfiles"

echo "═══════════════════════════════════════════════════════════"
echo "              VIRENS SYMLINK MANAGER"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "User instance: $USER_INSTANCE"
echo "Dotfiles directory: $DOTFILES_DIR"
echo ""

# Check if dotfiles directory exists
if [ ! -d "$DOTFILES_DIR" ]; then
    echo "❌ Dotfiles directory not found: $DOTFILES_DIR"
    exit 1
fi

# Dotfiles to symlink
DOTFILES=(
    ".zshrc"
    ".zshrc.local"
    ".zprofile"
    ".gitconfig"
    ".p10k.zsh"
)

# Create .virens pointer file
echo "$USER_INSTANCE" > "$HOME/.virens"
echo "✅ Created $HOME/.virens pointer"

# Create symlinks
for dotfile in "${DOTFILES[@]}"; do
    SOURCE="$DOTFILES_DIR/$dotfile"
    TARGET="$HOME/$dotfile"
    
    if [ -f "$SOURCE" ]; then
        # Backup existing file if not already a symlink
        if [ -f "$TARGET" ] && [ ! -L "$TARGET" ]; then
            echo "  Backing up existing $dotfile to ${dotfile}.backup"
            mv "$TARGET" "${TARGET}.backup"
        fi
        
        # Remove existing symlink if present
        [ -L "$TARGET" ] && rm "$TARGET"
        
        # Create symlink
        ln -s "$SOURCE" "$TARGET"
        echo "✅ Linked $dotfile"
    else
        echo "⚠️  $SOURCE not found, skipping"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Symlinks created! Restart your shell to apply changes."
echo "═══════════════════════════════════════════════════════════"
