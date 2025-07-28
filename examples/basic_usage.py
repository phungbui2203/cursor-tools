"""Example usage of the ClickHouse MCP Server."""

import asyncio
import json
from mcp import ClientSession


async def main():
    """Example of using the ClickHouse MCP server."""
    
    # Create a client session
    async with ClientSession.create("clickhouse-mcp-server") as session:
        print("Connected to ClickHouse MCP Server")
        
        # List databases
        print("\n1. Listing databases:")
        result = await session.call_tool("list_databases", {})
        print(result.content[0].text)
        
        # List tables in default database
        print("\n2. Listing tables in default database:")
        result = await session.call_tool("list_tables", {"database": "default"})
        print(result.content[0].text)
        
        # Execute a simple query
        print("\n3. Executing a simple query:")
        result = await session.call_tool("execute_query", {
            "query": "SELECT version()"
        })
        print(result.content[0].text)
        
        # Get table schema (if table exists)
        print("\n4. Getting table schema:")
        try:
            result = await session.call_tool("get_table_schema", {
                "database": "system",
                "table": "numbers"
            })
            print(result.content[0].text)
        except Exception as e:
            print(f"Error getting table schema: {e}")
        
        # Insert sample data (example)
        print("\n5. Inserting sample data:")
        sample_data = [
            {"id": 1, "name": "Alice", "age": 25},
            {"id": 2, "name": "Bob", "age": 30},
            {"id": 3, "name": "Charlie", "age": 35}
        ]
        
        try:
            result = await session.call_tool("insert_data", {
                "database": "default",
                "table": "users",
                "data": sample_data
            })
            print(result.content[0].text)
        except Exception as e:
            print(f"Error inserting data: {e}")
            print("Note: Table 'users' might not exist. Create it first with appropriate schema.")


if __name__ == "__main__":
    asyncio.run(main()) 