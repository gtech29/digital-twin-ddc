import asyncio
import random
from gmqtt import Client as MQTTClient

BROKER = 'mqtt-broker'

TOPICS = {
    "temperature": "dnp3/temperature",
    "valve_position": "dnp3/valve_position",
    "alarm": "dnp3/alarm"
}

client = MQTTClient("dnp3-1")

async def connect_with_retry():
    while True:
        try:
            await client.connect(BROKER)
            print(f"[DNP3] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[DNP3] Connection failed: {e}")
            await asyncio.sleep(5)

async def publish_values():
    while True:
        temp = round(random.uniform(18.0, 28.0), 2)
        valve_pos = random.randint(0, 100)  # % open
        alarm = random.choice(["NORMAL", "ALARM"])

        client.publish(TOPICS["temperature"], str(temp))
        client.publish(TOPICS["valve_position"], str(valve_pos))
        client.publish(TOPICS["alarm"], alarm)

        print(f"[DNP3] Published temp:{temp}, valve:{valve_pos}%, alarm:{alarm}")
        await asyncio.sleep(5)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_values())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
