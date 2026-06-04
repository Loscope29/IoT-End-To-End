import os

THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "1.3"))

SEUILS = {
  "moteurA": {"watt_max": 230 * 14 * 0.92},
  "compresseurB": {"watt_max": 400 * 32 * 0.88},
  "fourC": {"watt_max": 400 * 63 * 0.95},
}

def detecter(mesure):
  """Retourne une liste d'anomalies détectées"""
  anomalies = []
  device = mesure["device"]
  seuil = SEUILS.get(device, {})

  # Pic de consommation
  if mesure["watt"] > seuil.get("watt_max", 9999) * THRESHOLD:
    anomalies.append({
      "device": device, "type": "pic_conso",
      "valeur": mesure["watt"], "seuil": seuil["watt_max"] * THRESHOLD,
    })

  # Mauvais facteur de puissance
  if mesure["cos_phi"] < 0.85:
    anomalies.append({
      "device": device, "type": "cos_phi_bas",
      "valeur": mesure["cos_phi"], "seuil": 0.85,
    })

  return anomalies