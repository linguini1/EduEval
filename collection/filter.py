# Performs standard filtering operations on the dataset
__author__ = "Matteo Golin"

# Imports
import pandas as pd
import collection.utils.process as filters

# Constants
FILENAME: str = "pre_filtered_data"


# Main
def main():

    # Read raw data
    data = pd.read_parquet("data/rawdata.parquet.gzip")

    # Perform filter
    data.dropna(inplace=True)
    data.drop_duplicates(inplace=True)
    data = filters.filter_by_length(data)
    data = filters.filter_empty_comments(data)
    data = filters.filter_not_english(data)

    # Save data
    data.to_parquet(f"data/{FILENAME}.parquet.gzip", compression="gzip")


if __name__ == "__main__":
    main()
