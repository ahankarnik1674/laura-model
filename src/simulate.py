#Replays history through the growth sleeve's plan. 

import numpy as np

# Share of the sleeve held in stocks each plan year, 2027 through 2032.
GLIDE = [1.00, 1.00, 1.00, 0.75, 0.50, 0.25]
MONTHS = 72            # Jan 2027 to Dec 2032
PAYOUT_STOCKS = 0.25   # share of the kept money held in stocks after 2033
PAYOUT_MONTHS = 120    # Jan 2033 to Dec 2042


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


def run_payout(stock_returns, cash_returns, retained, gaps):
    """Spend the kept sleeve on the yearly bond gaps, 2033-2042.
    Returns the total unpaid amount (0 means every payment was covered)."""
    stocks = retained * PAYOUT_STOCKS
    cash = retained * (1 - PAYOUT_STOCKS)
    unpaid = 0.0
    for month in range(PAYOUT_MONTHS):
        if month % 12 == 0:                   
            owed = gaps[month // 12]
            from_cash = min(owed, cash)        
            cash -= from_cash
            owed -= from_cash
            from_stocks = min(owed, stocks)    
            stocks -= from_stocks
            unpaid += owed - from_stocks      
        stocks *= 1 + stock_returns[month]
        cash *= 1 + cash_returns[month]
    return unpaid


def replay_full(stock_returns, cash_returns, deposit_2027, deposit_2028, pledge, gaps):
    """Build phase (72 months), then pledge, then payout phase (120 months),
    for every historical window. Returns the unpaid amount per window."""
    total = MONTHS + PAYOUT_MONTHS
    n_windows = len(stock_returns) - total + 1
    results = []
    for start in range(n_windows):
        build = slice(start, start + MONTHS)
        payout = slice(start + MONTHS, start + total)
        value = run_plan(stock_returns[build], cash_returns[build], deposit_2027, deposit_2028)
        retained = value * (1 - pledge)        # what is left after the pledge
        results.append(run_payout(stock_returns[payout], cash_returns[payout], retained, gaps))
    return np.array(results)

def find_pledge(stock_returns, cash_returns, deposit_2027, deposit_2028, gaps, tolerance):
    """Largest pledge (in 1% steps, up to 75%) whose shortfall rate stays within tolerance."""
    best = 0.0
    for percent in range(0, 76):
        pledge = percent / 100
        unpaid = replay_full(stock_returns, cash_returns, deposit_2027, deposit_2028, pledge, gaps)
        if (unpaid > 0).mean() <= tolerance:    # still safe enough, so keep it
            best = pledge
    return best