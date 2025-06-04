import paho.mqtt.client as mqtt
import time
import os
import socket

MQTT_BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
CLIENT_ID = "trane_simulator"
TOPIC_BASE = "trane"

DEVICE_INFO = {
    "ip": "192.168.1.60",
    "model": "Trane Tracer SC+",
    "firmware": "v4.5.6",
}

def wait_for_broker(host, port, retries=10, delay=3):
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=3):
                print(f"[Trane] MQTT broker {host}:{port} is reachable.")
                return
        except OSError:
            print(f"[Trane] Waiting for MQTT broker ({i+1}/{retries})...")
            time.sleep(delay)
    raise ConnectionError(f"[Trane] MQTT broker {host}:{port} not reachable after {retries} attempts.")

def on_connect(client, userdata, flags, rc):
    print(f"[Trane MQTT] Connected with result code {rc}")
    client.subscribe(f"{TOPIC_BASE}/#")

def on_message(client, userdata, msg):
    print(f"[Trane MQTT] Echo: {msg.topic} => {msg.payload.decode()}")

def main():
    wait_for_broker(MQTT_BROKER, MQTT_PORT)

    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    while True:
        client.publish(f"{TOPIC_BASE}/ip", DEVICE_INFO["ip"])
        client.publish(f"{TOPIC_BASE}/model", DEVICE_INFO["model"])
        client.publish(f"{TOPIC_BASE}/firmware", DEVICE_INFO["firmware"])

        temperature = 70.0
        humidity = 50.0
        client.publish(f"{TOPIC_BASE}/temperature", temperature)
        client.publish(f"{TOPIC_BASE}/humidity", humidity)

        print(f"[Trane] Published data: temp={temperature}, humidity={humidity}")
        time.sleep(5)

if __name__ == "__main__":
    main()
