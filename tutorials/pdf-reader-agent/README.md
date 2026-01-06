# **PDF Reader (RAG) Agent**

An AI-powered agent that answers questions from PDF documents using retrieval-augmented generation and semantic search.

## **🎯 Overview**

This system creates an intelligent agent that reads and queries PDF documents:

* **Docling Model**: Extracts text from PDFs  
* **Vector Index**: Semantic search across documents  
* **RAG Agent**: Answers questions with source attribution  
* **Session Management**: Supports follow-up questions with context

## **🚀 Features**

* **Automatic PDF Processing**: Extract and index text from PDFs  
* **Semantic Search**: AI-powered document search  
* **Source Attribution**: Cites document sources and authors  
* **Conversational Interface**: Context-aware follow-up questions  
* **Batch Processing**: Handle multiple documents efficiently  
* **Web Deployment**: Deploy as accessible service

## **📋 Prerequisites**

## **🛠️ Installation**

1. Install the aiXplain SDK:

```shell
pip install aixplain
```

2. Set your API key:

```py
import os
os.environ["AIXPLAIN_API_KEY"] = "YOUR-API-KEY"
```

## **🏗️ Architecture**

### **Components**

1. **File Upload**: Upload PDFs to storage  
2. **Docling Model**: Extract text from PDFs  
3. **Vector Index**: Store and search embeddings  
4. **RAG Agent**: Query documents and generate answers

### **Data Flow**

```
PDF Upload → Docling → Record Creation → Index
                                          ↓
User Query → Agent → Search → Response
```

## **🚀 Usage**

### **1\. Upload and Process PDFs**

```py
from aixplain.factories import FileFactory, ModelFactory

# Upload PDF
s3_link = FileFactory.create("document.pdf", is_temp=True)

# Get Docling model and extract text
docling = ModelFactory.get("677bee6c6eb56331f9192a91")
text = docling.run(pdf_url).data
```

### **2\. Create Index and Add Documents**

```py
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record

# Create index
index = IndexFactory.create(
    name="My Documents",
    description="Document collection"
)

# Create records with metadata
records = []
for doc in data:
    text = docling.run(doc["pdf_url"]).data
    record = Record(
        id=doc["id"],
        value=text,
        attributes={
            "author": doc["author"],
            "title": doc["title"],
            "source": doc["pdf_url"]
        }
    )
    records.append(record)

# Upload to index
index.upsert(records)
```

### **3\. Create Agent**

```py
from aixplain.factories import AgentFactory

agent_instructions = '''
You are an AI assistant specialized in retrieving information from PDF documents.

RULES:
1. ONLY use your search tool to answer questions
2. DO NOT use your internal knowledge
3. ALWAYS cite the source document and author
4. If you can't find the answer in the PDFs, say so clearly
'''

agent = AgentFactory.create(
    name="PDF Reader Agent",
    description="Answers questions using PDF documents",
    instructions=agent_instructions,
    tools=[AgentFactory.create_model_tool(model=index.id)]
)
```

### **4\. Query the Agent**

```py
# Ask a question
response = agent.run("What roadside cover do I have?")
print(response.data.output)

# Follow-up question
session_id = response.data.session_id
response = agent.run(
    "Who would I contact for assistance?",
    session_id=session_id
)
print(response.data.output)
```

### **5\. Deploy Agent**

```py
agent.deploy()
print(f"https://platform.aixplain.com/discover/agent/{agent.id}")
```

## **⚙️ Configuration**

### **Document Data Structure**

```py
data = [
    {
        "id": "doc_1",
        "pdf_url": "path/to/document.pdf",
        "author": "Author Name",
        "title": "Document Title"
    },
]
```

### **Batch Processing**

```py
# Upload in batches of 500
for i in range(0, len(records), 500):
    batch = records[i:i + 500]
    index.upsert(batch)
    
# Verify upload
print(f"Total documents: {index.count()}")
```

## **🎯 Customization Examples**

### **Custom Metadata**

```py
record = Record(
    id=doc["id"],
    value=text,
    attributes={
        "author": doc["author"],
        "title": doc["title"],
        "source": doc["pdf_url"],
        "date": doc["publication_date"],
        "category": doc["document_type"]
    }
)
```

### **Multiple Indexes**

```py
# Create separate indexes
legal_index = IndexFactory.create(name="Legal Documents")
technical_index = IndexFactory.create(name="Technical Docs")

# Agent with multiple tools
agent = AgentFactory.create(
    name="Multi-Index Agent",
    tools=[
        AgentFactory.create_model_tool(model=legal_index.id),
        AgentFactory.create_model_tool(model=technical_index.id)
    ]
)
```

## **🔍 Troubleshooting**

Common issues and solutions:

* **PDF extraction fails**: Ensure PDF is not password-protected or image-only  
* **No search results**: Verify documents uploaded with `index.count()`  
* **Generic answers**: Strengthen agent instructions to enforce tool usage  
* **Slow responses**: Break large documents into smaller chunks

## **🤝 Contributing**

1. Fork the repository  
2. Create a feature branch  
3. Make your changes  
4. Test thoroughly  
5. Submit a pull request

## **📝 License**

This project is licensed under the MIT License \- see the LICENSE file for details.

## **🆘 Support**

For issues and questions:

* Check the aiXplain SDK documentation  
* Ensure your API key is valid and has proper permissions  
* Verify PDF format compatibility

