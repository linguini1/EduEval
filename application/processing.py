# Performs backend processing for the uploaded data
__author__ = "Matteo Golin"

# Imports
import nltk
import pandas as pd
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
from summarizer import Summarizer

# Constants
SENTIMENTS: dict[int, str] = {
    -1: "negative",
    1: "positive",
}
NUM_SENTENCES: int = 7
Feedback = dict[str, dict[str, dict[str, str]]]


# Setup
nltk.download("punkt")


# Functions
def create_professor_index(df: pd.DataFrame) -> dict[str, list[str]]:
    """Returns a dictionary which maps professor names to a list of courses they teach."""

    prof_index = {}
    professors = df["professor"].unique()

    for professor in professors:
        courses = df[df["professor"].str.contains(professor)]["course"].unique()
        prof_index[professor] = list(courses)

    return prof_index


def sentences(comment: str) -> list[str]:
    """Returns all the individual sentences in the list of comments."""
    separated_sentences = sent_tokenize(comment)
    return separated_sentences


def _sentiment(text: str) -> int:
    """
    Returns an integer to represent the sentiment polarity of the text.
    """

    polarity = TextBlob(text).sentiment.polarity

    if polarity >= 0:  # Positive
        return 1
    else:
        return -1


def analyze_sentiment(data: pd.DataFrame) -> pd.DataFrame:
    """
    Returns DataFrame with ratings split into individual sentences and assigned a sentiment score between -1 and 1.
    """

    data["comment"] = data["comment"].apply(sentences)  # Split comments into a list of sentences
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


def _separate_comments(course_comments: pd.DataFrame) -> dict[str, str]:
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
        categories[SENTIMENTS[sentiment]] = " ".join(categories[SENTIMENTS[sentiment]])

    return categories


def create_feedback_listing(grouped_data: pd.DataFrame, combinations: list) -> Feedback:
    """Creates feedback summaries for all the comments in the dataframe."""

    feedback = dict()
    model = Summarizer()

    for professor, course in combinations:

        # Storage for feedback summaries
        feedback[professor] = dict()
        feedback[professor][course] = dict()

        # Zip comments together with their sentiments
        comments = pd.concat([
            grouped_data["comment"][professor][course],
            grouped_data["sentiment"][professor][course]
        ], axis=1)
        sentimented_comments = _separate_comments(comments)

        # Create summaries
        for sentiment, ratings in sentimented_comments.items():
            summary = model(ratings, num_sentences=NUM_SENTENCES)
            feedback[professor][course][sentiment] = summary

    return feedback