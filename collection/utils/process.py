# Module for processing scraped data
__author__ = "Matteo Golin"

# Imports
from pandas import DataFrame
import functools
from typing import Callable

# Constants
MINIMUM_CHARS: int = 5


# Filter functions
def compose(*functions) -> Callable:
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def filter_by_length(data: DataFrame, minimum_chars: int = MINIMUM_CHARS) -> DataFrame:
    """Returns the DataFrame without comments that are shorter than the minimum character requirement."""
    return data[data["comment"].str.len() > minimum_chars]  # Can't have too few characters


def filter_empty_comments(data: DataFrame) -> DataFrame:
    """Returns the DataFrame with no empty comments."""
    return data[data["comment"].str.startswith("No Comments") == False]  # Removes empty comments

