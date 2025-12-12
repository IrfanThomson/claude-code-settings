# 🔐 Secrets Manager Quick Reference

## 📤 Export Your Secrets (Current Machine)

```bash
# Step 1: Extract secrets from your Claude Code config
python3 extract_secrets.py > secrets.env

# Step 2: Encrypt with a password
./encrypt-secrets.sh
# Enter a strong password when prompted
# This creates: secrets.env.enc

# Step 3: Backup the encrypted file
# - Save to password manager (1Password, Bitwarden)
# - Store in private cloud (Dropbox, Drive in private folder)
# - Keep on USB drive
# - Store in private git repo
```

## 📥 Import to New Machine

```bash
# Step 1: Clone the repo
git clone https://github.com/IrfanThomson/claude-code-settings
cd claude-code-settings

# Step 2: Get your encrypted secrets
# Download secrets.env.enc from wherever you backed it up

# Step 3: Run automated setup
./setup.sh
# Enter your password when prompted
# Done! Claude Code is configured
```

## 🔄 Update Secrets (After Changes)

```bash
cd claude-code-settings

# Re-extract after adding new MCP servers or changing API keys
python3 extract_secrets.py > secrets.env

# Re-encrypt
./encrypt-secrets.sh

# Update your backup
# Upload new secrets.env.enc to password manager/cloud
```

## 🛠️ Manual Mode (If You Prefer)

### Export
```bash
python3 extract_secrets.py > secrets.env
./encrypt-secrets.sh
```

### Import
```bash
./decrypt-secrets.sh
python3 restore-secrets.py
cp settings.json ~/.claude/settings.json
cp settings.local.json ~/.claude/settings.local.json
rm secrets.env  # cleanup
```

## 📋 What Secrets Are Stored?

Run to see:
```bash
cat secrets.env.template
```

Includes:
- **Jules API Key** - For Gemini 3 Thinking async agent
- **Jira/Confluence** - API tokens for Atlassian MCP
- **Docker MCP Gateway** - URL configuration
- **OAuth Account** - Your Claude Code account info

## 🔒 Security Notes

### ✅ Safe Files
- `secrets.env.enc` - Encrypted, safe to backup anywhere
- `secrets.env.template` - Just placeholders, safe to commit

### ❌ Never Commit
- `secrets.env` - Plain text secrets!
- Any `.backup` files

### 🔐 Encryption Details
- **Algorithm**: AES-256-CBC
- **Key Derivation**: PBKDF2 (password-based)
- **Salt**: Randomized per encryption
- **Tool**: OpenSSL (installed by default on most systems)

## 💡 Pro Tips

1. **Strong Password**: Use a password manager to generate a strong password
2. **Keep Encrypted Backup**: Store `secrets.env.enc` in multiple locations
3. **Delete Decrypted**: After running `setup.sh`, delete `secrets.env`
4. **Test Transfer**: Try the workflow once to make sure it works
5. **Document Password**: Store the password in your password manager with a clear label

## 🆘 Common Issues

### "Password incorrect" when decrypting
- Make sure you're using the exact password from encryption
- Check that the file wasn't corrupted during transfer
- Try re-downloading if transferred via cloud

### "secrets.env not found" during setup
- Make sure you ran `./decrypt-secrets.sh` first
- Or create manually: `cp secrets.env.template secrets.env` and fill in

### "Command not found: openssl"
- On most systems openssl is pre-installed
- Install: `sudo apt install openssl` (Debian/Ubuntu) or `brew install openssl` (Mac)

## 📞 Support

- [Full README](README.md) - Complete documentation
- [GitHub Issues](https://github.com/IrfanThomson/claude-code-settings/issues)
- [Claude Code Docs](https://code.claude.com/docs)
