#!/bin/bash
# Setup Claude Code from this configuration repo

set -e

echo "🚀 Claude Code Settings Setup"
echo "=============================="
echo ""

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code is not installed"
    echo "   Install it first: npm install -g @anthropic-ai/claude-code"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Decrypt secrets
echo "Step 1/3: Decrypt secrets"
echo "-------------------------"
if [ -f "secrets.env.enc" ]; then
    echo "Found encrypted secrets file."
    read -p "Decrypt secrets now? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        ./decrypt-secrets.sh
    fi
elif [ ! -f "secrets.env" ]; then
    echo "⚠️  No secrets file found."
    echo "   You need either:"
    echo "   - secrets.env.enc (encrypted, transfer from old machine)"
    echo "   - secrets.env (decrypted, fill from secrets.env.template)"
    echo ""
    echo "   Copy secrets.env.template to secrets.env and fill in your values."
    exit 1
fi

# Step 2: Restore secrets to config
echo ""
echo "Step 2/3: Apply secrets to configuration"
echo "----------------------------------------"
if [ -f "secrets.env" ]; then
    # Backup existing config
    if [ -f ~/.claude.json ]; then
        echo "📋 Backing up existing ~/.claude.json"
        cp ~/.claude.json ~/.claude.json.backup.$(date +%Y%m%d_%H%M%S)
    fi

    python3 restore-secrets.py
else
    echo "❌ secrets.env not found. Decrypt it first."
    exit 1
fi

# Step 3: Copy other config files
echo ""
echo "Step 3/3: Copy additional configuration files"
echo "---------------------------------------------"

# Create ~/.claude directory if it doesn't exist
mkdir -p ~/.claude/{plugins,memory,projects}

# Copy config files
if [ -f "settings.json" ]; then
    echo "📄 Copying settings.json"
    cp settings.json ~/.claude/settings.json
fi

if [ -f "settings.local.json" ]; then
    echo "📄 Copying settings.local.json"
    cp settings.local.json ~/.claude/settings.local.json
fi

if [ -f "CLAUDE.md" ]; then
    echo "📄 Copying CLAUDE.md"
    cp CLAUDE.md ~/.claude/CLAUDE.md
fi

# Copy plugin configs
if [ -d "plugins" ]; then
    echo "📦 Copying plugin configurations"
    cp plugins/*.json ~/.claude/plugins/ 2>/dev/null || true
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Your Claude Code is configured with:"
echo "   - Multi-agent setup (Claude Code + Jules)"
echo "   - Obsidian MCP integration"
echo "   - Atlassian MCP integration"
echo "   - Your personal settings"
echo ""
echo "🔒 Security reminder:"
echo "   Delete secrets.env: rm secrets.env"
echo ""
echo "Test it: claude"
