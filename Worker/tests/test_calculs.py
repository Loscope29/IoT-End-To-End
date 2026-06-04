from src.calculs import puissance_active, energie_kwh, enrichir

def test_puissance_active():
  assert puissance_active(230, 10, 1.0) == 2300.0
  assert puissance_active(400, 32, 0.88) == 11264.0

def test_energie_kwh():
  result = energie_kwh(3600, 1) # 3600W pendant 1s
  assert result == 0.001 # = 0.001 kWh

def test_enrichir():
  mesure = {"device": "moteurA", "volt": 230, "ampere": 10, "cos_phi": 1.0, "ts": 0}
  result = enrichir(mesure)
  assert result["watt"] == 2300.0
  assert "kwh" in result