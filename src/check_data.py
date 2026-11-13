#Quick check that the Ken French factor file loads correctly.

from loaders import load_french

factors = load_french("F-F_Research_Data_Factors.csv")

print(factors.head())
print(factors.tail())
print(factors.shape)