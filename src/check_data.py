"""Make the coverage chart."""

from reserve import load_bonds, payment_coverage
from plots import plot_coverage

bonds = load_bonds()
table = payment_coverage(bonds)
plot_coverage(table, "figures/coverage.png")

print("Saved figures/coverage.png")