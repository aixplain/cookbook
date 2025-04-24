# Multi-Agent Experiment Results
# 1318 Samples per run
| **Configuration**                                      | **Accuracy** | **Runtime (s)** | **Credits per Call** |
|--------------------------------------------------------|--------------|-----------------|----------------------|
| Multi-Agent (New TOP P)                                | 0.576        | -               | -                    |
| Single-Agent (New TOP P)                               | 0.683        | -               | -                    |
| Multi-Agent (No Planner) (New TOP P)                   | 0.660        | -               | -                    |
| Multi-Agent (Original, Top-p None, Temp=0)             | 0.840        | -               | -                    |
| Single-Agent (Original, Top-p None, Temp=0)             | 0.810        | -               | -                    |
| Multi-Agent (Reflexion) Original, Top-p None, Temp=0   | **0.893**    | 29.296          | 1.2468e-05           |
| Reflexion LLM Original, Top-p None, Temp=0             | 0.499        | 1.1             | 1.5899e-07           |
