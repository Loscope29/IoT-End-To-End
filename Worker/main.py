import json, time
from kafka import KafkaConsumer
from src.calculs import enrichir
from src.anomalies import detecter
from src.writers import ecrire_influx, ecrire_alerte, init_db
from dotenv import load_dotenv

load_dotenv()
init_db() # crée la table alertes si elle n'existe pas

consumer = KafkaConsumer(
  "elec-raw",
  bootstrap_servers="kafka:9092",
  value_deserializer=lambda m: json.loads(m.decode()),
  auto_offset_reset="earliest",
)

print("⚙️ Worker démarré — en attente de messages Kafka...")

for msg in consumer:
  mesure = enrichir(msg.value)
  anomalies = detecter(mesure)
  ecrire_influx(mesure)
  for a in anomalies:
    ecrire_alerte(a)
    print(f"🚨 Anomalie : {a}")
