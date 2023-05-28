import requests
import json
class RestApiSdk:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get(self, endpoint, headers, params=None):
        response = requests.get(f'{self.base_url}/{endpoint}', headers=headers, params=params)
        return response.json()
    
    def post(self, endpoint, data, headers):
        response = requests.post(f'{self.base_url}/{endpoint}', json=data, headers=headers)
        
        return response.json()
