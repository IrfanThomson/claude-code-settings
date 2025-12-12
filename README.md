# Claude Code Global Settings

This repository contains my global configuration files for Claude Code with **secure secrets management**.

## 🔐 Secrets Management

This repo includes an encrypted secrets management system that lets you safely transfer your configuration to new machines.

### Quick Start: New Machine Setup

```bash
# 1. Clone this repo
git clone https://github.com/IrfanThomson/claude-code-settings
cd claude-code-settings

# 2. Get your encrypted secrets file
# (transfer secrets.env.enc from old machine or password manager)

# 3. Run automated setup
./setup.sh
```

That's it! The setup script will:
- Decrypt your secrets
- Apply them to Claude Code configs
- Copy all settings files
- Set up your multi-agent environment

---

## 📁 Files

### Configuration Files
- `.claude.json` - Main configuration (sanitized - sensitive data removed)
- `settings.json` - Global settings
- `settings.local.json` - Local overrides
- `obsidian-mcp-config.json` - Obsidian MCP server configuration
- `CLAUDE.md` - Global Claude instructions
- `plugins/` - Plugin configurations

### Secrets Management Scripts
- `secrets.env.template` - Template showing what secrets are needed
- `encrypt-secrets.sh` - Encrypt your secrets with a password
- `decrypt-secrets.sh` - Decrypt secrets for use
- `restore-secrets.py` - Apply decrypted secrets to config files
- `setup.sh` - Complete automated setup for new machines
- `extract_secrets.py` - Extract secrets from current config

---

## 🚀 Usage Workflows

### First Time: Export Your Secrets

On your current machine with working Claude Code:

```bash
cd claude-code-settings

# Extract secrets from your current config
python3 extract_secrets.py > secrets.env

# Encrypt with a strong password
./encrypt-secrets.sh

# This creates: secrets.env.enc (encrypted, safe to transfer)
```

**Transfer `secrets.env.enc` to:**
- Password manager (1Password, Bitwarden, etc.)
- Private cloud storage
- USB drive
- Private git repository

### New Machine: Import Your Secrets

```bash
# Clone repo
git clone https://github.com/IrfanThomson/claude-code-settings
cd claude-code-settings

# Get your encrypted secrets
# (download from password manager, cloud, etc.)

# Run automated setup
./setup.sh

# Or manual steps:
./decrypt-secrets.sh                # Decrypt secrets
python3 restore-secrets.py          # Apply to configs
cp settings.json ~/.claude/         # Copy settings
rm secrets.env                      # Secure cleanup
```

### Update Secrets

When you add new MCP servers or update API keys:

```bash
cd claude-code-settings

# Re-extract secrets from current config
python3 extract_secrets.py > secrets.env

# Re-encrypt
./encrypt-secrets.sh

# Update your backup (password manager, cloud, etc.)
```

---

## 🛡️ Security Best Practices

### ✅ Safe Files (can commit to repo)
- `.claude.json` - Sanitized (all secrets are `REDACTED`)
- `secrets.env.template` - Just placeholders
- All `.sh` and `.py` scripts
- `settings.json` files (no secrets)

### ❌ Sensitive Files (NEVER commit)
- `secrets.env` - Plain text secrets
- `secrets.env.dec` - Decrypted secrets
- `*.backup` - Config backups with secrets

### ⚠️ Optional: Encrypted File
You can optionally commit `secrets.env.enc` to a **private repo** since it's password-encrypted. But for public repos, keep it separate.

---

## 🤖 Multi-Agent Setup

This configuration includes:

| Agent | Model | Type | Purpose |
|-------|-------|------|---------|
| **Claude Code** | Sonnet 4.5 | Synchronous | Interactive coding, git workflows |
| **Jules MCP** | Gemini 3 Thinking | Async | Background tasks, refactoring |
| **Obsidian MCP** | - | Integration | Note-taking and knowledge management |
| **Atlassian MCP** | - | Integration | Jira/Confluence integration |

### Using Multiple Agents

```bash
# Delegate async work to Jules
"Use Jules to refactor the authentication module while I work on the UI"

# Take notes in Obsidian
"Create an Obsidian note about this implementation"

# Create Jira tickets
"Create a Jira ticket for this bug"
```

