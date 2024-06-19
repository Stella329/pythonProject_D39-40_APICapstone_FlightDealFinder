# Amadeus Flight Search API (Free Signup, Credit Card not required) - https://developers.amadeus.com/
# Amadeus Flight Offer Docs - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference

import os
from dotenv import load_dotenv
import requests

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        ## TO GET
        self.read_env()
        self.AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
        self.AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')

        self.flight_url = 'https://test.api.amadeus.com/'

        self.token_endpoint = 'v1/security/oauth2/token'
        self.token = self.access_token()["access_token"]

        self.flightOffer_url = 'https://test.api.amadeus.com/v2'
        self.data_endpoint = '/shopping/flight-offers'

    def read_env(self):
        load_dotenv('E:\\Stella\\PythonProjectFiles\\EnvVar.env', verbose=True)

    def access_token(self):
        ## FIRST CALL: access token

        # Ensure API credentials are loaded
        if not self.AMADEUS_API_KEY or not self.AMADEUS_API_SECRET:
            print(self.AMADEUS_API_KEY, self.AMADEUS_API_SECRET)
            raise ValueError("API key and secret must be set in environment variables.")

        token_header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token_params = {
            'grant_type': 'client_credentials',
            'client_id': self.AMADEUS_API_KEY,
            'client_secret': self.AMADEUS_API_SECRET,
        }

        flight_response = requests.post(url=self.flight_url+self.token_endpoint, headers=token_header, data=token_params)
        return flight_response.json()

    def get_flight_data(self, originLocationCode, destinationLocationCode, departureDate, adults, money):

        data_header = {
            'Authorization': f'Bearer {self.token}',
        }

        data_params = {
            'originLocationCode': originLocationCode,
            'destinationLocationCode': destinationLocationCode,
            'departureDate': departureDate,
            'adults': adults,
            'currencyCode':'CNY',
            'maxPrice': money,
        }

        flight_search_response = requests.get(url=self.flightOffer_url+self.data_endpoint, headers=data_header, params=data_params)
        flight_search_response.raise_for_status()
        return flight_search_response.json()
