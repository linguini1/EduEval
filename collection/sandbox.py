# Sandbox for cleaning up dataset
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from utils.process import analyze_sentiment

# Constants
MINIMUM_COMMENTS: int = 10


# Main
def main():
    # Read in dataset
    data = pd.read_parquet("data/pre_filtered_data.parquet.gzip")

    # Set display
    pd.set_option("display.max_colwidth", 150)

    # Remove duplicates
    data["comment"] = data["comment"].drop_duplicates()
    data = data.drop_duplicates(subset=['professor', 'course'], keep='first')

    # Any courses with not enough reviews are dropped
    for course in data["course"].unique():
        if len(data[data["course"] == course]) < MINIMUM_COMMENTS:
            data = data[data["course"] != course]

    # Do sentiment analysis
    data = analyze_sentiment(data)

    # Save the cleaned data
    data.to_parquet("data/analyzed_data.parquet.gzip", compression="gzip")


if __name__ == '__main__':
    main()
