"""Scratch driver: runs the pieces built so far and prints the results."""

import numpy as np

from loaders import load_french
from funding import funding_split
from reserve import load_bonds, payment_coverage, PAYMENT, SCALE
from simulate import replay_full

# Monthly cash return (RF) and stock return (market excess + RF).
factors = load_french("F-F_Research_Data_Factors.csv")
cash = factors["RF"].to_numpy()
stock = (factors["Mkt-RF"] + factors["RF"]).to_numpy()

# Yearly gap the bonds leave uncovered, in plan dollars.
cov = payment_coverage(load_bonds())
gaps = list((PAYMENT - cov["cash"] / SCALE).clip(lower=0))
print("Total gap:", round(sum(gaps)))

# Try different pledge sizes.
split = funding_split()
for pledge in (0.75, 0.50, 0.25, 0.0):
    unpaid = replay_full(stock, cash, split["growth_2027"], split["growth_2028"], pledge, gaps)
    print(f"Pledge {pledge:.0%}: windows {len(unpaid)}, shortfall in {(unpaid > 0).mean():.1%}, worst unpaid {unpaid.max():,.0f}")