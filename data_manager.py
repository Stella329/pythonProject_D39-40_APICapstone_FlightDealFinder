# gg sheet: https://docs.google.com/spreadsheets/d/1zDVwTbfBexzE4-DLUz-sJKlQ4XBS5GNDfkZmY38UgNg/edit?gid=488826983#gid=488826983

import os
from dotenv import load_dotenv
import requests
import pprint

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.read_env()
        self.endpoint = os.getenv('Sheety_endpoint')
        self.token = os.getenv('Sheety_TOKEN')
        self.header = {
            'Authorization': f'Bearer {self.token}',
        }

        self.data = self.get_data()

    def read_env(self):
        load_dotenv("E:\\Stella\\PythonProjectFiles\\EnvVar.env", verbose=True)


    def get_data(self): ##GET
        response = requests.get(url=self.endpoint, headers=self.header)
        response.raise_for_status()
        self.data = response.json()['flightdeal']
        # pprint.pprint(self.data)
        return self.data
        ## self.data:
# [{'city': 'San Francisco',
#  'iataCode': 'SFO',
#  'id': 2,
#  'lowestPrice': 2018.2442961200002},
# {'city': 'Paris', 'iataCode': 'PAR', 'id': 3, 'lowestPrice': 419.173815348},
# {'city': 'Istanbul',
#  'iataCode': 'IST',
#  'id': 4,
#  'lowestPrice': 737.4354158900001}, {}, ...]



    def edit_row(self, id, column_name, content): ##PUT: https://api.sheety.co/phill/myWebsite/emails/2 --2为id，代表row
        '''aim: 一次改一列,对应一个id
        error handling: 是否存在该单元格'''

        sheet_input ={
            'flightdeal':{
                column_name: content,
            }
        }

        response = requests.put(url=f'{self.endpoint}/{id}', headers=self.header, json=sheet_input)
        print(response.status_code)
        print(f'sheet_editRow_response: {response.text}')


    def empty_cell_check(self, column_name):
        '''aim: Error Handling,防止cell（即改column下key-value)不存在
        method: 轮询'column_name'栏，筛选出空值（校验：填充‘EMPTY’）'''
        for row in self.data:
            id = row['id']

            try:  ## --尝试后发现：如'iataCode'连续为空，后续row中将不带此key；以下codes为解决这个问题：
                cell = row[column_name]
            except KeyError:
                print('KeyError')
                self.edit_row(id, column_name, 'EMPTY')
            else:
                if cell == '':
                    self.edit_row(id, column_name, 'EMPTY')
                    print('done')
