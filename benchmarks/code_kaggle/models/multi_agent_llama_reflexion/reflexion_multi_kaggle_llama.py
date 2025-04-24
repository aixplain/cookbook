__author__ = "thiagocastroferreira"

# install the libraries: pip install numpy pandas scipy scikit-learn sympy statsmodels matplotlib seaborn plotly wordcloud
import logging

logging.basicConfig(level=logging.WARN)

import sdk

sdk.load_credentials()
import os

os.environ["TEAM_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""

import json
from agentification.utilities.models import Agent, UtilityTool, UtilityToolType, TeamAgent
from agentification.team_agent import TeamAgentService, TeamAgentExecuteInput

PROMPT = suffix = """Please answer the question(s) based on the provided data file(s) and the user's request, utilizing the available tools.

Data File(s):
<<DATA_FILES>>

User Request:
<<USER_REQUEST>>

Question(s):
<<QUESTION>>

Answer Format:
```json
[
    {{
        "answer": "LETTER OF THE ANSWER",
        "explanation": "EXPLANATION"
    }}
]
```
"""

if __name__ == "__main__":
    os.makedirs("docs/experiments/code_kaggle/models/multi_agent_llama_new/results", exist_ok=True)

    agents = [
        Agent(
            id="",
            name="Python Code Generator and Executor",
            assets=[
                UtilityTool(
                    type="utility",
                    utility=UtilityToolType.PYTHON_REPL,
                    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
                )
            ],
            description="This is a Python Code Generator and Executor. Use it to generate and run Python commands. Input should describe a problem that can be solved programmatically. The output will be a detailed explanation of what the executed code achieved. If you receive code as input, you should either run it or explain why it cannot be executed. Additionally, ensure the tool prints the outcome!",
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
        plannerId="66b2708c6eb5635d1c71f611",
        assets=[],
    )

    with open("data/code_kaggle_20240712.jsonl") as f:
        data = [json.loads(line) for line in f.readlines()]

    for idx, _ in enumerate(data):
        if data[idx]["image_expected"] is False:
            content = data[idx]["messages"][0]["content"]
            data_files = (
                content.split("\nData Files:")[-1]
                .split("\n\n\n")[0]
                .split("Notebook:")[0]
                .strip()
                .replace("../input/", "data/code_kaggle_source/input/")
            )
            user_request = content.split("\nUser Request:")[-1].split("\n\n\n")[0].strip()

            inp = (
                PROMPT.replace("<<DATA_FILES>>", data_files)
                .replace("<<USER_REQUEST>>", user_request)
                .replace("<<QUESTION>>", str(data[idx]["questions"]))
            )
            for i in range(3):
                if os.path.exists(f"docs/experiments/code_kaggle/models/multi_agent_llama_new/results/{idx}_0.json") is False:
                    response = TeamAgentService.run(
                        TeamAgentExecuteInput(
                            agent=community,
                            query=inp,
                            chat_history=None,
                            api_key=os.getenv("TEAM_API_KEY"),
                            session_id="multi_kaggle",
                            executionParams={"maxIterations": 60},
                        )
                    )

                    print(response.output)
                    print(data[idx]["gt_answers"])
                    with open(f"docs/experiments/code_kaggle/models/multi_agent_llama_new/results/{idx}_0.json", "w") as f:
                        f.write(response.model_dump_json(indent=4))

                    if response.output.lower().startswith("sorry") is False:
                        break
