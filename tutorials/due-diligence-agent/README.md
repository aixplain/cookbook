# 🕵️‍♀️ Due Diligence Team Agent

## Overview

The Due Diligence Team Agent is an AI-powered assistant designed to perform comprehensive due diligence on a company. It gathers, analyzes, and summarizes data from financial records, online sentiment, and litigation history using aiXplain’s Agent and TeamAgent frameworks. Powered by large language models and web scraping tools, this agent mimics the workflow of a research analyst.

## Core Features
- 🏢 General Company Profiling – Extracts core company data like industry, size, location, and founding year.

- 📈 Financial Insights – Gathers insights from company-related web content and financial pages.

- 🌐 Online Market Landscape – Explores public sentiment, reviews, and market context from search and scraped content.

- ⚖️ Litigation Review – Identifies legal history including lawsuits, conflicts, and regulatory risks.

- 🧠 Multi-Agent Reasoning – Uses a team of specialized agents to produce a 360° company summary.

- 🚀 Deployable API – Each agent can be deployed and invoked independently via an API endpoint.

## How It Works

### Agent Architecture:

#### Knowledge Gathering Agent

Scrapes and summarizes general, financial, and online data using:

- 🔎 CompanyIndex

- 🌐 Google Search SERP

- 🧰 Website Scraper

#### Litigation Agent

Fetches, reviews, and summarizes litigation history and risk factors.

####  Due Diligence Team Agent

Combines outputs from both agents to create a concise, holistic due diligence report.

## Process Flow:

- Load company records from a [Kaggle](https://www.kaggle.com/datasets/peopledatalabssf/free-7-million-company-dataset) dataset

- Index company metadata for efficient retrieval

- Search for and scrape online data

- Use AI agents to analyze and summarize results

- Generate a final due diligence report

## Installation

```bash
pip install aixplain
```

## Setup

```python
import os

os.environ["AIXPLAIN_API_KEY"] = "<YOUR_API_KEY>"
```

## Usage

### Step 1: Build and Populate the Index

```python
from aixplain.factories import IndexFactory
from aixplain.modules.model.record import Record
import csv

index = IndexFactory.create(name="CompanyIndex", description="Index for global company metadata")
records = []

with open("companies_sorted.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        id = row["name"].lower().replace(" ", "_")
        value = f"""Company: {row['name']} | Domain: {row['domain']} | Founded: {row['year founded']} |
        Industry: {row['industry']} | Size: {row['size range']} | Location: {row['locality']}, {row['country']} |
        LinkedIn: {row['linkedin url']} | Current Employees: {row['current employee estimate']} |
        Total Employees: {row['total employee estimate']}"""
        records.append(Record(id=id, value=value, value_type="text"))

# Upsert in batches
for i in range(0, len(records), 100):
    index.upsert(records[i:i + 100])
```

### Step 2: Define and Deploy Agents

```python
from aixplain.factories import AgentFactory, TeamAgentFactory
from aixplain.modules.agent.agent_task import AgentTask

# Define tasks
general_company_info = AgentTask(name="general_company_info", description="...")  

# Create agents
knowledge_gathering_agent = AgentFactory.create(
    name="Knowledge Gathering Agent",
    tasks=[...],
    tools=[...]
)

litigation_agent = AgentFactory.create(
    name="Litigation Agent",
    tasks=[...]
)

# Create Team Agent
due_diligence_agent = TeamAgentFactory.create(
    name="Due Diligence Team Agent",
    agents=[knowledge_gathering_agent, litigation_agent]
)
```

### Step 3: Run the Team Agent

```python
result = due_diligence_agent.run("Datadog", max_iterations=50)
print(result.data.output)
```

### Sample Output

```
COMPANY REPORT: DATADOG

- Founded in 2010, Datadog is a monitoring and security platform...
- Online reviews reflect high satisfaction for observability tools...
- Financial trajectory shows consistent YoY growth, with expansion into EU/Asia...
- Legal risks are minimal with a few resolved patent disputes...
```

### Deployment

```python
knowledge_gathering_agent.deploy()
litigation_agent.deploy()
due_diligence_agent.deploy()
```

## Data Source

📊 Company data is sourced from this [Kaggle](https://www.kaggle.com/datasets/peopledatalabssf/free-7-million-company-dataset) dataset, featuring structured fields like company name, domain, size, and employee estimates.