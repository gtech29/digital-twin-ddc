# /home/admin/Desktop/digital-twin-ddc/docker/plc/plc_humidity.py
import os
import asyncio
import random
from gmqtt import Client as MQTTClient
from collections import deque

BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
TOPIC = "plc/humidity"

client = MQTTClient("plc-humidity-sim")
connected_event = asyncio.Event()
message_buffer = deque(maxlen=1000)

def buffer_message(topic, payload):
    message_buffer.append((topic, payload))

async def flush_buffer():
    while message_buffer and connected_event.is_set():
        topic, payload = message_buffer.popleft()
        try:
            client.publish(topic, payload)
            print(f"[PLC] Published buffered message to {topic}: {payload}")
        except Exception as e:
            print(f"[PLC] Failed to publish buffered message: {e}")
            message_buffer.appendleft((topic, payload))
            break

def on_connect(client, flags, rc, properties):
    print(f"[PLC] Connected to MQTT broker at {BROKER}")
    connected_event.set()

def on_disconnect(client, packet, exc=None):
    print("[PLC] Disconnected from MQTT broker")
    connected_event.clear()
    asyncio.create_task(connect_with_retry())  # reconnect in background

client.on_connect = on_connect
client.on_disconnect = on_disconnect

async def connect_with_retry():
    while not connected_event.is_set():
        try:
            await client.connect(BROKER)
            await connected_event.wait()
            await flush_buffer()
        except Exception as e:
            print(f"[PLC] Connection failed: {e}")
            await asyncio.sleep(5)

async def publish_humidity():
    while True:
        humidity = round(random.uniform(30.0, 60.0), 1)
        if connected_event.is_set():
            try:
                client.publish(TOPIC, str(humidity))
                print(f"[PLC] Published humidity: {humidity}")
            except Exception as e:
                print(f"[PLC] Publish failed: {e}")
                buffer_message(TOPIC, str(humidity))
        else:
            buffer_message(TOPIC, str(humidity))
            print(f"[PLC] Buffered humidity: {humidity}")
        await asyncio.sleep(3)

async def main():
    asyncio.create_task(connect_with_retry())
    asyncio.create_task(publish_humidity())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
