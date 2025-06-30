def convert_currency(amount: float, from_curr: str, to_curr: str, rates: dict):
    return amount * (rates[to_curr] / rates[from_curr])


def generate_exchange_pairs(data: dict):
    base = data["base"]
    rates = data["rates"]

    pairs = []

    for to_curr, rate in rates.items():
        pairs.append((base, to_curr, rate))

    return pairs
