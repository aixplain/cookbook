# Threads Posting Agent

## Overview

The Threads Posting Agent is an AI-powered social media assistant that generates, reviews, edits, and publishes content to Threads based on user input and feedback. It leverages multiple specialized AI agents to ensure high-quality content creation and compliance with platform guidelines.

## Core Features

✍️ Content Generation – Creates engaging, concise social media posts based on user input.

🔍 Content Review – Analyzes and provides constructive feedback to improve post quality.

📝 Content Editing – Modifies posts based on user feedback while maintaining consistency.

🚀 Content Publishing – Ensures quality standards and publishes posts directly to Threads.

🌐 Web Search Integration – Retrieves contextual information when necessary.

🤖 AI-Powered Workflow – Uses a structured pipeline to refine content iteratively.

🏆 Quality Assurance – Ensures posts are under 500 characters and free of offensive language.

## How It Works

1. User Input & Profile Definition:

- The user provides input and a profile description.

- The system generates an initial content draft.

2. Content Review:

- The draft is reviewed based on profile guidelines.

- If necessary, feedback is provided for improvement.

3. Content Editing:

- The content is refined based on review feedback.

- Web search is performed if additional context is needed.

4. Publishing:

- Final content is validated for length and appropriateness.

- Upon user approval, it is published to Threads.

## Requirements

- Python environment with aixplain and requests installed.

- An aiXplain access key for API authentication.

- Threads API credentials (User ID and Access Token).


## Installation

```python
pip install aixplain requests
```

## Setup

Before running the agent, set up your aiXplain access key:

```python
import os
os.environ["TEAM_API_KEY"] = "YOUR_ACCESS_KEY"
```

## Agent Components

The Threads Posting Agent consists of multiple specialized AI agents:

- **Content Generator**: Generates a short-form post.

- **Content Reviewer**: Reviews the generated content based on the user profile.

- **Content Editor**: Adjusts the content as per feedback.

- **Content Publisher**: Performs final checks and publishes the content to Threads.

## Usage

### Creating the Team Agent

```python
from aixplain.factories import AgentFactory, TeamAgentFactory, ModelFactory

GPT_4O_MINI_ID = "669a63646eb56306647e1091"
web_search_tool = AgentFactory.create_model_tool(model="6736411cf127849667606689")

content_generator_agent = AgentFactory.create(
    name="Content Generator",
    description="Generates engaging social media content.",
    llm_id=GPT_4O_MINI_ID,
    tools=[web_search_tool],
)

content_reviewer_agent = AgentFactory.create(
    name="Content Reviewer",
    description="Reviews social media content and provides feedback.",
    llm_id=GPT_4O_MINI_ID,
    tools=[],
)

content_editor_agent = AgentFactory.create(
    name="Content Editor",
    description="Edits content based on feedback.",
    llm_id=GPT_4O_MINI_ID,
    tools=[web_search_tool],
)

publish_to_threads_model = ModelFactory.create_utility_model(name="Publish to Threads Trial", code=publish_to_threads)
publish_to_threads_tool = AgentFactory.create_model_tool(model=publish_to_threads_model.id)

content_publisher_agent = AgentFactory.create(
    name="Content Publisher",
    description="Publishes validated content to Threads.",
    llm_id=GPT_4O_MINI_ID,
    tools=[publish_to_threads_tool],
)

team_agent = TeamAgentFactory.create(
    name="Threads Posting Agent",
    agents=[content_generator_agent, content_reviewer_agent, content_editor_agent, content_publisher_agent],
    description="Manages end-to-end social media content creation and publishing.",
    use_mentalist_and_inspector=True,
)
```

### Running the Agent

```python
QUERY = """
Profile:
{{profile}}

Content input:
{{content_input}}

User feedback:
{{user_feedback}}
"""

profile = "Professional business coach. Be concise and focus on actionable advice."
content_input = "One unknown but effective productivity hack."
user_feedback = "None"

response = team_agent.run(query=QUERY, content={"profile": profile, "content_input": content_input, "user_feedback": user_feedback})
print(response.data['output'])
```

### Editing the Content

```python
user_feedback = "Add a step-by-step implementation and use an emoji."
edit_response = team_agent.run(query=QUERY, content={"profile": profile, "content_input": response.data["output"], "user_feedback": user_feedback})
print(edit_response.data['output'])

Publishing the Content

user_feedback = "Looks good, publish it."
publish_response = team_agent.run(query=QUERY, content={"profile": profile, "content_input": edit_response.data["output"], "user_feedback": user_feedback})
print(publish_response.data['output'])
```

### Example Output

```OUTPUT:
🚀 Boost productivity with this simple trick: Break work into 25-min sprints (Pomodoro technique) & take 5-min breaks. Focus up! #ProductivityHacks


REVIEW PROCESS: 1 feedback
1: "Consider adding an emoji for visibility."


FINAL OUTPUT:
🚀 Boost productivity with this simple trick: Break work into 25-min sprints (Pomodoro technique) & take 5-min breaks. Focus up! ⏳ #ProductivityHacks
```


