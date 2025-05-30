#!/bin/sh
python3 -u app.py &               # Temperature
python3 -u plc_humidity.py &      # Humidity
python3 -u plc_setpoint.py &      # Setpoint
python3 -u plc_fan_status.py      # Fan logic
