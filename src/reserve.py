#Reserve Sleve: what our Treasury bonds pay, and thei corresponding date(s)
import pandas as pd

SETTLEMENT = pd.Timestamp("2026-11-06")

PAYMENT = 50_000  # each yearly payment to the residency
SCALE = 300_000 / 450_000  # our WInS portfolio is $300K; the real plan is $450K
YEARS = range(2033, 2043)  # the ten payment years: 2033 through 2042

def coupon_dates(maturity, after=SETTLEMENT):
    """List every coupon date after `after`, up to and including maturity."""
    dates = []
    date = maturity
    while date > after:  
        dates.append(date)
        date = date - pd.DateOffset(months=6)
    return sorted(dates)  

def cash_at_maturity(bond):
    """Total cash a bond has paid by maturity: all coupons plus face value."""
    n_coupons = len(coupon_dates(bond["maturity"]))
    one_coupon = bond["coupon"] * bond["face"] / 2  # coupons are paid twice a year
    return n_coupons * one_coupon + bond["face"]

def load_bonds():
    bonds = pd.read_csv("data/bonds.csv", parse_dates=["maturity"])
    bonds["face"] = bonds["quantity"] * 1000
    bonds["cost"] = bonds["quantity"] * bonds["price_paid"]
    bonds["cash"] = bonds.apply(cash_at_maturity, axis=1)
    return bonds

def payment_coverage(bonds): 
    """For each payment year, compare cash from our bonds ot the scaled target"""
    rows=[]
    for year in YEARS: 
        cash = 0.0
        for _, bond in bonds.iterrows():
            if pd.isna(bond["funds"]):  # this bond funds no payment
                continue
            years = [int(y) for y in str(bond["funds"]).split(";")]  # "2033;2034" -> [2033, 2034]
            if year in years:
                cash += bond["cash"] / len(years)  # split its cash evenly across its years
        rows.append({"year": year, "target": PAYMENT * SCALE, "cash": cash})
    table = pd.DataFrame(rows)
    table["coverage"] = table["cash"] / table["target"]  
    return table

