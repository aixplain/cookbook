# PPT Generator Agent

## Overview

The PPT Generator Agent converts any script, lecture notes, or written content into a complete, self-contained HTML presentation in the Jobs-style minimalist aesthetic — dark backgrounds, white typography, and the "one screen, one idea" principle. The output is a single `.html` file that runs directly in any browser with no extra software required.

## Core Features

🎨 **Jobs-Style Design** – Dark backgrounds (#000000), white text, ALL CAPS short titles (≤12 characters), and high whitespace — no clutter, no decoration.

📐 **9:16 Vertical Format** – Mobile-first aspect ratio, optimised for presenting on phones and vertical displays.

⚡ **Self-Contained HTML** – The entire presentation is one file with embedded Tailwind CSS, fonts, navigation, transitions, and a slide counter.

🗂️ **Intelligent Structuring** – The Presentation Planner tool automatically breaks your script into slides, assigns types (cover, statement, quote, stat, list, closing), and generates Jobs-style titles.

🚀 **Deployable AI Agent** – Can be published as an API to generate presentations on demand.

## How It Works

1. **Parse** – The Presentation Planner tool breaks the script into a structured JSON slide outline.
2. **Refine** – Applies Jobs-style title constraints and selects appropriate slide types.
3. **Generate** – Produces a single self-contained HTML file with animations and dark styling.
4. **Deliver** – Returns the complete HTML ready to open in any browser.

## Requirements

- Python environment with `aiXplain` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).

No external API keys required.

## Installation

```python
pip install -q aixplain
```

## Setup

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_AIXPLAIN_API_KEY"
```

## Usage

### Creating the Tool and Agent

```python
import inspect
from aixplain import Aixplain

aix = Aixplain(os.environ["TEAM_API_KEY"])

planner_tool = aix.Tool(
    name="Presentation Planner",
    integration="688779d8bfb8e46c273982ca",
    config={"code": inspect.getsource(plan_presentation_structure), "function_name": "plan_presentation_structure"},
)
planner_tool.save()

ppt_agent = aix.Agent(
    name="PPT Generator Agent",
    description="Converts scripts and notes into self-contained Jobs-style HTML presentations.",
    instructions="...",
    tools=[planner_tool],
)
```

### Running the Agent

```python
result = ppt_agent.run("Generate a presentation from this script:\n<your script here>")
print(result.data.output)
```

### Saving the Output

```python
html_output = result.data.output

# Strip markdown fences if present
if "```html" in html_output:
    html_output = html_output.split("```html")[1].split("```")[0].strip()

with open("presentation.html", "w") as f:
    f.write(html_output)

print("Saved to presentation.html — open it in any browser.")
```

### Saving the Agent

```python
ppt_agent.save()
```

## Slide Types

| Type | Description |
|---|---|
| `cover` | Large centred title + one-line subtitle |
| `statement` | Single bold sentence, centred, large |
| `quote` | Italic quote text + attribution |
| `stat` | Giant number/metric + short label |
| `list` | Max 3 items, left-aligned, large spacing |
| `image-text` | Left text + right image placeholder |
| `closing` | "THANK YOU" + CTA or contact line |

## Design Constraints

- Background: `#000000` or `#0a0a0a` only
- Text: `#ffffff` primary, `#999999` secondary
- Titles: ALL CAPS, maximum 12 characters
- Body: maximum 2 short lines per slide
- No bullet lists on content slides
- Fonts: Inter or Roboto via CDN
- Navigation: keyboard arrow keys + on-screen buttons
- Transitions: CSS fade or slide-up, 150–250ms
