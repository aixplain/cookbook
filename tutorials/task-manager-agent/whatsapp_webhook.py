import os
import requests
import time
import boto3
import urllib.parse  # For URL encoding filenames
import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, request
from datetime import datetime
from twilio.rest import Client
import re
import json

# ==============================
# aiXplain Configuration
# ==============================
AIXPLAIN_API_KEY = "YOUR_AIXPLAIN_API_KEY"  # Replace with your aiXplain API key
AIXPLAIN_AGENT_ID = "YOUR_AGENT_ID"  # Replace with your aiXplain agent ID
AIXPLAIN_POST_URL = f"https://platform-api.aixplain.com/sdk/agents/{AIXPLAIN_AGENT_ID}/run"

# ==============================
# AWS S3 Configuration
# ==============================
AWS_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"  # Replace with your AWS credentials
AWS_SECRET_KEY = "YOUR_AWS_SECRET_KEY"
AWS_BUCKET_NAME = "YOUR_AWS_BUCKET_NAME"
AWS_REGION = "us-east-2"  # Modify if using another region

# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# ==============================
# Twilio Configuration
# ==============================
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Replace with your Twilio WhatsApp number

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ==============================
# Google Sheets Configuration
# ==============================
GOOGLE_SHEETS_CREDENTIALS = "service_account.json"  # Ensure this file is in your project directory
GOOGLE_SHEET_NAME = "TaskManagerSheet"

# ==============================
# Flask App Initialization
# ==============================
app = Flask(__name__)

# ------------------------------
# Flask Webhook for WhatsApp Messages
# ------------------------------
@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Receives WhatsApp voice notes, processes them via aiXplain, updates Google Sheets,
       and sends a response back to the user."""
    print("Webhook received a request!")

    sender_number = request.values.get("From", "Unknown")
    media_url = request.values.get("MediaUrl0", None)
    message_type = request.values.get("MediaContentType0", "text")

    print(f"Incoming message from: {sender_number}")
    print(f"Media Type: {message_type}")
    print(f"Media URL: {media_url}")

    final_message = "Something went wrong. Please try again later."

    if media_url and "audio" in message_type:
        clean_number = sender_number.replace("whatsapp:", "").replace("+", "")
        file_name = f"{clean_number}.mp3"
        file_path = f"/tmp/{file_name}"

        if download_audio(media_url, file_path):
            s3_url = upload_to_s3(file_path, file_name)

            if s3_url:
                ai_response = process_with_aixplain(s3_url)

                if ai_response:
                    task, frequency, assignee = parse_ai_response(ai_response)
                    update_google_sheet(task, frequency, assignee)

                    # Success Message
                    final_message = f"✅ Task Recorded!\n\n *Task:* {task}\n *Frequency:* {frequency}\n *Assignee:* {assignee}"
                else:
                    final_message = "Failed to process the voice note. Please try again."
            else:
                final_message = "Error uploading the audio. Please resend the voice note."
        else:
            final_message = "Failed to download the voice note. Please try again."
    else:
        final_message = "Please send a voice note to create a task."

    # Send the final response to the user
    send_whatsapp_message(sender_number, final_message)

    return "OK", 200

# ------------------------------
# Helper Functions
# ------------------------------
def download_audio(url, save_path):
    """Downloads an audio file from Twilio and saves it locally."""
    print(f"Downloading audio file: {url}")

    response = requests.get(url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Audio file saved locally: {save_path}")
        return True
    else:
        print(f"Failed to download audio. Status Code: {response.status_code}")
        return False

def upload_to_s3(file_path, file_name):
    """Uploads the audio file to AWS S3 and returns a public URL."""
    try:
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, file_name)
        encoded_file_name = urllib.parse.quote(file_name)
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{encoded_file_name}"
        print(f"File uploaded to S3: {s3_url}")
        return s3_url
    except Exception as e:
        print(f"S3 Upload Failed: {e}")
        return None

def process_with_aixplain(audio_url):
    """Sends AWS S3 audio URL to aiXplain Task Manager Agent and polls for results."""
    print(f"Sending audio URL to aiXplain: {audio_url}")

    headers = {"x-api-key": AIXPLAIN_API_KEY, "Content-Type": "application/json"}
    payload = {"query": f"Extract text from this file and return markdown response for Task, Frequency, and Assignee: {audio_url}"}

    response = requests.post(AIXPLAIN_POST_URL, json=payload, headers=headers)

    if response.status_code == 201:
        response_data = response.json()
        request_id = response_data.get("requestId")
        result_url = response_data.get("data")  # Get the result URL

        print(f"aiXplain Request ID: {request_id}")
        print(f"Polling Result URL: {result_url}")

        if not result_url:
            print("No result URL received from aiXplain.")
            return None

        # Polling for completion
        while True:
            result_response = requests.get(result_url, headers=headers)
            result_data = result_response.json()

            if result_data.get("completed"):
                print(f"AI Task Extraction Successful: {result_data}")
                return result_data.get("data", {}).get("output", "No task extracted.")

            print("Waiting for aiXplain to process the request...")
            time.sleep(5)
    else:
        print(f"aiXplain API Error: {response.status_code} - {response.text}")
        return None

def parse_ai_response(ai_response):
    """Parses aiXplain response to extract Task, Frequency, and Assignee."""
    json_match = re.search(r"\{[\s\S]*?\}", ai_response)
    
    if json_match:
        try:
            json_data = json.loads(json_match.group(0))
            return json_data.get('query', {}).get('Task', 'Unknown'), \
                   json_data.get('query', {}).get('Frequency', 'Unknown'), \
                   json_data.get('query', {}).get('Assignee', 'Unknown')
        except json.JSONDecodeError:
            pass

    # Markdown pattern fallback
    task = re.search(r"\*\*Task:\*\*\s*(.+)", ai_response)
    frequency = re.search(r"\*\*Frequency:\*\*\s*(.+)", ai_response)
    assignee = re.search(r"\*\*Assignee:\*\*\s*(.+)", ai_response)

    return task.group(1) if task else "Unknown", \
           frequency.group(1) if frequency else "Unknown", \
           assignee.group(1) if assignee else "Unknown"

def update_google_sheet(task, frequency, assignee):
    """Update Google Sheets with extracted task information."""
    creds = Credentials.from_service_account_file("service_account.json")
    client = gspread.authorize(creds)
    sheet = client.open("TaskManagerSheet").sheet1

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, task, frequency, assignee])

    print("Google Sheet updated with extracted task information.")


def send_whatsapp_message(to, message):
    """Send a WhatsApp message using Twilio API."""
    twilio_client.messages.create(body=message, from_=TWILIO_WHATSAPP_NUMBER, to=to)
    print(f"Message sent to {to}: {message}")


# ------------------------------
# Start Flask Server
# ------------------------------
if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)