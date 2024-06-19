#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

import os
import requests
import datetime as dt
from pprint import pprint

from data_manager import DataManager
from flight_search import FlightSearch





#----SHEETY
sheety_obj = DataManager()
sheet_data = sheety_obj.get_row()
# pprint(sheet_data) #test


# for row in sheet_data:
#     '''轮询'iataCode'栏，筛选出空值（校验：填充‘EMPTY’）'''
#     id = row['id']
#     try:       ## 尝试后发现：如'iataCode'连续为空，后续row中将不带此key
#         row['iataCode']
#     except KeyError:
#         print('KeyError')
#         sheety_obj.edit_column(row['id'], 'iataCode', 'EMPTY')
#     else:
#         if row['iataCode'] == '':
#             sheety_obj.edit_column(row['id'], 'iataCode', 'EMPTY')




#TODO In main.py check if sheet_data contains any values for the "iataCode" key.
# If not, pass each city name in sheet_data one-by-one, to the FlightSearch class
# pass city name to FlightSearch
# get the result, write to Sheety (PUT)



# #----Amadeus
# today = dt.date.today()
#
# flight_search = FlightSearch()
# print(flight_search.token)
#
# search_result = flight_search.get_flight_data('SHA', 'MLE', today, 2, 2000)
# print(search_result)