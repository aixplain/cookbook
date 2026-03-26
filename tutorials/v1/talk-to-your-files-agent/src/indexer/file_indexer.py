import json
from pathlib import Path
from typing import Dict, Any, List
from aixplain.factories import ModelFactory
from ..config.settings import INDEXED_DIR, MAX_FILE_SIZE, BATCH_SIZE
from .document_processor import DocumentProcessor

class FileIndexer:
    def __init__(self, model_id: str):
        self.model = ModelFactory.get(model_id)
        self.document_processor = DocumentProcessor()
        self.index_path = INDEXED_DIR / "index.json"
        self.document_index = self._load_index()
        
    def _load_index(self) -> Dict[str, Any]:
        """Load the existing index or create a new one."""
        if self.index_path.exists():
            with open(self.index_path, "r") as f:
                return json.load(f)
        return {}
    
    def _save_index(self):
        """Save the current index to disk."""
        with open(self.index_path, "w") as f:
            json.dump(self.document_index, f, indent=2)
            
    def _should_index_file(self, file_path: str) -> bool:
        """Check if a file should be indexed based on size and last modified time."""
        path = Path(file_path)
        if not path.exists():
            return False
            
        if path.stat().st_size > MAX_FILE_SIZE:
            return False
            
        # Check if file has been modified since last indexing
        if file_path in self.document_index:
            last_indexed = self.document_index[file_path]["metadata"]["last_modified"]
            current_mtime = path.stat().st_mtime
            if current_mtime <= last_indexed:
                return False
                
        return True
    
    def index_files(self, file_paths: List[str]):
        """Index a batch of files to aiXplain."""
        # Filter files that need indexing
        files_to_index = [f for f in file_paths if self._should_index_file(f)]
        
        # Process in batches
        for i in range(0, len(files_to_index), BATCH_SIZE):
            batch = files_to_index[i:i + BATCH_SIZE]
            processed_docs = self.document_processor.batch_process(batch)
            
            for doc in processed_docs:
                try:
                    # Index to aiXplain
                    result = self.model.run({
                        "content": doc["content"],
                        "metadata": doc["metadata"]
                    })
                    
                    if result.status == "COMPLETED":
                        # Store in local index
                        self.document_index[doc["metadata"]["file_path"]] = {
                            "aixplain_id": result.id,
                            "metadata": doc["metadata"]
                        }
                    else:
                        print(f"Failed to index {doc['metadata']['file_path']}: {result.error_message}")
                        
                except Exception as e:
                    print(f"Error indexing {doc['metadata']['file_path']}: {str(e)}")
            
            # Save index after each batch
            self._save_index()
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """Get indexed document information."""
        return self.document_index.get(file_path) 