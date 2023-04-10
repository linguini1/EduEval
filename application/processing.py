# Performs backend processing for the uploaded data
__author__ = "Matteo Golin"

# Imports
import pandas as pd


# Functions
def create_professor_index(df: pd.DataFrame) -> dict[str, list[str]]:
    """Returns a dictionary which maps professor names to a list of courses they teach."""

    prof_index = {}
    professors = df["professor"].unique()

    for professor in professors:
        courses = df[df["professor"].str.contains(professor)]["course"].unique()
        prof_index[professor] = list(courses)

    return prof_index
