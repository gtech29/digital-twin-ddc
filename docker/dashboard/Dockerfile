FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
        gcc musl-dev linux-headers libffi-dev libressl-dev \
    && pip install --no-cache-dir --upgrade pip

# Copy requirements and install packages
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

# Clean up build deps
RUN apk del .build-deps

# Environment variables
ENV PYTHONIOENCODING=utf-8
ENV PYTHONPATH=/app

# Copy the rest of the code
COPY . .

# Run the app
CMD ["python3", "app.py", "-u"]
