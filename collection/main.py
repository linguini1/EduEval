# Contains the main logic for scraping data from RateMyProf
__author__ = "Matteo Golin"

# Imports
import ratemyprofessor
from ratemyprofessor import School, Professor
from query import load_queries
import pandas as pd

# Constants
QUERY_FILE: str = "./queries.json"
EXPORT_FILE: str = "./ratings.csv"
COLUMNS: list[str] = ["school", "professor", "course", "comment"]
MINIMUM_CHARS: int = 5


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

    # Complete all query searches
    for query in queries:
        school: School = ratemyprofessor.get_school_by_name(query.school)  # Get the school from RateMyProf

        # Get all the professors from RateMyProf
        for professor_name in query.professors:
            professor: Professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)

            # Get all the ratings for each course
            for course in professor.courses:
                print(f"{query.school}: {professor_name} - {course.name}")  # Print for each course to show progress
                for rating in professor.get_ratings(course_name=course.name):
                    # Add each rating to the DataFrame
                    dataset = write_row([school.name, professor.name, course.name, rating.comment], dataset)

    # Remove bad data
    dataset = dataset[dataset["comment"].str.len() > MINIMUM_CHARS]  # Can't have too few characters
    dataset = dataset[dataset["comment"].str.startswith("No Comments") == False]  # Removes empty comments

    # Write the DataFrame to a CSV file
    dataset.to_csv(EXPORT_FILE)


if __name__ == "__main__":
    main()
