import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import psycopg2, datetime

# ── InfluxDB
influx = InfluxDBClient(
  url="http://influxdb:8086",
  token=os.getenv("INFLUXDB_TOKEN"),
  org=os.getenv("INFLUXDB_ORG"),
)
write_api = influx.write_api(write_options=SYNCHRONOUS)

def ecrire_influx(mesure):
  point = (
    Point("capteur")
    .tag("device", mesure["device"])
    .field("watt", mesure["watt"])
    .field("kwh", mesure["kwh"])
    .field("volt", mesure["volt"])
    .field("ampere", mesure["ampere"])
    .field("cos_phi", mesure["cos_phi"])
  )
  write_api.write(bucket=os.getenv("INFLUXDB_BUCKET"), record=point)

# ── PostgreSQL
pg = psycopg2.connect(
  host="postgres", dbname="iot_elec",
  user="admin", password="password123"
)
pg.autocommit = True

def init_db():
  with pg.cursor() as cur:
    cur.execute("""
      CREATE TABLE IF NOT EXISTS alertes (
        id SERIAL PRIMARY KEY,
        ts TIMESTAMPTZ DEFAULT NOW(),
        device VARCHAR(50),
        type VARCHAR(50),
        valeur FLOAT,
        seuil FLOAT
      );
    """)

def ecrire_alerte(anomalie):
  with pg.cursor() as cur:
    cur.execute(
      "INSERT INTO alertes (device,type,valeur,seuil) VALUES (%s,%s,%s,%s)",
      (anomalie["device"], anomalie["type"], anomalie["valeur"], anomalie["seuil"])
    )