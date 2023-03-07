# Contains the main logic for scraping data from RateMyProf
__author__ = "Matteo Golin"

# Imports
import ratemyprofessor
from ratemyprofessor import School, Professor
from query import load_queries
import pandas as pd
import logging

# Constants
QUERY_FILE: str = "./queries.json"
COLUMNS: list[str] = ["school", "professor", "course", "comment"]


# Helper functions
def write_row(row: list[str], df: pd.DataFrame) -> pd.DataFrame:
    """Returns the DataFrame with the given row appended to it."""

    # Label the data for Pandas
    new_row = {}
    for label, value in zip(COLUMNS, row):
        new_row[label] = value

    # Add to the dataframe
    new_row = pd.Series(new_row).to_frame().T
    return pd.concat([df, new_row], ignore_index=True)


# Main
def main():

    # Load queries
    queries = load_queries(QUERY_FILE)

    # Set up dataset
    dataset = pd.DataFrame(columns=COLUMNS)

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Complete all query searches
    for query in queries:
        school: School = ratemyprofessor.get_school_by_name(query.school)  # Get the school from RateMyProf

        # Get all the professors from RateMyProf
        for professor_name in query.professors:
            professor: Professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
            logging.info(f"{query.school}: {professor_name}")

            # Get all the ratings for each course
            for course in professor.courses:
                for rating in professor.get_ratings(course_name=course.name):
                    dataset = write_row([school.name, professor.name, course.name, rating.comment], dataset)

    print(dataset)


if __name__ == "__main__":
    main()
