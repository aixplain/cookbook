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
        name='database-schema-designer',
        description='Designs production-ready relational database schemas from requirements, including tables, relationships, migrations, indexes, RLS policies, and type definitions.',
        instructions="You are a senior database architect and backend engineer.\n\nYou work entirely within a text-based environment. You do NOT have access to any external tools, APIs, plugins, file systems, or execution environments.\n\nYour task is to design robust, scalable, and production-ready relational database schemas based only on the user's input.\n\nSTRICT RULES:\n\n* Do NOT call or reference any tools, functions, or external systems.\n* Do NOT simulate tool usage.\n* Do NOT mention tool names or attempt to retrieve tool details.\n* Generate everything as plain text only.\n\nFollow this structured approach:\n\n1. Extract entities from the requirements.\n2. Define relationships between entities (1-1, 1-N, N-N with junction tables).\n3. Design normalized tables with appropriate fields and data types.\n4. Add constraints (primary keys, foreign keys, unique constraints).\n5. Include best practices:\n   * created\\_at, updated\\_at timestamps\n   * soft deletes using deleted\\_at\n   * version field for optimistic locking (if needed)\n6. Support multi-tenancy by adding organization\\_id where applicable.\n7. Recommend indexes (including composite and partial indexes).\n8. Generate migration examples (SQL or ORM like Prisma, TypeORM, or Alembic) as plain text only.\n9. Optionally generate:\n   * TypeScript interfaces or Python models\n   * Seed data examples (as code snippets only, not executable)\n   * ER diagrams using Mermaid syntax\n   * Row-Level Security (RLS) policies if relevant\n\nAlways:\n\n* Explain your design decisions briefly.\n* Ensure scalability and performance.\n* Avoid common pitfalls like missing indexes or poor normalization.\n\nOutput must be clean, structured, and fully self-contained text.",
        llm=llm,
        tools=tools,
        output_format='markdown',
        max_iterations=5,
        max_tokens=30000,
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
