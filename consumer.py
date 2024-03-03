import pika
import json
import psycopg2


def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Message received!")

    update_query = f"""
UPDATE taxi_trip_aggregate
SET aggregated_total_amount = aggregated_total_amount + {message['total_amount']},
    aggregated_trip_distance = aggregated_trip_distance + {message['trip_distance']},
    aggregated_passenger_count = aggregated_passenger_count + {message['passenger_count']}
WHERE "VendorID" = {message['VendorID']}
"""
    try:
        cursor.execute(update_query)
        db_connection.commit()
        print(f"Updated the aggregate table with the new values from the message: {message}")
        print(f"Message processed successfully!")
    except Exception as error:
        print(f"Error processing the message: {error}")

if __name__ == '__main__':

    # Defining database connection parameters
    db_params = {
        "host": "localhost",
        "database": "taxi_aggregate",
        "user": "postgres",
        "password": "postgres",
        "port": "5433"
    }
    global cursor
    global db_connection
    try:
        # Establishing a connection to the database
        db_connection = psycopg2.connect(**db_params)
        # Creating a cursor object to interact with the database
        cursor = db_connection.cursor()
        # Performing database operations here...
    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to the database: {error}")


    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='trip_logs', exchange_type='direct', durable=True)

    result = channel.queue_declare('taxi_trip_records')
    queue_name = result.method.queue

    binding_key = 'public.taxi_trip_records'
    channel.queue_bind(exchange='trip_logs', queue=queue_name, routing_key=binding_key)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()