# Market Analysis Agent

## Overview

The Market Analysis Agent is an AI-powered research assistant that delivers structured, enterprise-grade market intelligence. Given a company name, product, or industry, it produces detailed reports covering market trends, competitor analysis, user behaviour, and strategic opportunities — with deep expertise in the Chinese market.

## Core Features

📊 **Structured Reports** – Produces reports with Executive Summary, Market Trends, Competitor Analysis, User Behaviour, and Strategic Opportunities sections.

🏆 **Competitor Intelligence** – Identifies top players, maps market share, and highlights differentiation strategies.

👤 **User Behaviour Analysis** – Examines user segments, pain points, adoption channels, and engagement patterns.

🚀 **Strategic Opportunities** – Surfaces unmet needs, underserved segments, and product gaps for market entry or expansion.

🔄 **Context-Aware** – Follows up in the same session so you can drill deeper into any section ("go deeper on competitors", "what's the entry strategy?").

🌏 **China Market Focus** – Deep knowledge of Chinese platforms (WeChat, Douyin, Alipay, JD, Meituan), regulations, and consumer behaviour patterns.

## How It Works

1. **Parse** – The Market Analysis Planner tool converts a free-form request into a structured JSON brief with analysis dimensions, key questions, and suggested metrics.
2. **Research** – The agent uses the brief as an outline and fills each section with specific data, company names, and growth figures.
3. **Report** – Delivers a complete markdown report ready to share or paste into a document.

## Requirements

- Python environment with `aiXplain` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).

No external API keys required.

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

### Creating the Tool and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

planner_tool = aix.Tool(
    name="Market Analysis Planner",
    integration="688779d8bfb8e46c273982ca",
    config={
        "code": inspect.getsource(plan_market_analysis),
        "function_name": "plan_market_analysis",
    },
)
planner_tool.save()

market_agent = aix.Agent(
    name="Market Analysis Agent",
    description="Delivers structured market intelligence reports covering trends, competitors, user behaviour, and strategic opportunities.",
    instructions="...",
    tools=[planner_tool],
)
market_agent.save()
```

### Running the Agent

```python
result = market_agent.run("Give me a market analysis of the short-video industry in China")
print(result.data.output)
```

### Multi-Turn Research

```python
result = market_agent.run("Quick overview of China's fintech landscape")
print(result.data.output)

# Follow up in the same session
followup = market_agent.run(
    "Go deeper on strategic opportunities for a foreign fintech entrant",
    session_id=result.data.session_id
)
print(followup.data.output)
```

### Saving the Agent

```python
market_agent.save()
```

## Analysis Dimensions

| Dimension | What It Covers |
|---|---|
| Market Trends | Growth drivers, regulatory changes, technology disruption, market size & CAGR |
| Competitor Analysis | Top players, market share, competitive advantages, differentiation strategies |
| User Behaviour | User segments, pain points, adoption channels, engagement & retention metrics |
| Strategic Opportunities | Unmet needs, underserved segments, product gaps, partnership potential |

## Analysis Depth

| Depth | Description |
|---|---|
| `quick` | High-level overview, 2-3 bullet points per section |
| `standard` | Full report with supporting data points (default) |
| `deep` | Comprehensive report with sub-sections, tables, and extended metrics |

## Example Output

```
# Market Analysis: Short-Video Industry in China

## Executive Summary
- China's short-video market reached ¥300B+ in ad revenue in 2024, growing 18% YoY
- Douyin (抖音) and Kuaishou (快手) together hold ~85% market share
- The sector is shifting from pure entertainment to commerce — live-streaming e-commerce now accounts for 40%+ of GMV on both platforms
- Regulatory pressure on minors' screen time and content moderation is reshaping growth strategies
- International expansion (TikTok) has become a key growth lever as the domestic market matures

## Market Trends
### Growth Drivers
- Short-video e-commerce integration: Douyin Shop GMV exceeded ¥2T in 2024...
...
```
