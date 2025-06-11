"""Module for managing persistent storage of index information."""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class IndexStorage:
    def __init__(self, storage_dir: str):
        """Initialize the index storage."""
        self.storage_dir = Path(storage_dir)
        self.index_file = self.storage_dir / "index_state.json"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._load_state()
        
    def _load_state(self):
        """Load the index state from disk."""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    self.state = json.load(f)
                logger.info(f"Loaded index state from {self.index_file}")
            else:
                self.state = {
                    "files": {},  # File states
                    "last_update": None,  # Last update timestamp
                    "index_id": None,  # aiXplain index ID
                }
                logger.info("Created new index state")
        except Exception as e:
            logger.error(f"Error loading index state: {e}")
            self.state = {
                "files": {},
                "last_update": None,
                "index_id": None,
            }
            
    def _save_state(self):
        """Save the current state to disk."""
        backup_file = None
        try:
            # Create a backup of the current state file
            if self.index_file.exists():
                backup_file = self.index_file.with_suffix('.json.bak')
                self.index_file.rename(backup_file)
            
            # Write new state
            with open(self.index_file, 'w') as f:
                json.dump(self.state, f, indent=2)
                
            # Remove backup if save was successful
            if backup_file and backup_file.exists():
                backup_file.unlink()
                
            logger.debug("Successfully saved index state")
            
        except Exception as e:
            logger.error(f"Error saving index state: {e}")
            # Restore backup if available
            if backup_file and backup_file.exists():
                backup_file.rename(self.index_file)
                logger.info("Restored index state from backup")
            raise
            
    def get_file_state(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get the stored state of a file."""
        return self.state["files"].get(str(file_path))
        
    def update_file_state(self, file_path: str, metadata: Dict[str, Any]):
        """Update the state of a file."""
        try:
            self.state["files"][str(file_path)] = {
                "metadata": metadata,
                "last_indexed": datetime.now().isoformat()
            }
            self._save_state()
            logger.debug(f"Updated state for file: {file_path}")
        except Exception as e:
            logger.error(f"Error updating file state for {file_path}: {e}")
            raise
        
    def remove_file(self, file_path: str):
        """Remove a file from the index state."""
        try:
            self.state["files"].pop(str(file_path), None)
            self._save_state()
            logger.debug(f"Removed file from state: {file_path}")
        except Exception as e:
            logger.error(f"Error removing file {file_path} from state: {e}")
            raise
        
    def needs_indexing(self, file_path: str, current_metadata: Dict[str, Any]) -> bool:
        """Check if a file needs to be indexed based on its current state."""
        try:
            stored_state = self.get_file_state(file_path)
            
            if not stored_state:
                logger.debug(f"File not previously indexed: {file_path}")
                return True
                
            stored_metadata = stored_state["metadata"]
            
            # First time indexing after adding checksum - force reindex
            if "checksum" in current_metadata and "checksum" not in stored_metadata:
                logger.debug(f"First indexing with checksum, forcing reindex: {file_path}")
                return True
                
            # First check if checksum exists and differs (most accurate)
            if "checksum" in current_metadata and "checksum" in stored_metadata:
                checksum_changed = stored_metadata.get("checksum") != current_metadata.get("checksum")
                if checksum_changed:
                    logger.debug(f"File content changed (checksum): {file_path}")
                    return True
            else:
                # Fall back to traditional metadata if checksums not available
                size_changed = stored_metadata.get("size") != current_metadata.get("size")
                time_changed = stored_metadata.get("last_modified") != current_metadata.get("last_modified")
                
                if size_changed or time_changed:
                    logger.debug(f"File changed (size={size_changed}, time={time_changed}): {file_path}")
                    return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error checking if file needs indexing {file_path}: {e}")
            # If there's an error checking the state, assume we need to index
            return True
        
    def set_index_id(self, index_id: str):
        """Set the aiXplain index ID."""
        try:
            self.state["index_id"] = index_id
            self.state["last_update"] = datetime.now().isoformat()
            self._save_state()
            logger.info(f"Set index ID: {index_id}")
        except Exception as e:
            logger.error(f"Error setting index ID: {e}")
            raise
        
    def get_index_id(self) -> Optional[str]:
        """Get the stored aiXplain index ID."""
        return self.state.get("index_id")
        
    def get_indexed_files(self) -> Dict[str, Dict[str, Any]]:
        """Get all indexed files and their states."""
        return self.state["files"] 