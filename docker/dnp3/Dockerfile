# Use a slim Python base image
FROM python:3.9-slim

# Set a working directory
WORKDIR /app

# Copy only the requirements file first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the publisher script into the container
COPY dnp3_publisher.py .

# Configure the entrypoint
CMD ["python", "dnp3_publisher.py"]
