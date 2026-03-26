# GifGrep Agent

## Overview

The GifGrep Agent is an AI-powered GIF search assistant that finds the perfect GIF for any moment. It searches both **Giphy** and **Tenor** — the two largest GIF libraries — and returns direct links, previews, and metadata so you can quickly pick and share the right one.

## Core Features

🔍 **Dual-Platform Search** – Queries both Giphy and Tenor in one conversation so you always find the best match.

🎯 **Natural Language Queries** – Describe what you need ("reaction GIF for when code finally works") and the agent translates it into the right search terms.

🔗 **Direct Links** – Returns direct GIF URLs for embedding, page URLs for sharing, plus dimensions and file sizes.

⚡ **Context-Aware** – Follows up in the same session so you can refine ("something more dramatic", "show me Tenor results too").

🚀 **Deployable AI Agent** – Can be published as an API for integration into Slack bots, web apps, or any workflow.

## How It Works

1. **Understand the request** – extracts the mood, action, or concept from the user's message.
2. **Search both platforms** – runs the query on Giphy and/or Tenor.
3. **Recommend** – surfaces the top matches with direct links and descriptions.

## Requirements

- Python environment with `aiXplain` and `requests` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).
- A Giphy API key from the [Giphy Developer Portal](https://developers.giphy.com/dashboard/).
- A Tenor API key from the [Google Cloud Console](https://console.cloud.google.com/) (Tenor API v2).

## Installation

```python
pip install -q aixplain requests
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"]  = "YOUR_AIXPLAIN_API_KEY"
os.environ["GIPHY_API_KEY"] = "YOUR_GIPHY_API_KEY"
os.environ["TENOR_API_KEY"] = "YOUR_TENOR_API_KEY"
```

## Usage

### Creating the Tools and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

SCRIPT_INTEGRATION_ID = "688779d8bfb8e46c273982ca"

def _inject(fn, replacements):
    src = inspect.getsource(fn)
    for placeholder, value in replacements.items():
        src = src.replace(placeholder, f'"{value}"')
    return src

giphy_tool = aix.Tool(
    name="Giphy Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={
        "code": _inject(search_giphy, {'os.environ.get("GIPHY_API_KEY")': os.environ["GIPHY_API_KEY"]}),
        "function_name": "search_giphy",
    },
)
giphy_tool.save()

tenor_tool = aix.Tool(
    name="Tenor Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={
        "code": _inject(search_tenor, {'os.environ.get("TENOR_API_KEY")': os.environ["TENOR_API_KEY"]}),
        "function_name": "search_tenor",
    },
)
tenor_tool.save()

gifgrep_agent = aix.Agent(
    name="GifGrep Agent",
    description="Searches Giphy and Tenor to find the perfect GIF for any moment.",
    instructions="...",
    tools=[giphy_tool, tenor_tool],
)
gifgrep_agent.save()
```

### Running the Agent

```python
result = gifgrep_agent.run("Find me a GIF of a happy dog")
print(result.data.output)
```

### Saving the Agent

```python
gifgrep_agent.save()
```

## Example Output

```
Here are the top Giphy results for "happy dog":

[1] Happy Dog GIF
    Page:     https://giphy.com/gifs/dog-happy-...
    GIF URL:  https://media.giphy.com/media/.../giphy.gif
    Preview:  https://media.giphy.com/media/.../giphy-downsized-medium.gif
    Size:     480x270px, 1842KB

[2] Excited Puppy GIF
    Page:     https://giphy.com/gifs/puppy-excited-...
    GIF URL:  https://media.giphy.com/media/.../giphy.gif
    ...
```

## API Key Setup

| Key | Where to get it |
|---|---|
| `GIPHY_API_KEY` | [developers.giphy.com/dashboard](https://developers.giphy.com/dashboard/) — create an app, copy the API key |
| `TENOR_API_KEY` | [console.cloud.google.com](https://console.cloud.google.com/) — enable the Tenor API, create credentials |
