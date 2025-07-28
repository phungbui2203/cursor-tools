# Fixing ClickHouse MCP Server in Cursor

## Problem: ClickHouse MCP Server Shows 0 Tools

The MCP server is working correctly (we verified it has 5 tools), but Cursor is not detecting them. Here's how to fix this:

## ✅ Verified: MCP Server is Working

Our tests confirmed:
- ✅ Server has 5 tools: `list_databases`, `list_tables`, `get_table_schema`, `execute_query`, `insert_data`
- ✅ Tools are functional and can query ClickHouse
- ✅ Found 15 databases in your ClickHouse instance

## 🔧 Solution Steps

### Step 1: Verify Cursor MCP Configuration

Your `cursor-mcp-config.json` looks correct:

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

### Step 2: Copy Configuration to Cursor

1. **Find Cursor's config directory:**
   - Windows: `%APPDATA%\Cursor\User\globalStorage\cursor.mcp`
   - Or check Cursor settings for MCP configuration location

2. **Copy the configuration:**
   ```bash
   # Copy your config to Cursor's MCP directory
   copy cursor-mcp-config.json "%APPDATA%\Cursor\User\globalStorage\cursor.mcp\"
   ```

### Step 3: Restart Cursor Completely

1. **Close Cursor completely**
2. **Restart Cursor**
3. **Check if MCP server is loaded**

### Step 4: Alternative Configuration Method

If the above doesn't work, try adding the MCP server through Cursor's settings:

1. Open Cursor Settings (Ctrl+,)
2. Search for "MCP" or "Model Context Protocol"
3. Add a new MCP server with these settings:
   - **Name**: clickhouse
   - **Command**: `C:\Users\MY PHUNG\PycharmProjects\cursor-tools\venv\Scripts\python.exe`
   - **Arguments**: `["-m", "clickhouse_mcp_server.main"]`
   - **Environment Variables**: 
     - `PYTHONPATH`: `C:\Users\MY PHUNG\PycharmProjects\cursor-tools`

### Step 5: Test the Connection

Once configured, test the MCP server in Cursor:

1. **Open a new chat in Cursor**
2. **Ask**: "List the ClickHouse databases using the MCP server"
3. **Expected response**: Should show all 15 databases

## 🐛 Troubleshooting

### If still showing 0 tools:

1. **Check Cursor logs:**
   - Open Developer Tools (Ctrl+Shift+I)
   - Check Console for MCP-related errors

2. **Verify Python path:**
   ```bash
   # Test if the command works
   C:\Users\MY PHUNG\PycharmProjects\cursor-tools\venv\Scripts\python.exe -m clickhouse_mcp_server.main
   ```

3. **Check MCP server manually:**
   ```bash
   # Activate venv and test
   .\venv\Scripts\Activate.ps1
   python -m clickhouse_mcp_server.main
   ```

### Common Issues:

1. **Path with spaces**: The path `C:\Users\MY PHUNG\...` contains spaces
   - Try using short paths or escaping spaces
   - Or move the project to a path without spaces

2. **Virtual environment not activated**: Make sure the venv is properly set up
   - Run: `pip install -e .` in the venv

3. **MCP protocol version**: The server might need protocol version updates
   - Check MCP library version: `pip show mcp`

## 📋 Expected Tools

Once working, you should see these 5 tools in Cursor:

1. **list_databases** - List all databases in ClickHouse
2. **list_tables** - List tables in a specific database  
3. **get_table_schema** - Get schema information for a specific table
4. **execute_query** - Execute SQL queries
5. **insert_data** - Insert data into tables

## 🎯 Quick Test Commands

Once the MCP server is working in Cursor, try these commands:

- "List all ClickHouse databases"
- "Show tables in the 'bi' database"
- "Execute the query: SELECT version()"
- "Get the schema for table 'users' in database 'default'"

## 📞 If Still Not Working

If the MCP server still shows 0 tools after following these steps:

1. **Check Cursor version**: Make sure you're using the latest version
2. **Try a different MCP server**: Test with a simple MCP server to verify Cursor's MCP functionality
3. **Check system requirements**: Ensure Python 3.8+ and all dependencies are installed
4. **Contact Cursor support**: The issue might be with Cursor's MCP implementation

## ✅ Success Indicators

You'll know it's working when:
- Cursor shows 5 tools for the ClickHouse MCP server
- You can ask Cursor to "list ClickHouse databases" and get a response
- The AI can execute ClickHouse queries through the MCP interface 