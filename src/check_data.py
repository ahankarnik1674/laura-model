from loaders import all_returns

returns = all_returns()

print(returns.count())  # number of months of data for each ticker
print(returns.tail())   # last 5 rows
print(returns.shape)    # (rows, columns)