import json
import asyncio
import os
from config_secrets import get_secret

os.environ["GOOGLE_API_KEY"] = get_secret("GOOGLE_API_KEY")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from finance_assistant_agent.agent import finance_assistant_agent

_runner = None
_session_service = None

def _init():
    global _runner, _session_service
    if _runner is None:
        _session_service = InMemorySessionService()
        _runner = Runner(agent=finance_assistant_agent, app_name="finance_assistant", session_service=_session_service)

async def _run_agent(user_id: str, message: str) -> str:
    _init()
    session = await _session_service.create_session(app_name="finance_assistant", user_id=user_id)
    content = Content(role="user", parts=[Part(text=message)])
    response_text = ""
    async for event in _runner.run_async(user_id=user_id, session_id=session.id, new_message=content):
        if event.is_final_response() and event.content:
            response_text = event.content.parts[0].text
    return response_text

def handler(event, context):
    body = json.loads(event.get("body") or "{}")
    message = body.get("message")
    user_id = body.get("user_id", "default")

    if not message:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing 'message' in request body"})}

    response = asyncio.get_event_loop().run_until_complete(_run_agent(user_id, message))
    return {
        "statusCode": 200,
        "body": json.dumps({"response": response})
    }
