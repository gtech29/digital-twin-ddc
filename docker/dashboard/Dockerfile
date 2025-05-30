FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install only essential dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir \
        flask \
        flask-socketio \
        flask-cors \
        eventlet \
        paho-mqtt \
        requests \
        "python-socketio[asyncio,eventlet]>=5.8.0"

# Copy app code
COPY . .

# Run the dashboard
CMD ["python3", "app.py"]
