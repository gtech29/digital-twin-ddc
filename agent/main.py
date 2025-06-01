from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import os
import base64
import openai
import json

# 🔐 Load OpenAI API Key from base64-encoded file
def load_openai_key():
    key_path = os.path.join(os.path.dirname(__file__), "openai_key.b64")
    with open(key_path, "rb") as f:
        encoded = f.read()
    decoded = base64.b64decode(encoded).decode("utf-8").strip()
    return decoded

OPENAI_API_KEY = load_openai_key()
openai.api_key = OPENAI_API_KEY

# 🚀 Start FastAPI
app = FastAPI()

# ✅ Health check route
@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok", "message": "Agent is alive"})

# 🧪 Tool: Simulated temperature data query
def get_recent_temperatures(start_time: str = None, end_time: str = None):
    if not start_time or not end_time:
        end = datetime.utcnow()
        start = end - timedelta(hours=6)
    else:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)

    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "data": [
            {"timestamp": start.isoformat(), "temp": 72.5},
            {"timestamp": (start + timedelta(hours=2)).isoformat(), "temp": 74.0},
            {"timestamp": end.isoformat(), "temp": 73.2},
        ]
    }

# 🧪 Tool: Simulated anomaly detector
def get_anomalies_today():
    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    return {
        "date": start_of_day.date().isoformat(),
        "anomalies": [
            {"timestamp": (start_of_day + timedelta(hours=3)).isoformat(), "temp": 82.1, "status": "anomaly"},
            {"timestamp": (start_of_day + timedelta(hours=9)).isoformat(), "temp": 84.5, "status": "anomaly"},
        ]
    }

# 🧪 Tool: Simulated system health check
def check_system_health():
    return {
        "mqtt_broker": "connected",
        "plc": "active",
        "sensor": "publishing",
        "dashboard": "online",
        "status": "healthy"
    }

# 🧰 Tool registry for OpenAI function-calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_recent_temperatures",
            "description": "Retrieve temperature data over a specific time range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO format (e.g. 2025-06-01T12:00:00)"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO format (e.g. 2025-06-01T18:00:00)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_anomalies_today",
            "description": "Get a list of anomalies detected today.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_system_health",
            "description": "Check the health status of system components.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# 🔁 Route: Test get_recent_temperatures() directly
@app.get("/tools/get-temperatures")
def test_temp_tool():
    return get_recent_temperatures()

# 💬 Route: Smart agent with function-calling
@app.post("/ask")
async def ask_openai(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt", "Hello!")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can read sensor data and check system health."},
                {"role": "user", "content": user_prompt}
            ],
            functions=tools,
            function_call="auto"
        )

        choice = response.choices[0]
        if choice.finish_reason == "function_call":
            fn_name = choice.message.function_call.name
            args = json.loads(choice.message.function_call.arguments)

            if fn_name == "get_recent_temperatures":
                result = get_recent_temperatures(**args)
                return {
                    "response": f"Here is the temperature data from {result['start']} to {result['end']}.",
                    "data": result
                }

            elif fn_name == "get_anomalies_today":
                result = get_anomalies_today()
                return {
                    "response": f"Here are the anomalies for {result['date']}.",
                    "data": result
                }

            elif fn_name == "check_system_health":
                result = check_system_health()
                return {
                    "response": "System health check complete.",
                    "data": result
                }

        return {"response": choice.message.content}

    except Exception as e:
        return {"error": str(e)}
