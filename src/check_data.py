"""Scratch driver: runs the pieces built so far and prints the results."""

import numpy as np

from loaders import load_french
from funding import funding_split
from reserve import load_bonds, payment_coverage, PAYMENT, SCALE
from simulate import replay_full, replay, find_pledge

# Monthly cash return (RF) and stock return (market excess + RF).
factors = load_french("F-F_Research_Data_Factors.csv")
cash = factors["RF"].to_numpy()
stock = (factors["Mkt-RF"] + factors["RF"]).to_numpy()

# Yearly gap the bonds leave uncovered, in plan dollars.
cov = payment_coverage(load_bonds())
gaps = list((PAYMENT - cov["cash"] / SCALE).clip(lower=0))
print("Total gap:", round(sum(gaps)))

split = funding_split()
a, b = split["growth_2027"], split["growth_2028"]
values = replay(stock, cash, a, b)                      # sleeve value on Jan 1, 2033

# Largest pledge that keeps the shortfall chance within each tolerance.
for tol in (0.04, 0.05, 0.06, 0.08, 0.10):
    pledge = find_pledge(stock, cash, a, b, gaps, tol)
    contribution = values * pledge
    p10, p50, p90 = np.percentile(contribution, [10, 50, 90])
    print(f"Tolerance {tol:.0%}: pledge {pledge:.0%}; contribution 10th {p10:,.0f}, median {p50:,.0f}, 90th {p90:,.0f}")
