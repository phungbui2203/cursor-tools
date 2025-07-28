#!/usr/bin/env python3
"""Debug script to check configuration loading."""

import json
from pathlib import Path
from clickhouse_mcp_server.config import ClickHouseConfig

# Check if config file exists
config_file = Path("config.json")
print(f"Config file exists: {config_file.exists()}")

if config_file.exists():
    with open(config_file, "r") as f:
        config_data = json.load(f)
    print("Config file contents:")
    print(json.dumps(config_data, indent=2))

# Load configuration
config = ClickHouseConfig.from_file()
print(f"\nLoaded config:")
print(f"Host: {config.host}")
print(f"Port: {config.port}")
print(f"Username: {config.username}")
print(f"Password: {'*' * len(config.password) if config.password else 'None'}")
print(f"Secure: {config.secure}")
print(f"Database: {config.database}") 