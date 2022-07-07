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

def list_companies():
    company_list = data_to_dict()    
    for key, value in (company_list).items():
        print(key, ' - ', value)
   
def get_name(id):
    url = "https://api.hubapi.com/companies/v2/companies/"+ str(id)
    querystring = {"hapikey":API_KEY}
    headers = {
        'Content-Type': "application/json"
        }
    response = requests.get(url=url, params = querystring)
    response = response.text # makes response searchable
    x = response.find('"name":{"value":"') #looks for name in response and finds value it starts
    snippet = response[x:(x+150)] # encompasses area of response where name should be located
    company_name = snippet[17:snippet.find('","')] # filters thru snippet to get company name
    return company_name

def load_to_text(companies):
    with open("data.txt", "r+") as data:
        for company,id in companies.items():
            line = company + '-' + str(id) + '\n'
            print(line)
            data.write(line)  
    print("Data loaded succesfully")
    data.close

def make_parent(parent_id, child_id):
    try:
        api_response = client.crm.companies.associations_api.create(
            company_id = parent_id, 
            to_object_type = "company", 
            to_object_id = child_id, 
            association_type = "13"
            )
        print("SUCCESS: ", parent_id, "is now parent to", child_id)
    except ApiException as e:
        print("Exception when calling associations_api->create: %s\n" % e)

def make_parents():
    company_list = data_to_dict()
    failed = []
    count = 0
    open('failed.txt', 'w').close() # supposed to clear text in failed.txt before starting
    print("Beginning to make parent associations")
    with open("associations.txt", 'r') as infile:
        for line in infile:
            count = count + 1
            tokens = line.strip().split('\t')
            child = tokens[0]
            try:
                parent = tokens[1] # if there is a blank entery this will not work which is why its in try except 
                print("Attempting making association (", count, "/", len(company_list), ")")
            except:
                print("ERROR: There is probably a blank entry somewhere in all_companies.txt")
            if company_list.get(parent) == None: # if parent company is not in dictionary then ...
                print("ERROR: Parent company not found in list of companies")
                failed.append(parent + " failed to become parent of " + child) # appends failure message to failed array     
            elif company_list.get(child) == None: # if child company is not in dictionary then ...
                print("ERROR: Child company not found in list of companies")
                failed.append(child + " failed to become child of " + parent) # appends failure message to failed array
            elif (isinstance(company_list.get(parent),list)) and isinstance(company_list.get(child),list): # if parent and children are both lists
                for parent_id in company_list.get(parent):
                    for child_id in company_list.get(child):
                        make_parent(parent_id,child_id) # makes association for every instance of child and parent
            elif (isinstance(company_list.get(parent),list)) and (not isinstance(company_list.get(child),list)): #if multiple instances of parent but not child
                arr = company_list.get(parent) # make an array for parent ids
                child_id = company_list.get(child)
                for parent_id in arr: #makes association for every parent in lsit
                    make_parent(parent_id, child_id)    
            elif (isinstance(company_list.get(child),list)) and (not isinstance(company_list.get(parent),list)): #if multiple instance of children but not multiple parents
                arr = company_list.get(child) # makes array for child ids
                parent_id = company_list.get(parent)
                for child_id in arr: #makes association for every child in lsit
                    make_parent(parent_id, child_id)    
            else:
                parent_id = company_list.get(parent)
                child_id = company_list.get(child)
                make_parent(parent_id, child_id)
    infile.close
    with open("failed.txt", 'w') as out:
        if failed: print("Some failures, check failed.txt for more info")
        for x in failed: # for every element in failed array
            out.write("".join(x) + "\n") # prints to failed.txt

def data_to_dict(): #takes data from txt file and returns it in a dictionary
    emptyDict = {}
    with open("all_companies.txt", 'r') as infile:
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
                    array =[]
                    array.append(curr_val) # adds current value in dictionary
                    array.append(company_id) # adds new id
                    emptyDict.update({company_name : array}) #updates dictionary with new list of ids            
            else: # if not in dictionary...
                emptyDict.update({company_name : company_id})
        else:
            emptyDict[company_name] = company_id
    return emptyDict
                