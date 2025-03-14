# Online Shopping Agent

## Overview

The Online Shopping Agent is an AI-powered assistant designed to help individuals find the best deals on products they want to buy online. It uses a google search model, web scrapping and a large language model to find the best deals and present them to the user in a structured format.
## Core Features

User can search for products by name or category.

The agent will search the web for the best deals and present them to the user in a structured format.

Easy to use and deploy.

🚀 Deployable AI Agent – Can be published as an API for seamless integration into applications.

## How It Works 

The agent follows a structured workflow to find the best deals:

1. User Input: Receives a product name or category.

2. Product Search: Searches the web for the best deals.

3. Deal Analysis: Analyzes the deals and presents them to the user in a structured format.

4. Output Format: Provides a structured format of the deals.

## Requirements

- Python environment with `aiXplain` installed.

- An aiXplain access key to authenticate API calls.

## Installation

```python
pip install aixplain --upgrade
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
def main(query: str):
  import requests, json
  PROMPT = """
    Given the parsed page of an online product. Try to get the following information about the product, name, description, price, rate.
    Return your response in a json format like the following:
    {
      "name": <name>,
      "url": <url>,
      "description": <description>,
      "price": <price>,
      "rate": <rate>
    }
    Only return the json output in a format to be parsed directly using json.loads.
    The url is supposed to be the first line in the inout given to you.
    If the input parsed page doesn't seem to be of an online product, return {}
    PARSED PAGE:
  """
  search_model_url = "https://models.aixplain.com/api/v2/execute/65c51c556eb563350f6e1bb1"
  scrapping_model_url = "https://models.aixplain.com/api/v2/execute/66f423426eb563fa213a3531"
  llm_model_url = "https://models.aixplain.com/api/v2/execute/677c16166eb563bb611623c1"
  api_key = "YOUR_API_KEY"
  headers = {"x-api-key": api_key, "Content-Type": "application/json"}

  payload = {
      "text": f"I want to buy {query} online",
      "numResults": 100
  }
  r = requests.post(search_model_url, headers=headers, json=payload)
  resp = r.json()
  final_output = []
  for item in resp['details']:
    url = item['document']
    scrapping_payload = {
        "text": url
    }
    try:
      r = requests.post(scrapping_model_url, headers=headers, json=scrapping_payload)
      resp = r.json()
      llm_payload = {
          "text" : PROMPT + "\n" + url + "\n" + resp['data']
      }
      r = requests.post(llm_model_url, headers=headers, json=llm_payload)
      resp = r.json()
      try:
        json_output = json.loads(resp['data'].replace("```", ""))
        if json_output:
          final_output.append(json_output)
      except:
        continue

    except:
      continue




  return final_output

#main("iphone 16")

from aixplain.factories import ModelFactory
utility_search_model = ModelFactory.create_utility_model(
    name="Google Search",
    code=main,
    description="Search Google for the query"
    )

  

# Create agent
from aixplain.factories import AgentFactory
online_shopping_assistant = AgentFactory.create(
    name="Online Shopping Assistant4",
    tools=[utility_search_model],

    llm_id="677c16166eb563bb611623c1",
    description="An Agent for to help with online shopping.",
    instructions="""
      Given a user query, help the user decide where to buy it with the best price and rate.
      Start your response with "Here are the results I got:"
      Give the user as much information as possible that will help decide what to buy like the cheapest and the top rated product.
      Present your results in the following format:
          '''
          Product Name: <name>
          Description: <description>
          Price: <price>
          Rate: <rate>
          Url: <url>
          -------------------------------------
          Product Name: <name>
          Description: <description>
          Price: <price>
          Rate: <rate>
          Url: <url>
          -------------------------------------
          Product Name: <name>
          Description: <description>
          Price: <price>
          Rate: <rate>
          Url: <url>
          -------------------------------------
          Product Name: <name>
          Description: <description>
          Price: <price>
          Rate: <rate>
          Url: <url>
          '''
      You should give the user as much information as possible that will help decide what to buy.
    """
)
online_shopping_assistant.id
```

### Running the Agent

```python
result = online_shopping_assistant.run("whiteboard")
print(result['data']['output'])
```

### Deploying the Agent

```python
online_shopping_assistant.deploy()
```

## Example Output

```
"Here are the results I got: 
          Product Name: Quartet Whiteboard
          Description: A high-quality whiteboard for home or office use
          Price: $15
          Rate: 4.5
          Url: https://www.amazon.com/Quartet-Whiteboard-6x4-Feet-Aluminum-Frame
          -------------------------------------
          Product Name: Viz-Pro Whiteboard
          Description: A durable and easy-to-clean whiteboard for heavy use
          Price: $25
          Rate: 4.8
          Url: https://www.staples.com/Viz-Pro-Whiteboard-6x4-Feet-Aluminum-Frame
          -------------------------------------
          Product Name: Lockways Whiteboard
          Description: A budget-friendly whiteboard for basic use
          Price: $10
          Rate: 4.2
          Url: https://www.walmart.com/Lockways-Whiteboard-6x4-Feet-Plastic-Frame
          -------------------------------------
          Product Name: Ghent Whiteboard
          Description: A high-end whiteboard with a sleek and modern design
          Price: $50
          Rate: 4.9
          Url: https://www.officedepot.com/Ghent-Whiteboard-6x4-Feet-Aluminum-Frame"
```

