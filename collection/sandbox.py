# File for playing with data
__author__ = "Matteo Golin"

# Imports
import pandas as pd
import utils.process as proc

# Constants
POLARITY = -1

# Read data
data = pd.read_parquet("./data/ratings.parquet.gzip")

# Analyze sentiment
nearest_data = proc.analyze_sentiment(data.copy())
true_neutral_data = proc.analyze_sentiment(data.copy())

# Counts of sentimentality types
print("Nearest", nearest_data.value_counts("sentiment"))
print("True Neutral", true_neutral_data.value_counts("sentiment"))

prof = nearest_data["professor"].str.contains("Chao Shen") == True  # Filter by prof

# Filter by polarity
nearest_polarity = nearest_data["sentiment"] == POLARITY
true_neutral_polarity = true_neutral_data["sentiment"] == POLARITY

# Filter by polarity and professor
nearest_comments = nearest_data[nearest_polarity & prof]["comment"]
true_neutral_comments = true_neutral_data[true_neutral_polarity & prof]["comment"]

# Pad lists to be same length
nearest_comments = list(nearest_comments)
true_neutral_comments = list(true_neutral_comments)
padding = max(len(nearest_comments), len(true_neutral_comments)) - min(len(nearest_comments), len(true_neutral_comments))
min(nearest_comments, true_neutral_comments, key=lambda x: len(x)).extend([""] * padding)
comparison = pd.DataFrame({"nearest": nearest_comments, "true neutral": true_neutral_comments})

# Show comments side by side
pd.set_option('display.max_colwidth', None)
print(f"\nSentiment: {proc.SENTIMENTS[POLARITY].title()}")
print(comparison[["nearest", "true neutral"]].to_string(index=False))
