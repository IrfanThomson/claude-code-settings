#!/usr/bin/env python3
"""
Restore secrets from secrets.env to Claude Code configuration files
"""

import json
import os
import sys
import re
from pathlib import Path

def load_secrets(env_file='secrets.env'):
    """Load secrets from env file"""
    secrets = {}
    if not os.path.exists(env_file):
        print(f"❌ Error: {env_file} not found")
        print("Run ./decrypt-secrets.sh first to decrypt your secrets")
        sys.exit(1)

    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Parse KEY="value" format
                match = re.match(r'([^=]+)="?(.*?)"?$', line)
                if match:
                    key, value = match.groups()
                    secrets[key] = value

    return secrets

def env_key_to_json_path(env_key):
    """Convert ENV_KEY to json path"""
    # Example: PROJECTS__/HOME/IRFAN__MCPSERVERS__JULES__ENV__JULES_API_KEY
    # Returns: ['projects', '/home/irfan', 'mcpServers', 'jules', 'env', 'JULES_API_KEY']

    parts = env_key.lower().split('__')
    result = []

    for part in parts:
        # Convert snake_case to camelCase for known fields
        if '_' in part and part not in ['/home/irfan', 'jules_api_key']:
            words = part.split('_')
            if len(words) > 1:
                # Check if it should be camelCase
                if words[0] in ['oauth', 'mcp', 'jira', 'confluence', 'obsidian']:
                    result.append(''.join(w.capitalize() if i > 0 else w for i, w in enumerate(words)))
                else:
                    result.append(part)
            else:
                result.append(part)
        else:
            result.append(part)

    return result

def set_nested_value(obj, path, value):
    """Set a value in nested dict using path"""
    current = obj
    for i, key in enumerate(path[:-1]):
        if key not in current:
            current[key] = {}
        current = current[key]
    current[path[-1]] = value

def restore_to_config(secrets, config_path='~/.claude.json'):
    """Restore secrets to config file"""
    config_path = os.path.expanduser(config_path)

    # Backup existing config
    backup_path = f'{config_path}.backup'
    if os.path.exists(config_path):
        os.system(f'cp {config_path} {backup_path}')
        print(f"📋 Backed up existing config to {backup_path}")

    # Load current config or use template
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        with open('.claude.json') as f:
            config = json.load(f)

    # Apply secrets
    applied_count = 0
    for env_key, value in secrets.items():
        # Simple direct mapping for known keys
        if 'JULES_API_KEY' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'jules', 'env', 'JULES_API_KEY']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'JIRA_URL' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'JIRA_URL']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'JIRA_USERNAME' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'JIRA_USERNAME']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'JIRA_API_TOKEN' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'JIRA_API_TOKEN']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'CONFLUENCE_URL' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'CONFLUENCE_URL']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'CONFLUENCE_USERNAME' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'CONFLUENCE_USERNAME']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'CONFLUENCE_API_TOKEN' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'mcp-atlassian', 'env', 'CONFLUENCE_API_TOKEN']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'DOCKER-MCP-GATEWAY__URL' in env_key:
            path = ['projects', '/home/irfan', 'mcpServers', 'docker-mcp-gateway', 'url']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'EMAILADDRESS' in env_key:
            path = ['oauthAccount', 'emailAddress']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'ACCOUNTUUID' in env_key:
            path = ['oauthAccount', 'accountUuid']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'ORGANIZATIONUUID' in env_key:
            path = ['oauthAccount', 'organizationUuid']
            set_nested_value(config, path, value)
            applied_count += 1
        elif 'CLAUDECODEFIRSTTOKENDATE' in env_key:
            path = ['claudeCodeFirstTokenDate']
            set_nested_value(config, path, value)
            applied_count += 1

    # Save updated config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Applied {applied_count} secrets to {config_path}")
    print(f"")
    print(f"🎉 Your Claude Code configuration has been restored!")
    print(f"")
    print(f"Next steps:")
    print(f"  1. Copy other config files:")
    print(f"     cp settings.json ~/.claude/settings.json")
    print(f"     cp settings.local.json ~/.claude/settings.local.json")
    print(f"     cp -r plugins/* ~/.claude/plugins/")
    print(f"  2. Test with: claude")
    print(f"  3. Securely delete secrets.env: rm secrets.env")

if __name__ == '__main__':
    secrets = load_secrets()
    restore_to_config(secrets)
