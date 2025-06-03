FROM python:3.11-slim

WORKDIR /app

COPY jensys_sim.py .

RUN pip install paho-mqtt==1.6.1

CMD ["python","jensys_sim.py"]
