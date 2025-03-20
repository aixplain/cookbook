from pathlib import Path
from typing import Dict, Any, Optional
from docling.document_converter import DocumentConverter
from ..config.settings import SUPPORTED_EXTENSIONS

class DocumentProcessor:
    def __init__(self):
        self.converter = DocumentConverter()
        # Get list of actually supported formats from docling
        self.docling_supported_formats = self._get_docling_supported_formats()
        
    def _get_docling_supported_formats(self) -> list:
        """Get the actual list of formats supported by docling."""
        try:
            # Try to get the supported formats from docling
            return self.converter.get_supported_formats()
        except:
            # If method doesn't exist, provide a conservative list of known working formats
            return [".pdf", ".docx", ".pptx", ".xlsx"]
        
    def is_supported_file(self, file_path: str) -> bool:
        """Check if the file type is supported."""
        extension = Path(file_path).suffix.lower()
        return any(extension in exts for exts in SUPPORTED_EXTENSIONS.values())
    
    def is_docling_supported(self, file_path: str) -> bool:
        """Check if the file type is actually supported by docling."""
        extension = Path(file_path).suffix.lower()
        return extension in self.docling_supported_formats
    
    def process_document(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Process a document using docling and return its content and metadata."""
        try:
            if not self.is_supported_file(file_path):
                raise ValueError(f"Unsupported file type: {file_path}")
            
            # Check if docling actually supports this format
            if not self.is_docling_supported(file_path):
                print(f"Warning: File {file_path} has a supported extension but docling cannot process it")
                # For text files we can try a simple fallback
                if Path(file_path).suffix.lower() in [".txt", ".md", ".html", ".htm"]:
                    return self._process_text_file(file_path)
                return None
            
            # Add debug logging
            print(f"Processing document: {file_path}")
            
            # Convert document using docling
            result = self.converter.convert(file_path)
            
            # Check if conversion produced results
            if not result or not result.document:
                print(f"Docling conversion failed for {file_path}")
                return None
            
            # Extract text content
            markdown_content = result.document.export_to_markdown()
            
            # Add more debugging
            print(f"Extracted content length: {len(markdown_content) if markdown_content else 0}")
            
            # Get metadata
            metadata = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "file_type": Path(file_path).suffix.lower(),
                "size": Path(file_path).stat().st_size,
                "last_modified": Path(file_path).stat().st_mtime
            }
            
            return {
                "content": markdown_content,
                "metadata": metadata
            }
            
        except Exception as e:
            print(f"Error processing document {file_path}: {str(e)}")
            return None
            
    def _process_text_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Simple processor for text files when docling fails."""
        try:
            # Read the text content directly
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"Processed text file directly: {file_path}, content length: {len(content)}")
            
            # Get metadata
            metadata = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "file_type": Path(file_path).suffix.lower(),
                "size": Path(file_path).stat().st_size,
                "last_modified": Path(file_path).stat().st_mtime
            }
            
            return {
                "content": content,
                "metadata": metadata
            }
        except Exception as e:
            print(f"Error processing text file {file_path}: {str(e)}")
            return None
    
    def batch_process(self, file_paths: list[str]) -> list[Dict[str, Any]]:
        """Process multiple documents in batch."""
        results = []
        for file_path in file_paths:
            result = self.process_document(file_path)
            if result:
                results.append(result)
        return results 