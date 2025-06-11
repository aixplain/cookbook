AI Fact Verification Agent
==========================

This repository implements a fact verification system using aiXplain's LLM agents and the FEVEROUS dataset.
It supports both single-agent and multi-agent approaches to verifying claims based on evidence retrieved from the web.

Features
--------

- Uses aiXplain Agent APIs to build fact verification agents
- Integrates web search via Tavily tool for retrieving evidence
- Processes claims from the FEVEROUS dataset
- Computes classification metrics: accuracy, precision, recall, F1
- Saves predictions and raw JSON responses

Installation
------------

Run the following commands to install dependencies:

pip install -q pydantic
pip install -q --upgrade aixplain
pip install pandas scipy scikit-learn datasets seaborn matplotlib

Project Structure
-----------------

.
├── utils.py                 # Utility functions for evaluation and saving results
├── prediction_single.csv    # Single-agent predictions
├── prediction_multi.csv     # Multi-agent predictions
├── single_results/          # Raw JSON responses from single-agent runs
├── multi_results/           # Raw JSON responses from multi-agent runs
├──fever.ipynb                  # Main script
└── README.md               # This file

How It Works
------------

1. Load Dataset:

   - Uses the FEVEROUS dataset from Hugging Face.
2. Agent Setup:

   - Single-Agent: Uses Tavily search tool for fact verification.
   - Multi-Agent: Two agents - one for evidence extraction, the other for claim classification.
3. Execution:

   - For each claim, prompt is passed to the agent(s), response is saved, and results are evaluated.
4. Evaluation:

   - Calculates accuracy, precision, recall, and F1 using predicted and true labels.

Example Output Format
---------------------

{
  "classification": "1",
  "evidence": "The source article directly contradicts the claim."
}

Notes
-----

- Set your aiXplain API key before running: export TEAM_API_KEY="your_key_here"

Results
-------

Outputs:

- prediction_single.csv: Single-agent classification results
- prediction_multi.csv: Multi-agent classification results
