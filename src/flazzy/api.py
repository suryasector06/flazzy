import os
from typing import Optional

import click
import requests


def fetch_exchange_rates(from_curr: str, to_curr: str, to_date: str):
    try:
        response = requests.get(
            f"https://api.frankfurter.dev/v1/{to_date}?base={from_curr}&symbols={to_curr}"
        )
        data = response.json()

        data["rates"][from_curr] = 1.0

        if "message" in data and data["message"] == "not found":
            raise click.UsageError(
                f"Invalid input. Please double check the entered parameters."
            )

        return data["rates"]
    except requests.exceptions.RequestException as e:
        raise click.UsageError(f"Failed to contact API: {e}")


def fetch_rates_for_currency(currency: str, to_date: str):
    try:
        response = requests.get(
            f"https://api.frankfurter.dev/v1/{to_date}?base={currency}"
        )
        data = response.json()

        if data.get("message") == "not found":
            raise click.UsageError(
                f"Invalid input. Please double check the entered parameters."
            )

        return data
    except requests.exceptions.RequestException as e:
        raise click.UsageError(f"Failed to contact API: {e}")


def fetch_rates_by_date_range(
    from_curr: str, to_curr: str, from_date: str, to_date: str
):
    try:
        response = requests.get(
            f"https://api.frankfurter.dev/v1/{from_date}..{to_date}?base={from_curr}&symbols={to_curr}"
        )
        data = response.json()

        if data.get("message") == "not found":
            raise click.UsageError(
                f"Invalid input. Please double check the entered parameters."
            )

        return data["rates"]
    except requests.exceptions.RequestException as e:
        raise click.UsageError(f"Failed to contact API: {e}")


def fetch_list_currencies():
    try:
        response = requests.get("https://api.frankfurter.dev/v1/currencies")
        data = response.json()

        if data.get("message") == "not found":
            raise click.UsageError(
                f"Invalid input. Please double check the entered parameters."
            )

        return data
    except requests.exceptions.RequestException as e:
        raise click.UsageError("Failed to contact API: {e}")
