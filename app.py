import os
import json
from io import BytesIO
from api  import RestApiSdk
from dotenv import load_dotenv

class Client:
    def __init__(self):
        self.api = RestApiSdk('base_url') 
        load_dotenv()



    def sendRequest(self):
        
        payload = {

        }
        headers = {
        'Content-Type': 'application/json'
        }

        response = self.api.post('/endpoint', data=payload, headers=headers)

        # print(response)
        
        return response
