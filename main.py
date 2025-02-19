# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
# to achieve the program requirements.

import time
from datetime import date, timedelta

from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager

# Set your origin airport and city name:
ORIGIN_CITY_IATA = "MAD"
ORIGIN_CITY = "Madrid"

# Set your departure date and arrival date:
FROM_DATE = date.today() + timedelta(days=7)
TO_DATE = FROM_DATE + timedelta(days=7)

# setting variables:
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# get the destination data as Dataframe:
sheet_data = data_manager.dest_data

for index, row_data in sheet_data.iterrows():  # row_data is Series object
    city_code = row_data["iataCode"]
    destination = row_data["city"]
    if city_code == "":
        row_id = row_data["id"]
        airport_code = flight_search.get_airport_code(destination)
        data_manager.update_airport_code(airport_code, row_id)

    data = flight_search.check_flights(origin_city_code=ORIGIN_CITY_IATA, dest_city_code=city_code,
                                       from_date=FROM_DATE, to_date=TO_DATE, is_direct=True)

    if data:  # no server error or client error
        if not data["data"]:  # empty data
            print(f"No direct flights found to {destination}. Looking for indirect flights..")
            data = flight_search.check_flights(origin_city_code=ORIGIN_CITY_IATA, dest_city_code=city_code,
                                               from_date=FROM_DATE, to_date=TO_DATE, is_direct=False)
        if data:  # data exists !

            flight_data = FlightData(ORIGIN_CITY, destination, FROM_DATE, TO_DATE)
            flight_data.find_cheapest_flight(data)
            # notification_manager.send_sms(flight_data)
            notification_manager.send_emails(flight_data, data_manager.customers_data)
        print(data)

    # Slowing down requests to avoid rate limit
    time.sleep(2)
