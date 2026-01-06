**Startup Research Agent**

An AI-powered multi-agent system that researches AI startups by searching the web and scraping company websites to compile comprehensive reports.

## **🎯 Overview**

This system creates a team of specialized AI agents that work together to research startups:

* **Search Agent**: Searches the web for relevant information  
* **Scraper Agent**: Extracts detailed data from company websites  
* **Team Coordinator**: Orchestrates research and compiles findings

## **🚀 Features**

* **Multi-Agent Collaboration**: Two specialized agents work together  
* **Web Search**: Find up-to-date information on startups  
* **Website Scraping**: Extract detailed company data  
* **Structured Reports**: Generate markdown-formatted research reports  
* **Session Management**: Support for follow-up questions with context  
* **Web Deployment**: Deploy as accessible service

## **📋 Prerequisites**

* Python 3.7+  
* aiXplain SDK  
* Valid AIXPLAIN\_API\_KEY

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

1. **Search Agent**: Web search specialist using Tavily Search tool  
2. **Scraper Agent**: Website content extraction specialist  
3. **Team Agent**: Coordinates agents and compiles research

### **Workflow**

```
User Query → Team Coordinator → Search Agent → Find Startups
                               ↓
                        Scraper Agent → Extract Details
                               ↓
                        Compile Report → Markdown Output
```

## **🚀 Usage**

### **1\. Get Required Tools**

```py
from aixplain.factories import ToolFactory

# Get Tavily Search tool
search_tool = ToolFactory.get("6736411cf127849667606689")

# Get Website Scraper tool
scraper_tool = ToolFactory.get("66f423426eb563fa213a3531")
```

### **2\. Create Search Agent**

```py
from aixplain.factories import AgentFactory

search_agent = AgentFactory.create(
    name="Web Search Agent",
    description="An agent that searches the web for information",
    instructions="""
    You are a web search specialist. Your job is to:
    1. Search the web for relevant, up-to-date information
    2. Find multiple sources
    3. Extract key facts and data points
    4. Return your findings in a structured format

    Always search for recent information and cite your sources.
    """,
    tools=[
        AgentFactory.create_model_tool(
            model=search_tool.id,
            description="Search the web for current information"
        )
    ]
)
```

### **3\. Create Scraper Agent**

```py
scraper_agent = AgentFactory.create(
    name="Website Scraper Agent",
    description="An agent that scrapes websites for detailed information",
    instructions="""
    You are a website scraping specialist. Your job is to:
    1. Visit URLs provided to you
    2. Extract relevant information from the page content
    3. Focus on key details like funding, revenue, team size, etc.
    4. Return structured data

    Be thorough and extract all relevant details.
    """,
    tools=[
        AgentFactory.create_model_tool(
            model=scraper_tool.id,
            description="Scrape website content. Input must be a URL."
        )
    ]
)
```

### **4\. Create Team Agent**

```py
from aixplain.factories import TeamAgentFactory
from aixplain.modules.agent import OutputFormat

research_team = TeamAgentFactory.create(
    name="AI Startup Research Team",
    description="A team of agents that researches AI startups comprehensively",
    instructions="""
    You are a research team coordinator. Your goal is to find comprehensive
    information about AI startups.

    Process:
    1. Use the Search Agent to find relevant AI startups
    2. Use the Scraper Agent to get detailed information from their websites
    3. Compile findings into a structured report with:
       - Company name
       - Funding amount (if available)
       - What they do
       - Key details

    Be thorough and cite all sources.
    """,
    agents=[search_agent, scraper_agent],
    output_format=OutputFormat.MARKDOWN
)
```

### **5\. Run Research Query**

```py
from IPython.display import display, Markdown

response = research_team.run(
    query="""
    Find the top 5 AI startups founded in 2023-2024 and provide:
    1. Company name
    2. Total funding raised
    3. What they do (brief description)
    4. Website URL

    Format as a numbered list with clear sections.
    """
)

display(Markdown(response.data["output"]))
```

### **6\. Ask Follow-up Questions**

```py
# Get session ID for context
session_id = response.data["session_id"]

# Follow-up question
response = research_team.run(
    query="Which of these companies has raised the most funding?",
    session_id=session_id
)

display(Markdown(response.data["output"]))
```

### **7\. Deploy Team**

```py
research_team.deploy()
print(f"https://platform.aixplain.com/discover/agent/{research_team.id}")
```

## **⚙️ Configuration**

### **Customizing Search Agent**

```py
search_agent = AgentFactory.create(
    name="Custom Search Agent",
    instructions="Your custom instructions...",
    tools=[AgentFactory.create_model_tool(model=search_tool.id)]
)
```

### **Customizing Team Instructions**

```py
research_team = TeamAgentFactory.create(
    name="Custom Research Team",
    instructions="""
    Your custom team coordination instructions:
    1. Define research process
    2. Specify output format
    3. Set quality standards
    """,
    agents=[search_agent, scraper_agent],
    output_format=OutputFormat.MARKDOWN
)
```

### **Different Output Formats**

```py
# JSON output
research_team = TeamAgentFactory.create(
    output_format=OutputFormat.JSON
)

# Text output
research_team = TeamAgentFactory.create(
    output_format=OutputFormat.TEXT
)
```

## **🎯 Customization Examples**

### **Research Different Industries**

```py
response = research_team.run(
    query="Find top 5 fintech startups in Europe founded in 2024"
)
```

### **Custom Data Points**

```py
response = research_team.run(
    query="""
    Research AI healthcare startups and provide:
    - Company name and location
    - Founders and leadership team
    - Technology focus area
    - Clinical partnerships
    - Regulatory approvals
    """
)
```

### **Adding More Agents**

```py
# Create additional specialized agent
analysis_agent = AgentFactory.create(
    name="Analysis Agent",
    description="Analyzes and compares startup data",
    instructions="Your analysis instructions..."
)

# Add to team
research_team = TeamAgentFactory.create(
    agents=[search_agent, scraper_agent, analysis_agent]
)
```

## **🔍 Troubleshooting**

Common issues and solutions:

* **Search returns no results**: Check search query specificity and try broader terms  
* **Scraper fails**: Verify URL is accessible and website allows scraping  
* **Incomplete data**: Review agent instructions for clarity and completeness  
* **Session expired**: Generate new session\_id or start fresh conversation

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
* Verify tool IDs are correct and accessible

