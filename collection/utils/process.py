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
SENTIMENTS: dict[str, int] = {
    "negative": -1,
    "neutral": 0,
    "positive": 1,
}


def sentences(comment: str) -> list[str]:
    """Returns all the individual sentences in the list of comments."""
    return re.split(SENTENCE_SIGNIFIER, comment)[:-1]


def sentiment(text: str) -> int:
    """
    Returns an integer to represent the sentiment polarity of the text.
    1: positive
    0: neutral
    -1: negative
    """

    polarity = TextBlob(text).sentiment.polarity
    return min(SENTIMENTS.values(), key=lambda x: abs(x - polarity))


def analyze_sentiment(data: DataFrame) -> DataFrame:
    """
    Returns DataFrame with ratings split into individual sentences and assigned a sentiment score between -1 and 1.
    """

    data["comment"] = data["comment"].apply(sentences)  # Split comments into a list of sentences
    data = data.explode("comment")  # Give each sentence its own row
    data["comment"] = data["comment"].convert_dtypes(pd.StringDtype())  # Make comment column strings

    # Add column for sentiment
    data["sentiment"] = data["comment"].apply(
        lambda x: sentiment(str(x))  # 'Rounds' sentiment to a certain positive, negative or neutral value
    )
    data.astype({"sentiment": "float64"})  # Make sentiment column a float

    return data


# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def filter_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments

