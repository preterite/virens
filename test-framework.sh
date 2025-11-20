echo "═══════════════════════════════════════════════════════════"
echo "          VIRENS FRAMEWORK TEST"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Step 1: Verify framework structure
echo "Step 1: Verifying framework structure..."
echo ""

REQUIRED_DIRS=(
    "engine/infrastructure/core"
    "engine/infrastructure/install"
    "engine/framework/config"
    "engine/framework/modules"
    "engine/framework/bin"
    "engine/template/config"
    "engine/template/dotfiles"
    "engine/template/obsidian-vault"
    "engine/docs/legal"
)

ALL_PRESENT=true
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir (missing)"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ Framework structure incomplete"
    exit 1
fi

echo ""
echo "✅ Framework structure complete"

# Step 2: Verify license files
echo ""
echo "Step 2: Verifying license files..."
echo ""

if [ -f "LICENSE" ]; then
    echo "  ✅ LICENSE (AGPL-3.0)"
else
    echo "  ❌ LICENSE missing"
    ALL_PRESENT=false
fi

if [ -f "LICENSE-DOCS" ]; then
    echo "  ✅ LICENSE-DOCS (CC-BY-SA-4.0)"
else
    echo "  ❌ LICENSE-DOCS missing"
    ALL_PRESENT=false
fi

if [ -f "CONTRIBUTING.md" ]; then
    echo "  ✅ CONTRIBUTING.md"
else
    echo "  ❌ CONTRIBUTING.md missing"
    ALL_PRESENT=false
fi

# Check legal docs
LEGAL_DOCS=("index.md" "license-explained.md" "for-users.md" "for-institutions.md" "for-consultants.md" "for-developers.md" "faq.md")
for doc in "${LEGAL_DOCS[@]}"; do
    if [ -f "engine/docs/legal/$doc" ]; then
        echo "  ✅ legal/$doc"
    else
        echo "  ❌ legal/$doc missing"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ License files incomplete"
    exit 1
fi

echo ""
echo "✅ License files complete"

# Step 3: Check for personal data in Observatory
echo ""
echo "Step 3: Checking for personal data in Observatory fetchers..."
echo ""

FETCHER_DIR="engine/framework/modules/observatory/fetchers"
PERSONAL_DATA_FOUND=false

if rg -q "mike\.edwards@wsu\.edu|preterite" "$FETCHER_DIR" 2>/dev/null; then
    echo "  ❌ Found personal data in fetchers:"
    rg "mike\.edwards@wsu\.edu|preterite" "$FETCHER_DIR"
    PERSONAL_DATA_FOUND=true
else
    echo "  ✅ No email/username personal data found"
fi

if rg -q "scholar.*virens.*rhetoric.*composition" "$FETCHER_DIR" 2>/dev/null; then
    echo "  ❌ Found hardcoded repo names/keywords"
    PERSONAL_DATA_FOUND=true
else
    echo "  ✅ No hardcoded repo names found"
fi

if [ "$PERSONAL_DATA_FOUND" = true ]; then
    echo ""
    echo "⚠️  Personal data found in framework"
    echo "This should be cleaned before committing"
else
    echo ""
    echo "✅ Framework clean of personal data"
fi

# Step 4: Verify config loading in fetchers
echo ""
echo "Step 4: Verifying config loading in Observatory fetchers..."
echo ""

for fetcher in crossref.py openalex.py github.py; do
    if [ -f "$FETCHER_DIR/$fetcher" ]; then
        if grep -q "get_user_config" "$FETCHER_DIR/$fetcher"; then
            echo "  ✅ $fetcher has config loading"
        else
            echo "  ❌ $fetcher missing config loading"
            ALL_PRESENT=false
        fi
    fi
done

if grep -q "GITHUB_USERNAME\|ACADEMIC_KEYWORDS\|TRACKED_REPOS" "$FETCHER_DIR/github.py"; then
    echo "  ✅ github.py has GitHub-specific config"
else
    echo "  ❌ github.py missing GitHub config"
    ALL_PRESENT=false
fi

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ Observatory fetchers not properly configured"
    exit 1
fi

echo ""
echo "✅ Observatory fetchers properly configured"

# Step 5: Verify command-line tools
echo ""
echo "Step 5: Verifying command-line tools..."
echo ""

BIN_DIR="engine/framework/bin"
TOOLS=("scholar-status" "virens-update" "virens-enable" "virens-disable" "observatory-configure" "observatory-start")

for tool in "${TOOLS[@]}"; do
    if [ -x "$BIN_DIR/$tool" ]; then
        # Check syntax
        if zsh -n "$BIN_DIR/$tool" 2>/dev/null; then
            echo "  ✅ $tool (executable, no syntax errors)"
        else
            echo "  ⚠️  $tool (executable, but has syntax errors)"
            ALL_PRESENT=false
        fi
    else
        echo "  ❌ $tool (missing or not executable)"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ Command-line tools incomplete"
    exit 1
fi

echo ""
echo "✅ Command-line tools ready"

