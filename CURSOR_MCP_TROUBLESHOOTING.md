# Cursor MCP Server Troubleshooting Guide

## Problem: ClickHouse MCP Server Shows 0 Tools in Cursor

### ✅ Verified: Server is Working
- ✅ 5 tools available: `list_databases`, `list_tables`, `get_table_schema`, `execute_query`, `insert_data`
- ✅ Server connects to ClickHouse successfully
- ✅ Found 15 databases in your ClickHouse instance

## 🔧 Multiple Solutions to Try

### Solution 1: Use Cursor's Built-in MCP Settings

1. **Open Cursor Settings** (Ctrl+,)
2. **Search for "MCP"** or "Model Context Protocol"
3. **Add a new MCP server** with these exact settings:
   - **Name**: `clickhouse`
   - **Command**: `C:\Users\MY PHUNG\PycharmProjects\cursor-tools\venv\Scripts\python.exe`
   - **Arguments**: `["-m", "clickhouse_mcp_server.main"]`
   - **Environment Variables**:
     - `PYTHONPATH`: `C:\Users\MY PHUNG\PycharmProjects\cursor-tools`

### Solution 2: Manual Configuration File

1. **Create the MCP directory** (if it doesn't exist):
   ```powershell
   New-Item -Path "$env:APPDATA\Cursor\User\globalStorage\cursor.mcp" -ItemType Directory -Force
   ```

2. **Copy the configuration file**:
   ```powershell
   Copy-Item "cursor-mcp-config-v2.json" "$env:APPDATA\Cursor\User\globalStorage\cursor.mcp\config.json"
   ```

3. **Restart Cursor completely**

### Solution 3: Alternative Configuration Locations

Try placing the MCP config in these locations:

1. **User settings directory**:
   ```powershell
   Copy-Item "cursor-mcp-config-v2.json" "$env:APPDATA\Cursor\User\settings.json"
   ```

2. **Workspace settings** (create `.vscode/settings.json` in your project):
   ```json
   {
     "mcp.servers": {
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

### Solution 4: Simplified Configuration

Try the simplified config (`simple-mcp-config.json`):
```json
{
  "mcpServers": {
    "clickhouse": {
      "command": "python",
      "args": ["-m", "clickhouse_mcp_server.main"],
      "env": {
        "PYTHONPATH": "C:\\Users\\MY PHUNG\\PycharmProjects\\cursor-tools"
      }
    }
  }
}
```

## 🐛 Debugging Steps

### Step 1: Check Cursor Version
```powershell
# Check if Cursor is installed and version
Get-Command cursor -ErrorAction SilentlyContinue
```

### Step 2: Verify Python Path
```powershell
# Test if the Python command works
C:\Users\MY PHUNG\PycharmProjects\cursor-tools\venv\Scripts\python.exe -c "print('Python works')"
```

### Step 3: Test MCP Server Manually
```powershell
# Activate venv and test server
.\venv\Scripts\Activate.ps1
python -m clickhouse_mcp_server.main
```

### Step 4: Check Cursor Logs
1. **Open Cursor**
2. **Open Developer Tools** (Ctrl+Shift+I)
3. **Check Console** for MCP-related errors
4. **Look for** any error messages about MCP servers

### Step 5: Test with Different MCP Server
Try installing a simple MCP server to verify Cursor's MCP functionality:

```bash
pip install mcp-server-filesystem
```

Then add to config:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem"
    }
  }
}
```

## 🔍 Common Issues and Fixes

### Issue 1: Path with Spaces
**Problem**: `C:\Users\MY PHUNG\...` contains spaces
**Solution**: 
- Use short paths: `%USERPROFILE%\cursor-tools`
- Or escape spaces properly in JSON
- Or move project to path without spaces

### Issue 2: Virtual Environment Not Activated
**Problem**: Cursor can't find MCP dependencies
**Solution**:
- Use full path to venv Python: `C:\Users\MY PHUNG\PycharmProjects\cursor-tools\venv\Scripts\python.exe`
- Or install MCP globally: `pip install mcp clickhouse-connect`

### Issue 3: MCP Protocol Version Mismatch
**Problem**: Server and client use different MCP versions
**Solution**:
- Update MCP library: `pip install --upgrade mcp`
- Check Cursor's MCP protocol version support

### Issue 4: Cursor Not Loading MCP Config
**Problem**: Cursor ignores MCP configuration
**Solution**:
- Restart Cursor completely (not just reload)
- Check if Cursor has MCP support enabled
- Try different configuration file locations

## 📋 Verification Steps

After trying each solution:

1. **Restart Cursor completely**
2. **Open a new chat**
3. **Ask**: "What MCP servers are available?"
4. **Expected**: Should see "clickhouse" in the list
5. **Test**: "List ClickHouse databases"

## 🆘 If Nothing Works

If none of the above solutions work:

1. **Check Cursor version**: Make sure you're using the latest version
2. **Try a different MCP server**: Test with a simple filesystem MCP server
3. **Check system requirements**: Ensure Python 3.8+ and all dependencies
4. **Contact Cursor support**: The issue might be with Cursor's MCP implementation
5. **Alternative**: Use the MCP server directly without Cursor integration

## 📞 Alternative: Direct Usage

If Cursor integration doesn't work, you can still use the MCP server directly:

```python
import asyncio
from clickhouse_mcp_server.tools import ClickHouseMCPServer
from clickhouse_mcp_server.config import ClickHouseConfig

async def main():
    config = ClickHouseConfig.from_file()
    server = ClickHouseMCPServer(config)
    
    # List databases
    result = await server.list_databases({})
    print(result.content[0].text)

asyncio.run(main())
```

## ✅ Success Indicators

You'll know it's working when:
- Cursor shows "clickhouse" in the MCP servers list
- You can ask "List ClickHouse databases" and get a response
- The AI can execute ClickHouse queries through the MCP interface
- You see 5 tools available for the clickhouse MCP server 