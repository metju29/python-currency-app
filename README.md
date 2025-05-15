# Python Currency App

## Features

* The app retrieves up-to-date currency exchange rates from the National Bank of Poland API, providing users with reliable exchange information.
* Fetched data is saved into a local database for further processing and analysis.
* Users can browse currency rates via a simple web interface, selecting currencies and date ranges.
* The date selection form validates input, restricting the date range to the available data for the chosen currency to prevent errors.
* The template includes CSS styling, remembers previously selected dates in the form, and offers enhanced currency selection logic to improve user experience.

## Technologies

* Flask
* SQLAlchemy
* Docker
* requests

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/metju29/python-currency-app.git
   cd python-currency-app
   ```

2. Run the command to execute `loader.py`, which will fetch data from the NBP API and create the database:

   ```bash
   python loader.py
   ```

3. Build the Docker image:

   ```bash
   docker build -t currency-app .
   ```

4. Run the container:

   ```bash
   docker run -p 5000:5000 currency-app
   ```
