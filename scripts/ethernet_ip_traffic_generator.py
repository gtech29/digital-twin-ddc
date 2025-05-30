import cpppo
from cpppo.server.enip.client import connector
import time
import random

# Replace with your target device (e.g., a simulated PLC)
PLC_IP = "plc"  # hostname or IP of the EtherNet/IP target
PLC_PORT = 44818  # Standard EtherNet/IP port

# Example CIP tag path (make sure this exists on the target or mock it)
TAGS = [
    "@1/1/1",  # Class 1, Instance 1, Attribute 1
    "@4/100/3",  # Class 4, Instance 100, Attribute 3 (example)
]

# Open connection context to EtherNet/IP target
with connector(host=PLC_IP, port=PLC_PORT) as conn:
    print("[*] Connected to EtherNet/IP device")

    try:
        while True:
            tag = random.choice(TAGS)
            # Read
            print(f"[*] Reading tag {tag}")
            for values in conn.read(tag):
                print("[+] Read Result:", values)

            # Write (example writes value 42 to tag)
            print(f"[*] Writing 42 to {tag}")
            conn.write((tag, 42))

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")

    except Exception as e:
        print("[!] Error:", e)
