# Results

## Kaggle

| Configuration     | Run | Accuracy |
|-------------------|-----|----------|
| Single - Llama3.1 | 0   | 54.11    |
| Single - Llama3.1 | 1   | 54.11    |
| Single - Llama3.1 | 2   | 54.59    |
| Multi - Llama3.1  | 0   | 50.72    |
| Multi - Llama3.1  | 1   | 50.24    |
| Multi - Llama3.1  | 2   | 52.66    |
| Double - Llama3.1  | 0   | 27.05    |
| Reflexion - Llama3.1  | 0   | 54.59    |
| Single - GPT-4 Turbo  | 0   | 51.69    |

## Triple Quotes

LLMs were generating triple quotes in their responses. This was fixed by adding a check to remove them. This is the result of the experiment:

| Configuration     | Run | Accuracy |
|-------------------|-----|----------|
| Single - Llama3.1 - Triple Quotes | 0   | 41.06    |
| Single - Llama3.1 - Triple Quotes | 1   | 37.68    |
| Single - Llama3.1 - Triple Quotes | 2   | 39.61    |
| Single - Llama3.1 - w/o Triple Quotes | 0   | 43.00    |
| Single - Llama3.1 - w/o Triple Quotes | 1   | 40.58    |
| Single - Llama3.1 - w/o Triple Quotes | 2   | 40.10    |

# Official Results (November 19th)

| Model                          | Run | Accuracy | Used Credits | Elapsed Time |
|--------------------------------|-----|----------|--------------|--------------|
| single_agent_llama             | 0   | 0.46860  | 0.00000      | 7.48971      |
| single_agent_llama             | 1   | 0.47826  | 0.00000      | 7.48971      |
| single_agent_llama             | 2   | 0.47343  | 0.00000      | 7.48971      |
| orchestrator_agent_llama       | 0   | 0.24155  | 0.00002      | 32.95870     |
| orchestrator_agent_llama       | 1   | 0.23188  | 0.00002      | 32.95870     |
| orchestrator_agent_llama       | 2   | 0.29469  | 0.00002      | 32.95870     |
| multi_agent_llama              | 0   | 0.04348  | 0.00007      | 100.35112    |
| multi_agent_llama              | 1   | 0.05314  | 0.00007      | 100.35112    |
| multi_agent_llama              | 2   | 0.04348  | 0.00007      | 100.35112    |
| multi_agent_llama_reflexion    | 0   | 0.54589  | 0.00008      | 103.41158    |