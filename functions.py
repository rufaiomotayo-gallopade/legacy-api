from dotenv import load_dotenv, find_dotenv
from hubspot3 import Hubspot3
import os
import hubspot
from pprint import pformat, pprint
from hubspot.crm.companies import ApiException
import requests
from tkinter import *
from tkinter import filedialog
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from hubspot import HubSpot
import itertools 

load_dotenv()

client = HubSpot(access_token='pat-na1-25f38d93-dc4c-428c-b4fb-5b47217b2ea3')

def print_data():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select company file")
    company_list = data_to_dict("company", directory)    
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

def makeParent_companyToCompany(parent_id, child_id):
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

def makeParent_companyToContact(company_id, contact_id):
    try:
        api_response = client.crm.companies.associations_api.create(
            company_id = company_id, 
            to_object_type = "contact", 
            to_object_id = contact_id, 
            association_type = "2"
            )
        print("SUCCESS: ", company_id, "is now associated with", contact_id)
    except ApiException as e:
        print("Exception when calling associations_api->create: %s\n" % e)

def make_parents(x, y, contact_directory, company_directory):
    if (x == 'company') and (y == 'company'):
        company_list = data_to_dict("company", company_directory)
        failed = []
        open('failed.txt', 'w').close() # supposed to clear text in failed.txt before starting
        print("Beginning to make parent associations")
        with open("associations.txt", 'r') as infile:
            for line in infile:
                try:
                    tokens = line.strip().split('\t')
                    #print(tokens)
                    child = tokens[0]
                    #print(tokens[0])
                    parent = tokens[1] # if there is a blank entery this will not work which is why its in try except
                    #print(tokens[1])
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
                            makeParent_companyToCompany(parent_id, child_id) # makes association for every instance of child and parent
                elif (isinstance(company_list.get(parent),list)) and (not isinstance(company_list.get(child),list)): #if multiple instances of parent but not child
                    arr = company_list.get(parent) # make an array for parent ids
                    child_id = company_list.get(child)
                    for parent_id in arr: #makes association for every parent in lsit
                        makeParent_companyToCompany(parent_id, child_id)    
                elif (isinstance(company_list.get(child),list)) and (not isinstance(company_list.get(parent),list)): #if multiple instance of children but not multiple parents
                    arr = company_list.get(child) # makes array for child ids
                    parent_id = company_list.get(parent)
                    for child_id in arr: #makes association for every child in lsit
                        makeParent_companyToCompany(parent_id, child_id)    
                else:
                    parent_id = company_list.get(parent)
                    child_id = company_list.get(child)
                    makeParent_companyToCompany(parent_id, child_id)
        infile.close
        with open("failed.txt", 'w') as out:
            if failed: print("Some failures, check failed.txt for more info")
            for x in failed: # for every element in failed array
                out.write("".join(x) + "\n") # prints to failed.txt
    elif ((x == 'company') and (y == 'contact')) or ((x == 'contact') and (y == 'company')):
        company_list = data_to_dict("company", company_directory)
        contact_list = data_to_dict("contact", contact_directory)
        failed = []
        #print(contact_list)
        open('failed.txt', 'w').close() # supposed to clear text in failed.txt before starting
        print("Beginning to make parent associations")
        with open("associations.txt", 'r') as infile:
            for line in infile:
                try:
                    tokens = line.strip().split('\t')
                    #print(tokens)
                    company = tokens[0]
                    #print(tokens[0])
                    contact = tokens[1] # if there is a blank entery this will not work which is why its in try except
                    #print(tokens[1])
                except:
                    print("ERROR: There is probably a blank entry somewhere in all_companies.txt")
                if company_list.get(company) == None: # if company is not in dictionary then ...
                    print("ERROR: Company not found in list of companies")
                    failed.append("Company: "+ company + " was not found and failed to associate with " + contact) # appends failure message to failed array     
                elif contact_list.get(contact) == None: # if conatct is not in dictionary then ...
                    print("failed to get contact from contact list: ", contact, contact_list.get(contact))
                    print("ERROR: Contact not found in list of conatcts")
                    failed.append("Contact:" + contact + " was not found and failed to associate with " + company) # appends failure message to failed array
                elif (isinstance(company_list.get(company),list)) and isinstance(contact_list.get(contact),list): # if both are lists . . .
                    for contact_id in contact_list.get(contact):
                        for company_id in company_list.get(company):
                            makeParent_companyToContact(company_id, contact_id) # makes association for every instance of child and parent
                elif (isinstance(company_list.get(company),list)) and (not isinstance(contact_list.get(contact),list)): #if multiple instances of company but not contact
                    arr = company_list.get(company) # make an array for parent ids
                    contact_id = contact_list.get(contact)
                    for company_id in arr: #makes association for every parent in lsit
                        makeParent_companyToContact(company_id, contact_id)    
                elif (isinstance(contact_list.get(contact),list)) and (not isinstance(company_list.get(company),list)): #if multiple instance of contacts but not multiple companies
                    arr = contact_list.get(contact) # makes array for child ids
                    company_id = company_list.get(company)
                    for contact_id in arr: #makes association for every child in lsit
                        makeParent_companyToContact(company_id, contact_id)    
                else:
                    company_id = company_list.get(company)
                    contact_id = contact_list.get(contact)
                    makeParent_companyToContact(company_id, contact_id)
        infile.close
        with open("failed.txt", 'w') as out:
            if failed: print("Some failures, check failed.txt for more info")
            for x in failed: # for every element in failed array
                out.write("".join(x) + "\n") # prints to failed.txt
    else:
        print("Nah")

def data_to_dict(type, directory): #takes data from xlsx file and returns it in a dictionary
    print('data_to_dict has been called')
    data = {}
    #create instance of workbook
    wb = Workbook()
    if type == 'company':       
        #load exisiting work book
        wb = load_workbook(directory)
        
        # Create active worksheet
        ws = wb.active
        
        # Create variable for Columns
        column_a = ws['A'] # ids
        column_b = ws['B'] # company names

        # iterates over 3 lists and executes 
        # 2 times as len(value)= 2 which is the
        # minimum among all the three 
        for (a, b) in zip(column_a, column_b):
            try:
                if b.value in data:
                    if isinstance(data[b.value], list):
                        arr = data[b.value]
                        arr.append(a.value)
                        data.update( {b.value : arr} )
                    else:
                        arr = [data[b.value]]
                        arr.append(a.value)
                        data.update( {b.value : arr} )
                else:
                    data.update( {b.value : a.value} )
            except:
                    data.update( {b.value : a.value} )
        
    elif type == 'contact':
        #load exisiting work book
        wb = load_workbook(directory)

        # Create active worksheet
        ws = wb.active
        
        # Create variable for Columns
        column_a = ws['A']
        column_b = ws['B']
        column_c = ws['C']

        for (a, b, c) in zip(column_a, column_b, column_c):
            if b.value == None and c.value == None:
                full_name = ""
            elif b.value == None:
                full_name = c.value
            elif c.value == None:
                full_name = b.value
            else:
                full_name = b.value + " " + c.value
            try:
                if full_name in data:
                    if isinstance(data[full_name], list):
                        arr = data[full_name]
                        arr.append(a.value)
                        data.update( {full_name : arr} )
                    else:
                        arr = [data[full_name]]
                        arr.append(a.value)
                        data.update( {full_name : arr} )
                else:
                    data.update( {full_name : a.value} )
            except:
                    data.update( {full_name : a.value} )
    print(data)
    return data