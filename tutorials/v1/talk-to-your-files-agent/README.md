# Talk to Your Files

An intelligent agent that allows you to have conversations with your local files and Google Drive documents using docling and aiXplain's agentification features.

## Features

- Local file system integration with support for multiple file formats
  - Documents: .doc, .docx, .pdf, .txt, .rtf
  - Spreadsheets: .xls, .xlsx, .csv
  - Presentations: .ppt, .pptx
  - Text files: .md, .json, .yaml, .yml
- Google Drive integration with recursive folder scanning
- Natural language querying of document contents
- Intelligent document processing using docling
- Advanced search capabilities through aiXplain integration
- Automatic file indexing and metadata tracking
- Support for batch processing of documents
- Efficient caching and state management
- Comprehensive logging system

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with:
```
AIXPLAIN_API_KEY=your_aixplain_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

3. Google Drive Setup:
   1. Go to the [Google Cloud Console](https://console.cloud.google.com)
   2. Create a new project or select an existing one
   3. Enable the Google Drive API for your project
   4. Create OAuth 2.0 credentials:
      - Go to "Credentials" section
      - Click "Create Credentials" > "OAuth client ID"
      - Select "Desktop app" as application type
      - Download the client configuration file
   5. Rename the downloaded file to `client_secrets.json` and place it in your project root directory

4. Initialize the agent:
```python
from src.agent.agent import FileAgent

# Create and initialize the agent
agent = FileAgent()
agent.initialize()

# Authenticate with Google Drive
agent.authenticate_drive()
```

## Usage

```python
# Index local directory
agent.index_directory("/path/to/files")

# Index Google Drive folder
agent.index_drive_folder("folder_id")

# Query your documents
response = agent.query("What are the main topics discussed in my documents?")
print(response)

# Get statistics about indexed files
stats = agent.get_index_stats()
print(stats)
```

## Project Structure

- `src/`
  - `agent/`: Core agent implementation
    - `agent.py`: Main agent class with document interaction capabilities
  - `indexer/`: Document processing and indexing
    - `document_processor.py`: Handles document conversion and text extraction
    - `file_indexer.py`: Manages file indexing operations
    - `index_manager.py`: Coordinates index operations and storage
    - `index_storage.py`: Handles persistent storage of index information
  - `connectors/`: File system and Drive connectors
    - `local_connector.py`: Local file system operations
    - `drive_connector.py`: Google Drive integration
  - `config/`: Configuration settings
    - `settings.py`: Global configuration and constants
    - `aixplain_config.py`: aiXplain-specific settings
  - `utils/`: Utility functions
    - `logging_config.py`: Logging configuration
- `data/`
  - `indexed/`: Storage for indexed file metadata
- `tests/`: Test suite
- `examples/`: Example usage and notebooks

## Features in Detail

### Document Processing
- Automatic text extraction from various file formats
- Metadata tracking (file size, modification time, etc.)
- Batch processing for efficient handling of multiple files

### Search Capabilities
- Natural language queries using aiXplain's LLM
- Semantic search across all indexed documents
- Support for file type filtering and recursive search

### Google Drive Integration
- Secure OAuth 2.0 authentication
- Recursive folder scanning
- Support for Google Workspace formats
- Automatic file change detection
- Efficient caching of Drive contents

### Logging and Monitoring
- Comprehensive logging system
- File operation tracking
- Error handling and reporting
- Performance monitoring

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

MIT License 