# Runs the language model
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from summarizer import Summarizer
from collection.utils.process import separate_comments, sentences
import warnings

# Constants
NUM_SENTENCES: int = 4


# Main
def main():

    # Suppress annoying warnings
    warnings.filterwarnings("ignore")

    data = pd.read_parquet("data/analyzed_data.parquet.gzip")  # Read data
    model = Summarizer()  # Create BERT extractive summarizer model

    # Group data in a way that makes searching through combinations more convenient
    grouped_data = data.groupby(["school", "professor", "course"], group_keys=True)
    combinations = list(grouped_data.groups.keys())  # Unique combos of school, prof and course
    grouped_data = grouped_data.apply(lambda x: x)  # Make DataFrame searchable

    with open("data/summaries.txt", 'w') as file:

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
                # Write to file
                file.write(f"{sentiment.title()} Summary:\n")
                print(f"{sentiment.title()} Summary:")

                for s in sentences(summary):
                    file.write(f"* {s.strip()}\n")
                    print(f"* {s}")
                file.write("\n")
                print()


if __name__ == '__main__':
    main()
