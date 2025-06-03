# /home/admin/Desktop/digital-twin-ddc/docker/dnp3/dnp3_publisher.py

import asyncio
import random
import os
from gmqtt import Client as MQTTClient
from collections import deque

BROKER = os.getenv('MQTT_BROKER', 'mqtt-broker')

TOPICS = {
    "temperature": "dnp3/temperature",
    "valve_position": "dnp3/valve_position",
    "alarm": "dnp3/alarm"
}

client = MQTTClient("dnp3-1")
connected_event = asyncio.Event()
BUFFER_LIMIT = 1000
message_buffer = deque(maxlen=BUFFER_LIMIT)

# --- MQTT Lifecycle Events ---

def on_connect(client, flags, rc, properties):
    print("[DNP3] Connected to broker.")
    connected_event.set()


def on_disconnect(client, packet, exc=None):
    print("[DNP3] Disconnected from broker.")
    connected_event.clear()


client.on_connect = on_connect
client.on_disconnect = on_disconnect

# --- Connection Logic ---

async def connect_with_retry():
    while True:
        try:
            print(f"[DNP3] Attempting to connect to MQTT broker at {BROKER}...")
            await client.connect(BROKER)
            await connected_event.wait()
            print(f"[DNP3] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[DNP3] Connection failed: {e}")
            await asyncio.sleep(5)

# --- Buffer Publishing ---

def buffer_message(topic: str, payload: str):
    if len(message_buffer) >= BUFFER_LIMIT:
        print("[DNP3] Buffer full. Oldest message dropped.")
    message_buffer.append((topic, payload))

async def flush_buffer():
    while message_buffer:
        topic, payload = message_buffer.popleft()
        try:
            client.publish(topic, payload)
        except Exception as e:
            print(f"[DNP3] Buffered publish failed: {e}")
            message_buffer.appendleft((topic, payload))
            break

# --- Publishing Loop ---

async def publish_values():
    while True:
        temp = round(random.uniform(18.0, 28.0), 2)
        valve_pos = random.randint(0, 100)
        alarm = random.choice(["NORMAL", "ALARM"])

        print(f"[DNP3] Generated... temp: {temp}, valve: {valve_pos}%, alarm: {alarm}")

        buffer_message(TOPICS["temperature"], str(temp))
        buffer_message(TOPICS["valve_position"], str(valve_pos))
        buffer_message(TOPICS["alarm"], alarm)

        if connected_event.is_set():
            await flush_buffer()

        await asyncio.sleep(5)

# --- Main Entrypoint ---

async def main():
    await connect_with_retry()
    await publish_values()

if __name__ == '__main__':
    asyncio.run(main())