# X API Agent

## Overview

The X API Agent is an AI-powered social media assistant that interacts with X (Twitter) via the official API. It can post tweets, look up user profiles, and search recent posts — all through natural language instructions, using OAuth 1.0a authentication to avoid bot-detection issues.

## Core Features

✍️ **Post Tweets** – Composes and posts tweets on behalf of the authenticated user, with character-count validation and a returned tweet URL.

👤 **User Profile Lookup** – Retrieves any public account's display name, bio, follower count, following count, and total tweet count.

🔍 **Recent Tweet Search** – Searches posts from the last 7 days by keyword, hashtag, or account, with like and retweet counts.

🔐 **OAuth 1.0a Auth** – Uses the official X API v2 with `tweepy`, avoiding cookie-based workarounds that trigger bot detection.

🚀 **Deployable AI Agent** – Can be published as an API for integration into bots, dashboards, or content workflows.

## How It Works

1. **Connect X in Studio** — In [aiXplain Studio](https://studio.aixplain.com/), connect the **X (Twitter)** integration and complete OAuth so the platform can call the API on your behalf.
2. **Attach the integration as a tool** — Load that connected integration as a tool (for example with `Tool.get(...)`) when you build the agent in code or Studio.
3. **Understand the request** — The agent determines whether to post, look up a profile, or search.
4. **Call the right capability** — The X tool routes to posting, profile lookup, or search as needed.
5. **Report back** — Return the tweet URL, profile data, or formatted search results.

## Requirements

- Python environment with `aiXplain` (and `tweepy` if you extend with custom scripts).
- An aiXplain access key from [platform.aixplain.com → Integrations](https://platform.aixplain.com/account/integrations).
- The **X (Twitter) integration connected in Studio** before you use it as an agent tool — see [Connect the X integration in Studio](#connect-the-x-integration-in-studio) below.

## Connect the X integration in Studio

Do this **before** referencing the X integration as a tool on your agent:

1. Open [studio.aixplain.com](https://studio.aixplain.com/).
2. Open **Integrations** and select the **X (Twitter)** integration (or add it if prompted).
3. Sign in and authorize with X. You need a project and app from the [X Developer Portal](https://developer.x.com/en/portal/dashboard) with **Read and Write** permissions, and the credentials from the **Keys and Tokens** tab when the Studio flow asks for them.
4. After the integration shows as connected, open **Tools** (or your team’s tool list in Studio) and copy the tool path or ID for the X tool — you will pass that string to `Tool.get(...)` in the notebook or SDK.

Until the integration is connected in Studio, the X tool will not authenticate successfully for your agent.

## Installation

```python
pip install -q aixplain tweepy
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"
```

X API secrets are managed through the Studio integration connection flow, not necessarily as environment variables in your notebook, when you use the prebuilt X integration tool.

## Usage

### Load the X tool and create the agent

After the X integration is connected in Studio, load it by the identifier shown there (replace the placeholder with yours):

```python
from aixplain import Aixplain
import os

aix = Aixplain(os.environ["TEAM_API_KEY"])

# Tool path/ID from Studio after X is connected — not a random string
x_tool = aix.Tool.get("YOUR_TEAM/YOUR_X_TOOL_SLUG/composio")

x_agent = aix.Agent(
    name="X API Agent",
    description="Social media agent that posts tweets, looks up X user profiles, and searches recent posts using the official X API v2.",
    instructions="...",
    tools=[x_tool],
)
x_agent.save()
```

### Running the Agent

```python
# Search recent tweets
result = x_agent.run("What are people saying about AI agents on X this week?")
print(result.data.output)

# Look up a profile
result = x_agent.run("Look up the X profile for @OpenAI")
print(result.data.output)

# Post a tweet
result = x_agent.run("Post a tweet announcing that I just built an AI agent using aiXplain")
print(result.data.output)
```

### Saving the Agent

```python
x_agent.save()
```

## Tool Reference

The connected X integration typically exposes actions such as:

| Capability | What It Does | Typical parameters |
|---|---|---|
| Post tweet | Posts a tweet to X | Tweet text (≤280 characters) |
| User profile | Looks up a public profile | Username / handle |
| Search recent tweets | Searches tweets from the last 7 days | Query, result limit |

Exact tool names depend on how the integration is configured in Studio.

## X API Credentials (for Studio connection)

When you connect the integration in Studio, you may be asked for values that match the [X Developer Portal](https://developer.x.com/en/portal/dashboard) **Keys and Tokens** tab:

| Variable | Where to Find It |
|---|---|
| API Key | Your App → Keys and Tokens → API Key |
| API Secret | Your App → Keys and Tokens → API Key Secret |
| Access Token | Your App → Keys and Tokens → Access Token |
| Access Token Secret | Your App → Keys and Tokens → Access Token Secret |

> **Note:** Your app must have **Read and Write** permissions. If you only see Read, update the permissions in the Developer Portal and regenerate your access tokens.

## Rate Limits

| Tier | Monthly Post Limit |
|---|---|
| Free | 1,500 posts |
| Basic ($100/month) | Higher limits |

Search and profile lookup are available on the Free tier with standard rate limits.
