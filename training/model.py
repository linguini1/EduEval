# Runs the language model
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from summarizer import Summarizer
from collection.utils.process import SENTIMENTS
from nltk.tokenize import sent_tokenize
import warnings
import re

# Constants
NUM_SENTENCES: int = 4


# Helper functions
def separate_comments(course_comments: pd.DataFrame) -> dict[str, str]:
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


# Main
def main():

    # Suppress annoying warnings
    warnings.filterwarnings("ignore")

    data = pd.read_parquet("training/data/analyzed_data.parquet.gzip")  # Read data
    model = Summarizer()  # Create BERT extractive summarizer model

    # Group data in a way that makes searching through combinations more convenient
    grouped_data = data.groupby(["school", "professor", "course"], group_keys=True)
    combinations = list(grouped_data.groups.keys())  # Unique combos of school, prof and course
    grouped_data = grouped_data.apply(lambda x: x)  # Make DataFrame searchable

    with open("training/data/summaries.txt", 'w') as file:

        # Iterate through all unique combinations
        for school, professor, course in combinations:

            file.write(f"{school}: {professor}, {course}\n")
            print(f"{school}: {professor}, {course}")

            # Join the comments with their predicted sentiment
            comments = pd.concat(
                [grouped_data["comment"][school][professor][course],
                 grouped_data["sentiment"][school][professor][course]],
                axis=1
            )

            # Get sentiment based results
            sentimented_ratings = separate_comments(comments)

            # Make predictions
            for sentiment, ratings in sentimented_ratings.items():
                summary = model(ratings, num_sentences=NUM_SENTENCES)
                #summary = model(ratings, max_length=300, min_length=150)
                # Write to file
                file.write(f"{sentiment.title()} Summary:\n")
                print(f"{sentiment.title()} Summary:")
                print(summary)

                # for s in sent_tokenize(summary):
                #     s = re.sub(r'\.{2,}', '.', s)
                #     file.write(f"* {s}\n")
                #     print(f"* {s}")

                for s in summary.split(". "):
                    file.write(f"* {s.strip()}\n")
                    print(f"* {s}")
                file.write("\n")
                print()


if __name__ == '__main__':
    main()
