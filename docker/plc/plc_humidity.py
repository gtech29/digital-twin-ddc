import asyncio
from gmqtt import Client as MQTTClient
import random

BROKER = 'mqtt-broker'
TOPIC = 'plc/humidity'

client = MQTTClient("plc-humidity-sim")

# Optional: handle incoming messages
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

async def publish_humidity():
    while True:
        humidity = round(random.uniform(30.0, 55.0), 2)  # Simulate realistic humidity
        client.publish(TOPIC, str(humidity))
        print(f"[PLC] Published humidity: {humidity}")
        await asyncio.sleep(5)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_humidity())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
