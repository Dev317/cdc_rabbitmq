FROM postgres

USER root

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=taxi_trip

RUN apt-get update && apt-get install -y \
    postgresql-16-wal2json

CMD ["postgres", "-c", "wal_level=logical", "-c", "max_replication_slots=10", "-c", "max_wal_senders=10"]
