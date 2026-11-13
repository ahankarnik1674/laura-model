import pandas as pd
import io

LAST_FULL_MONTH = "2026-10-01"

#Loads the price files and converts them into monthly returns. 
def load_prices(ticker): 
    prices = pd.read_csv(f"data/raw/{ticker}.csv", parse_dates=["Date"])
    prices = prices[prices["Date"] <= LAST_FULL_MONTH] #drops partial months
    prices = prices.set_index("Date")
    return prices["Adj Close"]

#Return each month's % change in price, e.g., 0.03 indicates +3%. 
def monthly_returns(ticker):
    return load_prices(ticker).pct_change().dropna()

#Our 8 holdings in the portfolio
TICKERS = ["RSP", "VXUS", "TSM", "GOOGL", "TEAM", "MAR", "SPOT", "EDU"]

def all_returns(): 
    """Return table: per month, per ticker"""
    series = []
    for ticker in TICKERS: 
        series.append(monthly_returns(ticker))

    return pd.concat(series, axis=1, keys=TICKERS)

def load_french(filename): 
    """Reads a Ken French monthly file"""
    with open(f"data/raw/{filename}") as f:
        lines = f.readlines()  
    
    start = next(i for i, line in enumerate(lines) if line.startswith(","))
    end = start + 1
    while end < len(lines) and lines[end].strip() != "":
        end += 1

    table = pd.read_csv(io.StringIO("".join(lines[start:end])), index_col=0)
    table = table.replace([-99.99, -999], float("nan")) 
    table.index = pd.to_datetime(table.index.astype(str), format="%Y%m") 
    return table / 100 
