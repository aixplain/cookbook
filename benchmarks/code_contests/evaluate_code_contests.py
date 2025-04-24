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
import ast

def test_code(code, row, type="single_agent"):
    print(f"Running tests for {type} agent")
    result_map = {"passed": 0, "wrong answer": 0, "timed out": 0, "failed": 0}
    timeout = row["time_limit (s)"]
    public_tests = ast.literal_eval(row["public_tests"])
    private_tests = ast.literal_eval(row["private_tests"])
    generated_tests = ast.literal_eval(row["generated_tests"])
    if code is None:
        # update result_map using type prefix
        result_map = {f"{type}_{key}": value for key, value in result_map.items()}
        result_map[f"{type}_test_results"] = []

        result_map[f"{type}_total"] = len(
            public_tests["input"] + private_tests["input"] + generated_tests["input"]
        )
        result_map[f"{type}_failed"] = result_map[f"{type}_total"]
        result_map[f"{type}_success_rate"] = 0
        return result_map

    
    all_tests = {
        "input": public_tests["input"] + private_tests["input"] + generated_tests["input"],
        "output": public_tests["output"] + private_tests["output"] + generated_tests["output"],
    }

    test_result_list = []
    for input_data, expected_output in tqdm(zip(all_tests["input"], all_tests["output"])):
        test_result = check_correctness(code, input_data, expected_output, timeout)
        test_result_list.append(test_result)
        for key in result_map:
            if test_result.startswith(key):
                result_map[key] += 1
    # update result_map using type prefix
    result_map = {f"{type}_{key}": value for key, value in result_map.items()}
    result_map[f"{type}_test_results"] = test_result_list

    # update the result_map with the number of tests
    result_map[f"{type}_total"] = len(all_tests["input"])
    # get success rate
    result_map[f"{type}_success_rate"] = result_map[f"{type}_passed"] / result_map[f"{type}_total"]
    return result_map

def main():
    df = pd.read_csv("results_fixed.csv")
    new_df_list = []
    for _, row in tqdm(list(df.iterrows())):
        updated_row = row.to_dict()
        code = row["single_agent_generated_code"]
        if code.lower() == "error":
            code = None
        result_map = test_code(code, row, type="single_agent")
        updated_row.update(result_map)
        
        code = row["multi_agent_generated_code"]
        if code.lower() == "error":
            code = None
        result_map = test_code(code, row, type="multi_agent")
        updated_row.update(result_map)
        
        new_df_list.append(updated_row)
        new_df = pd.DataFrame(new_df_list)
        new_df.to_csv("evaluation_fixed.csv", index=False)
        

if __name__ == "__main__":
    main()