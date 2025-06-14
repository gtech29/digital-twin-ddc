import asyncio
import random
import os
import traceback
from gmqtt import Client as MQTTClient

# Get MQTT broker hostname from env var or fallback to default
BROKER = os.getenv('MQTT_BROKER', 'mqtt-broker')

TOPICS = {
    "temperature": "sensor/temperature",
    "humidity": "sensor/humidity"
}

# Create an MQTT client instance
client = MQTTClient("sensor-1")

async def connect_with_retry():
    while True:
        try:
            await client.connect(BROKER)
            print(f"[Sensor] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[Sensor] Connection failed: {e}")
            traceback.print_exc()
            await asyncio.sleep(5)

async def publish_values():
    while True:
        temp = round(random.uniform(19.0, 29.0), 2)
        humidity = round(random.uniform(35.0, 65.0), 2)

        client.publish(TOPICS["temperature"], str(temp))
        client.publish(TOPICS["humidity"], str(humidity))

        print(f"[Sensor] Published temp: {temp}, humidity: {humidity}")
        await asyncio.sleep(5)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_values())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
