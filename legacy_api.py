import functions

#functions.make_parent(8973324313, 8973418539) Fayette County Public Schools
functions.list_companies()


while True:
    user_input = input("Say something: ")
        #functions.get_company_info(input)
    if user_input == "quit":
        break
    elif user_input =="get_id":
        functions.get_id(user_input)
    else:
        print("Do sumn")

def get_id(user_input):
    functions.get_id()