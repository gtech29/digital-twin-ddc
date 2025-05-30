import asyncio
import random
from gmqtt import Client as MQTTClient

BROKER = 'mqtt-broker'

TOPICS = {
    "temperature": "plc/temperature",
    "setpoint": "plc/setpoint",
    "humidity": "plc/humidity",
    "fan_status": "plc/fan_status"
}

client = MQTTClient("plc-1")

async def connect_with_retry():
    while True:
        try:
            await client.connect(BROKER)
            print(f"[PLC] Connected to MQTT broker at {BROKER}")
            break
        except Exception as e:
            print(f"[PLC] Connection failed: {e}")
            await asyncio.sleep(5)

async def publish_values():
    while True:
        temp = round(random.uniform(20.0, 30.0), 2)
        setpoint = round(random.uniform(21.0, 25.0), 2)
        humidity = round(random.uniform(30.0, 60.0), 2)
        fan_status = random.choice(["ON", "OFF"])

        client.publish(TOPICS["temperature"], str(temp))
        client.publish(TOPICS["setpoint"], str(setpoint))
        client.publish(TOPICS["humidity"], str(humidity))
        client.publish(TOPICS["fan_status"], fan_status)

        print(f"[PLC] Published temp:{temp}, setpoint:{setpoint}, humidity:{humidity}, fan:{fan_status}")
        await asyncio.sleep(5)

async def main():
    await connect_with_retry()
    asyncio.create_task(publish_values())
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
