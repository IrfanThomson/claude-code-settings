#!/bin/bash
# Decrypt secrets file with password

set -e

ENCRYPTED_FILE="${1:-secrets.env.enc}"
OUTPUT_FILE="${2:-secrets.env}"

if [ ! -f "$ENCRYPTED_FILE" ]; then
    echo "❌ Error: $ENCRYPTED_FILE not found"
    echo "Usage: $0 [encrypted-file] [output-file]"
    exit 1
fi

echo "🔓 Decrypting $ENCRYPTED_FILE..."
echo "   Enter the password you used for encryption."
echo ""

# Decrypt using AES-256-CBC
openssl enc -aes-256-cbc -d -salt -pbkdf2 -in "$ENCRYPTED_FILE" -out "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Decrypted successfully: $OUTPUT_FILE"
    echo ""
    echo "🔒 Security reminder:"
    echo "   - secrets.env contains sensitive data"
    echo "   - It's in .gitignore (won't be committed)"
    echo "   - Delete it after applying to configs"
    echo ""
else
    echo "❌ Decryption failed - wrong password?"
    exit 1
fi
