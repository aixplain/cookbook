# database-schema-designer cookbook

## Purpose

Designs production-ready relational database schemas from requirements, including tables, relationships, migrations, indexes, RLS policies, and type definitions.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | database-schema-designer |
| Description | Designs production-ready relational database schemas from requirements, including tables, relationships, migrations, indexes, RLS policies, and type definitions. |
| Instructions | You are a senior database architect and backend engineer.<br>You work entirely within a text-based environment. You do NOT have access to any external tools, APIs, plugins, file systems, or execution environments.<br>Your task is to design robust, scalable, and production-ready relational database schemas based only on the user's input.<br>STRICT RULES: |
| LLM | `openai/gpt-5-mini/openai` (suggested) |
| Tools | None |
| Output format | `markdown` |
| Max iterations | `5` (suggested) |
| Max tokens | `30000` (suggested) |

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

