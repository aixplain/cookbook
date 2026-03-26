# Web Search Agent

## Overview

The Web Search Agent is an AI-powered research assistant that searches the live web using [Tavily](https://tavily.com) — an AI-optimised search API built specifically for agents. It supports general research, deep-dive queries, and news-focused searches, returning clean and relevant results with source citations.

## Core Features

🔍 **Live Web Search** – Searches the web in real time for current information, news, and facts using Tavily's AI-optimised search engine.

📰 **News Mode** – Targets recent news articles for breaking news and current events queries.

🔬 **Deep Research Mode** – Runs a more comprehensive search for complex research questions that require broader coverage.

📎 **Source Citations** – Always returns titles and URLs so every answer is traceable.

🔄 **Context-Aware** – Follows up in the same session to refine or expand on a previous answer.

🚀 **No Extra API Key** – Uses the Tavily tool already available on the aiXplain platform — only your aiXplain access key is needed.

## How It Works

1. **Understand the request** — determine whether it needs general research, deep research, or news.
2. **Search** — call the Tavily tool with a well-formed query.
3. **Synthesise** — summarise findings, cite sources, and present a clear answer.

## Requirements

- Python environment with `aiXplain` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).

No separate Tavily API key required.

## Installation

```python
pip install -q aixplain
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"
```

## Usage

### Loading the Tool and Creating the Agent

```python
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

# Load the Tavily Web Search tool from the aiXplain platform
search_tool = aix.Tool.get("tavily/tavily-web-search/tavily")

search_agent = aix.Agent(
    name="Web Search Agent",
    description="Research assistant that searches the live web using Tavily's AI-optimised search API.",
    instructions="...",
    tools=[search_tool],
)
search_agent.save()
```

### Running the Agent

```python
result = search_agent.run("What are the latest developments in AI agents?")
print(result.data.output)
```

### Multi-Turn Research

```python
result = search_agent.run("Give me an overview of retrieval-augmented generation")
print(result.data.output)

followup = search_agent.run(
    "What are the main limitations of RAG systems?",
    session_id=result.data.session_id
)
print(followup.data.output)
```

### Saving the Agent

```python
search_agent.save()
```

## Example Output

```
Based on my search, here are the latest developments in AI agents (2025):

**1. Anthropic releases Claude 4 with extended agentic capabilities**
Claude 4 introduces improved multi-step reasoning and tool use, enabling
agents to autonomously complete complex workflows without human intervention.
Source: https://anthropic.com/...

**2. OpenAI launches Operator for autonomous web tasks**
Operator can navigate websites, fill forms, and complete multi-step tasks
end-to-end, marking a shift toward truly autonomous agents.
Source: https://openai.com/...

Sources: anthropic.com, openai.com, techcrunch.com
```
