from sqlalchemy import text
from utils.utils import generate_dates
from utils.web import get_rates
from utils.files import make_filename, save_data_to_file
from utils.db import open_db, close_db, make_db_table
from utils.config import load_config


# start_date = "2025-01-01"
# wanted_curriencies = ["eur", "chf", "jpy"]
# rate_dates = generate_dates("2025-01-01")

# for date in rate_dates:
#     req_year, req_month, req_day = date
#     nbp_rates = get_rates(req_year, req_month, req_day,
#                           expected_currencies=wanted_curriencies)
#     for currency in nbp_rates:
#         currency_code = currency["code"]
#         filename = make_filename(req_year, req_month, req_day, currency_code)
#         save_data_to_file(currency, filename)

config = load_config()

db_con = open_db(config)
make_db_table(db_con)

rate = {"currency": "euro", "code": "EUR", "mid": 4.3646, "date": "2024-01-24"}

insert_query = '''
INSERT INTO rates (data, currency_code, exchange_rate)
VALUES (:date, :code, :mid);
'''
try:
    db_con.execute(text(insert_query), rate)
    db_con.commit()
except:
    print("Data insert error.")

close_db(db_con)


