from database.databases import *

init_db()

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

    create_user(id, name, surname, email, password, address)

def log_in():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    log_in(email, password)

def main():
    init_db()

    print("")