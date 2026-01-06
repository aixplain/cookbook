**Perplexity Research Agent**

An AI-powered content strategy research agent that identifies high-value content opportunities for B2B AI companies using Perplexity's research capabilities and automatically creates Google Sheets reports.

## **🎯 Overview**

This agent automates content opportunity research:

* **Perplexity Research**: Analyzes content landscape, trends, and gaps  
* **Competitor Analysis**: Identifies what competitors are NOT covering  
* **Community Insights**: Mines Reddit, LinkedIn, and forum discussions  
* **SEO Analysis**: Assesses search demand and competition levels  
* **Automated Reporting**: Creates structured Google Sheets with findings

## **🚀 Features**

* **Comprehensive Research**: Identifies 8-10+ distinct content opportunities  
* **Multi-Source Analysis**: Combines search data, discussions, and trends  
* **Structured Output**: Table format with 9 key data points per opportunity  
* **Priority Scoring**: Ranks opportunities based on impact potential  
* **Google Sheets Integration**: Auto-generates shareable spreadsheet reports  
* **Session Management**: Supports follow-up queries and refinement

## **📋 Prerequisites**

* Python 3.7+  
* aiXplain SDK  
* Valid AIXPLAIN\_API\_KEY  
* Perplexity account connected to aiXplain  
* Google account connected to aiXplain

## **🔧 Setup**

### **1\. Connect Integrations**

