import os
from datetime import datetime

import matplotlib.pyplot as plt
from rich.console import Console

from .utils import compute_percentage_changes, smooth_rates

console = Console()


def generate_and_save_currency_plot(from_curr: str, to_curr: str, data: dict):
    output_dir = os.path.expanduser("~/Pictures/plots/currency-rates")
    os.makedirs(output_dir, exist_ok=True)

    sorted_dates = sorted(data.keys())
    dates = sorted_dates
    rates = [data[date][to_curr] for date in sorted_dates]

    if len(dates) > 50:
        window = 5
    elif len(dates) > 150:
        window = 7
    else:
        window = 1

    rates, dates = smooth_rates(dates, rates, window)

    plt.figure(figsize=(10, 5))
    plt.plot(
        list(dates),
        list(rates),
        marker="o",
        linestyle="-",
        color="royalblue",
    )

    pct_changes = compute_percentage_changes(rates)
    for i, (x, y, pct) in enumerate(zip(dates, rates, pct_changes)):
        if pct:
            plt.annotate(
                pct,
                (x, y),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                fontsize=7.25,
                color="green" if "+" in pct else "red",
            )

    plt.title(f"Exchange Rate: {from_curr.upper()} to {to_curr.upper()}")
    plt.xlabel("Date")
    plt.ylabel("Rate")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{from_curr.lower()}_{to_curr.lower()}_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    plt.savefig(filepath)
    plt.close()

    console.print(f"[✓] Plot saved to: {filepath}")
