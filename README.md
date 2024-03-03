## High-level architecture
![image](https://github.com/Dev317/cdc_rabbitmq/assets/70529335/4a288fe5-9d04-4540-9256-5f42d2a57c41)

1. Change data capture (CDC) 
- Rely on Postgresql's WAL to register any changes to the tables that are being tracked
- Use wal2json plugin to read the changes in json format
- Create a decoder to parse the log changes and submit to a message broker (RabbitMQ)
2. Message exchange with RabbitMQ
- Use RabbitMQ to route the decoded log to the right queue for the right consumer
- RabbitMQ is using a pushing mechanism whereby messages are pushed to the consumer instead of having the consumer to poll for any incoming message
3. Aggregating result
- Consumer would receive the message and do necessary calculation to update the records in an aggregated database
- Note: There might be some blocking issues if the UPDATE statements in aggregated database are run concurrently

## How to stimulate
1. Spin up 2 PostgreSQL databases (`taxi_trip` and `taxi_aggregate`) and 1 RabbitMQ broker with `docker compose`:
  ```
  make build && make start 
  ```
2. Activate the python virtual environment
  ```
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```
3. Run the following script `ingest_taxi_records.py` to stimulate records being inserted:
  ```
  python3 scripts/ingest_taxi_records.py
  ```
4. Run both the following scripts to stimulate decoder and consumer:
  ```
  python3 decoder.py
  python3 consumer.py
  ```
  Pipeline flow:
  
  <img width="1015" alt="image" src="https://github.com/Dev317/cdc_rabbitmq/assets/70529335/a186611c-6ce8-4035-8664-d2a6135115d7">

  Aggregated records:
  
  <img width="660" alt="image" src="https://github.com/Dev317/cdc_rabbitmq/assets/70529335/2c1a6578-4fae-4e1c-a223-6de50f01eaa3">
