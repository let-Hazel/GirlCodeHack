from database.databases import *

def register():
    name = input("Name: ")
    surname = input("Surname: ")
    email = input("Email: ")

    identity = input("Are you using a Passport or South African ID (type 'P' for Passport or 'I' for ID): ").lower()
    if identity == "i":
        identity = input("Input your Id number: ")
    else:
        identity = input("Input your Passport number: ")

    address = input("Address: ")
    password = input("Enter a password: ")

    return create_user(identity, name, surname, email, password, address)

def log_in():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    return log_in(email, password)

def main():
    init_db()

    print("1. Login \n 2. Register")
    log = input("Enter a number: ")

    if log == "1":
        log_in()
    elif log == "2":
        register()
    else:
        print("Invalid!")

main()