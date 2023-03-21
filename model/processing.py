# Pre and post-processing for the model
__author__ = "Matteo Golin"

# Imports
from pandas import DataFrame

# Constants


# Helper functions
def separate_comments(course_comments: DataFrame) -> tuple[str, str, str]:
    """
    Returns three strings of comments, separated by sentimentality. Strings are returned in the order of positive,
    neutral and negative.

    :param course_comments A DataFrame containing the comments for a specific course and each comment's associated
    sentimentality score:
    """

    positive = course_comments[course_comments["sentimentality"] == 1]["comment"]
    neutral = course_comments[course_comments["sentimentality"] == 0]["comment"]
    negative = course_comments[course_comments["sentimentality"] == -1]["comment"]

    return " ".join(positive), " ".join(neutral), " ".join(negative)
