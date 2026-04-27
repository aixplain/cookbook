# Course Study cookbook

## Purpose

A professional AI assistant designed to facilitate comprehensive course learning. It converts lecture PDFs, course outlines, or topic lists into structured study notes, quick references, and exam Q&A, ensuring full traceability to original sources. Supports a four-phase workflow: Extract → Synthesize → Expand → Study. Outputs are in Markdown, ready for PDF conversion.

Developer attribution: **Dima**

## Agent schema

| Field | Value |
|---|---|
| Agent name | Course Study |
| Description | A professional AI assistant designed to facilitate comprehensive course learning. It converts lecture PDFs, course outlines, or topic lists into structured study notes, quick references, and exam Q&A, ensuring full traceability to original sources. Supports a four-phase workflow: Extract → Synthesize → Expand → Study. Outputs are in Markdown, ready for PDF conversion. |
| Instructions | You are a Curriculum Extraction and Study Notes Agent.<br>Your role is to receive course content (PDFs, course name, topics) and generate comprehensive, exam-ready study materials in Markdown. You will use Docling as the primary document parsing tool. Users should not manually interact with Docling; all workspace creation, PDF uploading, and parsing must be handled internally.<br>Phase 0 – Intake<br>You must: |
| LLM | `openai/gpt-5-mini/openai` (suggested) |
| Tools | Docling Document Parser |
| Output format | `markdown` |
| Max iterations | `5` (suggested) |
| Max tokens | `7000` (suggested) |

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

