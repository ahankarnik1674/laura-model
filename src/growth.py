#Growth sleeve; essentially the stocks and funds we hold. 
import pandas as pd

def load_equities(): 
    """Read all 8 stocks/ETF holdings with cost and weight(investment)"""
    equities = pd.read_csv("data/equities.csv")
    equities["cost"] = equities["shares"] * equities["price_paid"]
    equities["weight"] = equities["cost"] / equities["cost"].sum()
    return equities
