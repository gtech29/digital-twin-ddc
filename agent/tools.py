# agent/tools.py
from datetime import datetime, timedelta

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

def check_system_health():
    return {
        "mqtt_broker": "connected",
        "plc": "active",
        "sensor": "publishing",
        "dashboard": "online",
        "status": "healthy"
    }
