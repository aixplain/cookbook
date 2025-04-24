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
from datasets import load_dataset
from typing import List, Text


if __name__ == "__main__":
    os.makedirs("data/gsm8k", exist_ok=True)
    os.makedirs("data/gsm8k/results", exist_ok=True)
    os.makedirs("data/gsm8k/results/multi_agent_llama", exist_ok=True)
    from aixplain.enums import Function, Supplier
    
    agents = [
        Agent(
            id="",
            name="Python Code Executor",
            assets=[
                UtilityTool(
                    type="utility", 
                    utility=UtilityToolType.PYTHON_REPL,
                    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`."
                )
            ],
            description="You are an AI with advanced code understanding and planning capabilities. When you encounter a specific problem, your goal is to devise a Python code to solve it.",
            status="onboarded",
            teamId=1,
            llmId="66b2708c6eb5635d1c71f611"
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
        assets=[]
    )
    
    data = load_dataset("openai/gsm8k", "main", split="test")
    correct_answers = 0
    total_questions = len(data)
    import re
        
    
for idx in range(total_questions):
    result_file = f"data/gsm8k/results/multi_agent_llama/{idx}.json"

    
    inp = "Please return only the number, with no symbols or other punctuation." + data[idx]["question"]
    correct_answer = extract_final_number(data[idx]["answer"])  
    print("Correct Answer ", correct_answer)

    try:
        response = TeamAgentService.run(
            TeamAgentExecuteInput(
                agent=community,
                query=inp,
                chat_history=None,
                api_key=os.getenv("TEAM_API_KEY"),
                session_id="1234"
            )
        )
        result = response.output.strip()
        generated_answer = extract_final_number(result)  
        print(generated_answer)

        if generated_answer == correct_answer:
            correct_answers += 1
            accuracy = 1
        else:
            accuracy = 0

        current_accuracy = correct_answers / (idx + 1)

        output_data = {
            "question": data[idx]["question"],
            "generated_answer": generated_answer,
            "correct_answer": correct_answer,
            "accuracy": accuracy,
            "current_accuracy": current_accuracy, 
            "full_response": response.dict()
        }

        with open(result_file, "w") as f:
            json.dump(output_data, f, indent=4)

    except Exception as e:
        print(f"Error processing index {idx}: {str(e)}")
        pass

overall_accuracy = correct_answers / total_questions
print(f"Overall Accuracy: {overall_accuracy * 100:.2f}%")
