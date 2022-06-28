from dotenv import load_dotenv, find_dotenv
from hubspot3 import Hubspot3
import os
import hubspot
from pprint import pformat, pprint
from hubspot.crm.companies import ApiException

load_dotenv()
API_KEY = os.getenv("API_KEY")
client = hubspot.Client.create(api_key=API_KEY)

duplicates = []

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


def list_companies():
    try:
        api_response = client.crm.companies.basic_api.get_page(limit=100, archived=False)
        #pprint(api_response)
        list_companies = get_company_name(api_response)

        while(pformat(api_response).find("after")!= -1): # implements after feature so every single compnay is listed
            after = (pformat(api_response)[pformat(api_response).find("after")+9:pformat(api_response).find(",")-1])
            api_response = client.crm.companies.basic_api.get_page(limit=100, after=after, archived=False)
            list_companies.update(get_company_name(api_response))
    except ApiException as e:
        print("Exception when calling basic_api->get_page: %s\n" % e)
        
    #print_duplicates()
    print(len(list_companies))
    #print(list)
    for key, value in list_companies.items():
        print(key, ' - ', value)



def get_company_name(api_response):
    global duplicates
    count=1
    all_companies = {

    }

    formatted_api_response = pformat(api_response)
    try:
    
        for x in range(100):
                l = formatted_api_response.find("'name': '")
                response_snippet = formatted_api_response[l:formatted_api_response.find("}",l)] # small segment of api response to filter through
                name_start = response_snippet.find(" ",)+2 # the very beginning of the string with the company name, added 2 bc formatting
                name_end=len(response_snippet)-1
                company_name = response_snippet[name_start:name_end]
               
                l = formatted_api_response.find("'id': '")
                response_snippet = formatted_api_response[l:formatted_api_response.find(",",l)]
                id_start = response_snippet.find(" ",)+2
                id_end = len(response_snippet)-1
                company_id = response_snippet[id_start:id_end]
                if company_name in all_companies:
                    duplicates.append(company_name) # adds compamny name to list of duplicates
                    #print("B4: ", all_companies.get(company_name))
                    curr_val = all_companies.get(company_name)
                    if isinstance(curr_val, list):
                        curr_val.append(company_id)
                        all_companies.update({company_name : curr_val})
                    else:  
                        array =[]
                        array.append(curr_val)
                        array.append(company_id)
                        all_companies.update({company_name : array})
                    #print("AFTER: ", all_companies.get(company_name))
                    
                    #print("ARRAY", array)
                    #print("DICTIONARY: ", all_companies.get(company_name) )
                    #add_value(all_companies, company_name, company_id)
                else:
                    all_companies.update({company_name : company_id})
                count = count +1
                #print(company_name, count)
                if count == 100: # prints loading after every 1000 contacts, just to let me know that something is happening
                    print("Loading...")
                    #print(len(all_companies))
                formatted_api_response = formatted_api_response[formatted_api_response.find("properties_with_history")+1:]
                # moves to next item in json response
    except:
        print("ERROR")
    
    return all_companies

def print_duplicates():
    global duplicates
    if duplicates:
        print("Duplicates:", duplicates,)
        print("# of duplicates: ", len(duplicates))

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
