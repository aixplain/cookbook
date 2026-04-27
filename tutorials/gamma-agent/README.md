# Gamma Agent

## Overview

The Gamma Agent is an AI-powered content creation assistant that generates polished presentations, documents, and social media carousels using the [Gamma.app](https://gamma.app) API. Describe what you need and the agent produces a fully designed, shareable Gamma link in under a minute.

## Core Features

📊 **Presentations** – Generates slide decks in 16:9, 4:3, or fluid format. Ideal for pitch decks, talks, and reports.

📄 **Documents** – Generates long-form structured documents. Ideal for proposals, PRDs, and briefs.

📱 **Social Posts** – Generates social media carousels in 1:1, 4:5, or 9:16 format for LinkedIn, Instagram, and Stories.

🎨 **Customisable** – Control slide count, tone, target audience, aspect ratio, and image sourcing (AI-generated, web, or none).

🔗 **Shareable Links** – Returns a ready-to-share Gamma URL for every piece of content.

🚀 **Deployable AI Agent** – Can be published as an API for integration into workflows and content pipelines.

## How It Works

1. **Understand the request** — identify content type, topic, tone, audience, and format.
2. **Call the right tool** — route to presentation, document, or social post generator.
3. **Poll for completion** — waits for Gamma's async generation to finish (typically 20–60 seconds).
4. **Return the link** — delivers the shareable Gamma URL.

## Requirements

- Python environment with `aiXplain` and `requests` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).
- A Gamma API key from [gamma.app](https://gamma.app) → Settings → API.

## Installation

```python
pip install -q aixplain requests
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"]  = "YOUR_AIXPLAIN_API_KEY"
os.environ["GAMMA_API_KEY"] = "YOUR_GAMMA_API_KEY"
```

## Usage

### Creating the Tools and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

helper_src = inspect.getsource(_gamma_generate)

def _inject(fn):
    src = helper_src + "\n\n" + inspect.getsource(fn)
    return src.replace('os.environ.get("GAMMA_API_KEY")', f'"{GammaApiKey}"')

presentation_tool = aix.Tool(
    name="Create Gamma Presentation",
    integration="688779d8bfb8e46c273982ca",
    config={"code": _inject(create_presentation), "function_name": "create_presentation"},
)
presentation_tool.save()

gamma_agent = aix.Agent(
    name="Gamma Agent",
    description="Generates presentations, documents, and social carousels using Gamma.app.",
    instructions="...",
    tools=[presentation_tool, document_tool, social_tool],
)
gamma_agent.save()
```

### Running the Agent

```python
result = gamma_agent.run("Create a 10-slide pitch deck for an AI-powered recipe app targeting investors")
print(result.data.output)
```

### Saving the Agent

```python
gamma_agent.save()
```

## Tool Reference

| Tool | Content Type | Key Parameters |
|---|---|---|
| `create_presentation` | Slide deck | `topic`, `card_count`, `tone`, `audience`, `aspect_ratio` |
| `create_document` | Long-form doc | `topic`, `card_count`, `tone`, `audience` |
| `create_social_post` | Social carousel | `topic`, `card_count`, `tone`, `aspect_ratio` |

## Parameter Reference

### Tone
| Value | Best For |
|---|---|
| `professional` | Business presentations, reports |
| `casual` | Social content, internal comms |
| `educational` | Tutorials, explainers |
| `persuasive` | Pitch decks, sales content |

### Aspect Ratio
| Value | Use Case |
|---|---|
| `16x9` | Standard presentations (default) |
| `4x3` | Classic slide format |
| `fluid` | Flexible/scrollable docs |
| `1x1` | Instagram/LinkedIn square |
| `4x5` | Portrait social |
| `9x16` | Stories / Reels |

> **Generation time:** Gamma typically takes 20–60 seconds per request. The tools poll automatically and return the URL when complete.
