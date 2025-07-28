#!/usr/bin/env python3
"""
ClickHouse MCP Server using FastMCP
A modern, simplified implementation of the ClickHouse MCP server.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

import clickhouse_connect
from fastmcp import FastMCP, Context
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
            config_path = os.getenv("CLICKHOUSE_CONFIG", "C:\\Users\\Admin\\python\\cursor-tools\\config.json")
        
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


# Create FastMCP server instance
mcp = FastMCP("ClickHouse MCP Server 🚀")


class ClickHouseManager:
    """Manages ClickHouse connections and operations."""
    
    def __init__(self):
        self.config = ClickHouseConfig.from_file()
        self._client: Optional[clickhouse_connect.driver.client.Client] = None
    
    def get_client(self) -> clickhouse_connect.driver.client.Client:
        """Get or create ClickHouse client."""
        if self._client is None:
            self._client = self.config.get_client()
        return self._client


# Global ClickHouse manager instance
ch_manager = ClickHouseManager()


@mcp.tool
async def list_databases(ctx: Context) -> str:
    """List all databases in ClickHouse."""
    try:
        await ctx.info("📊 Fetching databases from ClickHouse...")
        
        client = ch_manager.get_client()
        result = client.query("SHOW DATABASES")
        
        databases = [row[0] for row in result.result_rows]
        
        await ctx.info(f"✅ Found {len(databases)} databases")
        return f"Available databases: {', '.join(databases)}"
        
    except Exception as e:
        await ctx.error(f"❌ Error listing databases: {str(e)}")
        return f"Error listing databases: {str(e)}"


@mcp.tool
async def list_tables(database: Optional[str] = None, ctx: Context = None) -> str:
    """
    List tables in a specific database.
    
    Args:
        database: Database name (optional, uses default if not specified)
    """
    try:
        db_name = database or ch_manager.config.database
        await ctx.info(f"📋 Fetching tables from database '{db_name}'...")
        
        client = ch_manager.get_client()
        result = client.query(f"SHOW TABLES FROM {db_name}")
        
        tables = [row[0] for row in result.result_rows]
        
        await ctx.info(f"✅ Found {len(tables)} tables in '{db_name}'")
        return f"Tables in database '{db_name}': {', '.join(tables)}"
        
    except Exception as e:
        await ctx.error(f"❌ Error listing tables: {str(e)}")
        return f"Error listing tables: {str(e)}"


@mcp.tool
async def get_table_schema(table: str, database: Optional[str] = None, ctx: Context = None) -> str:
    """
    Get schema information for a specific table.
    
    Args:
        table: Table name
        database: Database name (optional, uses default if not specified)
    """
    try:
        db_name = database or ch_manager.config.database
        await ctx.info(f"🔍 Getting schema for table '{table}' in database '{db_name}'...")
        
        client = ch_manager.get_client()
        result = client.query(f"DESCRIBE {db_name}.{table}")
        
        schema_info = []
        for row in result.result_rows:
            schema_info.append({
                "name": row[0],
                "type": row[1],
                "default_type": row[2],
                "default_expression": row[3],
                "comment": row[4],
                "codec_expression": row[5],
                "ttl_expression": row[6]
            })
        
        await ctx.info(f"✅ Retrieved schema for table '{table}'")
        return f"Schema for table '{table}':\n{json.dumps(schema_info, indent=2)}"
        
    except Exception as e:
        await ctx.error(f"❌ Error getting table schema: {str(e)}")
        return f"Error getting table schema: {str(e)}"


@mcp.tool
async def execute_query(query: str, limit: Optional[int] = None, ctx: Context = None) -> str:
    """
    Execute a SQL query.
    
    Args:
        query: SQL query to execute
        limit: Maximum number of rows to return (optional)
    """
    try:
        query_limit = limit or ch_manager.config.query_limit
        await ctx.info(f"⚡ Executing query (limit: {query_limit})...")
        await ctx.info(f"🔍 Query: {query[:100]}{'...' if len(query) > 100 else ''}")
        
        # Add LIMIT clause if not present and it's a SELECT query
        if query.strip().upper().startswith("SELECT") and "LIMIT" not in query.upper():
            query = f"{query} LIMIT {query_limit}"
        
        client = ch_manager.get_client()
        result = client.query(query)
        
        # Convert result to JSON-serializable format
        rows = []
        for row in result.result_rows:
            serializable_row = []
            for value in row:
                if hasattr(value, 'isoformat'):  # datetime objects
                    serializable_row.append(value.isoformat())
                else:
                    serializable_row.append(str(value))
            rows.append(serializable_row)
        
        await ctx.info(f"✅ Query executed successfully, returned {len(rows)} rows")
        return f"Query executed successfully. Results:\n{json.dumps(rows, indent=2)}"
        
    except Exception as e:
        await ctx.error(f"❌ Error executing query: {str(e)}")
        return f"Error executing query: {str(e)}"





def main():
    """Main entry point for the FastMCP ClickHouse server."""
    print("🚀 Starting ClickHouse FastMCP Server...", file=sys.stderr)
    print(f"📊 Connected to: {ch_manager.config.host}:{ch_manager.config.port}", file=sys.stderr)
    print(f"🗄️  Default database: {ch_manager.config.database}", file=sys.stderr)
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main() 