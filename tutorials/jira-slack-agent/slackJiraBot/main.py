import subprocess
import threading
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from tasks import chat  # this is your celery task module

app = FastAPI()

# Allow any origin for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "Slack JiraBot is running"}

@app.on_event("startup")
def on_startup():
    threading.Thread(
        target=lambda: subprocess.Popen([
            "celery", "-A", "tasks", "worker", "--loglevel=info"
        ])
    ).start()

@app.post("/slack")
async def slack_handler(request: Request):
    body = await request.json()

    # URL verification
    if "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})

    event = body.get("event", {})
    if event.get("type") == "message" and not event.get("bot_id"):
        chat.delay(body)  # Offload to Celery

    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