1. Go to [studio.aixplain.com](https://studio.aixplain.com/)  
2. Navigate to **Integrations**  
3. Connect your **Perplexity** account  
4. Connect your **Google** account  
5. Go to **Tools** section  
6. Copy the tool IDs for Perplexity and Google Sheets

### **2\. Install SDK**

```shell
pip install aixplain
```

### **3\. Set API Key**

```py
import os
os.environ["AIXPLAIN_API_KEY"] = "YOUR-API-KEY"
```

## **🏗️ Architecture**

### **Components**

1. **Perplexity Tool**: Research engine for content analysis  
2. **Google Sheets Tool**: Spreadsheet creation and population  
3. **Claude Code LLM**: Processes and structures research findings

### **Workflow**

```
Company Domain + Topics → Perplexity Research → Find Opportunities
                                ↓
                    Analyze: Trends, Gaps, Competition
                                ↓
                    Structure 8-10+ Opportunities
                                ↓
                    Create Google Sheet → Shareable Report
```

## **🚀 Usage**

### **1\. Get Tool IDs**

```py
from aixplain.factories import ToolFactory, ModelFactory

# Get your tool IDs from studio.aixplain.com after connecting integrations
perplexity_tool = ToolFactory.get("YOUR-PERPLEXITY-TOOL-ID")
google_sheets_tool = ToolFactory.get("YOUR-GOOGLE-SHEETS-TOOL-ID")

# Get LLM
claude_code = ModelFactory.get("claude-code")  # Replace with actual model ID
```

### **2\. Create Research Agent**

```py
from aixplain.factories import AgentFactory

research_agent = AgentFactory.create(
    name="Perplexity Research Agent",
    description="Content strategy research agent for B2B AI companies",
    llm_id=claude_code.id,
    instructions="""
    Research content opportunities using Perplexity and create Google Sheets.
    
    For each opportunity provide:
    - Content Topic/Angle
    - Target Audience Pain Point
    - Search/Discussion Volume (High/Medium/Low)
    - Competition Level (Low/Medium/High)
    - Recommended Format
    - Key Questions
    - SEO Keywords
    - Unique Angle
    - Priority Score (1-10)
    
    Output as table and create Google Sheet.
    """,
    tools=[
        AgentFactory.create_model_tool(
            model=perplexity_tool.id,
            description="Research content trends and data"
        ),
        AgentFactory.create_model_tool(
            model=google_sheets_tool.id,
            description="Create Google Spreadsheets"
        )
    ]
)
```

### **3\. Run Research**

```py
response = research_agent.run(
    query="""
    Research content opportunities for:
    
    Company: aiXplain (aixplain.com)
    Topic Focus: AI agent development, LLM orchestration
    Target Audience: AI engineers, ML developers
    
    Find 10 high-value content opportunities.
    """
)

print(response.data.output)
```

### **4\. Refine Results**

```py
# Get session for follow-up
session_id = response.data.session_id

# Prioritize quick wins
response = research_agent.run(
    query="Which 3 opportunities are quick wins (high volume, low competition)?",
    session_id=session_id
)

print(response.data.output)
```

### **5\. Research Specific Niches**

```py
# Deep dive into specific topic
response = research_agent.run(
    query="Find 5 opportunities specifically around RAG use cases",
    session_id=session_id
)

print(response.data.output)
```

### **6\. Deploy Agent**

```py
research_agent.deploy()
print(f"https://platform.aixplain.com/discover/agent/{research_agent.id}")
```

## **📊 Output Format**

The agent returns opportunities in this table structure:

| Content Topic | Pain Point | Volume | Competition | Format | Key Questions | Keywords | Unique Angle | Priority |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| AI Agent Debugging Best Practices | Developers struggle with debugging multi-agent systems | High | Low | Tutorial | How to trace agent decisions?, What tools exist?, Best logging practices? | ai agent debugging, multi-agent troubleshooting | First comprehensive guide as tools mature | 9 |
| RAG vs Fine-tuning Decision Framework | Teams waste resources on wrong approach | Medium | Medium | Comparison | When to use RAG?, When to fine-tune?, Cost comparison? | rag vs fine-tuning, llm optimization | New benchmarks available Q1 2024 | 8 |

## **⚙️ Configuration**

### **Different Industries**

```py
# SaaS company
response = research_agent.run(
    query="""
    Company: Acme SaaS (acmesaas.com)
    Topic: API integration, webhooks, developer tools
    Audience: Software developers, DevOps engineers
    """
)

# Marketing agency
response = research_agent.run(
    query="""
    Company: Growth Agency (growthagency.com)
    Topic: Growth marketing, conversion optimization
    Audience: Marketing managers, growth hackers
    """
)
```

### **Custom Research Parameters**

```py
research_agent = AgentFactory.create(
    instructions="""
    Your custom parameters:
    - Minimum 15 opportunities (not 8-10)
    - Focus on video content formats
    - Include estimated traffic potential
    - Add competitive analysis URLs
    - Suggest content partnerships
    """
)
```

## **🎯 Use Cases**

### **Product Launch Research**

```py
response = research_agent.run(
    query="Research content for launching a new AI code assistant. Focus on developer pain points and competitive gaps."
)
```

### **Quarterly Content Planning**

```py
response = research_agent.run(
    query="Plan Q2 content calendar for enterprise AI platform. Find 12 opportunities across different funnel stages."
)
```

### **Competitor Gap Analysis**

```py
response = research_agent.run(
    query="Analyze content gaps compared to Anthropic, OpenAI, and Hugging Face in the AI agent space."
)
```

### **Niche Topic Deep Dive**

```py
response = research_agent.run(
    query="Deep research on prompt engineering best practices. Find emerging discussions and unanswered questions."
)
```

## **🔍 Research Sources**

The agent analyzes:

* **Search Trends**: Google search volume and trends  
* **Community Discussions**: Reddit, LinkedIn, Hacker News  
* **Forum Activity**: Stack Overflow, GitHub discussions  
* **Competitor Content**: What's published and what's missing  
* **Industry Reports**: Recent publications and studies

## **💡 Best Practices**

### **Effective Research Queries**

* Specify company domain and positioning clearly  
* Define target audience precisely  
* Include competitor names for gap analysis  
* Mention specific content goals (thought leadership, lead gen, etc.)

### **Maximizing Results**

* Start broad, then refine with follow-ups  
* Request different content formats in separate queries  
* Combine multiple research sessions for comprehensive planning  
* Cross-reference with your own analytics data

### **Using the Output**

* Share Google Sheet with marketing team  
* Prioritize high-score, low-competition opportunities  
* Map opportunities to content calendar  
* Track performance and update priority scores

## **🔍 Troubleshooting**

Common issues and solutions:

* **Generic opportunities**: Provide more specific company/audience details  
* **Missing Google Sheet**: Verify Google integration is connected  
* **Limited results**: Try broader topic focus or different keywords  
* **Duplicate opportunities**: Request "distinct and unique" opportunities

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

* Verify Perplexity integration at studio.aixplain.com  
* Verify Google integration at studio.aixplain.com  
* Check the aiXplain SDK documentation  
* Ensure your API key has proper permissions  
* Confirm tool IDs are correct

