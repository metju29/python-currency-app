from pathlib import Path


def make_filename(year, month, day, currency, rates_dir_name="rates"):
    # Catalog
    current_dir = Path()
    rates_dir = current_dir / rates_dir_name.lower()
    rates_dir.mkdir(exist_ok=True)
    currency_dir = rates_dir / currency.lower()
    currency_dir.mkdir(exist_ok=True)
    
    return currency_dir / f"{year:04}_{month:02}_{day:02}.json"


def save_data_to_file(data, file_name):
    with open(f"{file_name}", "w", encoding="utf-8") as fp:
        json.dump(data, fp)