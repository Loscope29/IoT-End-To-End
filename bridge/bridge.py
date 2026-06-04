import json
import os
import time
from kafka import KafkaProducer
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

MQTT_HOST = os.getenv("MOSQUITTO_HOST", "localhost").strip()
MQTT_PORT = int(os.getenv("MOSQUITTO_PORT", "1883").strip() or 1883)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "/usine/ligneA/#")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092").strip()
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "elec-raw").strip()

if not MQTT_HOST:
    raise ValueError("MOSQUITTO_HOST is not set or empty")
if not KAFKA_BROKER:
    raise ValueError("KAFKA_BROKER is not set or empty")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

print(f"Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
print(f"Forwarding MQTT topic {MQTT_TOPIC} to Kafka topic {KAFKA_TOPIC}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT bridge connected to broker")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to MQTT topic {MQTT_TOPIC}")
    else:
        raise RuntimeError(f"MQTT connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
    except Exception as exc:
        print(f"Failed to parse MQTT message on {msg.topic}: {exc}")
        return

    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
    print(f"Forwarded MQTT {msg.topic} to Kafka {KAFKA_TOPIC}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_HOST, MQTT_PORT)
mqtt_client.loop_forever()
