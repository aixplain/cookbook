# Cpo Advisor cookbook

## Purpose

Provides strategic product leadership advice, including product vision, portfolio analysis, PMF scoring, and organizational design recommendations.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Cpo Advisor |
| Description | Provides strategic product leadership advice, including product vision, portfolio analysis, PMF scoring, and organizational design recommendations. |
| Instructions | You are a CPO Advisor.<br>* Evaluate product strategies, PMF, portfolio health, and organizational structures.<br>* Provide recommendations on Invest/Maintain/Kill decisions.<br>* Score PMF across retention, engagement, satisfaction, and growth. |
| LLM | `openai/gpt-4o/openai` (suggested) |
| Tools | None |
| Output format | `markdown` |
| Max iterations | `5` (suggested) |
| Max tokens | `2000` (suggested) |

## When to use

- Use this agent for tasks that match its domain description and instructions.
- Use it when you want a repeatable first draft before manual editing or validation.
- Use it when speed matters more than custom hand-written formatting on the first pass.

## How to use

- Primary input: a text query that clearly states the task, desired output, and any constraints or preferences.
- Best results come from including concrete context such as audience, format, scope, and success criteria in the query itself.
- This agent does not expose fixed file or parameter inputs in the cookbook; adapt it by refining the prompt for the specific use case.

## Sample queries

| Query | Expected output |
|---|---|
| Summarize what this agent does and the best way to use it. | A concise response describing the agent's scope, boundaries, and the best prompt format to use with it. |
| Handle a representative task in the agent's domain and explain your reasoning. | A structured response that completes the requested task in the agent's domain and follows the agent's built-in instructions. |
| Handle a representative task in the agent's domain and explain your reasoning. | A practical first draft that can be reviewed and refined rather than a raw brainstorm. |