---

## 📝 Manual Setup (without scripts)

If you prefer manual setup:

### 1. Backup Current Settings

```bash
cp ~/.claude.json ~/.claude.json.backup
```

### 2. Restore Config Files

```bash
# Main config (will need secrets added)
cp .claude.json ~/.claude.json

# Settings
cp settings.json ~/.claude/settings.json
cp settings.local.json ~/.claude/settings.local.json
cp CLAUDE.md ~/.claude/CLAUDE.md

# Plugins
mkdir -p ~/.claude/plugins
cp plugins/*.json ~/.claude/plugins/
```

### 3. Add Secrets Manually

Edit `~/.claude.json` and replace all `REDACTED` values with your actual:

#### Required Secrets:
- **Jules API Key**: Get from https://jules.google.com
  - Location: `projects["/home/irfan"].mcpServers.jules.env.JULES_API_KEY`

- **Jira/Confluence** (if using Atlassian MCP):
  - `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`
  - `CONFLUENCE_URL`, `CONFLUENCE_USERNAME`, `CONFLUENCE_API_TOKEN`
  - Location: `projects["/home/irfan"].mcpServers["mcp-atlassian"].env`

- **OAuth Account** (for Claude Code authentication):
  - `emailAddress`, `accountUuid`, `organizationUuid`
  - Location: `oauthAccount.*`

Use `secrets.env.template` as a reference for all required secrets.

---

## 🔄 Sync Settings Across Machines

### Option 1: Git Sync (with encrypted secrets)

```bash
# On Machine A (update settings)
cd claude-code-settings
python3 extract_secrets.py > secrets.env
./encrypt-secrets.sh
git add secrets.env.enc  # Only if private repo!
git add .claude.json settings.json plugins/*
git commit -m "Update settings"
git push

# On Machine B (pull updates)
cd claude-code-settings
git pull
./setup.sh
```

### Option 2: Manual Sync (most secure)

```bash
# Export from old machine
./encrypt-secrets.sh
# Transfer secrets.env.enc via secure channel

# Import on new machine
./decrypt-secrets.sh
python3 restore-secrets.py
```

---

## 🎯 Installed MCP Servers

This config includes:

1. **Jules MCP** - Async coding agent
   - Install location: `~/.local/lib/mcp-servers/node_modules/@iflow-mcp/google-jules-mcp`

2. **Obsidian MCP** - Note management
   - Install: `uvx obsidian-mcp`
   - Vault: Set `OBSIDIAN_VAULT_PATH` in secrets

3. **Atlassian MCP** - Jira/Confluence
   - Runs via Docker
   - Requires Jira/Confluence API tokens

4. **Docker MCP Gateway** - Docker integration
   - SSE connection on port 8081

---

## 🆘 Troubleshooting

### "secrets.env not found"
```bash
# Either decrypt existing secrets:
./decrypt-secrets.sh

# Or create from template:
cp secrets.env.template secrets.env
# Edit secrets.env with your values
```

### "Wrong password" when decrypting
- Make sure you're using the same password from encryption
- Check that `secrets.env.enc` wasn't corrupted during transfer

### "Jules not showing in /mcp"
- Verify secrets were applied: `cat ~/.claude.json | grep JULES_API_KEY`
- Check Jules MCP is installed: `ls ~/.local/lib/mcp-servers/node_modules`
- Restart Claude Code

### Permission errors
```bash
chmod +x *.sh *.py
```

---

## 🔗 Links

- [Claude Code Documentation](https://code.claude.com/docs)
- [Jules Documentation](https://jules.google.com/docs)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Repository](https://github.com/IrfanThomson/claude-code-settings)

---

## 🤝 Contributing

This is a personal configuration repo, but feel free to fork and adapt for your own use!

### To create your own version:

1. Fork this repo
2. Run `python3 extract_secrets.py` on your machine
3. Update `.claude.json` with your sanitized config
4. Customize `settings.json` for your preferences
5. Create your `secrets.env.enc`

---

**Generated with ❤️ using Claude Code**

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
