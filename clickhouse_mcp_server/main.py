"""Main entry point for the ClickHouse MCP Server."""

import asyncio
import sys
from typing import Any, Dict

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
from .tools import ClickHouseMCPServer


class ClickHouseMCPServerWrapper(Server):
    """MCP server wrapper for ClickHouse operations."""
    
    def __init__(self):
        super().__init__("clickhouse-mcp-server")
        self.config = ClickHouseConfig.from_file()
        self.clickhouse_server = ClickHouseMCPServer(self.config)
        print("ClickHouse MCP Server initialized", file=sys.stderr)
    
    async def list_tools(self, request: ListToolsRequest) -> ListToolsResult:
        """List available tools."""
        tools = self.clickhouse_server.get_tools()
        return ListToolsResult(tools=tools)
    
    async def call_tool(self, request: CallToolRequest) -> CallToolResult:
        """Call a specific tool."""
        tool_name = request.name
        arguments = request.arguments
        
        # Route to appropriate tool method
        if tool_name == "list_databases":
            return await self.clickhouse_server.list_databases(arguments)
        elif tool_name == "list_tables":
            return await self.clickhouse_server.list_tables(arguments)
        elif tool_name == "get_table_schema":
            return await self.clickhouse_server.get_table_schema(arguments)
        elif tool_name == "execute_query":
            return await self.clickhouse_server.execute_query(arguments)
        elif tool_name == "insert_data":
            return await self.clickhouse_server.insert_data(arguments)
        else:
            return CallToolResult(
                content=[
                    {
                        "type": "text",
                        "text": f"Unknown tool: {tool_name}"
                    }
                ]
            )


async def main():
    """Main entry point."""
    # Create server instance
    server = ClickHouseMCPServerWrapper()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="clickhouse-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main()) 