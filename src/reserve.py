#Reserve Sleve: what our Treasury bonds pay, and thei corresponding date(s)
import pandas as pd

def load_bonds():
    bonds = pd.read_csv("data/bonds.csv", parse_dates=["maturity"])
    bonds["face"] = bonds["quantity"] * 1000  
    bonds["cost"] = bonds["quantity"] * bonds["price_paid"] 
    return bonds
