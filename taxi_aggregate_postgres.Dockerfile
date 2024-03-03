FROM postgres

USER root

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=taxi_aggregate
COPY init.sql /docker-entrypoint-initdb.d/

CMD ["postgres", "-c", "wal_level=logical", "-c", "max_replication_slots=10", "-c", "max_wal_senders=10"]
