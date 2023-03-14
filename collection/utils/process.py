# Module for processing scraped data
__author__ = "Matteo Golin"

# Imports
from pandas import DataFrame
import functools
from typing import Callable
import re
from textblob import TextBlob

# Constants
MINIMUM_CHARS: int = 5
SENTENCE_SIGNIFIER: str = r"[\.][\s*]|[!][\s*]|[\?][\s*]"


def sentences(comments: list[str]) -> list[str]:
    """Returns all the individual sentences in the list of comments."""
    phrases = []
    for comment in comments:
        phrases.extend(re.split(SENTENCE_SIGNIFIER, comment)[:-1])
    return phrases


def analyze_sentiment(data: DataFrame):
    """Groups ratings on a per-sentence basis into piles of positive or negative data."""

    comments = data.groupby(
        ["school", "professor", "course"],
        group_keys=True
    ).apply(lambda x: list(x["comment"]))

    for school, professor, course in comments.index.values:
        course_comments = comments[school][professor][course]
        course_sentences = sentences(course_comments)
        break

# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def filter_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments

