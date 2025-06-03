#!/usr/bin/env python3
import os
import asyncio
import random
from gmqtt import Client as MQTTClient
from collections import deque

BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
TOPIC  = "plc/temperature"

client = MQTTClient("plc-temp-pub")
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
            break  # exit the loop to avoid flooding if broker is still down

def on_connect(client, flags, rc, properties):
    print(f"[PLC] Connected to MQTT broker at {BROKER}")
    connected_event.set()

def on_disconnect(client, packet, exc=None):
    print("[PLC] Disconnected from MQTT broker")
    connected_event.clear()

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

async def publish_temperature():
    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        if connected_event.is_set():
            try:
                client.publish(TOPIC, str(temp))
                print(f"[PLC] Published temperature: {temp}")
            except Exception as e:
                print(f"[PLC] Publish error: {e}")
                buffer_message(TOPIC, str(temp))
        else:
            buffer_message(TOPIC, str(temp))
            print(f"[PLC] Buffered temperature: {temp}")
        await asyncio.sleep(2)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_temperature())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
