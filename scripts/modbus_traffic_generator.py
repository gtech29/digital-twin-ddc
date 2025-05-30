from pymodbus.client import ModbusTcpClient
import time
import random

MODBUS_SERVER_HOST = "plc"     # or "localhost" if running locally
MODBUS_SERVER_PORT = 502       # Default Modbus TCP port

client = ModbusTcpClient(MODBUS_SERVER_HOST, port=MODBUS_SERVER_PORT)

if client.connect():
    print("[*] Connected to Modbus server")

    try:
        while True:
            # Read Coils (example: 0-9)
            rr = client.read_coils(0, 10, unit=1)
            if rr.isError():
                print("[!] Read Coils failed:", rr)
            else:
                print("[+] Read Coils:", rr.bits)

            # Write Single Coil (toggle random)
            coil_address = random.randint(0, 9)
            coil_value = random.choice([True, False])
            wr = client.write_coil(coil_address, coil_value, unit=1)
            print(f"[+] Write Coil at {coil_address} to {coil_value}")

            # Delay to simulate traffic interval
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

    finally:
        client.close()
        print("[*] Disconnected from Modbus server")

else:
    print("[!] Could not connect to Modbus server")
