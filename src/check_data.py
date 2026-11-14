"""Check the equity holdings and their weights."""

from growth import load_equities

equities = load_equities()

print(equities.round({"cost": 2, "weight": 3}))
print("Total cost:", round(equities["cost"].sum(), 2))