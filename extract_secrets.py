#!/usr/bin/env python3
import json
import sys
import os

# Load the actual config (not sanitized)
config_path = os.path.expanduser('~/.claude.json')
with open(config_path) as f:
    data = json.load(f)

secrets = {}

def extract_secrets(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f'{path}.{k}' if path else k

            # Check if this is a sensitive field
            is_sensitive = any(x in k.lower() for x in [
                'key', 'token', 'password', 'secret', 'credential',
                'auth', 'email', 'username', 'uuid'
            ])

            # Check for URLs that might contain credentials
            is_url_with_creds = k.lower() in ['url', 'jira_url', 'confluence_url', 'obsidian_url']

            if is_sensitive and isinstance(v, str) and v:
                secrets[new_path] = v
            elif is_url_with_creds and isinstance(v, str) and v:
                secrets[new_path] = v
            else:
                extract_secrets(v, new_path)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            extract_secrets(item, f'{path}[{i}]')

extract_secrets(data)

# Print as env file format
for key, value in sorted(secrets.items()):
    # Convert path to env var format
    env_key = key.replace('.', '__').replace('[', '_').replace(']', '').upper()
    # Escape quotes in value
    safe_value = value.replace('"', '\\"')
    print(f'{env_key}="{safe_value}"')
