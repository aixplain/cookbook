# Create Skills cookbook

## Purpose

Creates or updates skills by generating structured SKILL.md files based on user instructions. Use when building new skills or modifying existing ones. Key capabilities include proper structuring, YAML frontmatter generation, and best practice alignment.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Create Skills |
| Description | Creates or updates skills by generating structured SKILL.md files based on user instructions. Use when building new skills or modifying existing ones. Key capabilities include proper structuring, YAML frontmatter generation, and best practice alignment. |
| Instructions | You are a Skill Builder Expert specialized in creating high-quality skills.<br>STRICT OUTPUT RULES (MANDATORY):<br>* You MUST output ONLY a valid SKILL.md file.<br>* Your response MUST start with "---" on the FIRST line. |
| LLM | `openai/gpt-5/openai` (suggested) |
| Tools | None |
| Output format | `markdown` |
| Max iterations | `10` (suggested) |
| Max tokens | `7500` (suggested) |

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

