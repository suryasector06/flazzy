from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from flazzy.plot import generate_and_save_currency_plot


@pytest.fixture
def dummy_data():
    base_date = datetime(2024, 1, 1)
    return {
        (base_date + timedelta(days=i)).strftime("%Y-%m-%d"): {"EUR": 0.9 + i * 0.01}
        for i in range(10)
    }


@patch("flazzy.plot.os.makedirs")
@patch("flazzy.plot.os.path.expanduser", return_value="/tmp/test-plots")
@patch("flazzy.plot.plt.savefig")
@patch("flazzy.plot.plt.close")
@patch("flazzy.plot.console.print")
@patch(
    "flazzy.plot.smooth_rates", side_effect=lambda dates, rates, window: (rates, dates)
)
@patch(
    "flazzy.plot.compute_percentage_changes", return_value=["+0.0%" for _ in range(10)]
)
def test_generate_and_save_plot(
    mock_pct,
    mock_smooth,
    mock_console,
    mock_close,
    mock_savefig,
    mock_expanduser,
    mock_makedirs,
    dummy_data,
):
    generate_and_save_currency_plot("USD", "EUR", dummy_data)

    mock_makedirs.assert_called_once_with("/tmp/test-plots", exist_ok=True)

    args, _ = mock_savefig.call_args
    assert args[0].startswith("/tmp/test-plots/usd_eur_")
    assert args[0].endswith(".png")

    mock_console.assert_called()
