import os
import json
from io import BytesIO
from api  import RestApiSdk
from dotenv import dotenv_values

class Client:
    def __init__(self):
        
        self.config = dotenv_values(".env")
        self.api = RestApiSdk(self.config['url']) 
        self.headers = {
        'api_access_token': self.config['apikey']
        }


    def createMediaMessage(self, account_id, conversation_id, ):
        try:
            payload = {'message_type': 'incoming'}

            response = self.api.post(f'{account_id}/conversations/{conversation_id}/messages', data=payload, headers=self.headers)
            return response
        except Exception  as e:
            
            print(f"An error occurred CreateContact: {str(e)}")

            return str(e)
            

    def createMessage(self, account_id, conversation_id, message):
        try:
            payload = { 'content': message, 'message_type': 'incoming' }

            response = self.api.post(f'{account_id}/conversations/{conversation_id}/messages', data = payload, headers=self.headers)
            print(response.text)
            return response
        except Exception  as e:
            # Handle any exceptions that occur during the execution of the code
            print(f"An error occurred CreateContact: {str(e)}")

            return str(e)




 





