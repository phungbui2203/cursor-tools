# ClickHouse MCP Server

A Model Context Protocol (MCP) server for connecting to ClickHouse databases. This server provides tools for querying ClickHouse databases and managing database operations.

## Features

- Connect to ClickHouse databases
- Execute SQL queries
- List databases and tables
- Get table schemas
- Insert data into tables
- Manage database operations

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd cursor-tools
```

2. Install the package:
```bash
pip install -e .
```

## Configuration

Create a configuration file `config.json` with your ClickHouse connection details:

```json
{
  "host": "localhost",
  "port": 8123,
  "username": "default",
  "password": "",
  "database": "default"
}
```

## Usage

### Running the MCP Server

```bash
python -m clickhouse_mcp_server.main
```

### Using with MCP Clients

The server implements the following MCP tools:

- `list_databases`: List all databases
- `list_tables`: List tables in a database
- `get_table_schema`: Get schema information for a table
- `execute_query`: Execute SQL queries
- `insert_data`: Insert data into tables

### Example Usage

```python
# Example MCP client usage
from mcp import ClientSession

async with ClientSession.create("clickhouse-mcp-server") as session:
    # List databases
    databases = await session.call_tool("list_databases", {})
    
    # Execute a query
    result = await session.call_tool("execute_query", {
        "query": "SELECT * FROM my_table LIMIT 10"
    })
```

## Development

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
isort .
```

## License

MIT License 