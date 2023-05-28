import requests
import json

import random
import string
url = "https://chat.hormuud.com/api/v1/accounts/1/"
ul = "https://chat.hormuud.com/api/v1/accounts/2/contacts"

payload = {}
headers = {
  'api_access_token': 'J1Vm9nD3NVPahogDSAtJgsPs'
}


inbox_identifier = "fbGgK2tf5z19aBaMCmcHgd3R"
inbox_id = 2
# response = requests.get(url, headers=headers, json=payload)

# # response.json()
# print(response.text)

import requests

def getContacts(self, contactId):
    """
    Get the number of conversations for a contact.
    
    Args:
        self: The reference to the current instance.
        contactId (str): The ID of the contact.
        
    Returns:
        int: The number of conversations for the contact.
    """    
    try:
        response = requests.get(f'{url}/contacts/{contactId}/conversations', headers=headers)
        returnCode = response.status_code
        
        if returnCode == 200:
            responseObject = response.json()
            payload = responseObject.get('payload', [])
            # print("payload ", payload)
            return len(payload)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # Handle the error
    
    return 0  # Return 0 if an error occurs or the response is not 200


# def getContacts(self, contactId):
#         rq = requests.get(f'{url}/contacts/{contactId}/conversations',
#                           headers=headers)
#         returnCode = rq.status_code
#         if returnCode == 200:
#             responseObject = rq.json()
#             # print('responseObject ', responseObject)
#             payload = responseObject['payload']
           
#         return len(payload)
    
    
# 



def CreateContact(self, contactNumber, contactName):
    try:
        # Prepare the data payload for creating a contact
        data = {
            "inbox_id": inbox_id,
            "name": contactName,
            "phone_number": f'+{contactNumber}',
            "identifier": contactNumber,
            "source_id": contactNumber+contactName
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
  

def CreateContactconversation(self, source, contact_id):
    try:
        # Prepare the data for creating a conversation
        data = {
            "inbox_id": inbox_id,
            "contact_id": contact_id,
            "source_id": source
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
                    print("pl['inbox_id'] == inbox_id ", pl['inbox_id']  == inbox_id )
                    return  pl['id'] if pl['inbox_id'] == inbox_id else 'z'
                                         
            else:
                # If no conversations found, create a new conversation using CreateContactconversation method
                conversationID = CreateContactconversation('', source, contactId)
                return conversationID
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        print(f"An error occurred getConversation: {str(e)}")
        
        return {str(e)}
  
        

def CheckCustomerExist(self, waNumber, waname):
    try:
        # Send a GET request to search for contacts with the given waNumber
        rq = requests.get(f'{url}/contacts/search?q={waNumber}', headers=headers)
        
        returnCode = rq.status_code
        responseObject = rq.json()
        
        pyload = responseObject['payload']
        returnObject = {'conatctStatus': True, 'source_id': f'+'+waNumber + waname }
        # print("len(pyload) ", len(pyload))
        # print("payload[0]['conversations_count'] ", pyload[0]['conversations_count'])
        if len(pyload) == 1: 
            phone_number = pyload[0]['phone_number'][1:]
            contactID = pyload[0]['id']
            returnObject['contactId'] = contactID
            returnObject['identifier'] = phone_number
            
            if pyload[0]['conversations_count'] == 0:         
              
              #If conversation not exists create it and retrieve the conversationID
              conversationID =  CreateContactconversation('', phone_number + waname,  contactID) #getConversation('', contactId, phoneNumber + waname)
              returnObject['conversationID'] = conversationID
            else:
              conversationID = getConversation('', pyload[0]['id'], phone_number + waname) #if contacts['contact_inbox']['inbox']['id'] == 1 else 0 
              
              returnObject['conversationID'] = conversationID
              
            return  returnObject 
        else:
           
            contacts = CreateContact('', waNumber, waname)
            
            contactID = contacts['contact']['id']
            phone_number = contacts['contact']['phone_number']
            conversationID = getConversation('', contactID, phone_number + waname) if contacts['contact_inbox']['inbox']['id'] == 1 else 0 
            
            returnObject['contactId'] = contactID
            returnObject['identifier'] = contacts['contact']['identifier']
            returnObject['conversationID'] = conversationID
            
            return returnObject
    
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        print(f"An error occurred CheckCustomerExist : {str(e)}")
        
        return str(e)
       
                
 

# data = getContacts('',382330)
# print(contact)

# data = CheckCustomerExist('', '252615339350', 'MOHAMED MUHUDIN ABDI') 

# data = getConversation('', 381620, '252619999377'+'yahyeeeeeee')
# contact = True
# messageType = 1
# inbox_id = 2
# if contact  and messageType == 1 and inbox_id == 2:
#     print("hhhhhhhhoooooooooooooooooooooowwwwwwwwwwwwwwwwww")
# else:
#     print("aaaaaaaaaaaaaaaaaaaaa")


# print(data)