# GA4 Analytics Agent

## Overview

The GA4 Analytics Agent is an AI-powered analytics assistant that queries Google Analytics 4, Google Search Console, and real-time visitor data through natural language. Ask for a traffic overview, top pages, search queries, or live visitor counts — and the agent pulls the numbers directly from your property.

## Core Features

📊 **Traffic Reports** – Queries GA4 for sessions, users, page views, bounce rate, and session duration across any date range.

📄 **Content Performance** – Identifies top pages by views and engagement rate.

🔀 **Traffic Source Breakdown** – Shows sessions by source and medium (organic, direct, referral, social, etc.).

🟢 **Real-Time Visitors** – Fetches live active user counts and the pages they are currently viewing.

🔍 **Search Console Insights** – Returns top search queries and pages with clicks, impressions, CTR, and average position from Google Search Console.

📅 **Period Comparisons** – Compares two date ranges side-by-side to identify traffic trends.

🚀 **Deployable AI Agent** – Can be published as an API for integration into dashboards, Slack bots, or reporting workflows.

## How It Works

1. **Understand the request** — determine whether it needs historical GA4 data, real-time data, or Search Console data.
2. **Call the right tool** — route to GA4 Report, GA4 Realtime, or Search Console Report.
3. **Summarise** — present the numbers clearly, highlight anomalies, and suggest follow-up questions.

## Requirements

- Python environment with `aiXplain`, `google-analytics-data`, `google-api-python-client`, and `google-auth` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).
- A Google Cloud service account with the following APIs enabled:
  - Analytics Data API
  - Search Console API
- The service account added as a **Viewer** in your GA4 property and Google Search Console.

## Installation

```python
pip install -q aixplain google-analytics-data google-api-python-client google-auth
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"]            = "YOUR_AIXPLAIN_API_KEY"
os.environ["GA4_PROPERTY_ID"]         = "YOUR_GA4_PROPERTY_ID"       # numeric, e.g. "123456789"
os.environ["GA4_CLIENT_EMAIL"]        = "YOUR_SERVICE_ACCOUNT_EMAIL"
os.environ["GA4_PRIVATE_KEY"]         = "YOUR_SERVICE_ACCOUNT_PRIVATE_KEY"
os.environ["SEARCH_CONSOLE_SITE_URL"] = "https://example.com/"
```

## Google Cloud Setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and create or select a project.
2. Enable the **Analytics Data API** and **Search Console API**.
3. Create a **service account** under IAM & Admin → Service Accounts.
4. Generate a JSON key — copy the `client_email` and `private_key` fields.
5. In **GA4** → Admin → Property Access Management → Add users, add the service account email as **Viewer**.
6. In **Google Search Console** → Settings → Users and permissions, add the service account email.
7. Your GA4 Property ID is the numeric ID shown in GA4 → Admin → Property Settings.

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
        src = src.replace(placeholder, repr(value))
    return src

cred_map = {
    'os.environ.get("GA4_PROPERTY_ID")':        Ga4PropertyId,
    'os.environ.get("GA4_CLIENT_EMAIL")':        Ga4ClientEmail,
    'os.environ.get("GA4_PRIVATE_KEY")':         Ga4PrivateKey,
    'os.environ.get("SEARCH_CONSOLE_SITE_URL")': SearchConsoleSiteUrl,
}

ga4_report_tool = aix.Tool(
    name="GA4 Report",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": _inject(get_ga4_report, cred_map), "function_name": "get_ga4_report"},
)
ga4_report_tool.save()

ga4_agent = aix.Agent(
    name="GA4 Analytics Agent",
    description="Analytics assistant that queries GA4 and Search Console for traffic and SEO insights.",
    instructions="...",
    tools=[ga4_report_tool, ga4_realtime_tool, search_console_tool],
)
ga4_agent.save()
```

### Running the Agent

```python
result = ga4_agent.run("Give me a traffic overview for the last 30 days")
print(result.data.output)
```

### Multi-Turn Comparisons

```python
result = ga4_agent.run("How much traffic did we get last month?")
followup = ga4_agent.run(
    "How does that compare to the month before?",
    session_id=result.data.session_id
)
print(followup.data.output)
```

### Saving the Agent

```python
ga4_agent.save()
```

## Tool Reference

| Tool | What It Does | Key Parameters |
|---|---|---|
| `get_ga4_report` | Historical GA4 traffic data | `report_type`, `date_range` |
| `get_ga4_realtime` | Live active users right now | _(none)_ |
| `get_search_console_report` | Search Console queries & pages | `report_type`, `date_range` |

## Report Types

### GA4 Report (`report_type`)

| Type | What It Returns |
|---|---|
| `overview` | Sessions, users, page views, bounce rate, avg session duration |
| `content` | Top pages by views with engagement rate |
| `traffic` | Sessions by source and medium |
| `behavior` | Sessions and engagement by device and country |

### Search Console Report (`report_type`)

| Type | What It Returns |
|---|---|
| `queries` | Top search queries with clicks, impressions, CTR, position |
| `pages` | Top pages in Google search with clicks, impressions, CTR, position |

## Date Range Formats

| Format | Example | Description |
|---|---|---|
| Shorthand | `"7d"`, `"30d"`, `"90d"` | Last N days |
| ISO range | `"2025-01-01:2025-01-31"` | Explicit start and end date |
