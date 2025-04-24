__author__ = "thiagocastroferreira"

# install the libraries: pip install numpy pandas scipy scikit-learn sympy statsmodels matplotlib seaborn plotly wordcloud
import logging

logging.basicConfig(level=logging.WARN)

import sdk

sdk.load_credentials()
import os

os.environ["TEAM_API_KEY"] = "7315cd4fb7e85cf14361525fd7c5f994b3e45b7333c96835c02c613162118705"
os.environ["SERPAPI_API_KEY"] = "43d5bfc4ff7ff84dfb5a540c1f51734ac1bb196894e83cac0208b4e97936e462"

import json
from agentification.utilities.models import Agent, UtilityTool, UtilityToolType, TeamAgent
from agentification.team_agent import TeamAgentService, TeamAgentExecuteInput

PROMPT = """Given a target problem (labeled #PROBLEM#), your goal is to deduce the correct answer (#ANSWER#).

Please adhere to the following format:
First, express your #THOUGHTS# to reflect your understanding of the problem. Keep your #THOUGHTS# concise, not exceeding 5 sentences. Then, provide your #ANSWER# to the problem.

For example, your output can be:

#THOUGHTS#:
Let's think step by step ...
#ANSWER#:
12

Here is the problem.

#PROBLEM#:
<<PROBLEM>>

Now, please provide the #THOUGHTS# and #ANSWER# sections. Do not include additional explanations or reasoning processes under #ANSWER# section.

#THOUGHTS#: Let's think step by step:
#ANSWER#:"""

if __name__ == "__main__":
    os.makedirs("docs/experiments/math_kaggle/models/orchestrator_agent_llama/results", exist_ok=True)

    agents = [
        Agent(
            id="",
            name="Powerful Reasoning AI",
            assets=[
                UtilityTool(
                    type="utility",
                    utility=UtilityToolType.PYTHON_REPL,
                    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
                )
            ],
            description="You are an AI with advanced comprehension capabilities, akin to that of humans. This enables you to understand complex instructions, discern the user's intent, and apply logical reasoning across a variety of scenarios effectively.",
            status="onboarded",
            teamId=1,
            llmId="66b2708c6eb5635d1c71f611",
        )
    ]

    community = TeamAgent(
        id="66e81e65384523f1ba02ca6c",
        agents=agents,
        links=[],
        name="Test Agent 23423",
        status="onboarded",
        teamId=1,
        llmId="66b2708c6eb5635d1c71f611",
        supervisorId="66b2708c6eb5635d1c71f611",
        assets=[],
    )

    with open("data/math_standard_20240712.jsonl") as f:
        data = [json.loads(line) for line in f.readlines()]

    for idx, row in enumerate(data):
        if os.path.exists(f"docs/experiments/math_kaggle/models/orchestrator_agent_llama/results/{idx}.json") is False:
            for i in range(3):
                raw_problem = row["raw_problem"]
                inp = PROMPT.replace("<<PROBLEM>>", raw_problem)
                response = TeamAgentService.run(
                    TeamAgentExecuteInput(
                        agent=community,
                        query=inp,
                        chat_history=None,
                        api_key=os.getenv("TEAM_API_KEY"),
                        session_id="1234",
                        executionParams={"maxIterations": 60},
                    )
                )

                print(response.output)
                with open(f"docs/experiments/math_kaggle/models/orchestrator_agent_llama/results/{idx}_{i}.json", "w") as f:
                    f.write(response.model_dump_json(indent=4))
