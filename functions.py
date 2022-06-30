from dotenv import load_dotenv, find_dotenv
from hubspot3 import Hubspot3
import os
import hubspot
from pprint import pformat, pprint
from hubspot.crm.companies import ApiException
import requests

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


def list_companies():
    global company_list 
    print("Started")
    after_list = []
    try:
        api_response = client.crm.companies.basic_api.get_page(limit=100, archived=False)
        #pprint(api_response)
        # company_list = get_company_name(api_response)
        #count=0
        # while(pformat(api_response).find("after")!= -1): # implements after feature so every single compnay is listed
        #     count = count+1
        #     after = (pformat(api_response)[pformat(api_response).find("after")+9:pformat(api_response).find(",")-1])
        #     after_list.append(after)
        #api_response = client.crm.companies.basic_api.get_page(limit=100, after='8834361895', archived=False)
        #     # print("Loading...")
        #     print("Completed Page ", count)
        #print(api_response)
        #company_list.update(get_company_name(api_response))
        #load_to_text(company_list)
        #make_parents()
    except ApiException as e:
        print("Exception when calling basic_api->get_page: %s\n" % e)
    company_list = data_to_dict()
    # for key, value in (company_list).items():
    #     print(key, ' - ', value)
    #print(company_list)
    # print(after_list)

def remove_space(name_with_space):
        name_with_space = ( " ".join(name_with_space.split()))
        name = name_with_space.replace((" ' '"), " ")
        return name
        
def get_company_name(api_response):
    #global duplicates
    count=1
    all_companies = {

    }

    formatted_api_response = pformat(api_response)
    try:
        for x in range(100):
                l = formatted_api_response.find("'id': '") # some number where 'id': ' is located in api response
                response_snippet = formatted_api_response[l:formatted_api_response.find(",",l)] #snippet of api response from where it says 'id' to end of id number
                id_start = response_snippet.find(" ",)+2
                id_end = len(response_snippet)-1
                company_id = response_snippet[id_start:id_end] # filters thu api response to get id number

                company_name = get_name(company_id) # calls function that uses api and id to get company name
                # line = company_name + "-" + str(company_id)
                # with open("data.txt", "r+") as data:
                #     if company_name not in data:
                # # Write it; assumes file ends in "\n" already
                #         data.write(company_name + "-" + str(company_id))
                #         all_companies.update({company_name : company_id})
                #     else:
                #         print("NAME IN DATATATATATATAT")
                if company_name in all_companies: # if the company already exists in dictionary . .. 
                    #duplicates.append(company_name) # adds compamny name to list of duplicates
                    #print("B4: ", all_companies.get(company_name))
                    curr_val = all_companies.get(company_name) # stores current value of companyname to a variable
                    if isinstance(curr_val, list): # checks if value at company_name is already a list
                        curr_val.append(company_id) # if already a list it appends id
                        all_companies.update({company_name : curr_val}) # updates the dictionary with appended list
                    else:  #if value at company name is not already list then will make into a list
                        array =[] # initializing list
                        array.append(curr_val) # adds current value in dictionary
                        array.append(company_id) # adds new id
                        all_companies.update({company_name : array}) #updates dictionary with new list of ids            
                else: # if not in dictionary...
                    all_companies.update({company_name : company_id}) #adds to dictionary
                #data.close
                formatted_api_response = formatted_api_response[formatted_api_response.find("properties_with_history")+1:] # moves to next item in json response               
    except:
        print("ERROR")
    
    return all_companies

# def print_duplicates():
#     global duplicates
#     if duplicates:
#         print("Duplicates:", duplicates,)
#         print("# of duplicates: ", len(duplicates))

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

def get_id(search):
    global company_list
    id_input = input("Enter a company Name: ")
    #print(company_list)
    if company_list[id_input]:
        print (company_list[id_input])
    else:
        print("ERROR: Not Found")

def get_name(id):
    url = "https://api.hubapi.com/companies/v2/companies/"+ str(id)

    querystring = {"hapikey":API_KEY}


    headers = {
        'Content-Type': "application/json"
        }

    response = requests.get(url=url, params = querystring)
    response = response.text

    x = response.find('"name":{"value":"')
    y = x+150
    snippet = response[x:y]
    company_name = snippet[17:snippet.find('","')]
    return company_name

def thingy():
    print()
      
def load_to_text(companies):
    # with open("hi.txt", 'w') as out:
    #     for company,id in companies.items():
    #         line = company + '-' + str(id) + '\n'


            
    #         out.write(line)
    #Open for read+write
    with open("data.txt", "r+") as data:
        for company,id in companies.items():
            line = company + '-' + str(id) + '\n'
            print(line)
            data.write(line)
        
        # for company,id in companies.items():
        #     line = company + '-' + str(id) + '\n'
        # # A file is an iterable of lines, so this will
        # # check if any of the lines in myfile equals line+"\n"
        #     if line not in data:

        #         # Write it; assumes file ends in "\n" already
        #         data.write(line + '\n')
    
    print("Data loaded succesfully")
    data.close

def make_parents():
    global company_list
    failed = []
    with open("test.txt", 'r') as infile:
        for line in infile:
            tokens = line.strip().split('\t')
            child = tokens[0]
            print("Child is: ",child)
            parent = tokens[1]
            print("parent is: ",parent)
            if company_list.get(parent) == None: # if parent company is not in dictionary then ...
                failed.append(parent + " failed to become parent of " + child) # appends failure message to failed array     
            elif company_list.get(child) == None: # if child company is not in dictionary then ...
                failed.append(child + " failed to become child of " + parent) # appends failure message to failed array
            elif isinstance(company_list.get(parent),list):
                failed.append(parent + " has multiple instances and has failed to become parent of " + child) # appends failure message to failed array
            elif isinstance(company_list.get(child),list):
                failed.append(child + " has multiple instances and has failed to become parent of " + parent) # appends failure message to failed array
            else:
                parent_id = company_list.get(parent)
                child_id = company_list.get(child)
                make_parent(parent_id, child_id)
    infile.close
    with open("failed.txt", 'w') as out:
        for x in failed: # for every element in failed array
            out.write("".join(x) + "\n") # prints to failed.txt
    #print(company_list.get("Fayette County "))

def data_to_dict():
    emptyDict = {}
    with open("everything.txt", 'r') as infile:
        for line in infile:
            tokens = line.strip().split('\t')
            #print(tokens)
            company_name = tokens[1]
            #print("Company is: ",company_name)
            company_id = tokens[0]
            #print("ID is: ",company_id)
            if emptyDict.get(company_name): # if compnay already exists
                curr_val = emptyDict.get(company_name) # stores current value of companyname to a variable
                if isinstance(curr_val, list): # checks if value at company_name is already a list
                    curr_val.append(company_id) # if already a list it appends id
                    emptyDict.update({company_name : curr_val}) # updates the dictionary with appended list
                else:  #if value at company name is not already list then will make into a list
                    array =[] # initializing list
                    array.append(curr_val) # adds current value in dictionary
                    array.append(company_id) # adds new id
                    emptyDict.update({company_name : array}) #updates dictionary with new list of ids            
            else: # if not in dictionary...
                emptyDict.update({company_name : company_id}) #adds to dictionary
        else:
            emptyDict[company_name] = company_id
    return emptyDict
                