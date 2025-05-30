import asyncio
from gmqtt import Client as MQTTClient

BROKER = 'mqtt-broker'
TOPIC_TEMP = 'plc/temperature'
TOPIC_SETPOINT = 'plc/setpoint'
TOPIC_FAN = 'plc/fan_status'

client = MQTTClient("plc-fan-status")

latest_temp = None
latest_setpoint = None

def decide_fan_status():
    if latest_temp is None or latest_setpoint is None:
        return None
    try:
        temp = float(latest_temp)
        setpoint = float(latest_setpoint)
        return "ON" if temp > setpoint else "OFF"
    except ValueError:
        return None

def on_message(client, topic, payload, qos, properties):
    global latest_temp, latest_setpoint
    val = payload.decode()

    if topic == TOPIC_TEMP:
        latest_temp = val
    elif topic == TOPIC_SETPOINT:
        latest_setpoint = val

    status = decide_fan_status()
    if status:
        client.publish(TOPIC_FAN, status)
        print(f"[PLC] Published fan status: {status}")

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

async def main():
    await connect_with_retry()
    client.subscribe(TOPIC_TEMP)
    client.subscribe(TOPIC_SETPOINT)
    print(f"[PLC] Subscribed to {TOPIC_TEMP} and {TOPIC_SETPOINT}")

    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
