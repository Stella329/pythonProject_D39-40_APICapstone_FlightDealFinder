import os
from dotenv import load_dotenv
import requests

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self.read_env()
        self.endpoint = os.getenv('Sheety_endpoint')
        self.token = os.getenv('Sheety_TOKEN')
        self.header = {
            'Authorization': f'Bearer {self.token}',
        }


    def read_env(self):
        load_dotenv("E:\\Stella\\PythonProjectFiles\\EnvVar.env", verbose=True)


    def get_row(self): ##GET
        response = requests.get(url=self.endpoint, headers=self.header)
        response.raise_for_status()
        data = response.json()['flightdeal']
        return data


    def edit_column(self, id, column_name, content): ##PUT: https://api.sheety.co/phill/myWebsite/emails/2 --2为id，代表row
        '''一次只能改一列,对应一个id'''
        sheet_input ={
            'flightdeal':{
                column_name: content,
            }
        }

        response = requests.put(url=f'{self.endpoint}/{id}', headers=self.header, json=sheet_input)
        print(response.status_code)
        print(f'sheet_input_response: {response.text}')

