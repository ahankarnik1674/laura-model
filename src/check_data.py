"""Check how each deposit is split between bonds and growth."""

from funding import funding_split

split = funding_split()

for name, value in split.items():  # go through each label and its number
    print(f"{name}: {value:,.2f}")