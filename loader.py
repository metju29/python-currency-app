from utils.utils import generate_dates
from utils.web import get_rates
from utils.files import make_filename, save_data_to_file


start_date = "2025-01-01"
wanted_curriencies = ["eur", "chf", "jpy"]
rate_dates = generate_dates("2025-01-01")

for date in rate_dates:
    req_year, req_month, req_day = date
    nbp_rates = get_rates(req_year, req_month, req_day,
                          expected_currencies=wanted_curriencies)
    for currency in nbp_rates:
        currency_code = currency["code"]
        filename = make_filename(req_year, req_month, req_day, currency_code)
        save_data_to_file(currency, filename)


