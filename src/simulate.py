#Replays history through the growth sleeve's plan. 

import numpy as np

"""Replays history through the growth sleeve's plan."""

import numpy as np

# Share of the sleeve held in stocks each plan year, 2027 through 2032.
GLIDE = [1.00, 1.00, 1.00, 0.75, 0.50, 0.25]
MONTHS = 72  

def run_plan(stock_returns, cash_returns, deposit_2027, deposit_2028):
    """Run the plan through 72 months of returns; return the value on Jan 1, 2033."""
    stocks = 0.0
    cash = 0.0
    for month in range(MONTHS): 
        if month == 0:
            cash += deposit_2027 
        if month == 12:
            cash += deposit_2028 
        if month % 12 == 0:  
            total = stocks + cash
            stock_share = GLIDE[month // 12]  
            stocks = total * stock_share
            cash = total * (1 - stock_share)
        stocks *= 1 + stock_returns[month]  
        cash *= 1 + cash_returns[month]
    return stocks + cash


def replay(stock_returns, cash_returns, deposit_2027, deposit_2028):
    """Start the plan in every month of history; return every ending value."""
    n_windows = len(stock_returns) - MONTHS + 1
    results = []
    for start in range(n_windows):
        window = slice(start, start + MONTHS)  
        results.append(
            run_plan(stock_returns[window], cash_returns[window], deposit_2027, deposit_2028)
        )
    return np.array(results)