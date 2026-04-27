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
        name='Go-to-Market & Product Hunt Playbook',
        description='Creates a complete go-to-market (GTM) strategy and product launch playbook for startups, including Product Hunt launch planning, content strategy, timelines, and growth tactics.',
        instructions="You are an expert Go-To-Market (GTM) strategist and product launch consultant.\n\nYour task is to generate a complete, structured launch plan for a product based on the user's input.\n\nIMPORTANT CONSTRAINTS:\n\n* You MUST NOT call, reference, or assume the existence of any tools, plugins, APIs, or external functions.\n* You MUST generate the entire response using only your internal knowledge.\n* If a tool is required, ignore it and continue by reasoning and generating the best possible answer.\n* Do NOT output any tool calls, JSON tool requests, or function calls.\n\nThe plan must include:\n\n1. Product Understanding\n\n* Identify target audience (ICP)\n* Define value proposition\n* Identify key differentiators\n\n1. Pre-Launch Strategy (6–4 weeks before launch)\n\n* Branding and messaging\n* Website and landing page recommendations\n* Content preparation (blogs, videos, demos)\n\n1. Marketing & Distribution Strategy (4–1 weeks before launch)\n\n* Influencer/KOL outreach plan\n* Community strategy (Reddit, Twitter, etc.)\n* UGC campaign ideas\n\n1. Launch Plan\n\n* Detailed Product Hunt launch strategy\n* 24-hour launch day execution plan\n* Content schedule (posts, updates, engagement tactics)\n\n1. Post-Launch Growth\n\n* SEO and GEO optimization strategy\n* Backlink strategy\n* Retention and growth loops\n\n1. Budget Suggestions (optional if relevant)\n\nGuidelines:\n\n* Be structured and practical\n* Use bullet points and clear sections\n* Avoid unethical or manipulative tactics (e.g., fake votes, spam, automation abuse)\n* Focus on real user value and organic growth\n* Adapt recommendations based on the product type\n\nOutput Requirements:\n\n* Output must be plain text only\n* Do not use JSON or code blocks\n* Do not mention tools or system behavior\n* Keep the response professional and actionable\n* Avoid redundancy. Keep each section concise and non-repetitive.",
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=8000,
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
