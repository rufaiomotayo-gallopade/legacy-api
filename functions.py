from dotenv import load_dotenv, find_dotenv
from hubspot3 import Hubspot3
import os
import hubspot
from pprint import pformat, pprint
from hubspot.crm.companies import ApiException


load_dotenv()

API_KEY = os.getenv("API_KEY")



client = hubspot.Client.create(api_key=API_KEY)


def get_company_info(company_id):
    # 8959128878
    
    try:
        api_response = client.crm.companies.basic_api.get_by_id(company_id=company_id, archived=False)
        #pprint(api_response)
        formatted_api_response = pformat(api_response)
        #print(formatted_api_response)
        l = pformat(api_response).find("name")
        r = pformat(api_response).find(",",l)
        formatted_api_response = formatted_api_response[l:r]
        x = formatted_api_response.find(" ",)
        print("Company Name: "+ formatted_api_response[x+2:-2])

    # assoictaions stuff
        formatted_api_response = pformat(api_response)
        l = pformat(api_response).find("associations")
        r = pformat(api_response).find(",",l)
        formatted_api_response = formatted_api_response[l:r]
        x = formatted_api_response.find(" ",)
        print("The number of associations is: "+ formatted_api_response[x+1:])
    except ApiException as e:
        print("Exception when calling basic_api->get_by_id: %s\n" % e)