#!/bin/sh

python3 plc_humidity.py &
python3 plc_setpoint.py &
python3 plc_fan_status.py &
python3 plc_temperature.py &

# keep container alive
tail -f /dev/null
