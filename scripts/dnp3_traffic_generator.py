from pydnp3 import opendnp3, openpal, asiopal, asiodnp3
import time
import logging

logging.basicConfig(level=logging.INFO)

# Callback class for printing received data
class SimpleApplication(opendnp3.IMasterApplication):
    def __init__(self):
        super().__init__()

class SimpleSOEHandler(opendnp3.ISOEHandler):
    def Process(self, info, values):
        print(f"[+] Received data: {values.Count()} objects")

# Create DNP3 manager
manager = asiodnp3.DNP3Manager(1)
manager.Start()

# Create TCP client channel (master to outstation)
channel = manager.AddTCPClient(
    name="client",
    levels=opendnp3.levels.NORMAL,
    retry=asiopal.ChannelRetry.Default(),
    host="outstation",   # Change to 'localhost' or container name
    local="0.0.0.0",
    port=20000,
    listener=asiodnp3.PrintingChannelListener().Create()
)

# Master stack config
config = asiodnp3.MasterStackConfig()
config.master.responseTimeout = openpal.TimeDuration().Seconds(5)
config.link.LocalAddr = 1
config.link.RemoteAddr = 10

# Create master application
master = channel.AddMaster(
    alias="master",
    soeHandler=SimpleSOEHandler(),
    application=SimpleApplication(),
    config=config
)

master.Enable()

try:
    while True:
        # Integrity Poll (all data)
        master.PerformIntegrityScan()
        print("[*] Sent integrity scan")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Interrupted by user")

finally:
    manager.Shutdown()
    print("[*] DNP3 traffic generator stopped")
