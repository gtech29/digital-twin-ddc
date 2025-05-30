FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir gmqtt

CMD ["python3", "dnp3_publisher.py"]

