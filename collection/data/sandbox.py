# Sandbox for cleaning up dataset
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from collection.utils.process import analyze_sentiment

# Constants


# Main
def main():

    # Read in dataset
    data = pd.read_parquet("ratings.parquet.gzip")

    # Store courses for convenience of cleaner
    with open("courses.txt", 'w') as file:
        file.writelines([f"{course}\n" for course in data["course"].unique()])

    # Remove courses that don't make sense
    # Merge courses together if they are equivalent

    return  # Early return until all cleaning code is in place

    # Do sentiment analysis
    data = analyze_sentiment(data)

    # Save the cleaned data
    data.to_parquet("test_data.parquet.gzip", compression="gzip")


if __name__ == '__main__':
    main()
