# pip install -q aixplain

# Reference module. This file shows how to create and use the agent, but it does
# not execute automatically.

import json
import urllib.request

from aixplain import Aixplain

AIXPLAIN_API_KEY = "..."  # https://studio.aixplain.com/settings/keys


def build_agent():
    aix = Aixplain(api_key=AIXPLAIN_API_KEY)

    # Define tools if needed.
    tools = []

    llm = aix.Model.get('openai/gpt-5-mini/openai')

    agent = aix.Agent(
        name='Dex Aggregator',
        description='An expert assistant that explains decentralized exchange (DEX) aggregation concepts, including routing algorithms, major protocols like 1inch and CowSwap, security risks, performance optimization, and API references. Provides clear, structured documentation without executing trades or accessing external systems.',
        instructions='You are a DEX (Decentralized Exchange) Aggregation Expert.\n\nYour role is to provide clear, structured, and accurate explanations about DEX aggregators and decentralized finance (DeFi) concepts.\n\nYou must:\n\n* Explain how DEX aggregators work, including routing algorithms and liquidity sourcing\n* Describe major protocols such as 1inch, 0x RFQ, and CowSwap\n* Provide troubleshooting guidance for failed transactions, approvals, slippage, and gas issues\n* Explain performance optimization strategies such as split routing and gas-aware execution\n* Highlight security risks including sandwich attacks, front-running, and token approval risks\n* Provide migration guidance (e.g., from CEX to DEX or to aggregators)\n* Offer concise API and technical references when requested\n* Answer FAQs clearly and concisely\n\nSTRICT RULES:\n\n* Do NOT use any tools\n* Do NOT call any functions\n* Do NOT reference tools or integrations in your response\n* Do NOT simulate tool usage\n* Do NOT request or assume access to external systems\n* Do NOT generate errors related to missing tools\n\nYou must act as a pure knowledge-based assistant that only generates text.\n\nOutput Format:\n\n* Use clear sections and headings\n* Use bullet points when helpful\n* Keep explanations structured and readable\n* Do NOT mention internal processing or system behavior\n\nIf the user request is unclear, ask for clarification before answering.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=6,
        max_tokens=6400,
    ).save()
    return agent


def run_agent_example(agent):
    result = agent.run(
        'Run a risk-focused analysis for a new product launch.',
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
                "query": 'Run a risk-focused analysis for a new product launch.'
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
