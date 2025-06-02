import time

IP_ADDRESS = "192.168.1.10"
MODEL_NUMBER = "PC8000"
FIRMWARE_VERSION = "1.0.0"

def main():
    print(f"Starting JENsys Controller Simulator")
    print(f"IP Address: {IP_ADDRESS}")
    print(f"Model Number: {MODEL_NUMBER}")
    print(f"Firmware Version: {FIRMWARE_VERSION}")

    while True:
        # Simulate publishing sensor data (just print for now)
        print("Publishing temperature: 72.5°F, humidity: 45.0%")
        time.sleep(5)

if __name__ == "__main__":
    main()
