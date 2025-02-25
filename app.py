#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
# random.randint(0, 2)

import sys
import random
import requests
import json
import logging





def main(diction):
    
    logging.info(diction)
    
    if diction['action'] == 'create_ticket':
        url = 'https://verizon-dev2.tririga.com/oslc/so/cstServiceRequestDTOCF'
        
        # action, room, location, building, description, request_class
 
        payload = json.dumps({
          "spi:action": "Create OSLC",
          "spi:cstVZIDTX": "RT12345",
          "spi:cstLocationCodeTX": diction['location_code'],
          "spi:triRequestClassTX": diction['request_class'],
          "spi:cstWorkTypeTX": "",
          "spi:cstPriorityTX": "P2",
          "spi:cstAlternateContactPhoneTX": "555-1212",
          "spi:cstRoomTX": diction['room'],
          "spi:triDescriptionTX": diction['description']
        })
        headers = {
          'Properties': 'spi:triRecordIdSY,spi:triStatusTX,spi:cstServiceRequestIdTX,spi:triUserMessageTX,spi:cstServiceRequestURLTX',
          'Content-Type': 'application/json',
          'Authorization': 'Basic d2F0c29uYXNzaXN0YW50OkJlZVNtYXJ0ZXI='
        }
         
        response = requests.request("POST", url, headers=headers, data=payload)
         
        print(response.json())
        
        return { 'message': response.json()}
    elif diction['action'] == 'get_service_request':
        
        url = "https://verizon-dev2.tririga.com/oslc/spq/cstServiceRequestQC?oslc.select=*&oslc.where=spi:triRequestIdTX=\"{0}\"".format(diction['service_request_number'])
        payload = {}
        headers = {
          'Authorization': 'Basic d2F0c29uYXNzaXN0YW50OkJlZVNtYXJ0ZXI=',
          'Cookie': 'JSESSIONID=0000918mgnDZDDN6gPaitaKYiAt:-1'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return { 'message': response.json() }
        
    elif diction['action'] == 'get_cities':

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/Anna.su%40ibm.com_dev/default/QueryCityByState.json?state=MO"
        
        payload = {}
        headers = {}
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        print(response.text)

        
    elif diction['action'] == 'ticket_information':
        url = "https://verizon-dev2.tririga.com/oslc/spq/cstServiceRequestQC?oslc.select=*&oslc.where=spi:cstRequestedForVZIDTX=%22RT12345%22"

        payload={}
        headers = {
          'Authorization': 'Basic MTYzNjc1NjpwYXNzd29yZA==',
          'Cookie': 'JSESSIONID=0000XMvuq1vRUqfKQgVffSx8YnW:-1'
        }
        
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        
        
        return_dict = {}
        return_dict['number_tickets'] = len(response.json()['rdfs:member'])
        return_dict['tickets'] = response.json()['rdfs:member']
        ticket_list = []
        
        for i in return_dict['tickets']:
            if i['spi:triRequestStatusCL'] != 'Retired':
                ticket_list.append(i['spi:triRequestIdTX'])
        return_dict['labels'] = ticket_list
        return return_dict
        
    elif diction['action'] == 'cancel_ticket':
        url = 'https://verizon-dev2.tririga.com/oslc/so/cstServiceRequestActionCF'
 
        payload = json.dumps({
          "spi:action": "Create OSLC",
          "spi:cstServiceRequestIdTX": diction['service_request_number'],
          "spi:cstActionTX": "Cancel Request"
        })
        headers = {
          'Properties': 'spi:triRecordIdSY,spi:cstServiceRequestIdTX,spi:triUserMessageTX',
          'Content-Type': 'application/json',
          'Authorization': 'Basic d2F0c29uYXNzaXN0YW50OkJlZVNtYXJ0ZXI='
        }
         
        response = requests.request("POST", url, headers=headers, data=payload)
         
        return response.json()
        
    elif diction['action'] == 'update_ticket':
        url = 'https://verizon-dev2.tririga.com/oslc/so/cstServiceRequestActionCF'
 
        payload = json.dumps({
          "spi:action": "Create OSLC",
          "spi:cstServiceRequestIdTX": diction['service_request_number'],
          "spi:cstActionTX": "Add Comment",
          "spi:triCommentTX": diction['comment']
        })
        headers = {
          'Properties': 'spi:triRecordIdSY,spi:cstServiceRequestIdTX,spi:triUserMessageTX',
          'Content-Type': 'application/json',
          'Authorization': 'Basic d2F0c29uYXNzaXN0YW50OkJlZVNtYXJ0ZXI='
        }
         
        response = requests.request("POST", url, headers=headers, data=payload)
         
        return response.json()
    else:
        return { 'message': 'INVALID'}
