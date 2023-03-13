import pandas as pd
from utils.process import analyze_sentiment

data = pd.read_parquet("./data/ratings.parquet.gzip")
analyze_sentiment(data)
