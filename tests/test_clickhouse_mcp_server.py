"""Tests for ClickHouse MCP Server."""

import pytest
from unittest.mock import Mock, patch

from clickhouse_mcp_server.config import ClickHouseConfig
from clickhouse_mcp_server.tools import ClickHouseMCPServer


class TestClickHouseConfig:
    """Test ClickHouse configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ClickHouseConfig()
        assert config.host == "localhost"
        assert config.port == 8123
        assert config.username == "default"
        assert config.password == ""
        assert config.database == "default"
        assert config.secure is False
        assert config.verify is True
        assert config.compress is True
        assert config.query_limit == 1000
    
    @patch('builtins.open')
    @patch('json.load')
    def test_from_file(self, mock_json_load, mock_open):
        """Test loading configuration from file."""
        mock_json_load.return_value = {
            "host": "test-host",
            "port": 9000,
            "username": "test-user",
            "password": "test-pass",
            "database": "test-db"
        }
        mock_open.return_value.__enter__.return_value = Mock()
        
        config = ClickHouseConfig.from_file("test_config.json")
        assert config.host == "test-host"
        assert config.port == 9000
        assert config.username == "test-user"
        assert config.password == "test-pass"
        assert config.database == "test-db"


class TestClickHouseMCPServer:
    """Test ClickHouse MCP Server."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = ClickHouseConfig()
        self.server = ClickHouseMCPServer(self.config)
    
    def test_get_tools(self):
        """Test that tools are properly defined."""
        tools = self.server.get_tools()
        
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "list_databases",
            "list_tables", 
            "get_table_schema",
            "execute_query",
            "insert_data"
        ]
        
        assert set(tool_names) == set(expected_tools)
    
    @pytest.mark.asyncio
    async def test_list_databases_error_handling(self):
        """Test error handling in list_databases."""
        with patch.object(self.server, 'get_client') as mock_get_client:
            mock_client = Mock()
            mock_client.query.side_effect = Exception("Connection failed")
            mock_get_client.return_value = mock_client
            
            result = await self.server.list_databases({})
            assert "Error listing databases" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_execute_query_with_limit(self):
        """Test that SELECT queries get LIMIT added automatically."""
        with patch.object(self.server, 'get_client') as mock_get_client:
            mock_client = Mock()
            mock_result = Mock()
            mock_result.result_rows = [["test"]]
            mock_client.query.return_value = mock_result
            mock_get_client.return_value = mock_client
            
            result = await self.server.execute_query({
                "query": "SELECT * FROM test_table"
            })
            
            # Check that LIMIT was added
            mock_client.query.assert_called_with(
                "SELECT * FROM test_table LIMIT 1000"
            )
    
    @pytest.mark.asyncio
    async def test_execute_query_with_existing_limit(self):
        """Test that queries with existing LIMIT are not modified."""
        with patch.object(self.server, 'get_client') as mock_get_client:
            mock_client = Mock()
            mock_result = Mock()
            mock_result.result_rows = [["test"]]
            mock_client.query.return_value = mock_result
            mock_get_client.return_value = mock_client
            
            result = await self.server.execute_query({
                "query": "SELECT * FROM test_table LIMIT 50"
            })
            
            # Check that LIMIT was not added again
            mock_client.query.assert_called_with(
                "SELECT * FROM test_table LIMIT 50"
            ) 