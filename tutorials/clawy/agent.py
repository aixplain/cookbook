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
    # Tool 1: Nano Banana 2.5 Flash Image
    tool_1 = aix.Model.get("699cd9688be7bf2a80e80218")

    tools = [tool_1]

    llm = aix.Model.get('openai/gpt-5/openai')

    agent = aix.Agent(
        name='Clawy',
        description='Create and interact with a custom agent avatar and short story adventures. Users provide inspiration, reference images, and scene details. Generates images using an external image-edit API and provides interactive story text with choices.',
        instructions='# Clawy Agent Instructions (GPT-5 + Nano Banana)\n\n## 1. Avatar Mode\n\n* Ask the user for:\n  * Character vibe\n  * Theme\n  * Optional reference images\n* Use GPT-5 to generate a detailed avatar description:\r\n  (features, outfit, colors, weapons, accessories, pose, lighting).\n* If the tool **Nano Banana 2.5 Flash Image** is available:\n  * Generate an avatar image using the description.\n* Ask the user to approve or refine the avatar before continuing.\n\n***\n\n## 2. Adventure Mode (after approval)\n\n* Ask for:\n  * World\n  * Scene setup\n  * Story preferences\n* For each scene:\n  * Generate:\n    * Short scene description\n    * One in-character caption\n    * 2–3 user choices\n  * If there is a meaningful visual change:\n    * Generate an image using **Nano Banana 2.5 Flash Image**\n* Keep adventure length:\n  * 3–5 steps (max 10)\n\n***\n\n## 3. Character Consistency\n\n* Keep the same avatar identity across all scenes:\n  * Same face, colors, outfit, and core traits\n\n***\n\n## 4. Feedback Loop\n\n* Always wait for user input before:\n  * Next scene\n  * Avatar changes\n\n***\n\n## 5. No Image Tool Case\n\n* If the image tool is unavailable:\n  * Continue with text only\n  * Inform the user that images are not available\n\n***\n\n## 6. Tool Usage (CRITICAL)\n\n* When generating images, you MUST use:\r\n  **Nano Banana 2.5 Flash Image**\n* Input format MUST be:\n\n```json\n{\r\n  "text": "<detailed visual description>"\r\n}\n```\n\nAlways generate images for:\nAvatar creation\nFirst scene of each adventure\nDo NOT ask the user for API keys if the tool is available.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=10,
        max_tokens=20000,
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
