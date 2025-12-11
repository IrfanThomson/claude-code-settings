# Claude Code Global Settings

This repository contains my global configuration files for Claude Code.

## Files

- `.claude.json` - Main configuration file (sanitized - sensitive data removed)
- `settings.json` - Global settings
- `settings.local.json` - Local overrides
- `obsidian-mcp-config.json` - Obsidian MCP server configuration
- `CLAUDE.md` - Global Claude instructions
- `plugins/` - Plugin configurations

## Setup

To use these settings:

1. **Backup your current settings first!**
   ```bash
   cp ~/.claude.json ~/.claude.json.backup
   ```

2. **Restore settings** (after adding your own API keys):
   ```bash
   cp .claude.json ~/.claude.json
   cp settings.json ~/.claude/settings.json
   cp settings.local.json ~/.claude/settings.local.json
   cp obsidian-mcp-config.json ~/.claude/obsidian-mcp-config.json
   cp CLAUDE.md ~/.claude/CLAUDE.md
   cp -r plugins/* ~/.claude/plugins/
   ```

3. **Add your credentials**:
   - Edit `~/.claude.json` and replace `REDACTED` values with your actual API keys, tokens, and URLs
   - Update email addresses and organization IDs as needed

## Multi-Agent Setup

This configuration includes:
- **Claude Code** (Sonnet 4.5) - Interactive synchronous coding
- **Jules MCP** (Gemini 3 Thinking) - Async background tasks
- **Obsidian MCP** - Note-taking integration
- **Atlassian MCP** - Jira/Confluence integration

## Security Note

**IMPORTANT:** This repo contains sanitized configurations. Sensitive data like:
- API keys
- Tokens
- Credentials
- Email addresses
- Organization IDs

...have been replaced with `REDACTED`. You must add your own credentials before using these configs.

## Updates

To update this repo with your latest settings:

```bash
# From the claude-code-settings directory
cp ~/.claude.json .
# Sanitize sensitive data before committing!
# Then commit and push
```
