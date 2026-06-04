import json, time, random, os
import paho.mqtt.client as mqtt  
from dotenv import load_dotenv

load_dotenv()


# Configuration des machines

MACHINES = {
    "moteurA": {"volt_nom": 230, "amp_nom": 14, "cosphi_nom": 0.92},
    "compresseurB": {"volt_nom": 400, "amp_nom": 10, "cosphi_nom": 0.85},
    "fourC": {"volt_nom": 230, "amp_nom": 8, "cosphi_nom": 0.9},
}

# Fonction pour simuler les données de consommation
def generer_mesure(machine, config):
# Bruit gaussien ±2%
  volt = config["volt_nom"] * random.gauss(1.0, 0.02)
  amp = config["amp_nom"] * random.gauss(1.0, 0.02)
  cosphi = config["cosphi_nom"] * random.gauss(1.0, 0.01)

# Pic aléatoire 1% du temps → surcharge
  if random.random() < 0.01:
    amp *= random.uniform(1.4, 1.8)

  # Mauvais cos φ 0.5% du temps
  if random.random() < 0.005:
    cosphi = random.uniform(0.6, 0.75)

  return {
    "ts": int(time.time()),
    "device": machine,
    "volt": round(volt, 2),
    "ampere": round(amp, 2),
    "cos_phi": round(min(cosphi, 1.0), 3),
  }

# Configuration MQTT
client = mqtt.Client()
mqtt_host = os.getenv("MOSQUITTO_HOST", "localhost").strip()
mqtt_port_value = os.getenv("MOSQUITTO_PORT", "").strip()
if not mqtt_host:
    raise ValueError("MOSQUITTO_HOST is not set or empty")
if mqtt_port_value:
    mqtt_port = int(mqtt_port_value)
else:
    mqtt_port = 1883
print(f"Connecting to MQTT broker at {mqtt_host}:{mqtt_port}")
client.connect(mqtt_host, mqtt_port)
client.loop_start()

# Boucle de simulation
while True:
    for machine, config in MACHINES.items():
        mesure = generer_mesure(machine, config)
        topic = f"/usine/ligneA/{machine}"
        client.publish(topic, json.dumps(mesure))
    time.sleep(1)  # Envoi toutes les secondes


