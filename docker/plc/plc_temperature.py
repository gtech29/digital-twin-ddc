#!/usr/bin/env python3
import os
import asyncio
import random
from gmqtt import Client as MQTTClient

# Use the Docker service name or fallback to localhost
BROKER = os.getenv("MQTT_BROKER", "mqtt-broker")
TOPIC  = "plc/temperature"

# Give this publisher a distinct ID
client = MQTTClient("plc-temp-pub")

async def connect_with_retry():
    while True:
        try:
            await client.connect(BROKER)
            print(f"[PLC] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[PLC] Connection failed: {e}")
            await asyncio.sleep(5)

async def publish_temperature():
    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        client.publish(TOPIC, str(temp))
        print(f"[PLC] Published temperature: {temp}")
        await asyncio.sleep(2)

async def main():
    await connect_with_retry()
    # You don’t need to subscribe when you’re only publishing.
    asyncio.create_task(publish_temperature())
    # Keep the script alive
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
