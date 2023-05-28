import requests
import json
inbox_id = 2
url = "https://chat.hormuud.com/api/v1/accounts/1/"

headers = {
  'api_access_token': 'J1Vm9nD3NVPahogDSAtJgsPs'
}


def CheckCustomerExist(self, number):
        try:
            # Send a GET request to search for contacts with the given number
            rq = requests.get(f'{url}/contacts/search?q={number}', headers=headers)
            
            returnCode = rq.status_code
            responseObject = rq.json()
            
            pyload = responseObject['payload']
            returnObject = {'conatctStatus': True, 'source_id': f'00'+number}
            if len(pyload) == 1: 
                contactID = pyload[0]['id']
                returnObject['contactId'] = contactID
                returnObject['identifier'] = number
                                
                if pyload[0]['conversations_count'] == 0:         
                
                    #If conversation not exists create it and retrieve the conversationID
                    
                    conversationID =  CreateContactconversation('',number,  contactID) 
                    
                else:
                    conversationID = getConversation('',pyload[0]['id'], number) #if contacts['contact_inbox']['inbox']['id'] == 1 else 0 
                
                returnObject['conversationID'] = conversationID
                return  returnObject 
            else:
                
                name = getSubscriberInfo('', number, 'https://hsapi.hormuud.com/CCAppCustomerViewInfo') if number.startswith('25261') or number.startswith('25277') else  getSubscriberInfo('', number, 'https://hsapi.hormuud.com/CCAppCustomerViewInfo')
                contacts = CreateContact('',number, name)
                
                contactID = contacts['contact']['id']                
                conversationID = getConversation('',contactID, number) if contacts['contact_inbox']['inbox']['id'] == 2 else 0 
                
                returnObject['contactId'] = contactID
                returnObject['identifier'] = contacts['contact']['identifier']
                returnObject['conversationID'] = conversationID
                
                return returnObject
        
        except Exception as e:
            # Handle any exceptions that occur during the execution of the code
            print(f"An error occurred CheckCustomerExist : {str(e)}")
            
            return str(e)

def getConversation(self, contactId, source):
        try:
            # Send a GET request to retrieve conversations for the given contactId
            rq = requests.get(f'{url}/contacts/{contactId}/conversations', headers=headers)
            returnCode = rq.status_code
            
            if returnCode == 200:
                # Parse the response JSON
                responseObject = rq.json()
                
                payload = responseObject['payload']
                        

                if len(payload) >= 1:
                    # Iterate through the conversations
                    for pl in payload:
                        # Return the conversationID if the inbox_id matches
                        return  pl['id'] if pl['inbox_id'] == inbox_id else 0
                                            
                else:
                    # If no conversations found, create a new conversation using CreateContactconversation method
                    
                    conversationID = CreateContactconversation('',source, contactId)
                    return conversationID
        except Exception as e:
            # Handle any exceptions that occur during the execution of the code
            print(f"An error occurred getConversation: {str(e)}")
            
            return {str(e)}
    
    
    
def CreateContactconversation(self, source, contact_id):
    try:
        # Prepare the data for creating a conversation
        data = {
            "inbox_id": inbox_id,
            "contact_id": contact_id,
            "source_id": f'00'+source
        }
               
        # Send a POST request to create a conversation
        rq = requests.post(f'{url}/conversations', json=data, headers=headers)
        
        # Parse the response JSON
        responseObject = rq.json()
        
        # Extract the conversation ID from the response
        conversation = responseObject['id']
        
        # Return the conversation ID
        return conversation
    
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        print(f"An error occurred CreateContactconversation: {str(e)}")
        
        return str(e)

def CreateContact(self, contactNumber, contactName):
    try:
        # Prepare the data payload for creating a contact
        data = {
            "inbox_id": inbox_id,
            "name": contactName,
            "phone_number": f'+{contactNumber}',
            "identifier": contactNumber,
            "source_id": f'00'+contactNumber
        }

        # Send a POST request to create the contact
        rq = requests.post(f'{url}/contacts', json=data, headers=headers)

        # Parse the response JSON
        responseObject = rq.json()

        # Extract the contact ID from the response
        
        # print("responseObject v responseObject ", responseObject)
        contact = responseObject['payload']   #['contact']['id']

        # Return the contact ID
        return contact

    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        print(f"An error occurred CreateContact: {str(e)}")
        
        return str(e)
    
    

def CreateTheMessage(self,conversationID,messaage):
    try:
        date = {
                "content": messaage,
                "message_type": 1
                }
        rq = requests.post(f'{url}/conversations/{conversationID}/messages',json=date, headers=headers)   
        print("rq.text", rq.text)

        
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        print(f"An error occurred CreateContact: {str(e)}")
        
        return str(e)
        
            
    
    
    
    
    
    
    

def getToken(self):
        

        payload = "username=CCAPP@hormuud.com&password=CCapp_@2020&grant_type=password"
        headers = {'content-type': "application/x-www-form-urlencoded"}
        rq = requests.post("https://hsapi.hormuud.com/token", data = payload,headers=headers)

        # print("rq.text", rq.text)
        toJson=json.loads(rq.text)
        autoToken=toJson['access_token']
        return autoToken;

def getSubscriberInfo(self,phone_number, url): 
    
        token = getToken('');

        payload = json.dumps({
        "IsAllowedToView": "",
        "Callsub": phone_number,
        "UserID": "",
        "MacAddress": ""
        })
        headers = {
        'Authorization': 'Bearer '+token,
        'Content-Type': 'application/json'
        }
        
        response = requests.post(url, data=payload , headers=headers) if phone_number.startswith('25261') or phone_number.startswith('25277')   else requests.post(url, data=payload ,  headers = {
        'Content-Type': 'application/json'
        })
        
        data = json.loads(response.text)
        custName = data['data']['data'][0]['NAME']
        print('custName ', custName)

        return custName;

# data = getSubscriberInfo('', '252615339350', 'https://hsapi.hormuud.com/CCAppCustomerViewInfo')

# data = CheckCustomerExist('', '252615339350')

data = CreateTheMessage('', 137781, 'haaa wll')
print(data)