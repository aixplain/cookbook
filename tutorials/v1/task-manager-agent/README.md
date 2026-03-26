# WhatsApp AI Task Manager with aiXplain, Twilio & Google Sheets

## 🚀 Automate task management using Agents!

This project allows users to send voice notes via WhatsApp, which are then processed using custom aiXplain agents for speech recognition and summarization. The structured data is stored in Google Sheets for easy tracking.

## 🌟 Features

- **Voice-based task extraction** via WhatsApp
- **Custom aiXplain Agents** for speech-to-text & summarization
- **Google Sheets Integration** for task tracking
- **AWS S3 for audio file storage** (Alternative: Google Cloud Storage)
- **Scalable** beyond Twilio (Alternatives: Meta WhatsApp API, Vonage, Gupshup)

## Step 1: Create Your aiXplain Agents

Open the provided Jupyter Notebook (Task Manager.ipynb).

Follow these steps to create custom agents:

### Speech Recognition Agent

```python
from aixplain.factories import AgentFactory
from aixplain.modules.agent.tool.model_tool import ModelTool


speech_recognition_agent = AgentFactory.create(
    name = "Speech Recognition Agent",
    description = "An agent that can recognize speech from a given audio file and extract text from the audio",
    tools = [ModelTool(model = "65554171b43b276f44ebc9a9")]
)
```

### Text Summarization Agent

```python
text_summarization_tool = ModelTool(model = "64788e666eb56313aa7ebac1")

text_summarization_agent = AgentFactory.create(
    name = "Text Summarization Agent",
    description = "An agent that can summarize text into categories - Task, Frequency and Assignee",
    tools = [text_summarization_tool]
)
```

### Team Agent

```python
task_agent = TeamAgentFactory.create(
    name="Task Agent",
    description="""
    You are an AI assistant that extracts actionable tasks from audio files. Follow these steps:

    1. **Speech Recognition**: Extract the spoken text from the provided audio file.
    2. **Task Identification**: Identify the main task from the extracted text.
    3. **Frequency Extraction**: Identify how often the task needs to be done (e.g., daily, weekly, monthly).
    4. **Assignee Identification**: Extract the name of the person responsible for the task.

    **Output Format (Always follow this structure):**

    Task: <extracted task>
    Frequency: <extracted frequency>
    Assignee: <extracted assignee>

    Ensure the response strictly follows this format. If any component is missing in the text, return "Unknown" for that field.
    """,
    agents=[speech_recognition_agent, text_summarization_agent]
)
```

### Deploy the Agent to get endpoints

```python
task_agent.deploy()
```

Once deployed, get the Agent ID and URL. 

```python
print("Agent ID:", task_agent.id)
print("Agent API URL:", task_agent.url)
```


## Step 2: Set Up WhatsApp on Twilio

Twilio provides a sandbox for WhatsApp bot testing.

1. Sign up at [Twilio](https://login.twilio.com/u/signup?state=hKFo2SByaGk1c3hXOVg0cTZnMUpyd19rNjViR3ZhRG5KdUE5caFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIDRvU0YxbFFKemo4cWhsaFU2T01MeGIxM1pKd1dvekluo2NpZNkgTW05M1lTTDVSclpmNzdobUlKZFI3QktZYjZPOXV1cks)
2. Activate WhatsApp Sandbox under Messaging Services
3. Connect via join `code` message to Twilio’s number
4. Get your Account SID, Auth Token, and WhatsApp Number

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Step 3: Google Sheets Integration

Stores tasks, frequency, and assignees.

### Enable Google Sheets API

1. Go to Google Cloud Console. 
2. Enable Google Sheets API. 
3. Create a Service Account and download service_account.json
4. Share your Google Sheet with the Service Account email. 

### Install Dependencies

```
pip install gspread oauth2client
```

### Update Google Sheets

```python
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file("service_account.json")
client = gspread.authorize(creds)
sheet = client.open("Task Manager").sheet1

sheet.append_row(["Task", "Frequency", "Assignee"])
```

## Step 4:  AWS S3 for Audio Storage
Used for storing voice notes.

### Set Up AWS S3

1. Create an S3 bucket on AWS
2. Enable public access or use signed URLs
3. Store AWS credentials

```
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_BUCKET_NAME=your_bucket_name
AWS_REGION=us-east-2
```

### Upload Audio to S3

```python
import boto3

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file_path, file_name):
    s3_client.upload_file(file_path, {AWS_BUCKET_NAME}, file_name)
    return f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{encoded_file_name}"
```

## Step 5: Flask Webhook for WhatsApp

Handles incoming messages & AI processing.

### Install Flask & Twilio

```
pip install flask twilio requests boto3
```

### WhatsApp Webhook

```python
from flask import Flask, request
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    sender_number = request.values.get("From")
    media_url = request.values.get("MediaUrl0")

    if media_url:
        file_path = f"/tmp/{sender_number}.mp3"
        requests.get(media_url).content
        s3_url = upload_to_s3(file_path, f"{sender_number}.mp3")

        ai_response = requests.post(
            f"https://platform-api.aixplain.com/sdk/agents/{AIXPLAIN_AGENT_ID}/run",
            headers={"x-api-key": AIXPLAIN_API_KEY},
            json={"query": f"Extract task details: {s3_url}"}
        ).json()

        task, frequency, assignee = parse_ai_response(ai_response["data"]["output"])
        update_google_sheet(task, frequency, assignee)

        response = MessagingResponse()
        response.message(f"Task Recorded:\n {task}\n {frequency}\n{assignee}")
        return str(response)

    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```
## Ngrok for Local Testing

```
ngrok http 5000
```
Copy the **ngrok HTTPS URL** and set it as **Twilio Webhook**.

## Deployment Options
- Ngrok – For local testing
- AWS Lambda – Serverless deployment
- Google Cloud Run – Scalable API hosting
- Meta WhatsApp Cloud API – Production-ready messaging



## Conclusion
This AI-powered task manager automates WhatsApp-based voice note processing using custom aiXplain agents, AWS, and Google Sheets. 🚀

🔗 Join the community: [aiXplain Discord](https://www.google.com/url?q=https%3A%2F%2Fhttps%3A%2F%2Fdiscord.com%2Finvite%2FT5dCmjRSYA)