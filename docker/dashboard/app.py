from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import threading
from collections import defaultdict, deque
from sklearn.ensemble import IsolationForest
import numpy as np

app = Flask(__name__)

MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883

# Store latest values
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
    }
}

# Store historical data (up to 100 samples per parameter)
history = defaultdict(lambda: defaultdict(lambda: deque(maxlen=100)))

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
}

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

        # Save to history only if numeric
        try:
            value = float(payload)
            history[device][param].append(value)
        except ValueError:
            pass  # Non-numeric values like "ON", "NORMAL" will be ignored

mqtt_client = mqtt.Client(client_id="dashboard")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

def mqtt_loop():
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/device_data")
def device_data():
    return jsonify(latest_values)

@app.route("/api/predictions")
def predict_anomalies():
    # Example: anomaly detection for PLC temperature
    device = "plc"
    param = "temperature"
    data = history[device][param]

    if len(data) < 10:
        return jsonify({"message": "Not enough data yet", "anomalies": []})

    X = np.array(data).reshape(-1, 1)

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    preds = model.predict(X)

    anomalies = [
        {"index": i, "value": val, "status": "anomaly" if p == -1 else "normal"}
        for i, (val, p) in enumerate(zip(data, preds))
    ]

    return jsonify({
        "device": device,
        "param": param,
        "anomalies": anomalies
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
