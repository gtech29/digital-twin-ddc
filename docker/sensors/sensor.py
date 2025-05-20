import asyncio
import random
from gmqtt import Client as MQTTClient

BROKER = 'mqtt-broker'
TOPIC = 'sensors/temperature'

client = MQTTClient("sensor-1")

async def main():
    await client.connect(BROKER)

    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        message = f"{temp}"
        print(f"Published: {message}°C")
        client.publish(TOPIC, message)
        await asyncio.sleep(0.5)

if __name__ == '__main__':
    asyncio.run(main())


    
