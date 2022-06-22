from dotenv import load_dotenv, find_dotenv
from hubspot3 import Hubspot3
import os
import requests




#client = Hubspot3(api_key=API_KEY)

# all of the clients are accessible as attributes of the main Hubspot3 Client
# contact = client.contacts.get_contact_by_email('tayo.rufai@gallopade.com')
# contact = client.contacts.get_contact_by_email('tracy.hendrix@franklin.k12.ga.us')
# contact_id = contact['vid']

# all_companies = client.companies.get_all()

# # new usage limit functionality - keep track of your API calls
# client.usage_limits
# # <Hubspot3UsageLimits: 28937/1000000 (0.028937%) [reset in 22157s, cached for 299s]>

# client.usage_limits.calls_remaining
# # 971063
load_dotenv()

API_KEY = os.getenv("API_KEY")


import hubspot
from pprint import pformat, pprint
from hubspot.crm.companies import ApiException

client = hubspot.Client.create(api_key=API_KEY)


# # lists associations of given company
# try:
#     api_response = client.crm.companies.associations_api.get_all(company_id="8959128878", to_object_type="contacts", limit=500)
#     print(api_response)
# except ApiException as e:
#     print("Exception when calling associations_api->get_all: %s\n" % e)

def find_associations(company_id):
    # 8959128878
    try:
        api_response = client.crm.companies.basic_api.get_by_id(company_id=company_id, archived=False)
        #pprint(api_response)
        formatted_api_response = pformat(api_response)
        print("is working ??")
        print(formatted_api_response)
        l = formatted_api_response.find("associations")
        r = formatted_api_response.find(",",l)
        formatted_api_response = formatted_api_response[l:r]
        x = formatted_api_response.find(" ",)
        print("The number of associations is: "+ formatted_api_response[x+1:])
    except ApiException as e:
        print("Exception when calling basic_api->get_by_id: %s\n" % e)

find_associations(8959128878)
# if contact:
#     print("somethign happened")
#     print(contact)