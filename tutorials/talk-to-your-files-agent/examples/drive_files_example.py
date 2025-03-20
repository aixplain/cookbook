"""Example script demonstrating the use of FileAgent with Google Drive files."""
from dotenv import load_dotenv
load_dotenv(".env", override=True)

import os
from src.agent.agent import FileAgent

def main():
    # Initialize the agent
    agent = FileAgent(
        name="Drive Document Assistant",
        description="An intelligent agent that helps you interact with your Google Drive documents"
    )
    agent.initialize()
    
    # Authenticate with Google Drive
    credentials_path = os.path.expanduser("~/.credentials/drive_token.json")
    print("\nAuthenticating with Google Drive...")
    agent.authenticate_drive(credentials_path)
    
    # Index a Google Drive folder
    folder_id = "your_folder_id_here"  # Replace with actual folder ID
    print(f"\nIndexing files in Drive folder {folder_id}...")
    num_docs = agent.index_drive_folder(folder_id)
    print(f"Indexed {num_docs} documents")
    
    # Example queries
    queries = [
        "What types of documents are in my Drive folder?",
        "Find any spreadsheets related to budget planning and summarize them.",
        "What are the most recently modified presentations about?",
        "Find documents mentioning 'quarterly report' and translate the summary to French.",
        "Find all meeting notes from last month and convert them to speech."
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