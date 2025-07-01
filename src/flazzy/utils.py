import random
from datetime import date
from typing import Optional

from rich.console import Console
from rich.panel import Panel

console = Console()


def display_currency_table(
    pairs: list[tuple[str, str, float]], to_date: Optional[str] = "latest"
):
    if to_date == "latest":
        to_date = date.today().isoformat()

    lines = []

    for from_currency, to_currency, rate in pairs:
        line = (
            f"1.00 {from_currency.upper()} " f" →  " f"{rate:>7} {to_currency.upper()}"
        )
        lines.append(line)

    content = "\n".join(lines)
    console.print(
        Panel(content, title_align="right", title=f"Currency Rates at {to_date}")
    )


def display_conversion(
    amount: float,
    from_curr: str,
    to_curr: str,
    result: float,
    swap_result: Optional[float],
    to_date: Optional[str] = "latest",
):
    if to_date == "latest":
        to_date = date.today().isoformat()

    if swap_result:
        lines = []
        lines.append(
            f"{amount:.2f} {from_curr.upper()} "
            f"→ "
            f"{result:.2f} {to_curr.upper()}"
        )
        lines.append(
            f"{result:.2f} {to_curr.upper()} "
            f"→ "
            f"{swap_result:.2f} {from_curr.upper()}"
        )
        content = "\n".join(lines)

        console.print(
            Panel(
                content,
                title_align="right",
                title=f"Swap Exchange at {to_date}",
            )
        )

        return

    content = (
        f"{amount:.2f} {from_curr.upper()} "
        f"→ "
        f"{result:.2f} {to_curr.upper()}"
    )

    console.print(
        Panel(
            content, title_align="right", title=f"Conversion Result at {to_date}"
        )
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
    lines = []
    for currency, namecurr in sorted(data.items()):
        lines.append(
            f"{currency}: {namecurr}"
        )

    content = "\n".join(lines)
    console.print(
        Panel(
            content,
            title_align="right",
            title="Supported Currencies",
        )
    )
