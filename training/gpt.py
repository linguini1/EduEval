# Contains summarization logic using OpenAI API for comparison with BERT Extractive Summary model
__author__ = "Matteo Golin"

# Imports
import pandas as pd
import openai
from openai.error import InvalidRequestError
from secret import API_KEY
from collection.utils.process import separate_comments

# Constants
ENGINE: str = "text-davinci-003"
MAX_TOKENS: int = 1000
NUM_SENTENCES: int = 5
FILENAME: str = "data/gpt_summaries.txt"


# Helper functions
def expansion_prompt(review_block: str, n_sentences: int) -> str:
    """Provides the instructions for extractive summarization of the review."""

    return f"The following text is an amalgamation of students reviews of a professor. Please select {n_sentences} " \
           f"from these reviews to create an accurate bullet point summary of the reviews. Do not generate new " \
           f"sentences.\n{review_block}"


def ask(prompt: str) -> str:
    """Provide a prompt to the OpenAI language model and return the text."""

    try:
        response = openai.Completion.create(
            engine=ENGINE,
            prompt=prompt,
            temperature=0.5,
            max_tokens=MAX_TOKENS
        )
    except InvalidRequestError as error:
        response = f"Error: {error.user_message}"

    return response.choices[0]["text"]


# Main
def main():

    openai.api_key = API_KEY  # Set the API key
    data = pd.read_parquet("data/analyzed_data.parquet.gzip")  # Read data

    # Group data in a way that makes searching through combinations more convenient
    grouped_data = data.groupby(["school", "professor", "course"], group_keys=True)
    combinations = list(grouped_data.groups.keys())  # Unique combos of school, prof and course
    grouped_data = grouped_data.apply(lambda x: x)  # Make DataFrame searchable

    # Open file to save GPT summaries
    with open(FILENAME, 'w', encoding="utf-8") as file:

        # Iterate through all unique combinations
        for school, professor, course in combinations:

            # Join the comments with their predicted sentiment
            sentimented_ratings = separate_comments(pd.concat(
                [grouped_data["comment"][school][professor][course],
                 grouped_data["sentiment"][school][professor][course]],
                axis=1
            ))

            # Summarize with OpenAI and save results to text file
            for sentiment, ratings in sentimented_ratings.items():
                summary = ask(expansion_prompt(ratings, NUM_SENTENCES)).strip()

                # Write to file
                file.write(f"{school}-{professor}-{course}-{sentiment}\n")
                file.write(f"{summary}\n\n")

                # Show in console
                print(f"{school}-{professor}-{course}-{sentiment}")
                print(f"{summary}\n")


if __name__ == '__main__':
    main()
