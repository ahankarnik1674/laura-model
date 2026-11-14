"""Check the cash each bond pays by maturity."""

from reserve import load_bonds

bonds = load_bonds()

print(bonds[["symbol", "maturity", "cash"]])