from loaders import monthly_returns

r = monthly_returns("RSP")

print(r.head())
print(r.tail())
print(len(r))