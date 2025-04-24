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
from agentification.utilities.models import Agent, UtilityTool, UtilityToolType
from agentification.agent import AgentService, AgentExecuteInput


if __name__ == "__main__":
    os.makedirs("docs/experiments/code_kaggle/models/single_agent_gpt4/results", exist_ok=True)

    agent = Agent(
        id="",
        name="Python Code Executor",
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
        llmId="654a42a36eb5634a236f5eb1",
    )

    with open("data/code_kaggle_20240712.jsonl") as f:
        data = [json.loads(line) for line in f.readlines()]

    for idx, _ in enumerate(data):
        if data[idx]["image_expected"] is False:
            option = data[idx]["messages"][0]["content"].split("\nData Files:")[-1].split("\n\n\n")
            option = "Data Files:\n" + option[0].strip().replace("../input/", "data/code_kaggle_source/input/")

            suffix = f"""Answer the questions based on the data file, notebook and user request using the available tools.
Question:
{data[idx]['questions']}

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
            inp = option + "\n\n" + suffix
            if os.path.exists(f"docs/experiments/code_kaggle/models/single_agent_gpt4/results/{idx}.json") is False:
                response = AgentService.run(
                    AgentExecuteInput(
                        agent=agent, query=inp, chat_history=[], api_key=os.getenv("TEAM_API_KEY"), session_id="1234"
                    ),
                    chat_history=[],
                )

                print(response.output)
                with open(f"docs/experiments/code_kaggle/models/single_agent_gpt4/results/{idx}.json", "w") as f:
                    f.write(response.model_dump_json(indent=4))
