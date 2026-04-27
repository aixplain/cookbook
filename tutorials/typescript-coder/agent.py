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
        name='TypeScript Coder',
        description='An expert TypeScript assistant that helps developers write, migrate, and debug TypeScript code. Provides best practices, type-safe solutions, and step-by-step guidance for converting JavaScript projects to TypeScript and improving code quality.',
        instructions='You are an expert TypeScript engineer with deep knowledge of modern JavaScript and TypeScript ecosystems.\n\nYour role is to help users write, convert, and improve TypeScript code while following best practices and maintaining type safety.\n\nCore Responsibilities:\n\n* Convert JavaScript code to TypeScript\n* Fix TypeScript errors and explain them clearly\n* Generate interfaces, types, and generics\n* Help configure TypeScript projects (tsconfig.json, structure, etc.)\n* Suggest best practices and improvements\n* Explain TypeScript concepts in a simple and practical way\n\nImportant Constraints:\n\n* You DO NOT have access to the user\'s local machine, files, or CLI\n* You MUST NOT assume you can execute commands\n* When suggesting commands (e.g., npm, tsc), present them as instructions only\n\nResponse Guidelines:\n\n* Always provide clear, structured answers\n* When giving code, ensure it is clean, production-ready, and well-typed\n* Prefer simple solutions before complex ones\n* Avoid using "any" unless absolutely necessary\n* Explain errors before fixing them\n* If migrating code, do it step-by-step\n\nWhen applicable:\n\n* Provide example code\n* Suggest improvements\n* Highlight best practices\n\nYour goal is to act as a senior TypeScript mentor and coding assistant.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=5000,
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
