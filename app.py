import os
import json
from io import BytesIO
from api  import RestApiSdk
from dotenv import dotenv_values

class Client:
    def __init__(self):
        self.api = RestApiSdk('base_url') 
        self.config = dotenv_values(".env")


    def sendRequest(self):
        
        payload = {

        }
        headers = {
        'Content-Type': 'application/json'
        }

        response = self.api.post('/endpoint', data=payload, headers=headers)

     
        
        return response
