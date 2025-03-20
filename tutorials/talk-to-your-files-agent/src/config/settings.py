import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
INDEXED_DIR = DATA_DIR / "indexed"

# Create directories if they don't exist
INDEXED_DIR.mkdir(parents=True, exist_ok=True)

# API Keys and credentials
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# Supported file types
SUPPORTED_EXTENSIONS = {
    "document": [".doc", ".docx", ".pdf", ".txt", ".rtf"],
    "spreadsheet": [".xls", ".xlsx", ".csv"],
    "presentation": [".ppt", ".pptx"],
    "text": [".md", ".json", ".yaml", ".yml", ".html", ".htm"]
}

# Indexing settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
BATCH_SIZE = 10  # Number of files to process in one batch

# Agent settings
DEFAULT_CONTEXT_WINDOW = 2000  # Number of tokens for context window
MAX_RETRIES = 3  # Maximum number of retries for API calls 