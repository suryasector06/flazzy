from datetime import date
from typing import Optional

from rich.console import Console
from rich.table import Table

console = Console()


def display_currency_table(
    pairs: list[tuple[str, str, float]], to_date: Optional[str] = "latest"
):
    if to_date == "latest":
        to_date = date.today().isoformat()

    for from_currency, to_currency, rate in pairs:
        console.print(
            f"[bold cyan] 1.00"
            f"[bold cyan]{from_currency.upper()}[/bold cyan] "
            f"[bold white]→[/bold white] "
            f"[bold green]{rate:.2f} {to_currency.upper()}[/bold green] "
            f"in {to_date}"
        )


def display_conversion(
    amount: float,
    from_curr: str,
    to_curr: str,
    result: float,
    to_date: Optional[str] = "latest",
):
    if to_date == "latest":
        to_date = date.today().isoformat()

    console.print(
        f"[bold cyan]{amount:.2f} {from_curr.upper()}[/bold cyan] [bold white]→[/bold white] [bold green]{result:.2f} {to_curr.upper()}[/bold green] in {to_date}"
    )


def compute_percentage_changes(rates: list[float]):
    changes = [""]
    for i in range(1, len(rates)):
        delta = (rates[i] - rates[i - 1]) / rates[i - 1] * 100
        sign = "+" if delta >= 0 else "-"
        changes.append(f"{sign}{abs(delta):.2f}")
    return changes


def smooth_rates(dates: list, rates: list, window: int):
    smoothed_dates = []
    smoothed_rates = []

    for i in range(0, len(rates), window):
        group_dates = dates[i : i + window]
        group_rates = rates[i : i + window]

        if not group_rates:
            continue

        avg_rate = sum(group_rates) / len(group_rates)
        mid_date = group_dates[len(group_dates) // 2]
        smoothed_dates.append(mid_date)
        smoothed_rates.append(avg_rate)

    return smoothed_rates, smoothed_dates


def display_currencies(data: dict):
    for currency, namecurr in data.items():
        console.print(
            f"[bold cyan]{currency}[/bold cyan]: [bold green]{namecurr}[/bold green]"
        )
