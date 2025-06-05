import os
import random
import socket
import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

# Use environment variable for MQTT broker, default to 'mqtt-broker'
MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = 1883
print(f"[INFO] Using MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")

# Store latest values including JENEsys and Trane devices
latest_values = {
    "plc": {
        "temperature": None,
        "setpoint": None,
        "humidity": None,
        "fan_status": None
    },
    "dnp3": {
        "temperature": None,
        "valve_position": None,
        "alarm": None
    },
    "sensor": {
        "temperature": None,
        "humidity": None
    },
    "jensys": {
        "temperature": None,
        "humidity": None,
        "ip": None,
        "model": None,
        "firmware": None
    },
    "trane": {
        "ip": None,
        "model": None,
        "firmware": None,
        "temperature": None
    }
}

# Historical storage
historical_data = {
    "plc": {"temperature": []},
    "dnp3": {"temperature": []},
    "sensor": {"temperature": []},
    "jensys": {"temperature": []},
    "trane": {"temperature": []},
}

# MQTT topic to data mapping
TOPICS = {
    "plc/temperature": ("plc", "temperature"),
    "plc/setpoint": ("plc", "setpoint"),
    "plc/humidity": ("plc", "humidity"),
    "plc/fan_status": ("plc", "fan_status"),

    "dnp3/temperature": ("dnp3", "temperature"),
    "dnp3/valve_position": ("dnp3", "valve_position"),
    "dnp3/alarm": ("dnp3", "alarm"),

    "sensor/temperature": ("sensor", "temperature"),
    "sensor/humidity": ("sensor", "humidity"),

    "jensys/temperature": ("jensys", "temperature"),
    "jensys/humidity": ("jensys", "humidity"),
    "jensys/ip": ("jensys", "ip"),
    "jensys/model": ("jensys", "model"),
    "jensys/firmware": ("jensys", "firmware"),

    "trane/ip": ("trane", "ip"),
    "trane/model": ("trane", "model"),
    "trane/firmware": ("trane", "firmware"),
    "trane/temperature": ("trane", "temperature"),
}

# MQTT handlers
def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"[MQTT] Subscribed to {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Received on {topic}: {payload}")

    if topic in TOPICS:
        device, param = TOPICS[topic]
        latest_values[device][param] = payload

        if param == "temperature":
            timestamp = int(time.time())
            hist_list = historical_data.get(device, {}).get(param, [])
            hist_list.append({"timestamp": timestamp, "value": float(payload)})
            if len(hist_list) > 100:
                hist_list.pop(0)
            historical_data[device][param] = hist_list

# Try connecting to broker with fallback
mqtt_client = mqtt.Client(client_id="dashboard")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    def mqtt_loop():
        mqtt_client.loop_forever()

    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    print("[MQTT] Background loop started.")
except (socket.gaierror, ConnectionRefusedError) as e:
    print(f"[ERROR] Failed to connect to MQTT broker at {MQTT_BROKER}:{MQTT_PORT} — {e}")

# Flask routes
@app.route("/")
def index():
    return "Digital Twin Dashboard Backend Running", 200

@app.route("/api/device_data")
def device_data():
    # Simulate fake data for frontend testing
    fake_data = {
        "plc": {
            "temperature": round(20 + (5 * random.random()), 2),
            "setpoint": "22.5",
            "humidity": round(40 + (10 * random.random()), 2),
            "fan_status": "on"
        },
        "dnp3": {
            "temperature": round(19 + (6 * random.random()), 2),
            "valve_position": "open",
            "alarm": "normal"
        },
        "sensor": {
            "temperature": round(21 + (3 * random.random()), 2),
            "humidity": round(45 + (5 * random.random()), 2)
        },
        "jensys": {
            "temperature": round(23 + (2 * random.random()), 2),
            "humidity": round(40 + (10 * random.random()), 2),
            "ip": "192.168.1.50",
            "model": "JENEsys 8000",
            "firmware": "v3.1.2"
        },
        "trane": {
            "ip": "192.168.1.60",
            "model": "Tracer SC+",
            "firmware": "v4.5.6",
            "temperature": round(24 + (1 * random.random()), 2)
        }
    }
    return jsonify(fake_data)

@app.route("/api/historical_data")
def historical_data_api():
    device = request.args.get("device", "plc")
    param = request.args.get("param", "temperature")
    data = historical_data.get(device, {}).get(param, [])
    for entry in data:
        entry["time_iso"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(entry["timestamp"]))
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
