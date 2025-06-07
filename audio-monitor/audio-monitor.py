import subprocess
import numpy as np
import paho.mqtt.client as mqtt
import time
import json
import os

MQTT_BROKER = os.getenv("MQTT_BROKER", "core-mosquitto")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "homeassistant/audio/level")
ARECORD_DEVICE = os.getenv("ARECORD_DEVICE", "hw:1,0")
SAMPLE_DURATION = float(os.getenv("SAMPLE_DURATION", "0.1"))  # seconds

def get_audio_chunk():
    cmd = [
        "arecord",
        "-D", ARECORD_DEVICE,
        "-f", "S16_LE",
        "-c", "1",
        "-r", "16000",
        "-d", str(SAMPLE_DURATION),
        "-t", "raw"
    ]
    raw_data = subprocess.check_output(cmd)
    audio_data = np.frombuffer(raw_data, dtype=np.int16)
    return audio_data

def rms_db(audio_data):
    rms = np.sqrt(np.mean(audio_data**2))
    db = 20 * np.log10(rms / 32768 + 1e-6)
    return db

def main():
    client = mqtt.Client()
    client.connect(MQTT_BROKER)
    client.loop_start()

    print("Audio monitor started...")

    while True:
        try:
            audio_chunk = get_audio_chunk()
            level_db = rms_db(audio_chunk)
            payload = json.dumps({"level_db": round(level_db, 2)})
            client.publish(MQTT_TOPIC, payload)
            time.sleep(0.05)
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
