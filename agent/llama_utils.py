from llama_cpp import Llama
from tools import get_recent_temperatures, get_anomalies_today, check_system_health

llm = Llama(
    model_path="./model/mistrallite.Q4_K_M.gguf",
    n_ctx=1024,
    n_threads=2,
    n_batch=8,
    verbose=False
)

def ask_local_llm(prompt: str) -> str:
    prompt_lower = prompt.lower()

    if "temperature" in prompt_lower or "temperatures" in prompt_lower:
        data = get_recent_temperatures()
        return f"Here are the recent temperature readings: {data['data']}"

    elif "anomalies" in prompt_lower:
        data = get_anomalies_today()
        return f"Today's detected anomalies: {data['anomalies']}"

    elif "system health" in prompt_lower or "status" in prompt_lower:
        status = check_system_health()
        return f"System health report: {status}"

    result = llm(
        prompt=f"User: {prompt}\nAssistant:",
        max_tokens=128,
        stop=["User:", "Assistant:"]
    )
    return result["choices"][0]["text"].strip()
