from typing import List, Dict, Any, Optional
from aixplain.factories import AgentFactory
from aixplain.modules.agent.tool.model_tool import ModelTool
from ..indexer.index_manager import IndexManager
from ..connectors.local_connector import LocalConnector
from ..connectors.drive_connector import DriveConnector
from ..config.aixplain_config import create_tool, DEFAULT_LLM_ID, MAX_FILE_SIZE

class FileAgent:
    def __init__(self, name: str = "File Assistant", description: str = "An agent that helps you interact with your documents"):
        """Initialize the file agent."""
        self.name = name
        self.description = description
        self.local_connector = LocalConnector()
        self.drive_connector = DriveConnector()
        self.index_manager = None
        self.agent = None
        
    def initialize(self, llm_id: str = DEFAULT_LLM_ID, agent_id: str = None):
        """Initialize the agent with necessary tools and index."""
        # Create index for documents with a unique identifier
        self.index_manager = IndexManager(
            name=f"{self.name} Index",
            description=f"Index for {self.name}'s document collection",
            agent_id=self.name.replace(" ", "_").lower()
        )
        
        if agent_id:
            self.agent = AgentFactory.get(agent_id)
        else:
            # Create tools
            tools = [
                create_tool("speech_synthesis"),
                create_tool("translation"),
                create_tool("speech_recognition"),
                ModelTool(
                    model=self.index_manager.id,
                    description="This tool searches through indexed documents to find relevant information."
                )
            ]
            
            # Create agent
            self.agent = AgentFactory.create(
                name=self.name,
                description=self.description,
                tools=tools,
                llm_id=llm_id
            )
        
    def authenticate_drive(self, credentials_path: str = None):
        """Authenticate with Google Drive."""
        self.drive_connector.authenticate(credentials_path)
        
    def index_directory(self, directory_path: str, recursive: bool = True, force: bool = False) -> int:
        """Index all supported files in a directory, checking size before processing."""
        if not self.index_manager:
            raise ValueError("Agent not initialized. Call initialize() first.")
            
        # Scan directory for files
        files = list(self.local_connector.scan_directory(directory_path, recursive))
        
        # Prepare documents for indexing
        documents = []
        for file_path in files:
            # Check file size before processing
            file_size = self.local_connector.get_file_metadata(file_path).get('size', 0)
            if file_size <= MAX_FILE_SIZE:
                doc = {
                    "file_path": file_path,
                    "size": file_size
                }
                if force:
                    doc["force"] = True
                documents.append(doc)
        
        # Add to index
        return self.index_manager.add_documents(documents)
        
    def index_drive_folder(self, folder_id: str, recursive: bool = True, max_size: int = 10**6) -> int:
        """Index all supported files in a Google Drive folder, checking size before processing."""
        if not self.index_manager:
            raise ValueError("Agent not initialized. Call initialize() first.")
            
        if not self.drive_connector.service:
            raise ValueError("Not authenticated with Google Drive. Call authenticate_drive() first.")
            
        # Scan Drive folder for files
        documents = []
        for file_info in self.drive_connector.scan_folder(folder_id, recursive):
            try:
                # Get metadata and check file size before downloading
                metadata = self.drive_connector.get_file_metadata(file_info['id'])
                file_size = metadata.get('size', 0)
                if file_size <= max_size:
                    documents.append({
                        "file_id": file_info['id'],
                        "metadata": metadata
                    })
            
            except Exception as e:
                print(f"Error processing Drive file {file_info['name']}: {str(e)}")
                
        # Add to index
        return self.index_manager.add_documents(documents)
        
    def query(self, question: str, **kwargs) -> Dict[str, Any]:
        """Query the agent with a natural language question."""
        if not self.agent:
            raise ValueError("Agent not initialized. Call initialize() first.")
            
        try:
            response = self.agent.run(question, **kwargs)
            return response["data"]
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return {
                "output": "I apologize, but I encountered an error while processing your query.",
                "error": str(e)
            }
    
    def get_intermediate_steps(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get the intermediate steps from an agent response."""
        return response.get("intermediate_steps", [])
        
    def get_indexed_files(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all indexed files."""
        if not self.index_manager:
            raise ValueError("Agent not initialized. Call initialize() first.")
        return self.index_manager.get_indexed_files()
        
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed files."""
        files = self.get_indexed_files()
        
        total_size = 0
        file_types = {}
        last_indexed = None
        
        for file_info in files.values():
            metadata = file_info["metadata"]
            
            # Update total size
            total_size += metadata.get("size", 0)
            
            # Count file types
            file_type = metadata.get("file_type", "unknown")
            file_types[file_type] = file_types.get(file_type, 0) + 1
            
            # Track last indexed time
            indexed_time = file_info.get("last_indexed")
            if indexed_time and (not last_indexed or indexed_time > last_indexed):
                last_indexed = indexed_time
                
        return {
            "total_files": len(files),
            "total_size_bytes": total_size,
            "file_types": file_types,
            "last_indexed": last_indexed
        } 
        
    
    def deploy(self):
        """Deploy the agent to the cloud."""
        self.agent.deploy()
        return f"Agent {self.name} deployed successfully with id {self.agent.id}."