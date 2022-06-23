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
        api_response = client.crm.companies.basic_api.get_by_id(
            company_id=company_id, 
            archived=False
            )
        get_company_name(api_response)

    # # assoictaions stuff
    #     formatted_api_response = pformat(api_response)
    #     l = pformat(api_response).find("associations")
    #     r = pformat(api_response).find(",",l)
    #     formatted_api_response = formatted_api_response[l:r]
    #     x = formatted_api_response.find(" ",)
    #     print("The number of associations is: "+ formatted_api_response[x+1:])
    except ApiException as e:
        print("Exception when calling basic_api->get_by_id: %s\n" % e)


def list():
    try:
        api_response = client.crm.companies.basic_api.get_page(limit=5, archived=False)
        pprint(api_response)
        get_company_name(api_response)
        while(pformat(api_response).find("after")!= -1):
            #print(pformat(api_response)[pformat(api_response).find("after")+8:pformat(api_response).find(",")-1])
            after = (pformat(api_response)[pformat(api_response).find("after")+9:pformat(api_response).find(",")-1])
            # print("AFTER::::::")
            # print(after)
            api_response = client.crm.companies.basic_api.get_page(limit=100, after=after, archived=False)
            get_company_name(api_response)
    except ApiException as e:
        print("Exception when calling basic_api->get_page: %s\n" % e)


def get_company_name(api_response):
    #pprint(api_response)
    formatted_api_response = pformat(api_response)
    #print("COMPANY NAMES:")
    #print(formatted_api_response)
    for x in range(100):
        #print(formatted_api_response)
        if (pformat(api_response).find("name")):
            l = formatted_api_response.find("name")
            #print("just peeping: " + formatted_api_response[l:l+25])
            response_snippet = formatted_api_response[l:formatted_api_response.find(",",l)]
            #print()
            #print("breakpoint2:"+ response_snippet)
            name_start = response_snippet.find(" ",)
            comma_finder=response_snippet.find("}")
            print(response_snippet[name_start+2:comma_finder-1])
            formatted_api_response = formatted_api_response[formatted_api_response.find("properties_with_history")+1:]
            #print(formatted_api_response.find("properties_with_history"))
            #print()
            #print("breakpoint3:"+ formatted_api_response)
            #print("************** "+ formatted_api_response)
        else:
            print("Nah")


def make_parent(parent_id, child_id):
    try:
        api_response = client.crm.companies.associations_api.create(
            company_id = parent_id, 
            to_object_type = "company", 
            to_object_id = child_id, 
            association_type = "13"
            )
        print("SUCCESS")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling associations_api->create: %s\n" % e)
