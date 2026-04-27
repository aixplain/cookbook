# Sourcing in China cookbook

## Purpose

Helps users search for products and suppliers from China, analyze product details, and compare sourcing options based on price, MOQ, and supplier credibility.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Sourcing in China |
| Description | Helps users search for products and suppliers from China, analyze product details, and compare sourcing options based on price, MOQ, and supplier credibility. |
| Instructions | You are a China sourcing assistant.<br>Your job is to help users find products and suppliers from China using web search.<br>Workflow:<br>1. Use Tavily search to find products based on user query. |
| LLM | `openai/gpt-5-mini/openai` (suggested) |
| Tools | Tavily Web Search |
| Output format | `markdown` |
| Max iterations | `7` (suggested) |
| Max tokens | `4000` (suggested) |

## When to use

- Use this agent for tasks that match its domain description and instructions.
- Use it when you want a repeatable first draft before manual editing or validation.
- Use it when speed matters more than custom hand-written formatting on the first pass.

## How to use

- Primary input: a text query that clearly states the task, desired output, and any constraints or preferences.
- Best results come from including concrete context such as audience, format, scope, and success criteria in the query itself.
- If the agent uses tools, configure the request so the query names the task clearly enough for the tool-backed workflow to route correctly.

## Sample queries

| Query | Expected output |
|---|---|
| Summarize what this agent does and the best way to use it. | A concise response describing the agent's scope, boundaries, and the best prompt format to use with it. |
| Handle a representative task in the agent's domain and explain your reasoning. | A structured response that completes the requested task in the agent's domain and follows the agent's built-in instructions. |
| Handle a representative task in the agent's domain and explain your reasoning. | A practical first draft that can be reviewed and refined rather than a raw brainstorm. |

