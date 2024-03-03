#Cleaned up version of data-loading.ipynb
import os
import time
import pandas as pd
from sqlalchemy import create_engine
import random


def main(file_name):
    tb = "taxi_trip_records"
    # Create SQL engine
    engine = create_engine(f'postgresql://postgres:postgres@localhost:5432/taxi_trip')

    df = pd.read_csv(file_name, nrows=10)
    df_iter = pd.read_csv(file_name, iterator=True, chunksize=1)

    df.head(0).to_sql(name=tb, con=engine, if_exists='replace')

    count = 0
    for batch_df in df_iter:
        count += 1

        print(f'Inserting rows {count}...')
        b_start = time.time()
        batch_df.to_sql(name=tb, con=engine, if_exists='append')
        b_end = time.time()
        print(f'Inserted! time taken {b_end-b_start:10.3f} seconds.\n')
        time.sleep(random.uniform(1, 5))

if __name__ == '__main__':
    t_start = time.time()
    file = f"{os.getcwd()}/taxi_trip_raw_records.csv"
    main(file)
    t_end = time.time()
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds.')