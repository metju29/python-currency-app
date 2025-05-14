from datetime import datetime, timedelta
from flask import Flask, render_template
from utils.config import load_config
from utils.db import open_db, load_data_from_db, close_db, currency_list_from_db


CONFIG_FILE = "config.yaml"

# Załaduj konfigurację z pliku YAML
config = load_config(CONFIG_FILE)


app = Flask("Currency Application")


@app.route("/") # No parameters
@app.route("/rate") # No parameters
@app.route("/rate/<currency>") # Only currency
@app.route("/rate/<currency>/<start_date>") # Only currency and date from
@app.route("/rate/<currency>/<start_date>/<end_date>") # All parameters
def rate(currency="eur", start_date=None, end_date=None):
    # Today and 30 days ago
    today = datetime.now()
    today_30_days_ago = today - timedelta(days=30)

    # If arguments are missing - use calculated dates
    if not start_date:
        start_date = today_30_days_ago.strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    # Connect to the database
    db = open_db(config)
    # Fetch results
    results = load_data_from_db(db, currency, start_date, end_date)
    # Retrieve the list of currencies
    currencies = currency_list_from_db(db)
    # Close the database connection
    close_db(db)

    # Passing results to the template
    return render_template("rate.html", 
                           data=results, 
                           currencies=currencies, 
                           currency=currency, 
                           start_date=start_date, 
                           end_date=end_date
    )

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port=5000)
