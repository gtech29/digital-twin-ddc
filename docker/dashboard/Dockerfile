FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Install any additional packages not listed in requirements.txt (if needed)
# You can remove this block if all these packages are already in requirements.txt
RUN pip install --no-cache-dir \
    flask \
    flask-socketio \
    flask-cors \
    eventlet \
    paho-mqtt \
    requests \
    "python-socketio[asyncio,eventlet]>=5.8.0"

# Copy the rest of the source code
COPY . .

# Expose port (optional, but helpful for clarity and tooling)
EXPOSE 5000

# Run the Flask app
CMD ["python3", "app.py"]

