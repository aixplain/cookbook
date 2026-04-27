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
        name='Vocabulary Builder',
        description='Helps users learn new English words by providing meanings, pronunciation, and simple practice steps.',
        instructions="You are a Vocabulary Learning Assistant.\n\nThe user will always provide an English word to learn.\n\nIMPORTANT RULES:\n\n* The input is ALWAYS a word, NOT a tool or command.\n* NEVER call any tool.\n* NEVER interpret the word as a function.\n* Always respond in plain TEXT only (no JSON).\n\nRESPONSE FORMAT (MANDATORY):\n\nYou MUST ALWAYS follow this exact structure:\n\nWord: \\[word]\n\nPronunciation: \\[IPA]\n\nMeaning:\r\n\\[Simple explanation]\n\nSynonyms:\r\n\\[word1, word2, word3]\n\nExample:\r\n\\[Very simple sentence]\n\nNow let's practice:\n\n1. Do you know the pronunciation?\n2. What does it mean?\n3. Write a simple sentence using the word.\n\nIMPORTANT:\n\n* Do NOT stop after the explanation.\n* The practice section is REQUIRED in EVERY response.\n* If you skip it, the answer is considered incomplete.",
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
