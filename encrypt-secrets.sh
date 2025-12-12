#!/bin/bash
# Encrypt secrets file with password

set -e

SECRETS_FILE="${1:-secrets.env}"
OUTPUT_FILE="${2:-secrets.env.enc}"

if [ ! -f "$SECRETS_FILE" ]; then
    echo "❌ Error: $SECRETS_FILE not found"
    echo "Usage: $0 [secrets-file] [output-file]"
    exit 1
fi

echo "🔐 Encrypting $SECRETS_FILE..."
echo "   You'll be prompted for a password."
echo "   ⚠️  REMEMBER THIS PASSWORD - you'll need it to decrypt!"
echo ""

# Use AES-256-CBC encryption with salt and PBKDF2
openssl enc -aes-256-cbc -salt -pbkdf2 -in "$SECRETS_FILE" -out "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Encrypted successfully: $OUTPUT_FILE"
    echo ""
    echo "📦 Transfer this file to your new machine securely:"
    echo "   - Save to password manager"
    echo "   - Store in private git repo"
    echo "   - Transfer via secure channel"
    echo ""
    echo "⚠️  Keep this file safe and NEVER commit it to a public repo!"
else
    echo "❌ Encryption failed"
    exit 1
fi
