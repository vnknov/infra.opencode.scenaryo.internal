#!/usr/bin/env python3
"""Prints Caddy, MCP, and OpenCode configuration."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def print_caddy_config():
    """Display Caddyfile configuration."""
    caddyfile = PROJECT_ROOT / "Caddyfile"
    print("=== CADDY CONFIGURATION ===")
    print(f"File: {caddyfile.relative_to(PROJECT_ROOT)}\n")
    print(caddyfile.read_text().strip())
    print()


def print_mcp_servers():
    """Display MCP servers configured in opencode.json."""
    config = PROJECT_ROOT / "opencode.json"
    data = json.loads(config.read_text())
    
    print("=== MCP SERVERS ===")
    mcp_servers = data.get("mcp", {})
    
    if not mcp_servers:
        print("No MCP servers configured.")
        return
    
    for name, config in mcp_servers.items():
        enabled = "✓" if config.get("enabled", True) else "✗"
        server_type = config.get("type", "unknown")
        url = config.get("url", "N/A")
        
        print(f"\n[{enabled}] {name}")
        print(f"    Type:   {server_type}")
        print(f"    URL:    {url}")
        
        if "timeout" in config:
            print(f"    Timeout: {config['timeout']}ms")
        if "oauth" in config:
            print(f"    OAuth:  {config['oauth']}")
        if "headers" in config:
            headers = config["headers"]
            if "Authorization" in headers:
                auth = headers["Authorization"]
                if "{env:" in auth:
                    key = auth.split("{env:")[1].split("}")[0]
                    auth = f"Bearer ***{key[-4:]}" if len(key) > 4 else "Bearer ***"
                print(f"    Header: {auth}")
    print()


def print_opencode_config():
    """Display OpenCode server configuration."""
    config = PROJECT_ROOT / "opencode.json"
    data = json.loads(config.read_text())
    
    print("=== OPENCODE CONFIGURATION ===")
    
    model = data.get("model", "N/A")
    print(f"Model: {model}")
    
    provider_config = data.get("provider", {})
    for provider_name, provider in provider_config.items():
        print(f"\nProvider: {provider_name}")
        print(f"  NPM package:   {provider.get('npm', 'N/A')}")
        print(f"  Name:          {provider.get('name', 'N/A')}")
        
        options = provider.get("options", {})
        if "baseURL" in options:
            print(f"  Base URL:      {options['baseURL']}")
        if "apiKey" in options:
            api_key_ref = options["apiKey"]
            if "{env:" in api_key_ref:
                env_var = api_key_ref.split("{env:")[1].split("}")[0]
                print(f"  API Key Env:   ${env_var}")
        
        models = provider.get("models", {})
        if models:
            print(f"  Models:")
            for model_id, model_info in models.items():
                name = model_info.get("name", "N/A")
                print(f"    - {model_id}: {name}")
    
    print()


def main():
    try:
        print_caddy_config()
        print_mcp_servers()
        print_opencode_config()
    except FileNotFoundError as e:
        print(f"Error: Required file not found - {e.filename}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in opencode.json - {e}")
        exit(1)


if __name__ == "__main__":
    main()
