"""MCP tools for ClickHouse operations."""

import json
from typing import Any, Dict, List, Optional

import clickhouse_connect
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
)

from .config import ClickHouseConfig


class ClickHouseMCPServer:
    """MCP server for ClickHouse operations."""
    
    def __init__(self, config: ClickHouseConfig):
        self.config = config
        self.client: Optional[clickhouse_connect.driver.client.Client] = None
    
    def get_client(self) -> clickhouse_connect.driver.client.Client:
        """Get or create ClickHouse client."""
        if self.client is None:
            self.client = self.config.get_client()
        return self.client
    
    async def list_databases(self, arguments: Dict[str, Any]) -> CallToolResult:
        """List all databases in ClickHouse."""
        try:
            client = self.get_client()
            result = client.query("SHOW DATABASES")
            
            databases = []
            for row in result.result_rows:
                databases.append(row[0])
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Available databases: {', '.join(databases)}"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error listing databases: {str(e)}"
                    }
                ]
            )
    
    async def list_tables(self, arguments: Dict[str, Any]) -> CallToolResult:
        """List tables in a specific database."""
        try:
            database = arguments.get("database", self.config.database)
            client = self.get_client()
            
            # Switch to the specified database
            client.command(f"USE {database}")
            result = client.query("SHOW TABLES")
            
            tables = []
            for row in result.result_rows:
                tables.append(row[0])
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Tables in database '{database}': {', '.join(tables)}"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error listing tables: {str(e)}"
                    }
                ]
            )
    
    async def get_table_schema(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get schema information for a specific table."""
        try:
            database = arguments.get("database", self.config.database)
            table = arguments["table"]
            
            client = self.get_client()
            client.command(f"USE {database}")
            
            # Get table schema
            result = client.query(f"DESCRIBE {table}")
            
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
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Schema for table '{table}':\n{json.dumps(schema_info, indent=2)}"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error getting table schema: {str(e)}"
                    }
                ]
            )
    
    async def execute_query(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Execute a SQL query."""
        try:
            query = arguments["query"]
            limit = arguments.get("limit", self.config.query_limit)
            
            # Add LIMIT clause if not present and it's a SELECT query
            if query.strip().upper().startswith("SELECT") and "LIMIT" not in query.upper():
                query = f"{query} LIMIT {limit}"
            
            client = self.get_client()
            result = client.query(query)
            
            # Convert result to JSON-serializable format
            rows = []
            for row in result.result_rows:
                # Convert any non-serializable types to strings
                serializable_row = []
                for value in row:
                    if hasattr(value, 'isoformat'):  # datetime objects
                        serializable_row.append(value.isoformat())
                    else:
                        serializable_row.append(str(value))
                rows.append(serializable_row)
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Query executed successfully. Results:\n{json.dumps(rows, indent=2)}"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error executing query: {str(e)}"
                    }
                ]
            )
    
    async def insert_data(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Insert data into a table."""
        try:
            database = arguments.get("database", self.config.database)
            table = arguments["table"]
            data = arguments["data"]
            
            client = self.get_client()
            client.command(f"USE {database}")
            
            # Insert data
            client.insert(table, data)
            
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Successfully inserted {len(data)} rows into table '{table}'"
                    }
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Error inserting data: {str(e)}"
                    }
                ]
            )
    
    def get_tools(self) -> List[Tool]:
        """Get list of available tools."""
        return [
            Tool(
                name="list_databases",
                description="List all databases in ClickHouse",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="list_tables",
                description="List tables in a specific database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional, uses default if not specified)"
                        }
                    },
                    "required": []
                }
            ),
            Tool(
                name="get_table_schema",
                description="Get schema information for a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional, uses default if not specified)"
                        },
                        "table": {
                            "type": "string",
                            "description": "Table name"
                        }
                    },
                    "required": ["table"]
                }
            ),
            Tool(
                name="execute_query",
                description="Execute a SQL query",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to execute"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of rows to return (optional)"
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="insert_data",
                description="Insert data into a table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "database": {
                            "type": "string",
                            "description": "Database name (optional, uses default if not specified)"
                        },
                        "table": {
                            "type": "string",
                            "description": "Table name"
                        },
                        "data": {
                            "type": "array",
                            "description": "Array of data rows to insert",
                            "items": {
                                "type": "object"
                            }
                        }
                    },
                    "required": ["table", "data"]
                }
            )
        ] 