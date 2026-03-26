# Exa Web Search Agent

## Overview

The Exa Web Search Agent is an AI-powered research assistant that searches the live web using [Exa's](https://exa.ai) neural search API. It provides three specialised search tools — general web search, code and documentation lookup, and company research — giving it the ability to answer questions with up-to-date information from across the internet.

## Core Features

🔍 **General Web Search** – Searches the live web for current information, news, and facts using Exa's neural search engine.

💻 **Code Context Search** – Finds code examples and documentation from GitHub, Stack Overflow, and official framework docs.

🏢 **Company Research** – Gathers business intelligence, funding news, and recent updates about any organisation.

⚡ **Flexible Search Depth** – Supports `instant`, `fast`, `auto`, and `deep` search modes to balance speed and thoroughness.

🚀 **Deployable AI Agent** – Can be published as an API for seamless integration into your applications.

## How It Works

The agent selects the most appropriate tool based on the request:

1. **Understand the request** – determines whether it calls for general search, code lookup, or company research.
2. **Call the right tool** – routes to web search, code context, or company research accordingly.
3. **Synthesise results** – summarises findings, cites sources, and presents a clear answer.

## Requirements

- Python environment with `aiXplain` and `requests` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).
- An Exa API key from [dashboard.exa.ai](https://dashboard.exa.ai/api-keys).

## Installation

```python
pip install -q aixplain requests
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"
os.environ["EXA_API_KEY"] = "YOUR_EXA_API_KEY"
```

## Usage

### Creating the Tools and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

SCRIPT_INTEGRATION_ID = "688779d8bfb8e46c273982ca"

web_search_tool = aix.Tool(
    name="Exa Web Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": inspect.getsource(web_search_exa), "function_name": "web_search_exa"},
)
web_search_tool.save()

code_context_tool = aix.Tool(
    name="Exa Code Context Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": inspect.getsource(get_code_context_exa), "function_name": "get_code_context_exa"},
)
code_context_tool.save()

company_research_tool = aix.Tool(
    name="Exa Company Research",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": inspect.getsource(company_research_exa), "function_name": "company_research_exa"},
)
company_research_tool.save()

exa_agent = aix.Agent.create(
    name="Exa Web Search Agent",
    description="A research agent that searches the live web using Exa's neural search API.",
    instructions="...",
    tools=[web_search_tool, code_context_tool, company_research_tool],
)
```

### Running the Agent

```python
result = exa_agent.run("What are the latest developments in AI agents?")
print(result.data.output)
```

### Saving the Agent

```python
exa_agent.save()
```

## Example Output

```
Based on my search, here are the latest developments in AI agents in 2025:

[1] OpenAI Launches GPT-5 with Agentic Capabilities
URL: https://openai.com/...
OpenAI released GPT-5 with improved tool use and multi-step reasoning, enabling
agents to autonomously complete complex workflows...

[2] Google DeepMind's Gemini Agents Now Available in Production
URL: https://deepmind.google/...
Google announced production availability of Gemini-powered agents with real-time
web grounding and code execution...

Sources: openai.com, deepmind.google, techcrunch.com
```

## Search Tool Reference

| Tool | Best For | Key Parameters |
|---|---|---|
| `web_search_exa` | News, facts, general research | `query`, `num_results`, `search_type` |
| `get_code_context_exa` | Code examples, API docs | `query`, `num_results` |
| `company_research_exa` | Business intelligence, company news | `company_name`, `num_results` |

## Search Type Reference

| Type | Speed | Best For |
|---|---|---|
| `instant` | ~200ms | Simple factual lookups |
| `fast` | ~450ms | Quick searches |
| `auto` | ~1s | Balanced (default) |
| `deep` | 5–60s | Complex research questions |
