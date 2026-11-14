"""Check how well our bonds cover each yearly payment."""

from reserve import load_bonds, payment_coverage

bonds = load_bonds()
table = payment_coverage(bonds)

print(table.round({"target": 2, "cash": 2, "coverage": 3}))
print("Overall coverage:", round(table["cash"].sum() / table["target"].sum(), 3))