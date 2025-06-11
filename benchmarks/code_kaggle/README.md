# Python Code Execution and Evaluation with aiXplain Agents

This project demonstrates how to build a **Python code generation and execution agent** using aiXplain's LLM tooling. The pipeline loads Kaggle-style multiple-choice questions, allows an agent to run code for solving them, and evaluates the generated responses against ground-truth answers.

---

## Features

- Dynamic code generation using aiXplain’s LLM agent
- Runtime Python code execution with integrated tool
- Supports evaluation of JSON-formatted answers
- Computes accuracy of predicted answers against gold labels

---

## Installation

```bash
pip install datasets aixplain
```

---

## Project Files

```
.
├── data/
│   └── code_kaggle_20240712.jsonl      # Dataset of questions and expected answers
├──Code_Kaggle_aiXplain.ipynb                             # Python execution script
├── README.md
```

---

## Workflow Summary

1. **Agent Initialization**

   - Create a Python code execution tool using `AgentFactory.create_python_interpreter_tool()`
   - Construct an agent that understands how to execute Python code, reason, and **print the outcome**
2. **Data Handling**

   - Load questions and contextual data from `code_kaggle_20240712.jsonl`
   - Detect file references in the question and replace them with placeholder URLs
3. **Agent Prompting**

   - A formatted query is sent to the agent including:
     - Data file references
     - User question
     - Required JSON output format
4. **Execution and Evaluation**

   - The agent executes the Python logic and produces structured output
   - Accuracy is calculated by matching predicted answers with ground truth

---

## Answer Format

All predictions are expected to be returned in the following JSON structure:

```json
[
  {
    "answer": "A",
    "explanation": "EXPLANATION"
  }
]
```

---

## Evaluation Metric

Accuracy is computed as:

```
accuracy = correct_predictions / total_questions
```

Answers are case-insensitive and stripped of whitespace before comparison.

---

## Notes

- You must provide your aiXplain API key before running:
  ```bash
  export TEAM_API_KEY="your_key_here"
  ```
- Only samples where `image_expected` is `False` are processed.
- Make sure the paths to data files are valid if running with different datasets.

---
