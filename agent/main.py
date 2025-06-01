from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import base64

def load_openai_key():
    key_path = os.path.join(os.path.dirname(__file__), "openai_key.b64")
    with open(key_path, "rb") as f:
        encoded = f.read()
    decoded = base64.b64decode(encoded).decode("utf-8").strip()
    return decoded

OPENAI_API_KEY = load_openai_key()

app = FastAPI()

@app.get("/ping")
def ping():
    return JSONResponse(content={"status": "ok", "message": "Agent is alive"})
