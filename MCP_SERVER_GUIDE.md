# ClickHouse MCP Server Usage Guide

## Quick Answer: How Many Databases in ClickHouse?

**Your ClickHouse instance has 15 databases:**

1. bi
2. bi_sbh
3. default
4. f1_prd_bi
5. f1_prd_biw
6. f1_prd_staging
7. finan_prd
8. finan_prd_connect
9. finan_prd_sbh
10. prd_app_mart_v1
11. prd_bi_mart_v1
12. prd_f1_mart_v1
13. prd_fin_mart_v1
14. v2
15. v2_prd_raw_sbh

## How to Use the MCP Server

### 1. Setup and Installation

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install the package in development mode
pip install -e .
```

### 2. Starting the MCP Server

#### Method 1: Direct Python Module Execution
```bash
python -m clickhouse_mcp_server.main
```

#### Method 2: Using the Cursor MCP Config
The server is configured in `cursor-mcp-config.json` to work with Cursor IDE:

```json
{
  "mcpServers": {
    "clickhouse": {
      "command": "C:\\Users\\MY PHUNG\\PycharmProjects\\cursor-tools\\venv\\Scripts\\python.exe",
      "args": ["-m", "clickhouse_mcp_server.main"],
      "env": {
        "PYTHONPATH": "C:\\Users\\MY PHUNG\\PycharmProjects\\cursor-tools"
      }
    }
  }
}
```

### 3. Available MCP Tools

The server provides these tools:

#### `list_databases`
- **Description**: List all databases in ClickHouse
- **Parameters**: None
- **Example**: Returns list of all 15 databases

#### `list_tables`
- **Description**: List tables in a specific database
- **Parameters**: 
  - `database` (optional): Database name (uses default if not specified)
- **Example**: List all tables in the 'bi' database

#### `get_table_schema`
- **Description**: Get schema information for a specific table
- **Parameters**:
  - `database` (optional): Database name
  - `table` (required): Table name
- **Example**: Get schema for a specific table

#### `execute_query`
- **Description**: Execute SQL queries
- **Parameters**:
  - `query` (required): SQL query to execute
  - `limit` (optional): Maximum number of rows to return
- **Example**: Run SELECT queries, CREATE statements, etc.

#### `insert_data`
- **Description**: Insert data into tables
- **Parameters**:
  - `database` (optional): Database name
  - `table` (required): Table name
  - `data` (required): Array of data rows to insert
- **Example**: Insert sample data into a table

### 4. Configuration

The server uses `config.json` for connection settings:

```json
{
  "host": "clickhouse.finan.me",
  "port": 443,
  "username": "bi_team",
  "password": "7Jhb8ULusS9t",
  "database": "default",
  "secure": true,
  "verify": true,
  "compress": true,
  "query_limit": 1000
}
```

### 5. Testing the Connection

Run the test script to verify everything works:

```bash
python test_databases.py
```

This will:
- Connect to ClickHouse
- List all databases
- Show the total count (15 databases)
- Display the complete list

### 6. Example Usage in Code

```python
import asyncio
from clickhouse_mcp_server.tools import ClickHouseMCPServer
from clickhouse_mcp_server.config import ClickHouseConfig

async def main():
    # Load configuration
    config = ClickHouseConfig.from_file()
    
    # Create MCP server instance
    server = ClickHouseMCPServer(config)
    
    # List databases
    result = await server.list_databases({})
    print(result.content[0].text)
    
    # Execute a query
    result = await server.execute_query({
        "query": "SELECT COUNT(*) FROM system.numbers LIMIT 10"
    })
    print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

### 7. Troubleshooting

- **Module not found errors**: Make sure you're in the virtual environment
- **Connection errors**: Check your `config.json` settings
- **Permission errors**: Verify your ClickHouse credentials

### 8. Integration with Cursor IDE

1. Copy the `cursor-mcp-config.json` to your Cursor configuration
2. Restart Cursor
3. The ClickHouse MCP server will be available as a tool
4. You can now use AI to query your ClickHouse databases directly

## Summary

Your ClickHouse instance contains **15 databases** with various production and staging environments for different business units (BI, F1, Finance, etc.). The MCP server provides a convenient way to interact with these databases through standardized tools. 