# aiXplain Agent-Based Evaluation Suite

This project is a comprehensive framework built around **aiXplain’s LLM agent system**, enabling dynamic, context-aware generation and evaluation across a range of AI tasks.

It demonstrates how to use structured multi-agent workflows for **fact verification**, **text-to-SQL translation**, **code execution**, and **program synthesis**, using both benchmark datasets and agent tool integrations.

---

## Project Modules

### 1. Fact Verification

- **Dataset**: FEVEROUS (via Hugging Face)
- **Function**: Verifies factual claims using search tools and LLM reasoning.
- **Tech**: `AgentFactory`, `TeamAgentFactory`, and web search tools (Tavily).
- **Evaluation**: Classification accuracy (`SUPPORTS`, `REFUTES`, `NOT_ENOUGH_INFO`)

### 2. Text-to-SQL Generation

- **Datasets**: [BIRD](https://bird-bench.github.io/), [SPIDER](https://yale-lily.github.io/spider)
- **Function**: Converts natural language questions into SQL queries using agent prompting and schema-aware indexing.
- **Tech**: `IndexFactory`, custom `PROMPT` templates, execution verification tools
- **Evaluation**: SQL correctness, semantic alignment with schema, query execution

### 3. Python Code Execution & MCQ Evaluation

- **Dataset**: Kaggle-style QA in `code_kaggle_20240712.jsonl`
- **Function**: Generates and executes Python code to solve data-based MCQs.
- **Tech**: Python execution tool via `AgentFactory`, formatted JSON evaluation
- **Evaluation**: Accuracy of selected options vs. ground truth

### 4. Code Contests Program Synthesis

- **Dataset**: [DeepMind CodeContests](https://huggingface.co/datasets/deepmind/code_contests)
- **Function**: Solves programming problems by generating executable Python code
- **Tech**: Subprocess execution, timeout management, multi-test correctness
- **Evaluation**: Test case pass rate, full solution correctness, agent inference time

---

## 📁 Directory Structure

```
.
├── code_contests/             # Competitive programming with test cases
├── code_kaggle/               # Python execution + MCQ evaluation
├── fact_verification/         # Single and multi-agent FEVEROUS pipeline
├── text2sql/                  # Index-based generation for BIRD and SPIDER benchmark
└── README.md                  # This general documentation file
```

---

## Unified Evaluation Metrics

| Module            | Metric(s)                             |
| ----------------- | ------------------------------------- |
| Fact Verification | Accuracy, Precision, Recall, F1       |
| Text-to-SQL       | Query correctness, SQL match          |
| Kaggle MCQ        | Accuracy (% correct answers)          |
| Code Contests     | Test pass rate, sample-level accuracy |

---

## Agent Roles

Agents in this project can act in one or more of the following roles:

- **Reasoner**: Generates structured output based on natural language input
- **Retriever**: Retrieves schema, facts, or documents (using IndexFactory or tools)
- **Executor**: Runs SQL or Python code and returns results
- **Evaluator**: Compares outputs against reference values

---

## Setup Instructions

```bash
pip install aixplain datasets pandas scikit-learn nltk matplotlib seaborn
```

Set your aiXplain API key:

```bash
export TEAM_API_KEY="your_key_here"
```

---
