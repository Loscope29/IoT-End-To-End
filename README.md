# IoT-End-To-End

Monitoring from a simulated IoT sensor through MQTT, Kafka, InfluxDB and PostgreSQL.

## Run the stack

From the project root:

```powershell
docker compose up -d bridge worker simulator
```

## Verify end-to-end pipeline

To confirm recent data in InfluxDB from the worker container:

```powershell
cd "c:\Users\DELL\Desktop\Projet\IoT Monitoring\IoT-End-To-End"
& docker exec iot-end-to-end-worker-1 python -c "import os; from influxdb_client import InfluxDBClient; token=os.getenv('INFLUXDB_TOKEN'); org=os.getenv('INFLUXDB_ORG'); bucket=os.getenv('INFLUXDB_BUCKET'); client=InfluxDBClient(url='http://influxdb:8086', token=token, org=org); q='from(bucket:' + chr(34) + bucket + chr(34) + ') |> range(start: -5m) |> limit(n:5)'; res=client.query_api().query(org=org, query=q); print('tables', len(res)); [print({k:(v.isoformat() if hasattr(v,'isoformat') else v) for k,v in record.values.items()}) for table in res for record in table.records]"
```

This command prints recent InfluxDB measurement points from bucket `electricite`.
