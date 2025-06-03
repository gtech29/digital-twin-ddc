import paho.mqtt.client as mqtt
import time
import json
import os
import sys

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
CLIENT_ID = "jensys_simulator"
TOPIC_BASE = "jensys"

# Static device info (hardcoded for now, can later come from env or config files)
DEVICE_INFO = {
    "ip": "192.168.1.50",
    "model": "JENsys JENE-PC8000",
    "firmware": "v1.2.3",
}

def main():
    client = mqtt.Client(CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT)
    print(f"[JENsys] Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    sys.stdout.flush()

    while True:
        # Publish static device info
        client.publish(f"{TOPIC_BASE}/ip", DEVICE_INFO["ip"])
        client.publish(f"{TOPIC_BASE}/model", DEVICE_INFO["model"])
        client.publish(f"{TOPIC_BASE}/firmware", DEVICE_INFO["firmware"])

        # Simulate sensor readings
        temperature = 72.5
        humidity = 45.3

        client.publish(f"{TOPIC_BASE}/temperature", temperature)
        client.publish(f"{TOPIC_BASE}/humidity", humidity)

        print(f"[JENsys] Published data: temp={temperature}, humidity={humidity}")
        sys.stdout.flush()

        time.sleep(5)

if __name__ == "__main__":
    main()
