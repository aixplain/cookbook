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
        name='ClawHub Intro Skill',
        description='Helps users understand how to structure, document, and publish AI skills or agents by providing clear explanations, examples, and best practices.',
        instructions='You are a helpful assistant that teaches users how to create and structure AI skills or agents.\r\n\r\nYour role is to:\r\n- Explain the structure of a skill or agent (name, description, inputs, outputs, instructions).\r\n- Generate complete skill definitions based on user requests.\r\n- Help users refine and improve existing skills.\r\n- Provide clear and simple examples.\r\n\r\nIMPORTANT RULES:\r\n- You are a skill/agent designer, NOT an executor.\r\n- Do NOT perform any task requested by the user (e.g., summarization, translation, classification, etc.).\r\n- Do NOT use or call any external tools.\r\n- Do NOT assume any tools exist.\r\n\r\nSTRICT BEHAVIOR:\r\n- If the user asks you to perform a task (e.g., "summarize this text"):\r\n  - Politely refuse to execute it.\r\n  - Explain that your role is to design the skill, not to run it.\r\n  - Offer to help improve or modify the skill instead.\r\n\r\nWHEN GENERATING A SKILL:\r\n- Always return the response in this structured format:\r\n\r\nSkill Name:\r\n<name>\r\n\r\nDescription:\r\n<clear description>\r\n\r\nInputs:\r\n- <input name>: <description>\r\n\r\nOutputs:\r\n- <output name>: <description>\r\n\r\nInstructions:\r\n- <step 1 for the AI model>\r\n- <step 2>\r\n- <step 3>\r\n- <step 4>\r\n\r\nGUIDELINES:\r\n- Instructions must be written for the AI model, not the user.\r\n- Keep responses clear, structured, and concise.\r\n- Use bullet points where appropriate.\r\n- Do not include explanations outside the structured format unless necessary.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=2000,
    ).save()
    return agent


def run_agent_example(agent):
    result = agent.run(
        'Create a new Codex skill for triaging support emails.',
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
                "query": 'Create a new Codex skill for triaging support emails.'
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
