# Amadeus Flight Search API (Free Signup, Credit Card not required) - https://developers.amadeus.com/
# Amadeus Flight Offer Docs - https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference

import os
from dotenv import load_dotenv
import requests
import datetime as dt

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def __init__(self):
        ## TO GET
        self.read_env()
        self.AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
        self.AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')

        self.flight_url = 'https://test.api.amadeus.com/v1'

        self.token_endpoint = '/security/oauth2/token'
        self.token = self.access_token()["access_token"]

        self.flightOffer_url = 'https://test.api.amadeus.com/v2'
        self.data_endpoint = '/shopping/flight-offers'

        self.iataCode_endpoint = '/reference-data/locations/cities'

    def read_env(self):
        load_dotenv('E:\\Stella\\PythonProjectFiles\\EnvVar.env', verbose=True)

    def access_token(self):
        """API: the official authorisation guide to find the endpoint for the token: https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/API-Keys/authorization/
        aim: you request a new token using your API keys for every new request"""

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
        #-- return: {'type': 'amadeusOAuth2Token', 'username': 'xx', 'application_name': 'D39-40_FlightDealFinder', 'client_id': 'xx', 'token_type': 'Bearer', 'access_token': 'xx', 'expires_in': 1799, 'state': 'approved', 'scope': ''}


    def get_iataCode(self, city):
        """API: https://developers.amadeus.com/self-service/category/destination-experiences/api-doc/city-search/api-reference
        Aim: Pass each city name in sheet_data one-by-one to the FlightSearch class to get the corresponding IATA code for that city using the Flight Search API"""
        header = {
            'Authorization': f'Bearer {self.token}'
        }

        params ={
            'keyword': city.upper(),
            'include': 'AIRPORTS'
        }
        response = requests.get(url=self.flight_url+self.iataCode_endpoint, headers=header, params=params)
        response.raise_for_status()
        data = response.json()

        """- If the city is not found in the response data (i.e., the data array is empty, leading to 
            an IndexError), it logs a message indicating that no airport code was found for the city and 
            returns "N/A".
            - If the expected key is not found in the response (i.e., the 'iataCode' key is missing, leading 
            to a KeyError), it logs a message indicating that no airport code was found for the city 
            and returns "Not Found"."""
        try:
            code = data['data'][0]['iataCode'] #--iataCode
        except IndexError:
            print(f'IndexError: No city found for {city}')
            return 'N/A'
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"
        print('get_iataCode:')
        return code

        #--data return:  { {"meta":{}, "data": [
        # {
        #   "type": "location",
        #   "subType": "city",
        #   "name": "Paris",
        #   "iataCode": "PAR",
        #   "address": {
        #     "countryCode": "FR",
        #     "stateCode": "FR-75"
        #   },...] }



    def get_flight_data(self, originLocationCode, destinationLocationCode, departureDate, returnDate, adults, maxPrice):
        '''API doc: https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference'''

        data_header = {
            'Authorization': f'Bearer {self.token}',
        }

        data_params = {
            'originLocationCode': originLocationCode,
            'destinationLocationCode': destinationLocationCode,
            'departureDate': departureDate.strftime("%Y-%m-%d"), ##Dates are specified in the ISO 8601 YYYY-MM-DD format, e.g. 2017-12-25
            'returnDate': returnDate.strftime("%Y-%m-%d"),
            'adults': adults,
            'currencyCode':'CNY',
            'nonStop': 'true',
            'maxPrice': maxPrice,
            'max':'10',
        }

        flight_search_response = requests.get(url=self.flightOffer_url+self.data_endpoint, headers=data_header, params=data_params)
        flight_search_response.raise_for_status()
        result = flight_search_response.json()

        print('get_flight_data() 结果如下:')
        return result

