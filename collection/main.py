# Contains the main logic for scraping data from RateMyProf
__author__ = "Matteo Golin"

# Imports
import warnings
import ratemyprofessor
from ratemyprofessor import School, Professor
from utils.query import load_queries, Query
from utils.process import filter_empty_comments, filter_by_length, filter_not_english, COLUMNS, define_types
import pandas as pd
import os

# Constants
QUERY_FILE: str = "./queries.json"


def scrape_queries(queries: list[Query], df: pd.DataFrame, log: bool = True) -> None:
    """Adds the results of scraping the queries to a Pandas DataFrame."""

    for query in queries:
        school: School = ratemyprofessor.get_school_by_name(query.school)  # Get the school from RateMyProf

        # Get all the professors from RateMyProf
        for professor_name in query.professors:

            if professor_name in df["professor"].values:
                print(f"{professor_name} already scraped, continuing...")
                continue

            professor: Professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
            print(f"{query.school}: {professor_name}")

            # Add each rating to the DataFrame
            for rating in professor.get_ratings():
                df.loc[df.shape[0]] = [school.name, professor.name, rating.class_name, rating.comment, rating.date]


# Main
def main():

    # Load queries
    queries = load_queries(QUERY_FILE)

    # Ignore BS4 warnings
    warnings.filterwarnings("ignore")

    # Get desired filename (only allows unique filenames)
    filename = input("File name for the output: ")
    overwrite = 'n'
    while os.path.exists(f"./data/{filename}.parquet.gzip") and overwrite == 'n':
        overwrite = input("Do you want to overwrite that file? (y/n): ")
        if overwrite == 'y':
            break
        filename = input("File name for the output: ")

    # Set up dataset
    if os.path.exists(f"data/{filename}.parquet.gzip"):
        dataset = pd.read_parquet(f"data/{filename}.parquet.gzip")  # Start from last point
    else:
        dataset = pd.DataFrame(columns=list(COLUMNS.keys()))

    # Complete all query searches
    try:
        scrape_queries(queries, dataset, log=True)  # Show progress in console
    except (KeyboardInterrupt, AttributeError):
        # If there is an error, save the current progress
        print("Saving progress...")

    define_types(dataset)  # Specific datatypes

    # Save
    dataset.to_parquet(f"./data/{filename}.parquet.gzip", compression="gzip")


if __name__ == "__main__":
    main()
