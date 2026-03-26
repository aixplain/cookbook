# Exa Agent

## Overview

The Exa Agent is an AI-powered research assistant with direct access to [Exa's](https://exa.ai) neural search engine. It combines three capabilities — general web search, code and documentation lookup, and full-text content extraction from any URL — to answer questions with up-to-date, sourced information.

## Core Features

🔍 **Neural Web Search** – Searches the live web for current information, news, and facts using Exa's search engine. Supports `auto`, `neural`, `fast`, and `deep` search types.

💻 **Code Context** – Finds code examples and documentation from GitHub, Stack Overflow, and official framework docs.

📄 **Content Extraction** – Retrieves the full text of any URL, enabling the agent to read, summarise, and analyse specific pages on demand.

⚡ **Flexible Search Depth** – Choose from `instant`, `fast`, `auto`, or `deep` to balance speed and thoroughness.

🚀 **Deployable AI Agent** – Can be published as an API for integration into your applications and workflows.

## How It Works

The agent selects the most appropriate tool based on the request:

1. **Web Search** – for general questions, news, and factual lookups.
2. **Code Context** – for programming questions, API references, and library documentation.
3. **Content Extraction** – when given a specific URL to read, or to follow up on a promising search result.

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
os.environ["EXA_API_KEY"]  = "YOUR_EXA_API_KEY"
```

## Usage

### Creating the Tools and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

SCRIPT_INTEGRATION_ID = "688779d8bfb8e46c273982ca"

def _inject(fn, key_value):
    src = inspect.getsource(fn)
    return src.replace('os.environ.get("EXA_API_KEY")', f'"{key_value}"')

web_search_tool = aix.Tool(
    name="Exa Web Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": _inject(web_search_exa, ExaApiKey), "function_name": "web_search_exa"},
)
web_search_tool.save()

code_context_tool = aix.Tool(
    name="Exa Code Context",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": _inject(get_code_context_exa, ExaApiKey), "function_name": "get_code_context_exa"},
)
code_context_tool.save()

content_extraction_tool = aix.Tool(
    name="Exa Content Extraction",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": _inject(extract_content_exa, ExaApiKey), "function_name": "extract_content_exa"},
)
content_extraction_tool.save()

exa_agent = aix.Agent(
    name="Exa Agent",
    description="Neural web search agent that searches the live web, finds code examples, and extracts full content from any URL using Exa's search API.",
    instructions="...",
    tools=[web_search_tool, code_context_tool, content_extraction_tool],
)
exa_agent.save()
```

### Running the Agent

```python
result = exa_agent.run("What are the latest developments in AI agents?")
print(result.data.output)
```

### Content Extraction

```python
result = exa_agent.run("Read and summarise this page: https://docs.exa.ai/reference/search")
print(result.data.output)
```

### Saving the Agent

```python
exa_agent.save()
```

## Tool Reference

| Tool | Best For | Key Parameters |
|---|---|---|
| `web_search_exa` | News, facts, general research | `query`, `num_results`, `search_type` |
| `get_code_context_exa` | Code examples, API docs | `query`, `num_results` |
| `extract_content_exa` | Full-text reading of specific URLs | `urls` (list), `max_chars` |

## Search Type Reference

| Type | Speed | Best For |
|---|---|---|
| `auto` | ~1s | Balanced (default) |
| `neural` | ~1s | Semantic/conceptual queries |
| `fast` | ~450ms | Quick keyword lookups |
| `deep` | 5–60s | Complex research questions |

## Example Output

```
Based on my search, here are the latest developments in AI agents (2025):

[1] Anthropic Releases Claude 4 with Extended Agentic Capabilities
URL: https://anthropic.com/...
Claude 4 introduces improved multi-step reasoning and tool use, enabling
agents to autonomously complete complex workflows...

[2] OpenAI Launches Operator for Autonomous Web Tasks
URL: https://openai.com/...
Operator can navigate websites, fill forms, and complete tasks end-to-end
without human intervention...

Sources: anthropic.com, openai.com, techcrunch.com
```
