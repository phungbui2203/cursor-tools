"""Configuration management for ClickHouse MCP Server."""

import json
import os
from pathlib import Path
from typing import Optional

import clickhouse_connect
from pydantic import BaseModel


class ClickHouseConfig(BaseModel):
    """ClickHouse connection configuration."""
    
    host: str = "localhost"
    port: int = 8123
    username: str = "default"
    password: str = ""
    database: str = "default"
    secure: bool = False
    verify: bool = True
    compress: bool = True
    query_limit: int = 1000
    
    @classmethod
    def from_file(cls, config_path: Optional[str] = None) -> "ClickHouseConfig":
        """Load configuration from a JSON file."""
        if config_path is None:
            config_path = os.getenv("CLICKHOUSE_CONFIG", "config.json")
        
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, "r") as f:
                config_data = json.load(f)
            return cls(**config_data)
        
        return cls()
    
    def get_client(self) -> clickhouse_connect.driver.client.Client:
        """Create a ClickHouse client with the current configuration."""
        return clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            secure=self.secure,
            verify=self.verify,
            compress=self.compress,
        ) 