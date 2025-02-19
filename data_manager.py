import os
import pprint

import pandas
import requests

PRICES_END_POINT = "https://api.sheety.co/4fe5742347cd6e5cb42e639e4e5e3339/flightSearch/prices"
USERS_END_POINT = "https://api.sheety.co/4fe5742347cd6e5cb42e639e4e5e3339/flightSearch/users"

BEARER_TOKEN = os.environ["SHEETY_TOKEN"]


class DataManager:
    """
    This class is responsible for talking to the Google Sheet:
    The data represent the City, IATA code(Airport code) and Max price (return flight)

    """

    def __init__(self):
        """
        initialize the destination data.
        initialize all the customers details.

        """

        self.headers = {

            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

        self.dest_data = self.get_destinations_data()  # Dataframe object
        self.customers_data = self.get_customers_data()  # DataFrame object

    def get_destinations_data(self):
        """
        # Use the Sheety API to GET all the data in that sheet and print it out
        # columns: city, iataCode,id

        :return: Dataframe object
        """
        response = requests.get(url=PRICES_END_POINT, headers=self.headers)
        json_data = response.json()  # dict
        data = pandas.DataFrame(data=json_data["prices"])
        pprint.pp(data)

        return data

    def update_airport_code(self, airport_code, id):
        """
        Add the airport codes (IATA) for specific row.
        make a PUT request and use the row id from sheet_data
        to update the Google Sheet with the IATA codes.
        """
        update_row = {

            "price": {

                "iataCode": airport_code

            }

        }

        response = requests.put(url=f"{PRICES_END_POINT}/{id}", json=update_row, headers=self.headers)
        print(response.status_code)

    def get_customers_data(self):
        """
        :return: DataFrame object with all the customer's details.
        """
        response = requests.get(url=USERS_END_POINT, headers=self.headers)
        json_data = response.json()  # dict
        data = pandas.DataFrame(data=json_data["users"])
        pprint.pp(data)

        return data
