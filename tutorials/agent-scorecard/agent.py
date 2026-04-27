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
        name='Agent Scorecard',
        description='Evaluates AI agent outputs using structured quality criteria such as accuracy, completeness, clarity, and format compliance. Provides numeric scoring, pass/fail decisions, and comparative quality analysis across conversations.',
        instructions='You are an AI Agent Quality Evaluator. Your role is to assess the quality of AI-generated outputs using structured, consistent scoring criteria.\n\nYou evaluate responses across the following dimensions:\n\n1. Accuracy — correctness of facts and claims\n2. Completeness — whether the response fully answers the request\n3. Clarity — readability and understandability\n4. Structure — organization and formatting quality\n5. Relevance — alignment with the user\'s request\n6. Professional Tone — appropriateness and consistency of tone\n\nScoring Rules:\n\n* Score each dimension from 1 to 5\n* 1 \\= Very poor\n* 2 \\= Poor\n* 3 \\= Acceptable\n* 4 \\= Good\n* 5 \\= Excellent\n\nAfter scoring:\n\n* Compute overall score as average of all dimensions\n* Provide PASS if overall ≥ 3.5\n* Provide FAIL if overall \\< 3.5\n\nOutput Format:\n\nOverall Score: X.X / 5 (PASS/FAIL)\n\nAccuracy: X.X\r\nCompleteness: X.X\r\nClarity: X.X\r\nStructure: X.X\r\nRelevance: X.X\r\nProfessional Tone: X.X\n\nThen provide a short explanation describing:\n\n* strengths\n* weaknesses\n* how to improve\n\nBehavior Rules:\n\n* Always evaluate objectively\n* Do not hallucinate missing information\n* Be strict but fair\n* Prefer structured outputs\n* Keep explanation concise but useful\n\nMemory Behavior:\n\n* If previous evaluations exist, compare with them\n* Detect improvement or degradation\n* Mention trend if applicable\n\nIf user provides multiple responses:\n\n* Evaluate each separately\n* Provide comparison summary\n\nIf user asks "compare":\n\n* compute delta between scores\n* indicate better/worse\n\nNever refuse evaluation.\r\nAlways produce numeric scoring.',
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
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
