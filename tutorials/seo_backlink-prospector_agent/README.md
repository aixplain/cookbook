**Backlink Prospector**

An AI-powered SEO assistant that automatically finds and qualifies backlink opportunities by searching the web and extracting contact information from relevant websites.

## **🎯 Overview**

This agent automates the backlink prospecting process:

* **SERP Search**: Finds relevant websites for your topic/keywords  
* **Website Scraping**: Extracts text from homepages and contact pages  
* **Email Extraction**: Identifies email addresses from scraped content  
* **Prospect Qualification**: Validates and compiles quality backlink opportunities

## **🚀 Features**

* **Automated Prospecting**: Finds 5-10 relevant websites per query  
* **Contact Discovery**: Extracts emails from homepages and contact pages  
* **Contact Form Detection**: Notes when only contact forms are available  
* **Structured Output**: Returns JSON array with prospect metadata  
* **Quality Filtering**: Only includes sites with valid contact methods  
* **Web Deployment**: Deploy as accessible service

## **📋 Prerequisites**

* Python 3.7+  
* aiXplain SDK  
* Valid AIXPLAIN\_API\_KEY  
* Claude Code model access

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

1. **SERP Scraper Tool**: Searches Google for relevant websites  
2. **Website Scraper Tool**: Extracts content from web pages  
3. **Claude Code LLM**: Processes and analyzes scraped data  
4. **Email Extractor**: Identifies email patterns in text

### **Workflow**

```
Topic/Keywords → SERP Search → Find Websites
                                    ↓
              For each website: Scrape Homepage → Extract Emails
                                    ↓
                           No email? → Check Contact Page
                                    ↓
                        Compile Valid Prospects → JSON Output
```

## **🚀 Usage**

### **1\. Get Required Tools and Model**

```py
from aixplain.factories import ToolFactory, ModelFactory

# Get tools
scraper_tool = ToolFactory.get("66f423426eb563fa213a3531")  # Scrape2
serp_tool = ToolFactory.get("6931bdf462eb386b7158def3")  # SERP Scraper

# Get Claude Code model
claude_code = ModelFactory.get("claude-code")  # Replace with actual model ID
```

### **2\. Create Backlink Prospector Agent**

```py
from aixplain.factories import AgentFactory

backlink_agent = AgentFactory.create(
    name="Backlink Prospector",
    description="An SEO assistant that finds and qualifies backlink prospects",
    llm_id=claude_code.id,
    instructions="""
    You are an SEO assistant specialized in finding backlink opportunities.
    
    PROCESS:
    1. Use the SERP scraper tool to find 5-10 relevant websites
    2. For each website:
       a. Scrape homepage for email addresses
       b. If no email, check contact page
       c. Note if only contact form exists
       d. Skip sites with no contact method
    
    3. Output valid prospects as JSON array with:
       - site_url
       - email_list
       - contact_page
       - has_contact_form
       - notes
    """,
    tools=[
        AgentFactory.create_model_tool(
            model=serp_tool.id,
            description="Search Google for websites. Input: search query"
        ),
        AgentFactory.create_model_tool(
            model=scraper_tool.id,
            description="Scrape website content. Input: URL"
        )
    ]
)
```

### **3\. Run Prospect Search**

```py
response = backlink_agent.run(
    query="""
    Find backlink prospects for: "sustainable fashion brands"
    
    Look for fashion blogs, lifestyle websites, or sustainability-focused
    sites interested in sustainable fashion content.
    """
)

print(response.data.output)
```

### **4\. Filter and Refine Results**

```py
# Get session ID for follow-up
session_id = response.data.session_id

# Filter results
response = backlink_agent.run(
    query="Show only prospects with direct email addresses (exclude contact form only)",
    session_id=session_id
)

print(response.data.output)
```

### **5\. Deploy Agent**

```py
backlink_agent.deploy()
print(f"https://platform.aixplain.com/discover/agent/{backlink_agent.id}")
```

## **📊 Output Format**

The agent returns prospects in this structure:

```json
[
  {
    "site_url": "https://example.com",
    "email_list": ["contact@example.com", "info@example.com"],
    "contact_page": "https://example.com/contact",
    "has_contact_form": "yes",
    "notes": "Fashion blog with 50K monthly visitors. Covers sustainable brands regularly."
  },
  {
    "site_url": "https://another-site.com",
    "email_list": ["editor@another-site.com"],
    "contact_page": null,
    "has_contact_form": "no",
    "notes": "Lifestyle magazine. Email found in footer. Good domain authority."
  }
]
```

## **⚙️ Configuration**

### **Custom Search Queries**

```py
# Technology niche
response = backlink_agent.run(
    query="Find backlink prospects for: AI automation tools"
)

# Local SEO
response = backlink_agent.run(
    query="Find backlink prospects for: New York restaurants, target food blogs"
)

# B2B niche
response = backlink_agent.run(
    query="Find backlink prospects for: enterprise SaaS solutions"
)
```

### **Adjusting Agent Behavior**

```py
backlink_agent = AgentFactory.create(
    instructions="""
    Your custom instructions:
    - Focus on high-authority sites (DA > 30)
    - Prioritize sites with clear editorial contact
    - Check for guest post opportunities
    - Note social media presence
    """
)
```

## **🎯 Use Cases**

### **Content Marketing**

```py
response = backlink_agent.run(
    query="Find tech blogs that might link to an article about Python best practices"
)
```

### **Local Business**

```py
response = backlink_agent.run(
    query="Find local directories and community sites in Austin, Texas for a coffee shop"
)
```

### **E-commerce**

```py
response = backlink_agent.run(
    query="Find product review sites and shopping blogs in the home decor niche"
)
```

### **SaaS Product**

```py
response = backlink_agent.run(
    query="Find software comparison sites and SaaS review platforms"
)
```

## **🔍 Troubleshooting**

Common issues and solutions:

* **No prospects found**: Try broader keywords or different search terms  
* **Missing emails**: Agent will note "contact form only" \- these still have outreach value  
* **Irrelevant sites**: Refine your search query with more specific keywords  
* **Scraper errors**: Some sites block scraping \- agent will skip and continue

## **💡 Best Practices**

### **Effective Search Queries**

* Be specific about your niche  
* Include intent keywords ("guest post", "write for us", "contribute")  
* Specify geographic location if relevant  
* Mention content type (blog, magazine, directory)

### **Maximizing Results**

* Run multiple searches with different keyword variations  
* Follow up with filtering queries to refine prospects  
* Cross-reference with domain authority tools  
* Verify contact information before outreach

### **Outreach Tips**

* Personalize emails based on the notes provided  
* Reference specific content on their site  
* Explain mutual value clearly  
* Follow up if using contact forms

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
* Confirm Claude Code model access

