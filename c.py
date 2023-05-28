import requests, json
def CheckCustomerExist(self, number):
            try:
                # Send a GET request to search for contacts with the given number
                rq = requests.get(f'{self.chatwootURL}/contacts/search?q={number}', headers={'api_access_token': self.apikey})
                
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
                        
                        conversationID =  self.CreateContactconversation(number,  contactID) 
                        
                    else:
                        conversationID = self.getConversation(pyload[0]['id'], number) #if contacts['contact_inbox']['inbox']['id'] == 1 else 0 
                    
                    returnObject['conversationID'] = conversationID
                    return  returnObject 
                else:
                    
                    name = self.getSubscriberInfo(number, 'https://hsapi.hormuud.com/CCAppCustomerViewInfo') if number.startswith('25261') or number.startswith('25277') else  self.getSubscriberInfo(number, 'http://10.15.40.62:89/CCAppCustomerViewInfo')
                    contacts = self.CreateContact(number, name)
                    
                    contactID = contacts['contact']['id']                
                    conversationID = self.getConversation(contactID, number) if contacts['contact_inbox']['inbox']['id'] == 2 else 0 
                    
                    returnObject['contactId'] = contactID
                    returnObject['identifier'] = contacts['contact']['identifier']
                    returnObject['conversationID'] = conversationID
                    
                    return returnObject
            
            except Exception as e:
                # Handle any exceptions that occur during the execution of the code
                LOGGER.info(f"An error occurred CheckCustomerExist : {str(e)}")
                
                return str(e)

def getConversation(self, contactId, source):
        try:
            # Send a GET request to retrieve conversations for the given contactId
            rq = requests.get(f'{self.chatwootURL}/contacts/{contactId}/conversations', headers={'api_access_token': self.apikey})
            returnCode = rq.status_code
            
            if returnCode == 200:
                # Parse the response JSON
                responseObject = rq.json()
                
                payload = responseObject['payload']
                        

                if len(payload) >= 1:
                    # Iterate through the conversations
                    for pl in payload:
                        # Return the conversationID if the inbox_id matches
                        return  pl['id'] if pl['inbox_id'] == self.inbox_id else 0
                                            
                else:
                    # If no conversations found, create a new conversation using CreateContactconversation method
                    
                    conversationID = self.CreateContactconversation(source, contactId)
                    return conversationID
        except Exception as e:
            # Handle any exceptions that occur during the execution of the code
            LOGGER.info(f"An error occurred getConversation: {str(e)}")
            
            return {str(e)}
    
            
            
def CreateContactconversation(self, source, contact_id):
    try:
        # Prepare the data for creating a conversation
        data = {
            "inbox_id": self.inbox_id,
            "contact_id": contact_id,
            "source_id": f'00'+source
        }
            
        # Send a POST request to create a conversation
        rq = requests.post(f'{self.chatwootURL}/conversations', json=data, headers={'api_access_token': self.apikey})
        
        # Parse the response JSON
        responseObject = rq.json()
        
        # Extract the conversation ID from the response
        conversation = responseObject['id']
        
        # Return the conversation ID
        return conversation
    
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        LOGGER.info(f"An error occurred CreateContactconversation: {str(e)}")
        
        return str(e)

def CreateContact(self, contactNumber, contactName):
    try:
        # Prepare the data payload for creating a contact
        data = {
            "inbox_id": self.inbox_id,
            "name": contactName,
            "phone_number": f'+{contactNumber}',
            "identifier": contactNumber,
            "source_id": f'00'+contactNumber
        }

        # Send a POST request to create the contact
        rq = requests.post(f'{self.chatwootURL}/contacts', json=data, headers={'api_access_token': self.apikey})

        # Parse the response JSON
        responseObject = rq.json()

        # Extract the contact ID from the response
        
        # print("responseObject v responseObject ", responseObject)
        contact = responseObject['payload']   #['contact']['id']

        # Return the contact ID
        return contact

    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        LOGGER.info(f"An error occurred CreateContact: {str(e)}")
        
        return str(e)
            
            

def CreateTheMessage(self,conversationID,messaage):
    try:
        date = {
                "content": messaage,
                "message_type": "incoming"
                }
        rq = requests.post(f'{self.chatwootURL}/conversations/{conversationID}/messages',json=date, headers={'api_access_token': self.apikey})   


        
    except Exception as e:
        # Handle any exceptions that occur during the execution of the code
        LOGGER.info(f"An error occurred CreateContact: {str(e)}")
        
        return str(e)
    
        
        