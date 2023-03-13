# Module for processing scraped data
__author__ = "Matteo Golin"

# Imports
from pandas import DataFrame
import functools
from typing import Callable

# Constants
MINIMUM_CHARS: int = 5


# Format functions
def jsonify(data: DataFrame) -> dict[str, str | dict]:
    """
    Returns the DataFrame as a hierarchical JSON structure.
    Example structure:
    "School": {
        "Professor":{
            "Course": [
                "A rating about this course.",
                ...
            ],
            ...
        },
        ...
    },
    ...
    """

    json_data = {}
    for school in data["school"].unique():
        school_data = data[data["school"] == school]  # Filtered by school
        json_data[school] = {}
        for professor in school_data["professor"].unique():
            professor_data = school_data[school_data["professor"] == professor]  # Filtered by prof
            json_data[school][professor] = {}
            for course in professor_data["course"].unique():
                course_data = professor_data[professor_data["course"] == course]  # Filtered by course
                json_data[school][professor][course] = []
                for rating in course_data["rating"]:
                    course.append(rating)

    return json_data


# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def remove_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments

