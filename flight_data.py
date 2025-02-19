class FlightData:
    # This class is responsible for structuring the flight data.

    def __init__(self, origin, dest, departure_date, arrival_date):
        """

        :param origin:
        :param dest:
        :param departure_date:
        :param arrival_date:
        """
        self.origin = origin
        self.destination = dest
        self.departure_date = departure_date.strftime("%Y-%m-%d")
        self.arrival_date = arrival_date.strftime("%Y-%m-%d")
        self.stops = 0  # default value that might be changed in the future

        self.departure_airport_code = None
        self.arrival_airport_code = None
        self.cheapest_price = 0  # default value that might be changed in the future

    def find_cheapest_flight(self, data: dict):
        """
        Parses flight data received from the Amadeus API to identify the cheapest flight option among
         multiple entries. also retrieve all the relevant data of the cheapest flight.

        :param data: The JSON data containing flight information returned by the API.
        """

        lowest_price = float(data["data"][0]["price"]["total"])  # total price
        flight_idx = 0
        for index, flight_offer in enumerate(data["data"][1:]):  # list of Dict objects
            price = float(flight_offer["price"]["total"])  # total price

            if price < lowest_price:
                lowest_price = price
                flight_idx = index

        # retrieve other data:
        self.departure_airport_code = data["data"][flight_idx]["itineraries"][0]["segments"][0]["departure"]["iataCode"]
        self.arrival_airport_code = data["data"][flight_idx]["itineraries"][0]["segments"][-1]["arrival"]["iataCode"]
        self.stops = len(data["data"][flight_idx]["itineraries"][0]["segments"]) - 1
        self.cheapest_price = lowest_price
        print(lowest_price)


