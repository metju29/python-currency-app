import requests


def make_query_url(year, month, day, table="A"):
    return f"https://api.nbp.pl/api/exchangerates/tables/{table}/{year:04}-{month:02}-{day:02}?format=json"


def get_rates(
        year, month, day, 
        table="A",
        expected_currencies=["eur", "usd", "chf"]):
    expected_currencies_lower = [
        element.lower()
        for element in expected_currencies
        ]

    query_url = make_query_url(year, month, day, table)
    result = requests.get(query_url)

    if result.status_code != 200:
        return []
    
    table = result.json()[0]
    rates = table.get("rates", [])
    rates_filtered = [
        rate for rate in rates
        if rate["code"].lower() in expected_currencies_lower
    ]

    return rates_filtered
