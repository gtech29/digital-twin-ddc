from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_utils import ask_local_llm
from tools import get_recent_temperatures, get_anomalies_today, check_system_health
from datetime import datetime, timedelta

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] for tighter security in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok", "message": "Local LLM agent is alive"})

# Optional: Expose tools directly for manual testing
@app.get("/tools/get-temperatures")
def test_temp_tool():
    return get_recent_temperatures()

@app.get("/tools/get-anomalies")
def test_anomaly_tool():
    return get_anomalies_today()

@app.get("/tools/check-health")
def test_health_tool():
    return check_system_health()

# Main LLM interaction endpoint
@app.post("/ask")
async def ask_agent(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt", "").strip()

    if not user_prompt:
        return JSONResponse(status_code=400, content={"error": "Prompt is empty."})

    try:
        response_text = ask_local_llm(user_prompt)
        return {"response": response_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run the FastAPI app with: uvicorn agent.main:app --reload
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from llama_utils import ask_local_llm
from tools import get_recent_temperatures, get_anomalies_today, check_system_health
from datetime import datetime, timedelta

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:3000"] for tighter security in dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok", "message": "Local LLM agent is alive"})

# Optional: Expose tools directly for manual testing
@app.get("/tools/get-temperatures")
def test_temp_tool():
    return get_recent_temperatures()

@app.get("/tools/get-anomalies")
def test_anomaly_tool():
    return get_anomalies_today()

@app.get("/tools/check-health")
def test_health_tool():
    return check_system_health()

# Main LLM interaction endpoint
@app.post("/ask")
async def ask_agent(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt", "").strip()

    if not user_prompt:
        return JSONResponse(status_code=400, content={"error": "Prompt is empty."})

    try:
        response_text = ask_local_llm(user_prompt)
        return {"response": response_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run the FastAPI app with: uvicorn agent.main:app --reload
