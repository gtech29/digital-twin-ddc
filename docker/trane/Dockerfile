FROM python:3.11-slim

WORKDIR /app

COPY trane_sim.py .

RUN pip install paho-mqtt==1.6.1

CMD ["python","-u", "trane_sim.py"]
