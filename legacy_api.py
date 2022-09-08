import functions
from tkinter import *
from tkinter import filedialog

print("Started")


root = Tk()

def data_to_dict_handler_company():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select company file")
    functions.data_to_dict("company", directory)
    #print(functions.data_to_dict("company", directory))
    
myButton = Button (root, text="data to dic company!", padx=25, pady=25, command=data_to_dict_handler_company)
myButton.pack()

def data_to_dict_handler_contact():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select contact file")
    functions.data_to_dict("contact", directory)
    #print(functions.data_to_dict("contact", directory))
    
myButton = Button (root, text="data to dic contact!", padx=25, pady=25, command=data_to_dict_handler_contact)
myButton.pack()

def data_to_dict_handler_associations():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select associations file")
    functions.data_to_dict("associations", directory)
    
myButton = Button (root, text="data to dic associ!", padx=25, pady=25, command=data_to_dict_handler_associations)
myButton.pack()

def make_parents_contacts_to_company():
    contact_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select contact file")
    company_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select company file")
    associations_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select associations file")
    functions.make_parents("contact", "company", contact_directory, company_directory, associations_directory)
    #print(functions.data_to_dict("company", company_directory))
    
myButton = Button (root, text="Make parents contact -> company", padx=25, pady=25, command=make_parents_contacts_to_company)
myButton.pack()


root.mainloop()

#functions.data_to_dict("company")


#functions.make_parents("contact","company", directory)
#functions.list_companies()