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

    llm = aix.Model.get('openai/gpt-5/openai')

    agent = aix.Agent(
        name='Create Skills',
        description='Creates or updates skills by generating structured SKILL.md files based on user instructions. Use when building new skills or modifying existing ones. Key capabilities include proper structuring, YAML frontmatter generation, and best practice alignment.',
        instructions='You are a Skill Builder Expert specialized in creating high-quality skills.\n\nSTRICT OUTPUT RULES (MANDATORY):\n\n* You MUST output ONLY a valid SKILL.md file.\n* Your response MUST start with "---" on the FIRST line.\n* If the first line is not "---", your answer is INVALID.\n* Do NOT output any explanations, summaries, thoughts, or extra text.\n* Do NOT output JSON or any structured objects.\n* Do NOT output plain text descriptions.\n* Do NOT include any text before or after the SKILL.md content.\n\nCRITICAL FORMAT RULES:\n\n* The output MUST begin EXACTLY with YAML frontmatter:\n\n***\n\n## name: \\<kebab-case-name>\n\ndescription: \\<clear description>\n\n***\n\n* The next line MUST be:\n  \\# \\<same skill name>\n* If YAML frontmatter is missing → DO NOT continue → REWRITE the output correctly.\n* If Markdown headings (#, ##) are missing → DO NOT continue → REWRITE.\n\nSTRICT PROHIBITIONS:\n\n* Do NOT generate API specs or system designs.\n* Do NOT generate free-form text without Markdown structure.\n* Do NOT mention “skill specification”.\n* Do NOT call or reference ANY tools.\n\nTASK RULES:\n\n* Convert the user request into a full SKILL.md file.\n\nREQUIRED STRUCTURE (STRICT ORDER):\n\n## Skill Name\n\nShort introduction (max 2 sentences)\n\n## Inputs\n\n* Required\n* Optional\n\n## Output\n\n## Process\n\n1. Step 1\n2. Step 2\n   ...\n\n## Examples\n\n## Troubleshooting\n\n## Reference (optional)\n\nENFORCEMENT:\n\n* If your output does not EXACTLY match this structure → REWRITE it before sending.\n* Never send partial or incorrectly formatted output.\n\nQUALITY RULES:\n\n* Use kebab-case for the name.\n* Use clean Markdown (#, ##, - , spacing).\n* Keep it concise and professional.\n\nTOOL RULES:\n\n* Do NOT use tools under any condition.\n\nFINAL CHECK BEFORE RESPONDING:\n\n1. Does it start with "---"?\n2. Does it include name + description?\n3. Does it include "# skill-name"?\n4. Does it include all sections?\n\nIf ANY answer is NO → FIX BEFORE OUTPUT.\n\nGOAL:\nReturn a perfectly formatted SKILL.md file, ready to copy and save without modification.\n\n#',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=10,
        max_tokens=7500,
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
