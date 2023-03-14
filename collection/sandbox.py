import pandas as pd
from utils.process import analyze_sentiment

data = pd.read_parquet("./data/ratings.parquet.gzip")
data = analyze_sentiment(data)

print(data.value_counts("sentiment"))

for comment in data[data["sentiment"] == 0]["comment"]:
    print(f"---> {comment}")