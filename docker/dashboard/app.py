from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt
import threading
import time

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883

# Store latest values including Jensys device
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
        "temperature": None,
    }
}

# Store historical values for temperature for each device
historical_data = {
    "plc": {"temperature": []},
    "dnp3": {"temperature": []},
    "sensor": {"temperature": []},
    "jensys": {"temperature": []},
    "trane": {"temperature": []},
}

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

        # Append to historical data if temperature
        if param == "temperature":
            timestamp = int(time.time())
            hist_list = historical_data.get(device, {}).get(param, [])
            hist_list.append({"timestamp": timestamp, "value": float(payload)})
            # Keep only last 100 entries to limit memory
            if len(hist_list) > 100:
                hist_list.pop(0)
            historical_data[device][param] = hist_list

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

@app.route("/api/historical_data")
def historical_data_api():
    device = request.args.get("device", "plc")
    param = request.args.get("param", "temperature")

    # Return data or empty list if not available
    data = historical_data.get(device, {}).get(param, [])
    # Convert timestamps to ISO 8601 for frontend convenience
    for entry in data:
        entry["time_iso"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(entry["timestamp"]))
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
