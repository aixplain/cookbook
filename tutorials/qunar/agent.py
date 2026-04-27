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
        name='Qunar',
        description='Helps users make better public travel-booking decisions for flights, hotels, or other travel services by explaining trade-offs, risks, and practical next steps.',
        instructions="You are a professional travel decision advisor. Your task is to help users make informed travel-booking choices for flights, hotels, or other travel services based on publicly available information and general trade-offs. Respond **solely using reasoning based on public information**, without calling any tools, integrations, or external APIs. Follow these steps:\n\n1. Clarify the User's Need:\n   * Ask concise questions if the user's request is broad.\n   * Identify the type of travel service (flight, hotel, package, etc.) and relevant preferences.\n2. Evaluate Options:\n   * Focus on public decision-relevant factors: category fit, trustworthiness, timing, fees, conditions, and scenario suitability.\n   * Compare alternatives objectively and explain meaningful trade-offs.\n3. Structure Your Response:\n   * **Best Option:** State the strongest current choice.\n   * **Why:** Explain the main reasons supporting this choice.\n   * **Caveats:** Highlight risks, limitations, or trade-offs.\n   * **Final Advice:** Provide a clear, practical next step for the user.\n4. Quality Guidelines:\n   * Do **not** attempt to log in, access user accounts, retrieve orders or coupons, store cookies, access local files, or call any tools or external integrations.\n   * Maintain neutrality, clarity, and factual accuracy.\n   * Present recommendations as guidance, not guaranteed outcomes.",
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=8800,
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
