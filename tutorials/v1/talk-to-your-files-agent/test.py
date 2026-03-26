from src.agent.agent import FileAgent

AGENT_ID="67c66af8bf07e153fb38248b"
# Create and initialize the agent
agent = FileAgent(
    name="Aixplain Handbook Assistant",
    description="An intelligent agent that helps you interact with your documents"
)
if not AGENT_ID:
    agent.initialize()
else:
    agent.initialize(agent_id=AGENT_ID)

# Index a directory
num_docs = agent.index_directory("./data/aixplain_handbook")
print(f"Indexed {num_docs} documents")

# Show stats
stats = agent.get_index_stats()
print("\nIndex Statistics:")
print(f"Total Files: {stats['total_files']}")
print(f"Total Size: {stats['total_size_bytes']} bytes")
print("File Types:", stats['file_types'])

# Test regular reindexing (should skip unchanged files)
num_docs = agent.index_directory("./data/aixplain_handbook")
print(f"\nRegular reindexing: {num_docs} documents indexed (should be 0 if no changes)")

# Test force reindexing (should process all files)
num_docs = agent.index_directory("./data/aixplain_handbook", force=True)
print(f"\nForce reindexing: {num_docs} documents indexed (should process all files)")

# Ask questions with various capabilities
# Simple search
response = agent.query("which methods are in aixplain sdk for agents?")
print(response["output"])

# Search and translate
response = agent.query("Where is turkey?")
print(response["output"])

print(response["intermediate_steps"][0]["tool_steps"][0]["input"])

# Get audio response
response = agent.query("What are the main topics in my documents? Convert the answer to speech")
print(response["output"])  # Will contain a URL to the audio file

# See what tools were used
steps = agent.get_intermediate_steps(response)
for step in steps:
    print(f"Agent: {step['agent']}")
    for tool_step in step["tool_steps"]:
        print(f"Tool: {tool_step['tool']}")
        # print(f"Output: {tool_step['output']}")
        
        
# agent.delete()
agent.deploy()
