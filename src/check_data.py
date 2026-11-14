"""Check that the bond file loads and the totals look right."""

from reserve import load_bonds

bonds = load_bonds()

print(bonds[["symbol", "maturity", "quantity", "face", "cost"]])
print("Total face:", bonds["face"].sum())
print("Total cost:", round(bonds["cost"].sum(), 2))