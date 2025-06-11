# JiraSense Agent: AI-Powered Jira Insights with Slack Integration

**JiraSense** is an AI agent built with [aiXplain](https://aixplain.com/) to deliver deep insights into project velocity, team bandwidth, bottlenecks, and system health using Jira data. This project demonstrates the orchestration of multi-agent systems, Slack integration, and scalable deployment via FastAPI and Celery.

---

## Core Features

- 🤖 **Multi-agent orchestration** with built-in planning, I/O validation, and memory.
- 🌐 **Model access** from OpenAI, Meta, AWS, Google, and more — over 100 LLMs and 38,000 AI utilities.
- 🔁 **Model switching** between GPT-4o, LLaMA 3.1 70B, and others.
- 🛠 **Tooling** for fine-tuning and benchmarking.
- 🚀 **One-click API deployment** with OpenAI-compatible interface (Python, Swift, cURL).
- 📊 **Observability** with logs and interaction stats.
- 🏢 **Enterprise-ready** security, scalability, and compliance.

---

## Quick Start Guide

### Prerequisites

- [aiXplain Account](https://aixplain.com/) — get your access key from the [Integrations](https://platform.aixplain.com/account/integrations) page.
- Jira API token and email (for custom tools).

### Local Development Setup

```bash
# Clone repo and install dependencies
git clone <repo-url>
cd <repo-folder>
pip install -r requirements.txt
```

##  Building the Agent
Create two utility models:

- **Jira User Search** using the Jira User API

- **Jira Issue Search** using the JQL query API

Then create the JiraSense Agent:

```python
from aixplain.factories import AgentFactory

agent = AgentFactory.create(
    name="JiraSense",
    description="An agent to retrieve data from Jira.",
    instructions=ROLE_DESCRIPTION,  # see role in notebook
    tools=[
        AgentFactory.create_python_interpreter_tool(),
        AgentFactory.create_model_tool(model=name_search_utility.id),
        AgentFactory.create_model_tool(model=issue_search_utility.id),
    ]
)

agent.deploy()
```

### Example Use Cases

```python
agent.run("Give me a complete report about the work of Thiago in the first week of January 2025.")
agent.run("What is the status of the story PROD-1141?")
agent.run("How many bugs (BUG) were resolved in Jan 2025 compared to Dec and Nov 2024?")
```

## Slack Integration

#### `main.py` (FastAPI Entry Point)
Handles incoming Slack events and starts Celery worker.

#### `tasks.py` (Celery Worker)
Processes Slack messages asynchronously using aiXplain agent.

```python
@celery_app.task(name="chat")
def chat(body: dict):
    ...
    response = agent.run(text, session_id=thread_ts)
    slack_client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=response["data"]["output"])
```

###  Deployment

#### Slack Setup

1. Add your public endpoint to Slack Events API.

2. Configure environment variables in `.env`:

```makefile
SLACK_BOT_TOKEN=
AIXPLAIN_API_KEY=
AGENT_ID=
REDIS_URL=
```

#### Run Server + Worker

```bash
uvicorn main:app --reload
# Celery auto-starts from FastAPI on startup
```

### Monitoring and Debugging

```python
from pprint import pprint
pprint(response["data"]["executionStats"])
```

### requirements.txt

```text
fastapi
uvicorn
slack_sdk
requests
python-dotenv
celery
redis
aixplain
```


