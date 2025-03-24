import os
import hashlib
from pathlib import Path
from typing import List, Generator
from ..config.settings import SUPPORTED_EXTENSIONS

class LocalConnector:
    def __init__(self):
        self.indexed_paths = set()
        
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if the file type is supported."""
        extension = file_path.suffix.lower()
        return any(extension in exts for exts in SUPPORTED_EXTENSIONS.values())
    
    def scan_directory(self, directory_path: str, recursive: bool = True) -> Generator[str, None, None]:
        """Scan a directory for supported files."""
        try:
            directory = Path(directory_path)
            if not directory.exists():
                raise ValueError(f"Directory does not exist: {directory_path}")
            
            if not directory.is_dir():
                raise ValueError(f"Path is not a directory: {directory_path}")
            
            # Walk through directory
            for root, _, files in os.walk(directory):
                if not recursive and root != str(directory):
                    continue
                    
                for file in files:
                    file_path = Path(root) / file
                    if self._is_supported_file(file_path):
                        yield str(file_path)
                        
        except Exception as e:
            print(f"Error scanning directory {directory_path}: {str(e)}")
            
    def get_file_content(self, file_path: str) -> str:
        """Read the content of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return ""
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate checksum from the first part of a file for fast comparison."""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                # Read only first 8KB of file for fast comparison
                chunk = f.read(8192)
                hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {str(e)}")
            return ""
            
    def get_file_metadata(self, file_path: str) -> dict:
        """Get metadata for a file."""
        path = Path(file_path)
        try:
            stats = path.stat()
            
            # Calculate checksum from first 8KB of file (fast yet reasonably accurate)
            checksum = self._calculate_file_checksum(path)
            
            return {
                "file_path": str(path),
                "file_name": path.name,
                "file_type": path.suffix.lower(),
                "size": stats.st_size,
                "last_modified": stats.st_mtime,
                "created": stats.st_ctime,
                "checksum": checksum  # Add checksum to metadata
            }
        except Exception as e:
            print(f"Error getting metadata for {file_path}: {str(e)}")
            return {} 