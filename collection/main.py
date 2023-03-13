# Contains the main logic for scraping data from RateMyProf
__author__ = "Matteo Golin"

# Imports
import warnings
import ratemyprofessor
from googletrans import Translator
from ratemyprofessor import School, Professor
from collection.utils.query import load_queries, Query
import pandas as pd
import os

# Constants
QUERY_FILE: str = "./queries.json"
EXPORT_FILE: str = "./ratings.csv"
COLUMNS: list[str] = ["school", "professor", "course", "comment"]


def scrape_queries(queries: list[Query], df: pd.DataFrame, translator: Translator, log: bool = True) -> None:
    """Adds the results of scraping the queries to a Pandas DataFrame."""

    for query in queries:
        school: School = ratemyprofessor.get_school_by_name(query.school)  # Get the school from RateMyProf

        # Get all the professors from RateMyProf
        for professor_name in query.professors:
            professor: Professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)

            # Get all the ratings for each course
            for course in professor.courses:

                # Print for each course to show progress
                if log:
                    print(f"{query.school}: {professor_name} - {course.name}")

                # Add each rating to the DataFrame
                for rating in professor.get_ratings(course_name=course.name):

                    comment = rating.comment
                    if translator.detect(comment).lang != 'en':  # Checks if the language is not English
                        comment = translator.translate(comment)  # Translates the rating to English

                    df.loc[df.shape[0]] = [school.name, professor.name, course.name, comment]


# Main
def main():

    # Load queries
    queries = load_queries(QUERY_FILE)

    # Set up dataset
    dataset = pd.DataFrame(columns=COLUMNS)

    # Creates translator instance
    translator = Translator()

    # Ignore BS4 warnings
    warnings.filterwarnings("ignore")

    # Get desired filename (only allows unique filenames)
    filename = input("File name for the CSV output: ")
    overwrite = 'n'
    while os.path.exists(f"./{filename}.csv") and overwrite == 'n':
        overwrite = input("Do you want to overwrite that file? (y/n): ")
        if overwrite == 'y':
            break
        filename = input("File name for the CSV output: ")

    # Complete all query searches
    try:
        scrape_queries(queries, dataset, translator, log=True)  # Show progress in console
    except (KeyboardInterrupt, ValueError):
        # If there is an error, save the current progress
        pass

    # Write the DataFrame to a CSV file
    dataset.to_csv(f"./{filename}.csv", index=False, encoding='utf-8')


if __name__ == "__main__":
    main()
