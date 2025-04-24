from dotenv import load_dotenv

load_dotenv()
import aixplain.utils.config as aixplain_config

from agentification.utilities.models import TeamAgentExecuteInput, AgentExecuteInput, AgentResponse
from agentification.team_agent import TeamAgentService
from agentification.agent import AgentService
from datasets import load_dataset
from check_correctness import check_correctness
import pandas as pd
from tqdm import tqdm
import re
import time
RUN_ONLY_ERRORS = False
RUN_SINGLE_MULTI_PROBLEM = False


def get_code_from_output(response):
    try:
        code = re.findall(r"```python*(.*?)\s```", response.output, re.DOTALL)[0]
        return code
    except Exception as e:
        # iterate over intermediate steps to check for the code, check from last to first
        for step in response.intermediate_steps[::-1]:
            try:
                code = re.findall(r"```python*(.*?)\s```", step.output, re.DOTALL)[0]
                return code
            except Exception as e:
                continue
    return None


def get_result(code, response, type="single_agent"):
    # convert intermediate steps to a list of dict
    intermediate_steps = [elem.__dict__ for elem in response.intermediate_steps]
    result_map = {f"{type}_response": response.output, f"{type}_intermediate_steps": intermediate_steps}
    code = code if code is not None else "Error"
    result_map[f"{type}_generated_code"] = code
    return result_map


def main():
    if RUN_ONLY_ERRORS:
        df = pd.read_csv("evaluation.csv")
    elif RUN_SINGLE_MULTI_PROBLEM:
        df = pd.read_csv("evaluation_pass_2.csv")
    else:
        dataset = load_dataset("deepmind/code_contests", split="test")
        df_list = []
        for row in dataset:
            name = row["name"]
            example = row["description"]
            time_limit = row["time_limit"]
            cf_id = row["cf_contest_id"]
            cf_index = row["cf_index"]
            cf_url = f"https://codeforces.com/contest/{cf_id}/problem/{cf_index}"
            public_tests = row["public_tests"]
            private_tests = row["private_tests"]
            generated_tests = row["generated_tests"]
            difficulty = row["difficulty"]
            df_list.append(
                {
                    "name": name,
                    "example": example,
                    "time_limit (s)": time_limit["seconds"],
                    "cf_url": cf_url,
                    "public_tests": public_tests,
                    "private_tests": private_tests,
                    "generated_tests": generated_tests,
                    "difficulty": difficulty,
                }
            )
        df = pd.DataFrame(df_list)
        
    coder_description = "You are an AI with advanced code understanding and planning capabilities. When you encounter a specific problem, your goal is to produce a valid python code that correctly solves the problem. You MUST test the code with the provided test cases to make sure the code is working properly. The code MUST output correct answers under any valid inputs, not only just for the examples inputs given in the problem description, CREATE other examples and test them to make sure the code DOES NOT timeout when receiving large numbers. You can assume that ALWAYS input and output will follow the restrictions in the problem statement. Make sure to fully address the problem goals following the rules and constraints. The code should be robust and general."
    input_data = {
        "agent": {
            "id": "66758985e39f1c11f9102700",
            "name": "python coder",
            "description": coder_description,
            "status": "onboarded",
            "teamId": 646,
            "llmId": "6646261c6eb563165658bbb1",
            "assets": [],
            "tools": [],
            "createdAt": "2024-06-21T14:09:09.903Z",
            "updatedAt": "2024-06-21T14:09:09.903Z",
        },
        "query": "",
        "chat_history": [],
        "api_key": aixplain_config.TEAM_API_KEY,
    }
    single_agent_input = AgentExecuteInput(**input_data)

    input_data = {
        "agent": {
            "id": "66758985e39f1c11f9102700",
            "name": "Test Community",
            "status": "onboarded",
            "teamId": 646,
            "llmId": "6646261c6eb563165658bbb1",
            "supervisorId": "6646261c6eb563165658bbb1",
            "plannerId": "6646261c6eb563165658bbb1",
            "links": [],
            "assets": [],
            "agents": [
                {
                    "id": "66758985e39f1c11f91027cf",
                    "name": "python coder",
                    "description": coder_description,
                    "status": "onboarded",
                    "teamId": 646,
                    "llmId": "6646261c6eb563165658bbb1",
                    "assets": [],
                    "createdAt": "2024-06-21T14:09:09.903Z",
                    "updatedAt": "2024-06-21T14:09:09.903Z",
                    "number": 1,
                    "type": "AGENT",
                    "label": "OUTPUT",
                }
            ],
            "createdAt": "2024-06-21T14:09:09.903Z",
            "updatedAt": "2024-06-21T14:09:09.903Z",
        },
        "query": "",
        "chat_history": [],
        "api_key": aixplain_config.TEAM_API_KEY,
    }
    community_execute_input = TeamAgentExecuteInput(**input_data)
    k = 1
    new_df_list = []
    if RUN_ONLY_ERRORS:
        df = df[(df["single_agent_generated_code"] == "Error") | (df["multi_agent_generated_code"] == "Error")]
    elif RUN_SINGLE_MULTI_PROBLEM:
        df = df[(df["single_agent_success_rate"] == 1.0) & (df["multi_agent_success_rate"] != 1.0)]
    for _, row in tqdm(list(df.iterrows())):
        for _ in range(k):
            example = row["example"]
            time_limit = row["time_limit (s)"]
            query = (
                f"Generate Python code to solve the following problem. The code MUST be in the Final Answer with format ```python ```. You MUST test the code in the Final Answer and make sure it is working for the example test cases. For this problem timeout is {time_limit} seconds:\n"
                + example
            )
            chat_history = []
            updated_row = row.to_dict()
            start = time.time()
            # single agent run
            try:
                single_agent_input.query = query
                single_agent_input.session_id = "123"
                response = AgentService.run(single_agent_input, chat_history)
                code = get_code_from_output(response)
            except Exception as e:
                print("ERROR!")
                code = None
            elapsed = time.time() - start
            result_map = get_result(code, response, type="single_agent")
            result_map["single_agent_elapsed_time"] = elapsed
            updated_row.update(result_map)
            # TODO test the code
            # result_map = test_code(code, row, type="single_agent")
            # updated_row.update(result_map)

            # multi agent run
            start = time.time()
            try:
                community_execute_input.query = query
                community_execute_input.session_id = "123"
                response = TeamAgentService.run(community_execute_input, chat_history)
                code = get_code_from_output(response)
            except Exception as e:
                print("ERROR!")
                code = None

            elapsed = time.time() - start
            result_map = get_result(code, response, type="multi_agent")
            result_map["multi_agent_elapsed_time"] = elapsed
            updated_row.update(result_map)
            # TODO test the code
            # result_map = test_code(code, row, type="multi_agent")
            # row.update(result_map)

            new_df_list.append(updated_row)
            new_df = pd.DataFrame(new_df_list)
            new_df.to_csv("results_gpt4o.csv", index=False)


if __name__ == "__main__":
    main()