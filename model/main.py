# Runs the language model
__author__ = "Matteo Golin"

# Imports
import pandas as pd
from summarizer import Summarizer
from processing import separate_comments

# Constants


# Main
def main():

    data = pd.read_parquet("collection/data/analyzed_data.parquet.gzip")
    model = Summarizer()


    with open('results.txt', 'w') as f:
        for course in data["course"].unique():
            f.write(course + ": \n")
            subset = data[['comment', 'sentiment']]
            df = subset[data['course'] == course]
            dict = separate_comments(df)
            pos_result = model(dict.get("positive"), ratio=0.5)
            f.write("Postive Feedback: \n"+ pos_result +"\n")
            neg_result = model(dict.get("negative"), ratio = 0.5)
            f.write("Negative Feedback: \n"+ neg_result +"\n\n")



    # comments = data[data["course"].str.contains("SYSC2320") == True]["comment"]
    # text_mass = ". ".join(comments)

    # model = Summarizer()
    # result = model(text_mass, num_sentences=4)
    # bullets = result.split(". ")

    # for bullet in bullets:
    #     print(f"* {bullet}")


if __name__ == '__main__':
    main()
