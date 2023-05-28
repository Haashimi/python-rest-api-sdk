
import json
from api  import RestApiSdk



def __init__(self):
    self.api = RestApiSdk('base_url') 



def sendRequest(self):
    
    payload = {

    }
    headers = {
    'Content-Type': 'application/json'
    }

    response = self.api.post('/endpoint', data=payload, headers=headers)

    # print(response)
    
    return response

