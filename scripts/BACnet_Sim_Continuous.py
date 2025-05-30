import logging
import time
from bacpypes.core import run, stop
from bacpypes.app import BIPSimpleApplication
from bacpypes.local.device import LocalDeviceObject
from bacpypes.pdu import Address
from bacpypes.apdu import ReadPropertyRequest, WritePropertyRequest

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define a BACnet device object
local_device = LocalDeviceObject(
    objectName="HVACController",
    objectIdentifier=1001,
    maxApduLengthAccepted=1024,
    segmentationSupported="segmentedBoth",
    vendorIdentifier=15
)

# Define a BACnet application
application = BIPSimpleApplication(local_device, Address("192.168.1.100"))

# Function to read a property from a device
def read_property(device_address, object_identifier, property_identifier):
    request = ReadPropertyRequest(
        objectIdentifier=object_identifier,
        propertyIdentifier=property_identifier
    )
    request.pduDestination = Address(device_address)
    application.request(request)

# Function to write a property to a device
def write_property(device_address, object_identifier, property_identifier, value):
    request = WritePropertyRequest(
        objectIdentifier=object_identifier,
        propertyIdentifier=property_identifier,
        propertyValue=value
    )
    request.pduDestination = Address(device_address)
    application.request(request)

# Run the BACnet application
if __name__ == "__main__":
    # Start the BACnet application
    run()

    # Define the duration for sending packets (e.g., 60 seconds)
    duration = 60
    start_time = time.time()

    # Loop to send packets for the specified duration
    while time.time() - start_time < duration:
        # Example: Read temperature from a thermostat
        read_property("192.168.1.101", ("analogInput", 1), "presentValue")

        # Example: Set temperature setpoint on a thermostat
        write_property("192.168.1.101", ("analogOutput", 1), "presentValue", 22.0)

        # Example: Read airflow from an air handling unit
        read_property("192.168.1.102", ("analogInput", 2), "presentValue")

        # Example: Set airflow setpoint on an air handling unit
        write_property("192.168.1.102", ("analogOutput", 2), "presentValue", 500.0)

        # Example: Read chiller status
        read_property("192.168.1.103", ("binaryInput", 3), "presentValue")

        # Example: Start chiller
        write_property("192.168.1.103", ("binaryOutput", 3), "presentValue", True)

        # Sleep for a short interval to avoid overwhelming the network
        time.sleep(1)

    # Stop the BACnet application
    stop()