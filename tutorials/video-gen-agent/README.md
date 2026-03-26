# Video Gen Agent

## Overview

The Video Gen Agent is an AI-powered short video production assistant that generates videos from text prompts or reference images. It uses [BytePlus Seedance](https://studio.aixplain.com/browse/model/695ea397253de54a56dc5aa1) — a production-grade video generation model available directly on the aiXplain platform — to produce 2–12 second clips in any standard aspect ratio.

## Core Features

🎬 **Text-to-Video** – Describe any scene, product, or concept and the agent generates a polished video clip.

🖼️ **Image-to-Video** – Provide a reference image and Seedance animates it into a video.

📐 **Multi-Format Output** – Supports 16:9 (YouTube/landscape), 9:16 (TikTok/Reels), 1:1 (Instagram), 4:3, and 21:9.

🎯 **Prompt Engineering** – The agent translates natural language requests into precise, Seedance-optimised prompts without overriding the user's intent.

🚀 **No Extra API Key** – Uses the BytePlus Seedance model already available on the aiXplain platform — only your aiXplain access key is needed.

## How It Works

1. **Understand the request** — extract scene, style, aspect ratio, duration, and any reference image.
2. **Compose the prompt** — translate the request into a precise video prompt with camera movement, lighting, and mood.
3. **Generate** — call the Seedance model with the prompt and video parameters.
4. **Deliver** — return the video URL when generation completes (~1–3 minutes).

## Requirements

- Python environment with `aiXplain` installed.
- An aiXplain access key from [platform.aixplain.com](https://platform.aixplain.com/account/integrations).

No separate BytePlus or video API key required.

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

### Loading the Tool and Creating the Agent

```python
from aixplain import Aixplain
from aixplain.factories import ModelFactory

aix = Aixplain(os.environ["TEAM_API_KEY"])

# Load the BytePlus Seedance model from the aiXplain platform
video_tool =aix.Model.get("bytedance/seedance-1-5-pro/bytedance")

video_agent = aix.Agent(
    name="Video Gen Agent",
    description="Generates short videos from text prompts or reference images using BytePlus Seedance.",
    instructions="...",
    tools=[video_tool],
)
video_agent.save()
```

### Running the Agent

```python
result = video_agent.run(
    "Generate a 5-second 9:16 product ad for a sleek black coffee machine, cinematic lighting, slow zoom in"
)
print(result.data.output)
```

### Multi-Turn Refinement

```python
result = video_agent.run("Create a sunset ocean video for Instagram Reels")
print(result.data.output)

# Refine in the same session
followup = video_agent.run(
    "Make it more dramatic — stormy sky, bigger waves, darker mood",
    session_id=result.data.session_id
)
print(followup.data.output)
```

### Saving the Agent

```python
video_agent.save()
```

## Video Parameters

| Parameter | Options | Default |
|---|---|---|
| Aspect ratio | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` | `16:9` |
| Duration | 2–12 seconds | 5s |
| Resolution | `480p`, `720p`, `1080p` | `720p` |

## Supported Use Cases

| Use Case | Recommended Format |
|---|---|
| YouTube / landscape content | 16:9 |
| TikTok / Instagram Reels | 9:16 |
| Instagram feed / square | 1:1 |
| Product demos and ads | 16:9 or 9:16 |
| Brand intros | 16:9 |
| B-roll and mood footage | Any |

## Example Prompts

```
"A coffee cup on a marble table, steam rising slowly, warm morning light,
 cinematic macro shot, 5 seconds, 9:16"

"A futuristic city skyline at night with neon reflections on wet streets,
 slow pan from left to right, 8 seconds, 16:9"

"A hand opening a luxury skincare product box with soft studio lighting,
 product reveal shot, 5 seconds, 1:1"
```

> **Generation time:** Videos typically take 1–3 minutes to generate. The agent returns the URL once complete.
