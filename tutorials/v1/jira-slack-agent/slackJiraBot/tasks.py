from celery import Celery
import os, json, time, requests
from slack_sdk import WebClient
from aixplain.factories import AgentFactory
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

# Get environment variables
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
AGENT_ID = os.getenv("AGENT_ID")
AIXPLAIN_API_KEY = os.getenv("AIXPLAIN_API_KEY")

# Now set these as needed
os.environ["SLACK_TOKEN"] = SLACK_TOKEN
os.environ["AGENT_ID"] = AGENT_ID
os.environ["AIXPLAIN_API_KEY"] = AIXPLAIN_API_KEY


redis_url = os.getenv("REDIS_URL")
celery_app = Celery("tasks", broker=redis_url, backend=redis_url)
slack_client = WebClient(token=os.environ["SLACK_TOKEN"])

@celery_app.task(name="chat")
def chat(body: dict):
    event = body.get("event", {})
    user = event.get("user")
    channel = event.get("channel")
    text = event.get("text")
    thread_ts = event.get("ts")

    if not text:
        return

    agent = AgentFactory.get("67f83c494fac2f025fe87542")
    response = agent.run(text, session_id=thread_ts)

    slack_client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=response["data"]["output"]
    )

