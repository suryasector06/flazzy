from flazzy.converter import convert_currency, generate_exchange_pairs


def test_convert_currency():
    rates = {"USD": 1.0, "EUR": 0.9, "JYP": 110.0}

    assert convert_currency(100, "USD", "EUR", rates) == 90.0
    assert convert_currency(100, "EUR", "USD", rates) == 100 / 0.9
    assert convert_currency(100, "USD", "JYP", rates) == 100 * 110


def test_generata_exchange_pair():
    data = {"base": "USD", "rates": {"EUR": 0.9, "JYP": 110}}

    expected = [("USD", "EUR", 0.9), ("USD", "JYP", 110.0)]

    assert generate_exchange_pairs(data) == expected
