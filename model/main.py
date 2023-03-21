# Runs the language model
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from summarizer import Summarizer

# Constants


# Main
def main():

    data = pd.read_parquet("../collection/data/test_data.parquet.gzip")
    comments = data[data["course"].str.contains("SYSC2320") == True]["comment"]

    text_mass = ". ".join(comments)

    model = Summarizer()
    result = model(text_mass, num_sentences=4)
    bullets = result.split(". ")

    for bullet in bullets:
        print(f"* {bullet}")


if __name__ == '__main__':
    main()
