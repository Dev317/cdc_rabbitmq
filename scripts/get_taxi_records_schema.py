import os
import pandas as pd
import random
from sqlalchemy import create_engine

def main():
    raw_data_path = f"{os.getcwd()}/taxi_trip_records"
    random_pq_file = f"{raw_data_path}/{os.listdir(raw_data_path)[1]}"
    print(random_pq_file)
    table_name = 'taxi_trip.records'

    engine = create_engine('postgresql://postgres:postgres@localhost:5432/taxi_trip')

    df = pd.read_parquet(path=random_pq_file)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    ddl = pd.io.sql.get_schema(df, table_name, con=engine)
    # Write to sql file
    with open(f"{os.getcwd()}/init.sql", 'w') as file:
        file.write(ddl)

if __name__ == "__main__":
    main()