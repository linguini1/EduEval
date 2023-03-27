# Module for processing scraped data
__author__ = "Matteo Golin"

# Imports
import pandas as pd
import langdetect
from pandas import DataFrame
import re
import functools
from typing import Callable
from textblob import TextBlob
from googletrans import Translator

# Constants
COLUMNS: dict[str, str | type] = {
    "school": "category",
    "professor": "category",
    "course": "category",
    "comment": pd.StringDtype(),
    "date": "datetime64[ns]"
}
MINIMUM_CHARS: int = 5
SENTENCE_SIGNIFIER: str = r"[\.][\s*]|[!][\s*]|[\?][\s*]"
SENTIMENTS: dict[int, str] = {
    -1: "negative",
    1: "positive",
}


def _sentences(comment: str) -> list[str]:
    """Returns all the individual sentences in the list of comments."""
    return re.split(SENTENCE_SIGNIFIER, comment)[:-1]  # TODO prevent splits on periods such as Prof. John Doe


def _sentiment(text: str) -> int:
    """
    Returns an integer to represent the sentiment polarity of the text.
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity >= 0:  # Positive
        return 1
    else:
        return -1


def analyze_sentiment(data: DataFrame) -> DataFrame:
    """
    Returns DataFrame with ratings split into individual sentences and assigned a sentiment score between -1 and 1.
    """

    data["comment"] = data["comment"].apply(_sentences)  # Split comments into a list of sentences
    data = data.explode("comment")  # Give each sentence its own row
    data.reset_index(inplace=True)  # Re-index
    data["comment"] = data["comment"].convert_dtypes(pd.StringDtype())  # Make comment column strings
    data = data[data["comment"].str.startswith("<NA>") == False]  # Filter out artifacts from the split

    # Add column for sentiment
    data["sentiment"] = data["comment"].apply(
        lambda x: _sentiment(str(x))  # 'Rounds' sentiment to a definite +ve, -ve or neutral value
    )
    data.astype({"sentiment": int})  # Make sentiment column integers

    return data


def define_types(data: DataFrame) -> None:
    """Gives columns of the DataFrame the correct types."""

    for column, dtype in COLUMNS.items():
        data[column] = data[column].astype(dtype)


# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def filter_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments


def filter_not_english(data: DataFrame) -> DataFrame:
    """Translates any non-english comments in the DataFrame."""

    translator = Translator()  # Create translator instance
    langdetect.DetectorFactory.seed = 0

    def translate_comment(comment: str) -> str:
        """Returns the translated comment if it is not English, otherwise returns the original."""

        if langdetect.detect(comment) == "en":
            return comment
        return translator.translate(comment).text

    data["comment"] = data["comment"].apply(translate_comment)
    return data

