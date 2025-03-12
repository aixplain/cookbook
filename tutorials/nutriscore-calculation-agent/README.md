# NutriScore Agent

## Overview

The NutriScore Agent is an AI-powered tool that calculates the Nutri-Score for food items, beverages, and cooking fats based on their nutritional content. It integrates with the aiXplain platform and leverages prebuilt utility models for accurate scoring.

## Core Features

🏷 Nutri-Score Calculation – Computes a health-based food rating (A-E) using macronutrient data.

📊 Category-Specific Scoring – Applies distinct models for general food, beverages, and cooking fats.

🔍 OCR Support – Extracts nutritional data from images using an integrated OCR model.

🤖 AI-Powered Reasoning – Guides users by requesting missing nutritional details when needed.

🚀 API Deployable – Can be published and integrated into various applications.

## How It Works

1. User Input:

- The user provides macronutrient details or an image of a nutrition label.

- The agent asks clarifying questions if necessary.

2. Food Classification:

- The agent classifies the item as a beverage, cooking fat, or general food.

3. Nutri-Score Calculation:

- Calls the relevant model to compute the Nutri-Score.

4. Result Formatting:

- Outputs the Nutri-Score in a structured format (e.g., "Nutri-Score of provided food is B").

## Requirements

- Python environment with aiXplain and nutriscore installed.

- An aiXplain access key for API authentication.


## Installation

```python
pip install -q aixplain nutriscore
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
from nutriscore.nutriscore import get_nutriscore
from nutriscore.nutriscore_beverage import get_nutriscore_beverage_score
from nutriscore.nutriscore_cooking_fats import get_nutriscore_cooking_fat_score

nutriscore_default_utility = ModelFactory.get("67bede734547417162861ac6")
nutriscore_beverage_utility = ModelFactory.get("67bede75058286b62912e280")
nutriscore_cooking_fat_utility = ModelFactory.get("67bede77058286b62912e281")

agent = AgentFactory.create(
    name="NutriScore Agent",
    description="Agent that calculates NutriScore for foods, beverages, and cooking fats.",
    instructions="""
    - Classify food as a general item, beverage, or cooking fat.
    - Request any missing nutritional information from the user.
    - Use the appropriate Nutri-Score model to compute the score.
    - If an image is provided, use OCR to extract macronutrient data.
    - Output the Nutri-Score in the format: 'Nutri-Score of provided food is <score>'.
    """,
    tools=[
        AgentFactory.create_model_tool(model=nutriscore_default_utility.id, description="General Nutri-Score Calculator"),
        AgentFactory.create_model_tool(model=nutriscore_beverage_utility.id, description="Nutri-Score Calculator for Beverages"),
        AgentFactory.create_model_tool(model=nutriscore_cooking_fat_utility.id, description="Nutri-Score Calculator for Cooking Fats"),
        AgentFactory.create_model_tool(model="646f5ce8cfb5f83af659e392", description="OCR tool for extracting nutritional information from images"),
    ],
)
```

### Running the Agent

```python
query = """Calculate Nutri-Score of food with these macros:
energy_kcal=250,
sugars_g=12,
sat_fat_g=3,
salt_mg=500,
fruit_veg_percent=50,
fibre_g=3,
protein_g=4"""
agent_response = agent.run(query)
print(agent_response['data']['output'])
```

## Example Output

```
Nutri-Score of provided food is C.
```

## Running the Agent with an Image

```python
query = """Calculate Nutri-Score from an image: https://images.openfoodfacts.org/images/products/509/983/929/3832/nutrition_en.5.full.jpg"""
agent_response = agent.run(query)
print(agent_response['data']['output'])
```

## Session-Based Queries

```python
session_id = agent_response["data"]["session_id"]
print(f"Session id: {session_id}")
```

