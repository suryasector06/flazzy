from unittest.mock import MagicMock, patch

import click
import pytest
from requests import RequestException

from flazzy.api import (fetch_exchange_rates, fetch_list_currencies,
                        fetch_rates_by_date_range, fetch_rates_for_currency)


@patch("flazzy.api.requests.get")
def test_fetch_exchange_rates_success(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"EUR": 0.9}}

    result = fetch_exchange_rates("USD", "EUR", "2024-01-01")
    assert result == {"EUR": 0.9, "USD": 1.0}


@patch("flazzy.api.requests.get")
def test_fecth_exchange_rates_error_message(mock_get):
    mock_get.return_value.json.return_value = {"message": "not found", "rates": {}}
    with pytest.raises(click.UsageError):
        fetch_exchange_rates("XXX", "YYY", "2024-01-01")


@patch("flazzy.api.requests.get", side_effect=RequestException("network error"))
def test_fetch_exchange_rates_network_error(mock_get):
    with pytest.raises(click.UsageError):
        fetch_exchange_rates("USD", "EUR", "2024-01-01")


@patch("flazzy.api.requests.get")
def test_fetch_rates_by_date_range_success(mock_get):
    mock_get.return_value.json.return_value = {
        "rates": {
            "2024-01-01": {"EUR": 0.9},
            "2024-01-02": {"EUR": 0.91},
        }
    }
    result = fetch_rates_by_date_range("USD", "EUR", "2024-01-01", "2024-01-02")
    assert isinstance(result, dict)
    assert "2024-01-01" in result


@patch("flazzy.api.requests.get")
def test_fetch_rates_for_currency_success(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"EUR": 0.9}}
    result = fetch_rates_for_currency("USD", "2024-01-01")
    assert result == {"rates": {"EUR": 0.9}}


@patch("flazzy.api.requests.get")
def test_fetch_rates_for_currency_error_message(mock_get):
    mock_get.return_value.json.return_value = {"message": "not found"}
    with pytest.raises(click.UsageError):
        fetch_rates_for_currency("INVALID", "2024-01-01")


@patch("flazzy.api.requests.get")
def test_fetch_rates_by_date_range_invalid(mock_get):
    mock_get.return_value.json.return_value = {"message": "not found"}
    with pytest.raises(click.UsageError):
        fetch_rates_by_date_range("XXX", "YYY", "2024-01-01", "2024-01-02")


@patch("flazzy.api.requests.get")
def test_fetch_list_currencies_success(mock_get):
    mock_get.return_value.json.return_value = {"USD": "US Dollar", "EUR": "Euro"}
    result = fetch_list_currencies()
    assert result["USD"] == "US Dollar"
    assert "EUR" in result


@patch("flazzy.api.requests.get")
def test_fetch_list_currencies_error(mock_get):
    mock_get.return_value.json.return_value = {"message": "not found"}
    with pytest.raises(click.UsageError):
        fetch_list_currencies()
