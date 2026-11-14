#Charts fo rthe report
import matplotlib.pyplot as plt

"""Charts for the report."""

import matplotlib.pyplot as plt


def plot_coverage(table, path):
    """Bar chart: cash from our bonds each payment year vs. the payment target."""
    fig, ax = plt.subplots(figsize=(7, 4))  # a blank chart, 7 x 4 inches
    ax.bar(table["year"], table["cash"], color="#2a6f97", label="Cash from bonds")
    ax.axhline(table["target"].iloc[0], color="black", linestyle="--", label="Payment target")
    ax.set_xticks(table["year"])  # one label per year
    ax.set_xlabel("Payment year (January)")
    ax.set_ylabel("Dollars (scaled to the $300K portfolio)")
    ax.set_title("Bond cash vs. payment target")
    ax.legend()
    fig.savefig(path, dpi=200, bbox_inches="tight")  # save as a PNG file

