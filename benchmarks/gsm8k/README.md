# GSM8K Math Problem Solver using aiXplain Agents

This project evaluates a single-agent AI system capable of solving grade-school math problems from the [GSM8K dataset](https://huggingface.co/datasets/openai/gsm8k) using a combination of code execution and LLM-based reasoning. The agent is built using the [aiXplain](https://aixplain.com) platform and is equipped with both a Python interpreter and a language model tool.

## Project Structure

The system follows a simple yet powerful agent architecture:

- **LLM Tool**: Used to validate or revise outputs from the code tool.
- **Python Tool**: Used to compute intermediate results via dynamic code execution.
- **Prompt Template**: Guides the agent to prioritize tool-based reasoning over internal knowledge.
- **Evaluation Loop**: Runs through a specified number of GSM8K test samples, records predictions, and tracks cost, time, and accuracy metrics.

## Directory Structure

```
.
├── gsm8k.ipynb                  # Main execution script
├── results/                	 # Output directory for individual sample logs
│   ├── sample_1.json
│   ├── sample_2.json
│   └── ...
├── README.md                	 # Project documentation
```

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/gsm8k-agent-evaluator.git
   cd gsm8k-agent-evaluator
   ```
2. **Install Dependencies**Requires Python 3.8+, `datasets`, and `aixplain` SDK.

   ```bash
   pip install datasets aixplain
   ```
3. **Run the Script**

   ```bash
   python main.py
   ```

## API Configuration

Set the following environment variables:

```python
os.environ["TEAM_API_KEY"] = "your_team_api_key_here"
```

## Evaluation Details

- **Dataset**: `openai/gsm8k` (test split)
- **Sample Size**: 1319
- **Tools Used**:
  - Python interpreter tool
  - LLM validation tool
- **Metrics Tracked**:
  - Accuracy
  - Average inference time
  - Cumulative and per-sample cost
  - Intermediate reasoning steps

## Agent Instructions

The agent is given explicit instructions to:

- Solve problems using **Python code first**
- Avoid using internal LLM knowledge for final answers
- Output only the final result, not the reasoning or code

## Sample Output (JSON)

Each prediction is logged in a JSON file:

```json
{
  "index": 5,
  "question": "Jane has 5 apples...",
  "ground_truth": "3",
  "prediction": 3,
  "is_correct": true,
  "intermediate_steps": ["Tool: Python", "...", "Tool: LLM", "..."],
  "output": "3 apples",
  "time": 1.23,
  "cost": 0.002,
  "accuracy_so_far": 85.7,
  "avg_cost": 0.0019,
  "avg_time": 1.12
}
```

## Final Result

Upon completion, the script prints:

```
Final Accuracy on 1319 GSM8K samples: {result:.2f}%
```

## Notes

- The agent is sensitive to prompt design. Changes to the `PROMPT_TEMPLATE` may significantly affect accuracy.
- Outputs are saved individually to aid in post-hoc analysis and error breakdowns.
- The model and agent are powered by aiXplain's `ModelFactory` and `AgentFactory` abstractions.
