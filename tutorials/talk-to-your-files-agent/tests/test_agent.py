"""Test suite for the FileAgent class."""

import os
import pytest
from unittest.mock import Mock, patch
from src.agent.agent import FileAgent
from src.indexer.index_manager import IndexManager
from aixplain.factories import AgentFactory, IndexFactory

@pytest.fixture
def mock_index():
    """Create a mock index."""
    index = Mock()
    index.id = "test_index_id"
    return index

@pytest.fixture
def mock_agent():
    """Create a mock agent."""
    agent = Mock()
    agent.run.return_value = {
        "data": {
            "output": "Test response",
            "intermediate_steps": [
                {
                    "agent": "test_agent",
                    "tool_steps": [
                        {
                            "tool": "search",
                            "output": "Test search result"
                        }
                    ]
                }
            ]
        }
    }
    return agent

@pytest.fixture
def file_agent(mock_index, mock_agent):
    """Create a FileAgent instance with mocked dependencies."""
    with patch('src.indexer.index_manager.IndexFactory.create') as mock_index_factory:
        with patch('src.agent.agent.AgentFactory.create') as mock_agent_factory:
            mock_index_factory.return_value = mock_index
            mock_agent_factory.return_value = mock_agent
            
            agent = FileAgent()
            agent.initialize()
            return agent

def test_initialization(file_agent):
    """Test agent initialization."""
    assert file_agent.name == "File Assistant"
    assert file_agent.description == "An agent that helps you interact with your documents"
    assert file_agent.index_manager is not None
    assert file_agent.agent is not None

def test_index_directory(file_agent, tmp_path):
    """Test indexing a local directory."""
    # Create test files
    test_file = tmp_path / "test.txt"
    test_file.write_text("Test content")
    
    # Index directory
    num_docs = file_agent.index_directory(str(tmp_path))
    assert num_docs == 1

def test_query(file_agent):
    """Test querying the agent."""
    response = file_agent.query("Test question")
    assert response["output"] == "Test response"
    
    steps = file_agent.get_intermediate_steps(response)
    assert len(steps) == 1
    assert steps[0]["agent"] == "test_agent"
    assert steps[0]["tool_steps"][0]["tool"] == "search"

@pytest.mark.asyncio
async def test_drive_integration(file_agent):
    """Test Google Drive integration."""
    with patch('src.connectors.drive_connector.DriveConnector.authenticate') as mock_auth:
        with patch('src.connectors.drive_connector.DriveConnector.scan_folder') as mock_scan:
            # Mock Drive API responses
            mock_scan.return_value = [
                {
                    'id': 'test_file_id',
                    'name': 'test.txt',
                    'modified_time': '2024-01-01T00:00:00Z',
                    'size': 1024
                }
            ]
            
            # Test Drive authentication
            file_agent.authenticate_drive("test_credentials.json")
            mock_auth.assert_called_once_with("test_credentials.json")
            
            # Test indexing Drive folder
            num_docs = file_agent.index_drive_folder("test_folder_id")
            assert num_docs == 1
            mock_scan.assert_called_once_with("test_folder_id", True)

def test_error_handling(file_agent):
    """Test error handling in the agent."""
    # Test initialization error
    uninit_agent = FileAgent()
    with pytest.raises(ValueError, match="Agent not initialized"):
        uninit_agent.query("Test question")
        
    # Test Drive authentication error
    with pytest.raises(ValueError, match="Not authenticated with Google Drive"):
        file_agent.index_drive_folder("test_folder_id")
        
    # Test query error
    file_agent.agent.run.side_effect = Exception("Test error")
    response = file_agent.query("Test question")
    assert "error" in response
    assert response["output"].startswith("I apologize") 