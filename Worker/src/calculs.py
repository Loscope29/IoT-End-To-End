def puissance_active(volt, ampere, cos_phi):
  """Puissance active en Watts : P = V × I × cos φ"""
  return round(volt * ampere * cos_phi, 2)

def energie_kwh(watt, delta_t_sec):
  """Énergie consommée en kWh sur delta_t secondes"""
  return round((watt * delta_t_sec) / 3_600_000, 6)

def enrichir(mesure):
  """Ajoute les métriques calculées à une mesure brute"""
  watt = puissance_active(
    mesure["volt"], mesure["ampere"], mesure["cos_phi"]
  )
  return {
    **mesure,
    "watt": watt,
    "kwh": energie_kwh(watt, 1),
  }