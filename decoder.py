import os
import psycopg2
from psycopg2.extras import LogicalReplicationConnection
import json
import pika


def main():
    conn = psycopg2.connect(
        database="taxi_trip",
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432',
        connection_factory=LogicalReplicationConnection
    )

    cur = conn.cursor()
    options = {
        'include-timestamp': True,
        'add-tables': 'public.taxi_trip_records',
        'actions': 'insert',
        'pretty-print': True,
    }

    slot_name = 'taxi_trip_slot'

    try:
        cur.start_replication(slot_name=slot_name, decode=False, options=options)
    except psycopg2.ProgrammingError:
        cur.create_replication_slot(slot_name, output_plugin='wal2json')
        cur.start_replication(slot_name=slot_name, decode=False, options=options)

    class Decoder(object):
        def __init__(self):
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.exchange = 'trip_logs'
            self.exchange_type = 'direct'
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
            self.channel.queue_declare(queue='taxi_trip_records')
            self.channel.queue_bind(exchange=self.exchange, queue='taxi_trip_records', routing_key='public.taxi_trip_records')

        def __call__(self, msg):
            print("Original Message:\n",msg.payload)
            message = msg.payload
            formatted_message = format(message)

            if formatted_message is not None:
                for fm in formatted_message:
                    print(f"Formatted Message: {fm}")
                    routing_key = f"{fm['schema']}.{fm['table']}"
                    self.channel.basic_publish(exchange=self.exchange,
                                               routing_key=routing_key,
                                               body=json.dumps(fm['data']),
                                               properties=pika.BasicProperties(
                                                    delivery_mode = 2, # make message persistent
                                                ))
            msg.cursor.send_feedback(flush_lsn=msg.data_start)

    decoder = Decoder()

    def start_stream():
        cur.consume_stream(decoder)

    def format(msg):
        decoded_msg = json.loads(msg.decode())
        if len(decoded_msg["change"]) == 0:
            return None

        formatted_msg = []
        extracted_column_names = [
            "VendorID",
            "passenger_count",
            "trip_distance",
            "total_amount"
        ]

        for change in decoded_msg["change"]:
            if change["kind"] != "insert" \
                and change["schema"] != "public" \
                and change["table"] != "taxi_trip_records":
                continue

            idx_map = {}
            for idx, column in enumerate(change["columnnames"]):
                if column in extracted_column_names:
                    idx_map[column] = idx

            formatted_data = {
                "change_kind": change["kind"],
                "schema": change["schema"],
                "table": change["table"],
                "data":  {k: change["columnvalues"][v] for k, v in idx_map.items()}
            }

            formatted_msg.append(formatted_data)

        return formatted_msg

    try:
        start_stream()
    except Exception as e:
        print(e)
        decoder.connection.close()

if __name__ == '__main__':
    main()