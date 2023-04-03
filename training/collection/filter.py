# Performs standard filtering operations on the dataset
__author__ = "Matteo Golin"

# Imports
import pandas as pd
import utils.process as filters
import os 

# Constants
FILENAME: str = "pre_filtered_data"


# Main
def main():
    # Read raw data
    data = pd.read_parquet("training/data/rawdata.parquet.gzip")

    # Perform filter
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    data = filters.filter_by_length(data)
    data = filters.filter_empty_comments(data)
    data = filters.filter_not_english(data)

    # Save data
    data.to_parquet(f"training/data/{FILENAME}.parquet.gzip", compression="gzip")

    print(pd.read_parquet(f"training/data/{FILENAME}.parquet.gzip", engine='pyarrow'))


if __name__ == "__main__":
    main()
