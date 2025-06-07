FROM python:3.11-slim

RUN apt-get update && apt-get install -y alsa-utils && rm -rf /var/lib/apt/lists/*

RUN pip install paho-mqtt numpy

COPY audio_monitor.py /audio_monitor.py

CMD ["python", "/audio_monitor.py"]
