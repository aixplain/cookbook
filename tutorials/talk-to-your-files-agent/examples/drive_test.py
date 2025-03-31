"""Test script for Google Drive integration with FileAgent."""
from dotenv import load_dotenv
load_dotenv(".env", override=True)

import os
from datetime import datetime
from src.agent.agent import FileAgent
from src.utils.logging_config import setup_logging, get_logger

# Set up logging
setup_logging()
logger = get_logger('drive_test')

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def test_drive_authentication():
    """Test Google Drive authentication."""
    agent = FileAgent(
        name="Drive Test Agent",
        description="Testing Google Drive integration"
    )
    agent.initialize()
    
    # Set up credentials path
    credentials_dir = os.path.expanduser("~/.credentials")
    os.makedirs(credentials_dir, exist_ok=True)
    credentials_path = os.path.join(credentials_dir, "drive_token.json")
    
    # Test authentication
    logger.info("Testing Drive authentication...")
    try:
        agent.authenticate_drive(credentials_path)
        logger.info("Drive authentication successful")
        return agent
    except Exception as e:
        logger.error(f"Drive authentication failed: {e}", exc_info=True)
        raise

def test_drive_indexing(agent: FileAgent, folder_id: str):
    """Test indexing files from Google Drive."""
    logger.info(f"Testing Drive folder indexing for folder: {folder_id}")
    
    try:
        # First indexing
        logger.info("First indexing run...")
        num_docs = agent.index_drive_folder(folder_id)
        logger.info(f"First indexing complete: {num_docs} documents indexed")
        
        # Show index statistics
        stats = agent.get_index_stats()
        logger.info("\nIndex Statistics:")
        logger.info(f"Total Files: {stats['total_files']}")
        logger.info(f"Total Size: {format_size(stats['total_size_bytes'])}")
        logger.info("\nFile Types:")
        for file_type, count in stats['file_types'].items():
            logger.info(f"  {file_type}: {count} files")
        if stats['last_indexed']:
            last_indexed = datetime.fromisoformat(stats['last_indexed'])
            logger.info(f"\nLast Indexed: {last_indexed.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test reindexing (should skip unchanged files)
        logger.info("\nTesting reindexing (should skip unchanged files)...")
        num_docs = agent.index_drive_folder(folder_id)
        logger.info(f"Reindexing complete: {num_docs} documents indexed (should be 0 if no changes)")
        
        return True
    except Exception as e:
        logger.error(f"Drive indexing failed: {e}", exc_info=True)
        return False

def test_drive_queries(agent: FileAgent):
    """Test querying indexed Drive documents."""
    logger.info("Testing queries on Drive documents...")
    
    test_queries = [
        "List all documents in my Drive folder",
        "What are the most recently modified files?",
        "Find any spreadsheets and summarize their content",
        "Find documents containing the word 'test' and translate the summary to Spanish",
        "What are the main topics discussed in these documents?"
    ]
    
    for query in test_queries:
        try:
            logger.info(f"\nExecuting query: {query}")
            response = agent.query(query)
            logger.info(f"Query successful, response length: {len(response['output'])}")
            
            # Show which tools were used
            logger.debug("Tools used:")
            for step in agent.get_intermediate_steps(response):
                for tool_step in step["tool_steps"]:
                    logger.debug(f"- {tool_step['tool']}")
                    
        except Exception as e:
            logger.error(f"Query failed: {e}", exc_info=True)

def main():
    """Run Drive integration tests."""
    logger.info("Starting Drive integration tests")
    
    try:
        # Get folder ID
        test_folder_id = input("Enter your Google Drive folder ID: ")
        logger.info(f"Using Drive folder ID: {test_folder_id}")
        
        # Test authentication
        agent = test_drive_authentication()
        
        if agent:
            # Test indexing
            if test_drive_indexing(agent, test_folder_id):
                # Test queries
                test_drive_queries(agent)
                
    except Exception as e:
        logger.error(f"Test suite failed: {e}", exc_info=True)
    finally:
        logger.info("Drive integration tests completed")
        
if __name__ == "__main__":
    main() 