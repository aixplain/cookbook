# 🩺 Patient Report Agent

## Overview

The Patient Report Agent is an AI-powered assistant designed to generate natural language summaries of structured patient records stored in a medical database. Built for healthcare and clinical research applications, it leverages synthetically generated EHR data to automate patient case review.

## Core Features

- 🧬 Human-Readable Reports – Generates clinical summaries based on age, gender, conditions, medications, and encounters.

- 🗂 Structured Record Parsing – Extracts and processes raw EHR data from a Synthea-generated SQLite database.

- 📄 Context-Aware Prompting – Constructs detailed prompts that incorporate the patient's full medical timeline.

- 🚀 Deployable AI Agent – Can be deployed as an API endpoint for use in dashboards or clinician tools.

## How It Works

The agent follows a streamlined flow to transform data into summaries:

- Patient Selection: Choose a synthetic patient ID from the database.

- EHR Retrieval: Extracts data on demographics, conditions, medications, and encounters.

- Prompt Construction: Compiles all relevant patient details into a structured LLM prompt.

- Response Delivery: Returns a complete medical case summary in natural language.

## Installation

```bash
pip install -q aixplain
```

## Setup

Before running the agent, export your aiXplain access key:

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_ACCESS_KEY"
```

## Usage

### Creating the Agent

```python
from aixplain.factories import AgentFactory, ModelFactory


llm_id = "6646261c6eb563165658bbb1"  # Example: GPT-4o

# Create the patient agent
patient_agent = AgentFactory.create(
    name="Patient Report Agent",
    description="Generates patient summaries using structured EHR data from Synthea.",
    instructions="""
    You will be given structured data for a patient including conditions, medications, and encounters.
    Generate a concise medical summary as if preparing a physician's report.
    Highlight key conditions and treatments chronologically.
    """,
    llm_id=llm_id
)
```



### Connect to the database

```python
from sqlite3 import connect

conn = connect("patients.db")
cursor = conn.cursor()
```

### Run agent

```python
result = patient_agent.run(structured_prompt)
print(result['data']['output'])
```

### Deploying the Agent

```python
patient_agent.deploy()
```

## Example Output

```
PATIENT SUMMARY:
Jane Smith, a 72-year-old female, was first diagnosed with chronic kidney disease in 2017. She began taking lisinopril in early 2018 and has had regular nephrology visits every 6 months since. In 2021, she was additionally diagnosed with type 2 diabetes and prescribed metformin...
```

## Data Source
🧪 Synthea – All patient data is synthetic and was generated using the open-source project [Synthea](https://github.com/synthetichealth/synthea), which models realistic but fictional health records.


