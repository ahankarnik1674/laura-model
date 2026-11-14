#Splits the client's money into intwo sleves: growth(stocks/ETFs) and resevre(bonds)
from reserve import load_bonds, SCALE

DEPOSIT_2027 = 300_000 
DEPOSIT_2028 = 150_000 

def funding_split(): 
    """Amount bought as bonds each year, and amount left over for growth.

    Assumption: the Feb 2031 bond is bought in Jan 2028; the other 7 in Jan 2027.
    """
    bonds = load_bonds()
    bonds["real_cost"] = bonds["cost"] / SCALE  # scale $300K portfolio up to the $450K plan

    is_2031 = bonds["maturity"].dt.year == 2031  # True for the Feb 2031 bond, False otherwise
    bought_2028 = bonds.loc[is_2031, "real_cost"].sum() 
    bought_2027 = bonds.loc[~is_2031, "real_cost"].sum()  

    return {
        "reserve_2027": bought_2027,
        "reserve_2028": bought_2028,
        "growth_2027": DEPOSIT_2027 - bought_2027,
        "growth_2028": DEPOSIT_2028 - bought_2028,
    }
