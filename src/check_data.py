"""Replay history through the growth sleeve and print the spread of outcomes."""

import numpy as np

from loaders import load_french
from funding import funding_split
from simulate import replay

french = load_french("F-F_Research_Data_Factors.csv")
cash_returns = french["RF"].to_numpy()  # T-bill rate each month
stock_returns = french["Mkt-RF"].to_numpy() + cash_returns  # market return = excess + cash rate

split = funding_split()
results = replay(stock_returns, cash_returns, split["growth_2027"], split["growth_2028"])

print("Windows:", len(results))
print("Money put in:", round(split["growth_2027"] + split["growth_2028"]))
for p in [5, 10, 25, 50, 75, 90]:
    print(f"{p}th percentile: {np.percentile(results, p):,.0f}")