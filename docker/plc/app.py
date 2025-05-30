import asyncio
from gmqtt import Client as MQTTClient
import random

BROKER = 'mqtt-broker'   # Docker service name
TOPIC = 'plc/temperature'

client = MQTTClient("plc-1")

# Callback: what to do when a message is received
def on_message(client, topic, payload, qos, properties):
    print(f"[PLC] Received message on {topic}: {payload.decode()}")

client.on_message = on_message

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
        temp = round(random.uniform(20.0, 30.0), 2)  # Simulate temperature
        client.publish(TOPIC, str(temp))
        print(f"[PLC] Published temperature: {temp}")
        await asyncio.sleep(2)  # Publish every 2 seconds

async def main():
    await connect_with_retry()
    client.subscribe(TOPIC)
    print(f"[PLC] Subscribed to topic: {TOPIC}")

    asyncio.create_task(publish_temperature())

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
