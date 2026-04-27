# Clawy cookbook

## Purpose

Create and interact with a custom agent avatar and short story adventures. Users provide inspiration, reference images, and scene details. Generates images using an external image-edit API and provides interactive story text with choices.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Clawy |
| Description | Create and interact with a custom agent avatar and short story adventures. Users provide inspiration, reference images, and scene details. Generates images using an external image-edit API and provides interactive story text with choices. |
| Instructions | # Clawy Agent Instructions (GPT-5 + Nano Banana)<br>## 1. Avatar Mode<br>* Ask the user for:<br>* Character vibe |
| LLM | `openai/gpt-5/openai` (suggested) |
| Tools | Nano Banana 2.5 Flash Image |
| Output format | `markdown` |
| Max iterations | `10` (suggested) |
| Max tokens | `20000` (suggested) |

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

