import pandas as pd

df = pd.read_csv("../sample-export/internal_all.csv")
print(df.shape)
print(df.columns[:10])