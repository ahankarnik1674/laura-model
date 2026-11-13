import pandas as pd

prices = pd.read_csv("data/raw/RSP.csv", parse_dates=["Date"])

print(prices.head())
print(prices.tail())
print(prices.shape)
