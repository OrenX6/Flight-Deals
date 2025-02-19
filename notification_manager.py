import os
import smtplib

from twilio.rest import Client

MY_EMAIL = "orenbechor6@gmail.com"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.account_sid = os.environ["TWILIO_SID"]
        self.auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(self.account_sid, self.auth_token)

        self.virtual_number = os.environ["TWILIO_VIRTUAL_NUMBER"]

        self.email_password = os.environ["EMAIL_PASSWORD"]

    def send_sms(self, data):
        """
        Sends an SMS message through the Twilio API.
        This function takes a flight_data as an input and uses the Twilio API to send an SMS from
        a predefined virtual number (provided by Twilio) to your own "verified" number.

        :param data :  The flight data content of the SMS message to be sent.
        :return: None
        """
        message = self.client.messages.create(
            body=f"Low price alert! Only {data.cheapest_price}$ to fly from "
                 f"{data.origin}({data.departure_airport_code}) to {data.destination}({data.arrival_airport_code}),"
                 f"on {data.departure_date} until {data.arrival_date}.",
            from_=self.virtual_number,
            to=os.environ["TWILIO_VERIFIED_NUMBER"],
        )

    def send_emails(self, flight_data, customers_data):
        """
        Sends an email message to each of the customer about the latest flight deals.
        :param flight_data: FlightData object that contains all the details about the flight deal.
        :param customers_data: DataFrame object that contains all the details about the customer.
        """
        for index, customer in customers_data.iterrows():
            first_name = customer["whatIsYourFirstName?"]
            email = customer["whatIsYourEmail?"]
            message = (f"Subject: Deals alert from Flight Club\n\nDear {first_name},\n"
                       f"Low price alert! Only {flight_data.cheapest_price}$ to fly from {flight_data.origin}"
                       f"({flight_data.departure_airport_code}) to {flight_data.destination}"
                       f"({flight_data.arrival_airport_code}), with {flight_data.stops} stop(s) departing on "
                       f"{flight_data.departure_date} and returning on {flight_data.arrival_date}").encode("utf8")

            with smtplib.SMTP(host="smtp.gmail.com") as smtpObj:
                smtpObj.starttls()
                smtpObj.login(user=MY_EMAIL, password=self.email_password)
                smtpObj.sendmail(from_addr=MY_EMAIL, to_addrs=email, msg=message)
