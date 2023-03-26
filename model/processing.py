# Pre- and post-processing for the model
__author__ = "Matteo Golin"

# Imports
from pandas import DataFrame
from collection.utils.process import SENTIMENTS


# Helper functions
def separate_comments(course_comments: DataFrame) -> dict[str, str]:
    """
    Returns a dictionary containing the sentiment name as a key, and the string of comments associated with the
    sentiment as a value.
    {
        "negative": "Some long string of negative comments.",
        ...
    }

    :param course_comments A DataFrame containing the comments for a specific course and each comment's associated
    sentimentality score:
    """

    # Collect categories
    categories = {}
    for sentiment in SENTIMENTS:
        categories[SENTIMENTS[sentiment]] = course_comments[course_comments["sentiment"] == sentiment]["comment"]
        categories[SENTIMENTS[sentiment]] = ". ".join(categories[SENTIMENTS[sentiment]])

    return categories
