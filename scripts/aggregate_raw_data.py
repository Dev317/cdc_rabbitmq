import os
import pandas as pd

def main():
    raw_data_path = f"{os.getcwd()}/taxi_trip_records"

    # Get the list of files in the raw data directory
    files = os.listdir(raw_data_path)

    # Create an empty list to store the dataframes
    df = []

    # Loop through the files
    for file in files:
        # Check if the file is a CSV file
        if file.endswith('.parquet'):
            # Read the CSV file into a dataframe
            cur_df = pd.read_parquet(f"{raw_data_path}/{file}")

            # Append the dataframe to the list
            df.append(cur_df)

    # Concatenate the dataframes in the list
    df = pd.concat(df)

    # Set the path to the output file
    output_file = f"{os.getcwd()}/taxi_trip_raw_records.csv"

    # Write the dataframe to a CSV file
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    main()