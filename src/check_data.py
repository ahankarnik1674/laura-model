"""Scratch driver: checks the 8 holdings line up."""

from loaders import all_returns
from growth import cost_weights

returns = all_returns()                   # one column per holding
weights = cost_weights()

print("Weights:", {t: round(w, 3) for t, w in weights.items()})
print("Total weight:", round(sum(weights.values()), 4))
print()
print("Months of history per holding:")
print(returns.count())
print()
common = returns.dropna()
print("Months where ALL 8 exist:", len(common))
print("From", common.index.min().date(), "to", common.index.max().date())

