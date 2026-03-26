# Fitness Chef Agent

## Overview

The Fitness Chef Agent is an AI-powered assistant designed to generate innovative, fitness-focused recipes based on a user's desired protein intake and available ingredients. It leverages web scraping and a vast recipe index to optimize meal planning for health-conscious individuals.

## Core Features

🍽 Personalized Recipe Generation – Generates unique recipes based on available ingredients and protein goals.

📊 Protein Content Analysis – Scrapes a trusted nutritional database to estimate the protein content of ingredients.

🔍 Recipe Inspiration – Searches an extensive recipe index to find similar meals as a reference.

🏋️ Fitness-Oriented Planning – Ensures that meals align with specified protein intake goals.

🚀 Deployable AI Agent – Can be published as an API for seamless integration into applications.

## How It Works

The agent follows a structured workflow to generate meal plans:

1. User Input: Receives a protein goal and a list of available ingredients.

2. Protein Analysis: Scrapes an online nutritional guide for protein content.

3. Ingredient Selection: Adjusts ingredient proportions to meet the protein target.

4. Recipe Search: Fetches relevant recipes from a large indexed database.

5. Recipe Generation: Creates a unique recipe tailored to the user's needs.

6. Output Format: Provides a breakdown of protein content, a step-by-step custom recipe, and two similar recipes for reference.

## Requirements

- Python environment with `aiXplain` installed.

- An aiXplain access key to authenticate API calls.

## Installation

```python
pip install -q aixplain
```

## Setup

Before running the agent, set up your aiXplain access key:

```python
import os
AccessKey = "YOUR_ACCESS_KEY"
os.environ["TEAM_API_KEY"] = AccessKey
```

## Usage

### Creating the Agent

```python
from aixplain.factories import AgentFactory, ModelFactory

# Define tools
scraper_tool = ModelFactory.get("66f423426eb563fa213a3531")
search_tool = ModelFactory.get("67bbfd9022816c001dca44ed")

# Create agent
protein_agent = AgentFactory.create(
    name="Fitness Chef Agent",
    description="An AI-powered nutritionist that creates recipes based on protein goals and available ingredients.",
    instructions="""
    - Analyze ingredients' protein content using a web scraping tool.
    - Adjust quantities to match the protein goal.
    - Search for similar recipes in the database.
    - Generate a custom recipe with step-by-step instructions.
    """,
    tools=[scraper_tool, search_tool],
    llm_id="6646261c6eb563165658bbb1"  # GPT-4o
)
```

### Running the Agent

```python
result = protein_agent.run("Protein goal: 135g. Available ingredients: ground pork, bok choi, egg, wonton wrappers, shrimp, noodles, rice, yam.")
print(result['data']['output'])
```

### Deploying the Agent

```python
protein_agent.deploy()
```

## Example Output

```
PROTEIN BREAKDOWN:
1. Ground pork (150g) - 45g protein
2. Eggs (2 units) - 12g protein
3. Shrimp (100g) - 20g protein
...
Total: 135g protein

UNIQUE RECIPE:
Step 1: Prepare ingredients...
Step 2: Cook ground pork...
...
Estimated protein: 135g

SIMILAR RECIPES:
RECIPE 1:
  Name: Shrimp & Pork Dumplings
  Ingredients: Ground pork, wonton wrappers, shrimp, ...
  Instructions:
    1. Mix ingredients...
    2. Steam dumplings...
```

