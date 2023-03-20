#Contains the analysis of the data scraped from RateMyProf 
__author__ = "Hamnah Qureshi"


#Imports
import pandas as pd
import os
from graph import histogram, plot

#retusn the avaerge given x and y vals and creates histogram plot
def avg_histogram(data, xVal, yVal, xMax, yMax, title, yAxis) -> float:
    group_data = data.groupby(yVal)[xVal].nunique()
    freq = (group_data).values
    numOfY = data[yVal].nunique()
    numOfX = data[xVal].nunique()
    histogram(freq, xVal, yVal, xMax, yMax, title, yAxis)
    return round(numOfX/numOfY,2)

#returns the average number of sentences per rating
def avg_sentence_comment (data) -> float:
    ratings = data["comment"].tolist()
    numRatings = len(ratings)
    count =0
    for rating in ratings:
        count += rating.count('.') 
        count += rating.count('?')
        count += rating.count('!')
    return round(count/numRatings,2)

#returns the average number of words per rating
def avg_word_comment(data) -> float:
    ratings = data["comment"].tolist()
    numRatings = len(ratings)
    count =0
    for rating in ratings:
        count += rating.count(' ') 
    return round(count/numRatings,2)


def main():

    data = pd.read_parquet("collection/data/ratings.parquet.gzip")
    stats = ""
    stats += "Avg courses/professor: " + str(avg_histogram(data,"course", "professor", 60, 18, "Number of coureses taught by professor", 0)) +"\n"
    stats += "Avg ratings/professor: " + str(avg_histogram(data, "comment", "professor", 225, 10, "Number of ratings for the professor", 1)) + "\n"
    stats += "Avg sentences/rating: " + str(avg_sentence_comment(data)) + "\n"
    stats += "Avg words/ratings: " + str(avg_word_comment(data)) + "\n"
    stats += "Number of professors in universities: "
    numProfessors = (str(data.groupby('school')["professor"].nunique()).replace("school", '')).replace('Name: professor, dtype: int64', '')
    stats += numProfessors
    plot(stats)


    
    


if __name__ == "__main__":
    main()
