import os

import requests

URL_FLIGHT_DATES = "https://test.api.amadeus.com/v1/shopping/flight-dates"
URL_CITY_SEARCH = "https://test.api.amadeus.com/v1/reference-data/locations/cities"

URL_FLIGHT_OFFERS = "https://test.api.amadeus.com/v2/shopping/flight-offers"

URL_TOKEN = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    """
    This class is responsible for talking to the Flight Cheapest Date Search API of Amadeus company.
    add the cheapest dates? "What are the cheapest dates to fly from Munich to São Paulo?"

    """

    def __init__(self):

        self.api_key = os.environ["AMADEUS_API_KEY"]
        self.api_secret = os.environ["AMADEUS_SECRET"]

        self.headers = {

            # Getting a new token every time program is run
            "Authorization": f"Bearer {self.get_access_token()}"

        }

    def check_flights(self, origin_city_code: str, dest_city_code: str, from_date, to_date, is_direct=True):
        """
        Searches for flight options between two cities on specified departure and return dates
        using the Amadeus API.

        :param origin_city_code: IATA code from which the traveler will depart
        :param dest_city_code: IATA code to which the traveler is going
        :param to_date: departure date as datetime.date object.
        :param from_date: arrival date as datetime.date object.
        :param is_direct: search Amadeus to see if there are direct/indirect flights
        :return: json data (dict) or None

        """

        flight_params = {

            "originLocationCode": origin_city_code,
            "destinationLocationCode": dest_city_code,
            "departureDate": from_date.strftime("%Y-%m-%d"),
            "returnDate": to_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "travelClass": "ECONOMY",
            "nonStop": "true" if is_direct else "false",
            "currencyCode": "USD",
            "max": 5
        }

        response = requests.get(url=URL_FLIGHT_OFFERS, params=flight_params, headers=self.headers)

        if response.status_code != 200:
            print(f"response body: {response.text}")
            print("Sorry there was a problem with the flight search server, or the request contains\n"
                  "bad syntax")
            return None

        return response.json()  # dict

    def get_airport_code(self, city_name: str) -> str:
        """
        Retrieves the IATA code for a specified city using the Amadeus Location API.


        :param city_name:  The name of the city for which to find the IATA code
        :return : airport_code:  The IATA code
        """

        city_params = {

            "keyword": city_name.upper(),
            "max": 2,
            "include": "AIRPORTS"
        }

        response = requests.get(URL_CITY_SEARCH, params=city_params, headers=self.headers)

        try:
            airport_code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"
        else:
            return airport_code

    def get_access_token(self):
        """
        Generates the authentication token used for accessing the Amadeus API and returns it.
        To request an access token you need to send a POST request (Create a new data)

        :return: str
        """
        token_params = {

            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret

        }

        response = requests.post(url=URL_TOKEN, data=token_params)

        data = response.json()
        token = data["access_token"]

        return token
