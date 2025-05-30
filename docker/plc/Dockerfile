FROM python:3.11-slim

WORKDIR /app

# Copy and install only the MQTT library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all publisher scripts and the start-up helper
COPY . .

# Make sure start.sh is executable
RUN chmod +x start.sh

# Launch all PLC publishers in parallel
CMD ["./start.sh"]
