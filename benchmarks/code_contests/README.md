# Python Code Contests with aiXplain LLM Agent

This project evaluates the capability of a large language model (LLM) to solve competitive programming problems from the [DeepMind CodeContests dataset](https://huggingface.co/datasets/deepmind/code_contests) using aiXplain agents. It performs automated code generation, execution, and test-based evaluation.

---

## Features

- Uses aiXplain LLM agent to generate Python code solutions from problem descriptions
- Executes code with timeouts using subprocess and multiprocessing
- Compares results against public test cases from the dataset
- Tracks test results, accuracy, success rate, and performance metrics
- Saves all evaluations to JSON files for further analysis

---

## Installation

```bash
pip install datasets aixplain
```

---

## Directory Structure

```
.
├── code_contests_results/           		  # Output folder for JSON results
│   ├── 1_results.json               		  # Result of sample 1
│   ├── 2_results.json               		  # Result of sample 2
│   └── code_contests_results.jsonl  		  # Aggregated logs in JSON Lines format
├── config.yaml                      		  # Optional config file for sample control
├── code_contests_aixplain.ipynb                  # Main script for execution
├── README.md
```

---

## Execution Workflow

1. **Agent Setup**:

   - Initializes a single aiXplain agent using `AgentFactory`.
2. **Dataset Load**:

   - Loads the `test` split of the DeepMind CodeContests dataset via Hugging Face.
3. **Prompt Construction**:

   - Constructs a code-generation prompt using the problem description and time limit.
4. **Code Execution**:

   - Extracts and runs the generated Python code using `subprocess` within a safe execution sandbox.
   - Timeout and correctness checks are enforced.
5. **Evaluation**:

   - Each code is tested on public test cases provided in the dataset.
   - Success rate and overall accuracy are computed per sample.
6. **Logging**:

   - All results are saved as `.json` files and appended to a `.jsonl` log file for audit and analysis.

---

## Evaluation Criteria

- **Success Rate** = Passed Tests / Total Tests
- **Correctness** = True if all tests passed
- **Accuracy** = Mean success rate across all evaluated samples

---

## Notes

- Set your aiXplain API key before execution:

```bash
export TEAM_API_KEY="your_key_here"
```

- You can control the number of samples processed by changing `max_samples` in `main()`.

---

## Sample Output (per problem)

```json
{
  "sample_index": 1,
  "name": "sum_of_digits",
  "description": "Write a function that returns the sum of digits...",
  "generated_code": "...",
  "agent_response": "...",
  "is_correct": true,
  "success_rate": 1.0,
  "test_results": [
    {"test_id": 1, "result": "passed"},
    {"test_id": 2, "result": "passed"}
  ]
}
```

---
