# Text-to-SQL with aiXplain Agents

This repository implements a **Text-to-SQL generation pipeline** using aiXplain agents. It supports both the **BIRD** 🐦 and **SPIDER** 🕷️ benchmark datasets for SQL query generation from natural language questions, using large language models and team-based agent collaboration.

---

## Key Features

- Uses aiXplain LLM agents to generate SQL queries from text
- Employs a retrieval-augmented index using the `IndexFactory` for relevant schema and examples
- Executes SQL queries and verifies results
- Evaluates predictions and computes performance metrics
- Stores output in structured JSON and CSV formats

---

## Installation

```bash
pip install aixplain nltk
```

---

## Datasets

- **[BIRD Benchmark](https://bird-bench.github.io/)**
- **[SPIDER Benchmark](https://yale-lily.github.io/spider)**

Make sure to download and place the datasets in the appropriate folder before running the script.

---

## Project Structure

```
.
├── experiments/                         # Output directory for predictions and logs
├── utilities.py                         # Helper functions for processing, agents, and evaluation
├── selected_bird_questions_100.json     # Sampled BIRD queries
├── selected_spider_questions_100.json   # Sampled SPIDER queries
├── results/                             # Directory for saved results
├── bird.ipynb				 # Bird dataset script
├── spider.ipynb		         # Spider dataset script
└── README.md
```

---

## Workflow Overview

1. **Preprocessing**

   - Chunk dataset entries for indexing
   - Build an `Index` with aiXplain’s `IndexFactory`
2. **Question Selection**

   - Select 100 evaluation questions using utility scripts
3. **Agent Roles**

   - `Text2SQL Agent`: Generates SQL queries based on retrieved context
   - `SQL Execution Agent`: Executes the SQL to verify correctness
   - `Team Agent`: Coordinates execution using both agents
4. **Prompt Template**

   - Injects schema, knowledge, examples, and query into a rich prompt for SQL generation
5. **Execution**

   - Runs 10 selected questions through the workflow
   - Evaluates results and saves them to `experiments/` directory

---

## Prompt Format

```
**Question**:
<user question>

**External Knowledge**:
<retrieved schema snippets>

**Examples**:
<retrieved examples>

**SQL**:
SELECT ...
```

---

## Output and Evaluation

- JSON responses are saved in:

  - `experiments/text2sql_bird_single_agent/results/`
  - `experiments/text2sql_spider_single_agent/results/`
- Final evaluation metrics are computed and stored using:

  - `process_and_save_results(...)`
  - `evaluate_predictions(...)`
  - `evaluate_sql_predictions(...)`

---

## Notes

- You must set your aiXplain API key:
  ```bash
  export TEAM_API_KEY="your_key_here"
  ```
- Ensure your datasets and schemas are available locally and paths are updated accordingly.
- Update the `LLM_ID` if using a different aiXplain-hosted LLM model.
