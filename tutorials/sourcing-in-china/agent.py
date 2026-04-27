# pip install -q aixplain

# Reference module. This file shows how to create and use the agent, but it does
# not execute automatically.

import json
import urllib.request

from aixplain import Aixplain

AIXPLAIN_API_KEY = "..."  # https://studio.aixplain.com/settings/keys


def build_agent():
    aix = Aixplain(api_key=AIXPLAIN_API_KEY)

    # Define tools used by this agent.
    tools = []

    # Public tool 1: Tavily Web Search
    tool_1 = aix.Model.get("6931bdf462eb386b7158def3")
    tools.append(tool_1)


    llm = aix.Model.get('openai/gpt-5-mini/openai')

    agent = aix.Agent(
        name='Sourcing in China',
        description='Helps users search for products and suppliers from China, analyze product details, and compare sourcing options based on price, MOQ, and supplier credibility.',
        instructions='You are a China sourcing assistant.\n\nYour job is to help users find products and suppliers from China using web search.\n\nWorkflow:\n\n1. Use Tavily search to find products based on user query.\n2. Extract product information:\n   * Product name\n   * Price (if available)\n   * MOQ (if available)\n   * Supplier name\n   * Product link\n3. Identify suppliers from results:\n   * Classify them as Manufacturer or Trading Company if possible\n4. Extract product details when links are available\n5. Compare results and recommend best options\n\nRules:\n\n* Always use Tavily search tool\n* Use 1–2 searches maximum\n* Prefer specific queries like:\r\n  "LED strip light supplier China MOQ price"\n* Output must be structured:\n  * Products list\n  * Suppliers list\n  * Final recommendation',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=7,
        max_tokens=4000,
    ).save()
    return agent


def run_agent_example(agent):
    result = agent.run(
        'Summarize what this agent does and the best way to use it.',
        progress_format="logs",
        progress_verbosity=2,
    )
    print(result.data.output)
    print(result.data)  # Debug helper
    return result


def rest_example(agent):
    request = urllib.request.Request(
        f"https://platform-api.aixplain.com/sdk/agents/{agent.id}/run",
        data=json.dumps(
            {
                "query": 'Summarize what this agent does and the best way to use it.'
            }
        ).encode("utf-8"),
        headers={
            "x-api-key": AIXPLAIN_API_KEY,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))
