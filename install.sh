#!/usr/bin/env bash
# VIRENS Installation Script
# Creates a new user instance from the template

set -e

# Determine paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VIRENS_CONTAINER="$(dirname "$SCRIPT_DIR")"
ENGINE_DIR="$SCRIPT_DIR/engine"

echo "═══════════════════════════════════════════════════════════"
echo "              VIRENS INSTALLATION"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Framework: $SCRIPT_DIR"
echo "Container: $VIRENS_CONTAINER"
echo ""

# Step 1: Bootstrap
echo "Step 1: Checking dependencies..."
bash "$ENGINE_DIR/infrastructure/install/bootstrap.sh"

# Step 2: Dependency check
echo ""
echo "Step 2: Verifying dependencies..."
if ! bash "$ENGINE_DIR/infrastructure/install/dependency-check.sh"; then
    echo ""
    echo "❌ Dependency check failed. Please install missing dependencies and try again."
    exit 1
fi

# Step 3: Determine user instance path
echo ""
echo "Step 3: Setting up user instance..."

# Check if user instances already exist
USER_DIR="$VIRENS_CONTAINER"
NEXT_USER=1

if [ -d "$USER_DIR" ]; then
    # Count existing user directories
    while [ -d "$USER_DIR/user$NEXT_USER" ]; do
        NEXT_USER=$((NEXT_USER + 1))
    done
fi

USER_INSTANCE="$USER_DIR/user$NEXT_USER"

echo "Creating user instance: $USER_INSTANCE"

# Ask user for confirmation
read -p "Is this location correct? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "Enter desired user instance path: " CUSTOM_PATH
    USER_INSTANCE="${CUSTOM_PATH/#\~/$HOME}"
fi

# Create user instance directory
mkdir -p "$USER_INSTANCE"

echo "✅ User instance will be created at: $USER_INSTANCE"

# Step 4: Copy template
echo ""
echo "Step 4: Copying template..."

# Copy all template contents
cp -r "$ENGINE_DIR/template/"* "$USER_INSTANCE/"

# Handle .gitignore specially (remove .template extension)
if [ -f "$USER_INSTANCE/.gitignore.template" ]; then
    mv "$USER_INSTANCE/.gitignore.template" "$USER_INSTANCE/.gitignore"
fi

echo "✅ Template copied"

# Step 5: Remove .template extensions from config files
echo ""
echo "Step 5: Setting up configuration files..."

cd "$USER_INSTANCE/config"
for file in *.template; do
    if [ -f "$file" ]; then
        basename="${file%.template}"
        mv "$file" "$basename"
        echo "  Created config/$basename"
    fi
done

cd "$USER_INSTANCE/dotfiles"
for file in *.template; do
    if [ -f "$file" ]; then
        basename="${file%.template}"
        mv "$file" "$basename"
        echo "  Created dotfiles/$basename"
    fi
done

echo "✅ Configuration files ready for customization"

# Step 6: Collect user information
echo ""
echo "Step 6: Configuring user information..."
echo ""
echo "Please provide your information (will be saved to config/user.yaml):"
echo ""

read -p "Your full name: " USER_NAME
read -p "Your email: " USER_EMAIL
read -p "Your institution: " USER_INSTITUTION
read -p "Your department (optional): " USER_DEPARTMENT

# Update user.yaml with provided information
cd "$USER_INSTANCE"
cat > config/user.yaml << USEREOF
# VIRENS User Configuration

user:
  name: "$USER_NAME"
  email: "$USER_EMAIL"
  institution: "$USER_INSTITUTION"
  department: "$USER_DEPARTMENT"
  orcid: ""  # Optional ORCID identifier
  
preferences:
  default_citation_style: "chicago-note-bibliography"
  obsidian_daily_note_format: "YYYY-MM-DD"
  observatory_update_frequency: "weekly"
USEREOF

echo "✅ User configuration saved"

# Step 7: Configure machine
echo ""
echo "Step 7: Configuring machine..."
echo ""

MACHINE_NAME=$(scutil --get ComputerName 2>/dev/null || hostname)
echo "Detected machine name: $MACHINE_NAME"
read -p "Use this name? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter machine name: " MACHINE_NAME
fi

echo ""
echo "Is this machine a hub or workstation?"
echo "  Hub: Central machine running Observatory dashboard, primary automation"
echo "  Workstation: Syncs with hub, full research capabilities"
echo ""
read -p "Machine role (hub/workstation) [workstation]: " MACHINE_ROLE
MACHINE_ROLE=${MACHINE_ROLE:-workstation}

cat > config/machine.yaml << MACHINEEOF
# Machine Configuration

role: $MACHINE_ROLE
name: $MACHINE_NAME

capabilities:
  observatory_dashboard: true
  handles_automation: true
  primary_research: true
MACHINEEOF

echo "✅ Machine configuration saved"

# Step 8: Create symlinks
echo ""
echo "Step 8: Creating symlinks..."
bash "$ENGINE_DIR/infrastructure/install/symlink-manager.sh" "$USER_INSTANCE"

# Step 9: Initialize git repository for user instance
echo ""
echo "Step 9: Initializing user instance repository..."
cd "$USER_INSTANCE"

git init
git add .
git commit -m "Initial user instance from VIRENS template

User: $USER_NAME
Email: $USER_EMAIL
Institution: $USER_INSTITUTION
Machine: $MACHINE_NAME ($MACHINE_ROLE)
"

echo "✅ User instance repository initialized"

# Step 10: Create machine identity
echo ""
echo "Step 10: Creating machine identity..."

mkdir -p "machines/$MACHINE_NAME"
cat > "machines/$MACHINE_NAME/identity.json" << IDENTITYEOF
{
  "name": "$MACHINE_NAME",
  "role": "$MACHINE_ROLE",
  "user": "$USER_NAME",
  "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "virens_version": "$(cat "$SCRIPT_DIR/VERSION" 2>/dev/null || echo "unknown")"
}
IDENTITYEOF

git add "machines/$MACHINE_NAME"
git commit -m "Add $MACHINE_NAME machine identity"

echo "✅ Machine identity created"

# Final summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "              INSTALLATION COMPLETE!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "You now have TWO Git repositories:"
echo ""
echo "1. VIRENS Framework (public):"
echo "   Location: $SCRIPT_DIR"
echo "   Purpose: The shared framework that runs VIRENS"
echo "   Updates: Run 'virens-update' to get new features"
echo ""
echo "2. Your User Instance (private):"
echo "   Location: $USER_INSTANCE"
echo "   Purpose: Your personal research data and configurations"
echo "   Updates: You control this - push to your own private remote"
echo ""
echo "Keep these separate! Your private data will never be pushed"
echo "to the public VIRENS repository."
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit your configuration:"
echo "   cd $USER_INSTANCE/config"
echo "   # Customize modules.yaml, observatory.yaml, paths.yaml"
echo ""
echo "2. Restart your shell:"
echo "   exec zsh"
echo ""
echo "3. Verify installation:"
echo "   scholar-status"
echo ""
echo "4. (Optional) Set up Observatory:"
echo "   # Add your GitHub token to config/observatory.yaml"
echo "   # Then run: observatory-configure"
echo ""
echo "5. (Optional) Create private Git remote:"
echo "   cd $USER_INSTANCE"
echo "   git remote add origin git@github.com:yourusername/my-research.git"
echo "   git push -u origin main"
echo ""
echo "Documentation: $ENGINE_DIR/docs/"
echo ""
echo "═══════════════════════════════════════════════════════════"
