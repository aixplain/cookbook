# Tavily Search Skill cookbook

## Purpose

An advanced web-intelligence agent powered by Tavily's search engine. It specializes in real-time information retrieval, source verification, and synthesized research. Unlike standard search tools, this agent filters for high-relevance data, extracts key insights from multiple URLs, and maintains a structured knowledge base for complex decision-making.

Developer attribution: **Rahaf**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Tavily Search Skill |
| Description | An advanced web-intelligence agent powered by Tavily's search engine. It specializes in real-time information retrieval, source verification, and synthesized research. Unlike standard search tools, this agent filters for high-relevance data, extracts key insights from multiple URLs, and maintains a structured knowledge base for complex decision-making. |
| Instructions | ### IDENTITY & STRATEGY<br>You are the "Search Intelligence Specialist." Your purpose is to bridge the gap between static knowledge and the real-time world. You don't just "search"; you "investigate."<br>### SEARCH PROTOCOLS (The 3-Step Scan)<br>Whenever you are asked for information not in your training data or requiring real-time updates (News, Prices, Tech Specs, Legal changes): |
| LLM | `openai/gpt-4o-mini/openai` (suggested) |
| Tools | Tavily Web Search |
| Output format | `markdown` |
| Max iterations | `5` (suggested) |
| Max tokens | `2000` (suggested) |

## When to use

- Use this agent when you need a first-pass SKILL.md draft from a plain-English request.
- Use it to standardize skill structure, frontmatter, and section ordering before manual review.
- Use it when speed matters more than custom hand-written formatting on the first pass.

## How to use

- Primary input: a text query describing the skill you want, including its purpose, expected output, and any required sections or formatting rules.
- Best results come from specifying the target domain, required workflow steps, output constraints, and whether the request is for a brand-new skill or an update to an existing one.
- This agent does not require file inputs or fixed parameters; adapt it for different purposes by changing the prompt details, strictness, and scope of the requested skill.

## Sample queries

| Query | Expected output |
|---|---|
| Create a new Codex skill for triaging support emails. | A draft SKILL.md with YAML frontmatter and the required markdown sections in the correct order. |
| Summarize what this agent does and the best way to use it. | A concise explanation of what the skill should do and the best input shape to provide before generating a full draft. |
| Handle a representative task in the agent's domain and explain your reasoning. | A reusable skill draft that is ready for review, cleanup, and validation. |

