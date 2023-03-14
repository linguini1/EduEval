# Module for processing scraped data
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from pandas import DataFrame, Series
import re
import functools
from typing import Callable, Iterable
from textblob import TextBlob

# Constants
MINIMUM_CHARS: int = 5
SENTENCE_SIGNIFIER: str = r"[\.][\s*]|[!][\s*]|[\?][\s*]"


def sentences(comment: str) -> list[str]:
    """Returns all the individual sentences in the list of comments."""
    return re.split(SENTENCE_SIGNIFIER, comment)[:-1]


def analyze_sentiment(data: DataFrame):
    """Groups ratings on a per-sentence basis into piles of positive or negative data."""

    data["comment"] = data["comment"].apply(sentences)  # Split comments into a list of sentences
    data = data.explode("comment")  # Give each sentence its own row
    data["comment"] = data["comment"].convert_dtypes(pd.StringDtype())  # Make comment column strings

    # Add column for sentiment
    data["sentiment"] = data["comment"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    data.astype({"sentiment": "float64"})  # Make sentiment column a float

    print(data.dtypes)


# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def filter_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments

