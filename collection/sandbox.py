import pandas as pd
import utils.process as proc

data = pd.read_parquet("./data/ratings.parquet.gzip")

data = proc.analyze_sentiment(data)

print(data.value_counts("sentiment"))

positive = data["sentiment"] == 1
lynn = data["professor"].str.contains("Lynn Marshall") == True

for comment in data[positive & lynn]["comment"]:
    print(comment)
