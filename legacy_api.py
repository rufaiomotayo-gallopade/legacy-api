# from tkinter import messagebox
import functions
from tkinter import *
from tkinter import filedialog
from flask import Flask
import time

# app = Flask(__name__)


def data_to_dict_handler_company():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select company file")
    print(functions.data_to_dict("company", directory))

def data_to_dict_handler_contact():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select contact file")
    print(functions.data_to_dict("contact", directory))

def data_to_dict_handler_associations():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select associations file")
    print(functions.data_to_dict("associations", directory))

def data_to_dict_handler_product():
    directory = filedialog.askopenfilename(initialdir="C:/", title="select products file")
    print(functions.data_to_dict("products", directory))

def make_parents_contacts_to_company():
    contact_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select contact file")
    company_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select company file")
    associations_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select associations file")
    functions.make_parents("contact-company", contact_directory, company_directory, associations_directory)

def make_parents_company_to_company():
    company_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select company file")
    associations_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select associations file")
    functions.make_parents("company-company", "", company_directory, associations_directory) # contact delivery is a blank string bc its not neccesary

# def import_products_handeler():
#     directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select products file")
#     functions.handle_products(directory)

def update_products_handeler():
    product_directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select file containg al products in hubspot")
    directory = filedialog.askopenfilename(initialdir=r"C:\Users\tayor\Desktop\legacy_api", title="Please select file with products you wish to import")
    functions.update_products(directory, product_directory)
    

# @app.route('/')
# def initial():
print("Started at ",(time.strftime("%H:%M:%S", time.localtime())))
root = Tk()
root.title('LUQMAN')
label1 = Label(root, text="Printing options:")
label2 = Label(root, text="Associtaion options:")
label3 = Label(root, text="Import options:")
company_print_button = Button (root, text="Print companies.xlsx", padx=25, pady=25, command=data_to_dict_handler_company)
contact_print_button = Button (root, text="Print contacts.xlsx", padx=25, pady=25, command=data_to_dict_handler_contact)
association_print_button = Button (root, text="Print association.xlsx", padx=25, pady=25, command=data_to_dict_handler_associations)
assocation_contacts_company = Button (root, text="Make parents: contact -> company", padx=25, pady=25, command=make_parents_contacts_to_company)
assocation_company_company = Button (root, text="Make Parents: company -> company", padx=25, pady=25, command=make_parents_company_to_company)
print_products = Button (root, text="Print Products", padx=25, pady=25, command=data_to_dict_handler_product)
#import_products = Button (root, text="Import Products", padx=25, pady=25, command=import_products_handeler)
update_products = Button (root, text="Import / Update Products", padx=25, pady=25, command=update_products_handeler)
quit_button = Button(root, text="EXIT", command=root.quit)

label1.grid(row=0, column=2)
company_print_button.grid(row=2, column=2)
contact_print_button.grid(row=3, column=2)
association_print_button.grid(row=4, column=2)
print_products.grid(row=5, column=2)

quit_button.grid(row=7, column=3)

label2.grid(row=0, column=4)
assocation_contacts_company.grid(row=2, column=4)
assocation_company_company.grid(row=3, column=4)

label3.grid(row=0, column=6)    
#import_products.grid(row=2, column=6)
update_products.grid(row=3, column=6)


root.mainloop() 
print("Ended at ",(time.strftime("%H:%M:%S", time.localtime())))