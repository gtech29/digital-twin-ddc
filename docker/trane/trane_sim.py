import paho.mqtt.client as mqtt
import time
import json
import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
CLIENT_ID = "trane_simulator"
TOPIC_BASE = "trane"

# Static device info
DEVICE_INFO = {
    "ip": "192.168.1.60",
    "model": "Trane Tracer SC+",
    "firmware": "v4.5.6",
}

def main():
    client = mqtt.Client(CLIENT_ID)
    client.connect(MQTT_BROKER, MQTT_PORT)

    while True:
        # Publish static device info
        client.publish(f"{TOPIC_BASE}/ip", DEVICE_INFO["ip"])
        client.publish(f"{TOPIC_BASE}/model", DEVICE_INFO["model"])
        client.publish(f"{TOPIC_BASE}/firmware", DEVICE_INFO["firmware"])

        # Simulate sensor data (example values)
        temperature = 70.0
        humidity = 50.0

        client.publish(f"{TOPIC_BASE}/temperature", temperature)
        client.publish(f"{TOPIC_BASE}/humidity", humidity)

        print(f"[Trane] Published data: temp={temperature}, humidity={humidity}")
        time.sleep(5)

if __name__ == "__main__":
    main()
