from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

MQTT_BROKER = "mqtt-broker"
MQTT_PORT = 1883

# Store latest readings per device and parameter
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

# MQTT topics mapped to device parameters
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
    for topic in TOPICS.keys():
        client.subscribe(topic)
        print(f"[MQTT] Subscribed to {topic}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"[MQTT] Received on {topic}: {payload}")
    if topic in TOPICS:
        device, param = TOPICS[topic]
        latest_values[device][param] = payload

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
