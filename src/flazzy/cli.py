from time import sleep
from datetime import date, timedelta

import click
from rich.console import Console
from rich.spinner import Spinner

from .plot import generate_and_save_currency_plot
from .utils import (
    display_conversion,
    display_currencies,
    display_currency_table,
)

from .api import (
    fetch_exchange_rates,
    fetch_list_currencies,
    fetch_rates_by_date_range,
    fetch_rates_for_currency,
)
from .converter import convert_currency, generate_exchange_pairs

console = Console()


@click.group()
@click.version_option("0.2.0", prog_name="Flazzy")
def cli():
    """
    Currency CLI Application.

    Use this tool to convert currencies and display real-time exchange rates
    from a base currency to other supported currencies.
    """
    pass


@cli.command()
@click.option(
    "-a",
    "--amount",
    "amount",
    type=float,
    required=True,
    help="The amount of money to convert (float).",
)
@click.option(
    "-f",
    "--from",
    "from_curr",
    type=str,
    required=True,
    help="The source currency code (e.g., USD).",
)
@click.option(
    "-t",
    "--to",
    "to_curr",
    type=str,
    required=True,
    help="The target currency code (e.g., IDR).",
)
@click.option(
    "-d",
    "--date",
    "to_date",
    type=str,
    show_default=True,
    default="latest",
    help="The date of the exchange rate (format: YYYY-MM-DD).",
)
def exchange(amount: float, from_curr: str, to_curr: str, to_date: str):
    """
    Convert a specific amount from one currency to another using real-time exchange rates.

    Example:
        flazzy exchange -a 100 -f USD -t IDR
    """

    rates = fetch_exchange_rates(from_curr.upper(), to_curr.upper(), to_date)
    result = convert_currency(amount, from_curr.upper(), to_curr.upper(), rates)

    with console.status("Fetch data from API...", spinner="line"):
        sleep(2.5)

    display_conversion(amount, from_curr, to_curr, result, to_date)


@cli.command()
@click.option(
    "--currency",
    "--base",
    type=str,
    default="USD",
    show_default=True,
    help="The base currency code to fetch exchange rates for (e.g., EUR, USD, IDR).",
)
@click.option(
    "--date",
    "--to-date",
    "to_date",
    type=str,
    show_default=True,
    default="latest",
    help="The date of the exchange rate (format: YYYY-MM-DD).",
)
def rates(to_date: str, currency: str):
    """
    Display a table of exchange rates from a base currency to other currencies.

    This command retrieves real-time exchange rates using the given base
    currency and prints them in a formatted table using Rich. If no currency
    is provided, it defaults to 'USD'.

    Example:
        flazzy rates --base EUR
    """
    data = fetch_rates_for_currency(currency.upper(), to_date)
    pairs = generate_exchange_pairs(data)

    with console.status("Fetch data from API...", spinner="line"):
        sleep(2.5)

    console.print("", end="")
    display_currency_table(pairs, to_date)


@cli.command()
@click.argument("from_curr", type=str)
@click.argument("to_curr", type=str)
@click.option(
    "--days",
    "--back-days",
    "bk_date",
    type=int,
    required=True,
    help="Number of days to look back from today to retrieve historical exchange rates (e.g., 30 means last 30 days).",
)
def chart(from_curr: str, to_curr: str, bk_date: int):
    """
    Generate a historical line chart showing currency exchange trends.

    This command retrieves historical exchange rate data between the source
    currency (`from_curr`) and target currency (`to_curr`) for a specific
    number of past days, then renders a chart using Rich.

    Example usage:
        flazzy chart USD EUR --days 30
    """

    from_date = date.today() - timedelta(days=bk_date)
    data = fetch_rates_by_date_range(
        from_curr.upper(), to_curr.upper(), from_date.isoformat(), date.today().isoformat()
    )

    with console.status("Fetch data from API...", spinner="line"):
        sleep(2.5)

    generate_and_save_currency_plot(from_curr, to_curr, data)


@cli.command()
@click.option(
    "--list-all",
    is_flag=True,
    help="Show the full list of availalbe currencies.",
    required=True,
)
def currencies(list_all):
    """
    Lists all available currencies retrieved from an external API.

    Fetches currency codes along with their corresponding names and presents
    them in a structured table format in the terminal. This helps users identify
    supported currencies before using other commands like conversion or rate lookup.

    Example usage:
        $ flazzy currencies --list-all
    """

    data = fetch_list_currencies()

    with console.status("Fetch data from API...", spinner="line"):
        sleep(2.5)

    display_currencies(data)


if __name__ == "__main__":
    cli()
