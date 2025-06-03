#!/bin/sh

# Start each script in the background and redirect output to stdout
python3 plc_humidity.py &
python3 plc_setpoint.py &
python3 plc_fan_status.py &
python3 plc_temperature.py &

# Wait for all background jobs
wait