# Step 6: Verify installation scripts
echo ""
echo "Step 6: Verifying installation scripts..."
echo ""

INSTALL_SCRIPTS=("bootstrap.sh" "dependency-check.sh" "symlink-manager.sh")
INSTALL_DIR="engine/infrastructure/install"

for script in "${INSTALL_SCRIPTS[@]}"; do
    if [ -x "$INSTALL_DIR/$script" ]; then
        if bash -n "$INSTALL_DIR/$script" 2>/dev/null; then
            echo "  ✅ $script (executable, no syntax errors)"
        else
            echo "  ⚠️  $script (has syntax errors)"
            ALL_PRESENT=false
        fi
    else
        echo "  ❌ $script (missing or not executable)"
        ALL_PRESENT=false
    fi
done

# Check main install script
if [ -x "install.sh" ]; then
    if bash -n "install.sh" 2>/dev/null; then
        echo "  ✅ install.sh (executable, no syntax errors)"
    else
        echo "  ⚠️  install.sh (has syntax errors)"
        ALL_PRESENT=false
    fi
else
    echo "  ❌ install.sh (missing or not executable)"
    ALL_PRESENT=false
fi

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ Installation scripts incomplete"
    exit 1
fi

echo ""
echo "✅ Installation scripts ready"

# Step 7: Verify template structure
echo ""
echo "Step 7: Verifying template structure..."
echo ""

TEMPLATE_DIR="engine/template"

# Check config templates
CONFIG_TEMPLATES=("user.yaml.template" "machine.yaml.template" "modules.yaml.template" "observatory.yaml.template" "paths.yaml.template" "Brewfile.template")
for template in "${CONFIG_TEMPLATES[@]}"; do
    if [ -f "$TEMPLATE_DIR/config/$template" ]; then
        echo "  ✅ config/$template"
    else
        echo "  ❌ config/$template missing"
        ALL_PRESENT=false
    fi
done

# Check dotfile templates
DOTFILE_TEMPLATES=(".zshrc.template" ".zprofile.template" ".gitconfig.template")
for template in "${DOTFILE_TEMPLATES[@]}"; do
    if [ -f "$TEMPLATE_DIR/dotfiles/$template" ]; then
        echo "  ✅ dotfiles/$template"
    else
        echo "  ❌ dotfiles/$template missing"
        ALL_PRESENT=false
    fi
done

# Check vault structure
VAULT_DIRS=("000_inbox" "100_daily" "200_readings" "300_zettels" "400_domain" "500_projects" "600_teaching" "700_lab" "800_outputs" "900_meta")
for vdir in "${VAULT_DIRS[@]}"; do
    if [ -d "$TEMPLATE_DIR/obsidian-vault/$vdir" ]; then
        echo "  ✅ obsidian-vault/$vdir"
    else
        echo "  ❌ obsidian-vault/$vdir missing"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo ""
    echo "❌ Template structure incomplete"
    exit 1
fi

echo ""
echo "✅ Template structure complete"

# Step 8: Test Git repository state
echo ""
echo "Step 8: Checking Git repository state..."
echo ""

if [ -d ".git" ]; then
    echo "  ✅ Git repository initialized"
    
    # Check for uncommitted changes
    if git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "  ✅ No uncommitted changes"
    else
        CHANGED=$(git status --porcelain | wc -l | xargs)
        echo "  ⚠️  $CHANGED uncommitted changes"
        echo ""
        echo "Modified files:"
        git status --short
    fi
    
    # Check commit count
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null)
    echo "  ✅ $COMMIT_COUNT commits in history"
else
    echo "  ❌ Not a Git repository"
    ALL_PRESENT=false
fi

echo ""

# Final summary
echo "═══════════════════════════════════════════════════════════"
echo "          TEST RESULTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ "$ALL_PRESENT" = true ] && [ "$PERSONAL_DATA_FOUND" = false ]; then
    echo "✅ FRAMEWORK READY FOR USE"
    echo ""
    echo "All tests passed! The framework is ready to:"
    echo "  - Be committed to Git"
    echo "  - Be pushed to GitHub"
    echo "  - Be cloned and installed by users"
    echo ""
    echo "Next steps:"
    echo "  1. Review any uncommitted changes (git status)"
    echo "  2. Commit final changes (git commit -am 'message')"
    echo "  3. Create GitHub repository: github.com/preterite/virens"
    echo "  4. Add remote: git remote add origin git@github.com:preterite/virens.git"
    echo "  5. Push: git push -u origin main"
    echo ""
    exit 0
else
    echo "❌ FRAMEWORK NOT READY"
    echo ""
    echo "Issues found:"
    if [ "$ALL_PRESENT" = false ]; then
        echo "  - Some required files/directories missing"
    fi
    if [ "$PERSONAL_DATA_FOUND" = true ]; then
        echo "  - Personal data found in framework"
    fi
    echo ""
    echo "Please address issues above before pushing to GitHub"
    echo ""
    exit 1
fi
