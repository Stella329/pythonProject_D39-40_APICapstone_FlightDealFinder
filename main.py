#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
#Angela's version: https://gist.github.com/TheMuellenator/150d346a928e4c5dac17005e213634bc


import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
import flight_data

DEPARTURE_CITY = 'SHA'
today = dt.datetime.now()
x=60 #去程-返程：中间相隔x天
departureDate = today + dt.timedelta(days=1)
returnDate = today + dt.timedelta(days=x)



# --SET UP SHEETY
sheety = DataManager()
sheet_data = sheety.data

#--return: [{'city': 'San Francisco',
#  #  'iataCode': 'EMPTY',
#  #  'id': 2,
#  #  'lowestPrice': 2018.2442961200002},
#  # {'city': 'Paris', 'iataCode': 'PAR', 'id': 3, 'lowestPrice': 419.173815348},
#  # {'city': 'Istanbul',
#  #  'iataCode': 'IST',
#  #  'id': 4,
#  #  'lowestPrice': 737.4354158900001},...]


#--SET UP Amadeus
flight_search = FlightSearch()
# print(flight_search.token) ## --test:toekn


# #--Check and Update iataCode for GG Sheet
# sheety.empty_cell_check('iataCode')
#
# for row in sheet_data:
#     '''check if sheet_data contains any values for the "iataCode" key. If not, pass each city name in sheet_data one-by-one, to the FlightSearch class'''
#     if row['iataCode'] == 'EMPTY':
#         city = row['city']
#         id = row['id']
#         iataCode = flight_search.get_iataCode(city)
#         sheety.edit_row(id, 'iataCode', iataCode)
#         print(f'iata={iataCode}')


# #--Check Lowest Prices for each destination; If found, update prices for GG Sheet
for row in sheet_data:
    iataCode = row['iataCode']
    lowestPrice = float(row['lowestPrice'])

    #--Search for Flight
    result = flight_search.get_flight_data(DEPARTURE_CITY, iataCode, departureDate, returnDate, 1, int(lowestPrice))
    cheapestFlight = flight_data.find_cheapest_flight(result)
    print(f'目的地机场={cheapestFlight.destination_airport}, 轮询价格={cheapestFlight.price}')
    if cheapestFlight.price != 'N/A' and cheapestFlight.price < lowestPrice:
        sheety.edit_row(row['id'], 'lowestPrice', cheapestFlight.price)



