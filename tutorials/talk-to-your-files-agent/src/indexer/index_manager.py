from typing import List, Dict, Any
from pathlib import Path
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record
from .document_processor import DocumentProcessor
from .index_storage import IndexStorage
from ..connectors.local_connector import LocalConnector
from ..connectors.drive_connector import DriveConnector
from ..config.settings import INDEXED_DIR
from ..utils.logging_config import get_logger

logger = get_logger('indexer')

class IndexManager:
    def __init__(self, name: str, description: str, agent_id: str):
        """Initialize the index manager with a unique index for each agent."""
        # Create a unique directory for each agent's index state
        agent_index_dir = INDEXED_DIR / agent_id
        agent_index_dir.mkdir(parents=True, exist_ok=True)
        
        self.storage = IndexStorage(agent_index_dir)
        self.document_processor = DocumentProcessor()
        self.local_connector = LocalConnector()
        self.drive_connector = DriveConnector()
        
        # Try to reuse existing index if available
        existing_index_id = self.storage.get_index_id()
        if existing_index_id:
            try:
                self.index = IndexFactory.get(existing_index_id)
                logger.info(f"Reusing existing index: {existing_index_id}")
            except Exception as e:
                logger.warning(f"Failed to get existing index: {e}")
                self.index = self._create_new_index(name, description)
        else:
            self.index = self._create_new_index(name, description)
            
    def _create_new_index(self, name: str, description: str):
        """Create a new aiXplain index."""
        try:
            index = IndexFactory.create(name=name, description=description)
            self.storage.set_index_id(index.id)
            logger.info(f"Created new index: {index.id}")
            return index
        except Exception as e:
            if "Collection name already exists" in str(e):
                logger.warning(f"Index with name {name} already exists. Using existing index.")
                return IndexFactory.get(self.storage.get_index_id())
            else:
                logger.error(f"Failed to create index: {e}", exc_info=True)
                raise
            
        
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the index, processing them and skipping unchanged files."""
        records_to_index = []
        skipped_count = 0
        error_count = 0
        
        for doc_info in documents:
            try:
                file_path = doc_info.get("file_path")
                file_id = doc_info.get("file_id")
                metadata = doc_info.get("metadata", {})
                content = None
                force = doc_info.get("force", False)
                
                # Handle local files
                if file_path:
                    # Get metadata with checksum but WITHOUT processing the document content
                    file_metadata = self.local_connector.get_file_metadata(file_path)
                    
                    # Skip if file hasn't changed and we're not forcing reindex
                    if not force and not self.storage.needs_indexing(file_path, file_metadata):
                        logger.debug(f"Skipping unchanged file: {file_path}")
                        skipped_count += 1
                        continue
                    
                    # Only process the document content if we determined it needs indexing
                    processed_doc = self.document_processor.process_document(file_path)
                    if not processed_doc:
                        logger.error(f"No content extracted for document {file_path}")
                        continue
                        
                    # Keep the checksum we already calculated
                    processed_doc["metadata"]["checksum"] = file_metadata.get("checksum", "")
                    metadata = processed_doc["metadata"]
                    content = processed_doc["content"]
                
                # Handle Google Drive files
                elif file_id:
                    if not metadata:
                        # This should already be provided by the agent but just in case
                        metadata = self.drive_connector.get_file_metadata(file_id)
                    
                    # For Drive files, we use the file_id as the key
                    if not self.storage.needs_indexing(file_id, metadata):
                        logger.debug(f"Skipping unchanged Drive file: {file_id}")
                        skipped_count += 1
                        continue
                    
                    # Download and process the file
                    file_content = self.drive_connector.download_file(file_id)
                    if not file_content:
                        continue
                    
                    # Process the document (this would need to be updated to handle file content)
                    # For now, just use the plain content as text
                    content = file_content.getvalue().decode('utf-8', errors='replace')
                
                if not content:
                    logger.error(f"No content extracted for document {file_path or file_id}")
                    continue
                
                # Create record for indexing
                record = Record(
                    value=content,
                    value_type="text",
                    id=file_path or file_id,
                    attributes=metadata
                )
                records_to_index.append(record)
                
                # Update storage with new state
                file_key = file_path or file_id
                if file_key:
                    self.storage.update_file_state(file_key, metadata)
                    logger.info(f"Prepared file for indexing: {file_key} (size: {metadata.get('size', 0)} bytes)")
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing document {file_path or file_id}: {e}", exc_info=True)
        
        # Only make API call if there are documents to index
        if records_to_index:
            try:
                self.index.upsert(records_to_index)
                logger.info(f"Successfully indexed {len(records_to_index)} new or modified documents")
                for record in records_to_index:
                    logger.debug(f"Successfully indexed file: {record.id}")
            except Exception as e:
                logger.error(f"Error upserting documents to index: {e}", exc_info=True)
                raise
                
        logger.info(f"Indexing summary: {len(records_to_index)} indexed, {skipped_count} skipped, {error_count} errors")
        return len(records_to_index)
            
    def search(self, query: str, **kwargs):
        """Search the index with the given query."""
        try:
            logger.debug(f"Searching index with query: {query}")
            result = self.index.search(query, **kwargs)
            logger.debug(f"Search completed successfully")
            return result
        except Exception as e:
            logger.error(f"Search failed: {e}", exc_info=True)
            raise
    
    def get_indexed_files(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all indexed files."""
        return self.storage.get_indexed_files()
    
    @property
    def id(self):
        """Get the index ID."""
        return self.index.id 