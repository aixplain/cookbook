"""Example script demonstrating the use of FileAgent with local files."""
from dotenv import load_dotenv
load_dotenv(".env", override=True)
from datetime import datetime
from src.agent.agent import FileAgent




def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def main():
    # Initialize the agent
    agent = FileAgent(
        name="Document Assistant",
        description="An intelligent agent that helps you interact with your documents"
    )
    agent.initialize()
    
    # Index a local directory
    documents_path = "./data/test_folder_to_index"
    print(f"\nIndexing files in {documents_path}...")
    num_docs = agent.index_directory(documents_path)
    print(f"Indexed {num_docs} documents")
    
    # Show index statistics
    print("\nIndex Statistics:")
    stats = agent.get_index_stats()
    print(f"Total Files: {stats['total_files']}")
    print(f"Total Size: {format_size(stats['total_size_bytes'])}")
    print("\nFile Types:")
    for file_type, count in stats['file_types'].items():
        print(f"  {file_type}: {count} files")
    if stats['last_indexed']:
        last_indexed = datetime.fromisoformat(stats['last_indexed'])
        print(f"\nLast Indexed: {last_indexed.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Try indexing again to show unchanged files are skipped
    print("\nRe-indexing the same directory...")
    num_docs = agent.index_directory(documents_path)
    print(f"Indexed {num_docs} documents (should be 0 if no files changed)")
    
    # Example queries
    queries = [
        "What are the main topics in my documents?",
        "Find any documents related to project planning and summarize them.",
        "What are the most recently modified documents about?",
        "Find documents mentioning 'machine learning' and translate the summary to Spanish.",
        "Summarize the content of my PDF files and convert the summary to speech."
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = agent.query(query)
        print("Response:", response["output"])
        
        # Show which tools were used
        print("\nTools used:")
        for step in agent.get_intermediate_steps(response):
            for tool_step in step["tool_steps"]:
                print(f"- {tool_step['tool']}")
                
if __name__ == "__main__":
    main() 