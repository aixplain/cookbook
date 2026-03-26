# UI/UX Pro Max Agent

## Overview

The UI/UX Pro Max Agent is an AI-powered design intelligence assistant that generates complete design systems and provides implementation-ready guidance for building polished, accessible interfaces. Given a product type, visual style, and technology stack, it produces everything from color tokens to component states — tailored to your specific framework and platform.

## Core Features

🎨 **Design System Generation** – Produces color tokens, typography scales, spacing rhythm, border radius, shadows, and animation tokens for any product type and style direction.

🔍 **Pattern Search** – Returns domain-specific best practices for navigation, forms, accessibility, charts, and animation, with framework-specific implementation tips.

♿ **Accessibility First** – Every recommendation is checked against WCAG AA standards, including contrast ratios, touch target sizes, keyboard navigation, and screen reader support.

📱 **Multi-Platform Support** – Covers Web, iOS, Android, and Desktop across React, Next.js, Vue, Svelte, Flutter, React Native, SwiftUI, Tailwind, shadcn, and more.

🚀 **Deployable AI Agent** – Can be published as an API for seamless integration into your development workflow.

## How It Works

The agent follows a structured workflow to deliver design recommendations:

1. **Triage** – Extracts product type, technology stack, platform, and visual style from the request.
2. **Design System Generation** – Calls the token generator tool to produce a complete design spec.
3. **Pattern Search** – Calls the pattern search tool for domain-specific UX and implementation guidance.
4. **Delivery** – Returns design tokens, code snippets in the user's stack, accessibility notes, and anti-patterns to avoid.

## Requirements

- Python environment with `aiXplain` installed.
- An aiXplain access key to authenticate API calls.

## Installation

```python
pip install -q aixplain
```

## Setup

Before running the agent, set up your aiXplain access key:

```python
import os
AccessKey = "YOUR_AIXPLAIN_API_KEY"
os.environ["TEAM_API_KEY"] = AccessKey
```

## Usage

### Creating the Tools and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(AccessKey)

SCRIPT_INTEGRATION_ID = "688779d8bfb8e46c273982ca"

design_tokens_tool = aix.Tool(
    name="UI UX Design Token Generator",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": inspect.getsource(generate_design_tokens), "function_name": "generate_design_tokens"},
)
design_tokens_tool.save()

design_patterns_tool = aix.Tool(
    name="UI UX Pattern Search",
    integration=SCRIPT_INTEGRATION_ID,
    config={"code": inspect.getsource(search_design_patterns), "function_name": "search_design_patterns"},
)
design_patterns_tool.save()

uiux_agent = aix.Agent.create(
    name="UI/UX Pro Max Agent",
    description="Design intelligence agent that generates design systems and provides implementation-ready UI/UX guidance across web and mobile stacks.",
    instructions="...",
    tools=[design_tokens_tool, design_patterns_tool],
)
```

### Running the Agent

```python
result = uiux_agent.run(
    """I'm building a fintech mobile app for iOS using React Native. 
    I want a professional, trustworthy feel. Generate a complete design system."""
)
print(result.data.output)
```

### Saving the Agent

```python
uiux_agent.save()
```

## Example Output

```
# Design System — Fintech App (Corporate Professional)
**Stack:** react-native | **Platform:** ios | **Style:** corporate professional

## Color Tokens
--primary:              #1E40AF
--primary-foreground:   #FFFFFF
--secondary:            #374151
--background:           #FFFFFF
--surface:              #F9FAFB
--error:                #B91C1C
...

## Typography Scale
Heading font: IBM Plex Sans
Body font: IBM Plex Sans
Mono font: IBM Plex Mono

display:   3rem / 1.1 / -0.02em
h1:        2.25rem / 1.2 / -0.01em
body:      1rem / 1.5 / 0
...

## Touch & Interaction
- Minimum touch target: 44x44pt (Apple HIG minimum)
- Interaction feedback: within 80-150ms

## Stack Implementation
react-native: Create a theme.ts constants file; use useColorScheme for dark/light switching.
```

## Supported Stacks

| Stack | Platform |
|---|---|
| React, Next.js | Web |
| Vue, Nuxt, Svelte | Web |
| Tailwind CSS, shadcn | Web |
| Flutter | iOS, Android |
| React Native | iOS, Android |
| SwiftUI | iOS |
| Jetpack Compose | Android |

## Supported Style Directions

- `minimal clean` – Blue primary, neutral greys, white backgrounds
- `bold vibrant` – Purple/pink palette, high contrast
- `corporate professional` – Deep blue, formal typography
- `dark elegant` – Dark backgrounds, violet accents
- `playful friendly` – Warm reds/oranges, rounded elements
