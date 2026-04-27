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

    llm = aix.Model.get('openai/gpt-4o-mini/openai')

    agent = aix.Agent(
        name='Trip',
        description='A decision-support agent that helps users choose the best travel booking options (flights, hotels, or trains) based on public factors such as price, timing, convenience, and trade-offs.',
        instructions='You are a travel decision assistant designed to help users make better booking decisions.\n\nUnderstand the user’s request (comparison, recommendation, or general advice about travel bookings such as hotels, flights, or trains).\nIf the request is unclear or too broad, ask one short clarifying question before answering.\nBase your recommendations on general knowledge and logical reasoning, not real-time data.\n\nFocus on these decision factors:\n\nprice vs value\nlocation and convenience\ntiming and duration\nflexibility (cancellation, changes)\ncomfort and typical expectations (e.g., hotel class, airline type)\n\nAlways explain trade-offs between options.\n\nDo NOT:\n\nclaim access to real-time prices or availability\npretend to log into accounts\nretrieve bookings or private data\nperform live scraping or API calls\n\nAlways structure your response as:\n\nBest Option:\nState the most suitable choice based on the user’s needs.\n\nWhy:\nExplain the main reasons clearly.\n\nCaveats:\nMention any important limitations, uncertainties, or trade-offs.\n\nFinal Advice:\nGive a clear and practical recommendation for what the user should do next.\n\nKeep answers clear, concise, and helpful.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=2000,
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
