import asyncio
from gmqtt import Client as MQTTClient
import random

BROKER = 'mqtt-broker'
TOPIC = 'plc/setpoint'

client = MQTTClient("plc-setpoint-sim")

async def connect_with_retry():
    while True:
        try:
            await client.connect(BROKER)
            print(f"[PLC] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[PLC] Connection failed: {e}")
            await asyncio.sleep(5)

async def publish_setpoint():
    while True:
        setpoint = round(random.uniform(21.0, 23.0), 2)  # Simulated target temp
        client.publish(TOPIC, str(setpoint))
        print(f"[PLC] Published setpoint: {setpoint}")
        await asyncio.sleep(10)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_setpoint())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
