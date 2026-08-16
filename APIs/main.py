# from database.databases import *
# import _json

# def register(request):
#     name = request["name"]
#     surname = request["surname"]
#     email = request["email"]
#     identity = request["identity"]
#     address = request["address"]
#     password = request["password"]

#     return create_user(identity, name, surname, email, password, address)

# def log_in(request):
#     email = request["email"]
#     password = request["password"]
#     return log_in(email, password)

# def main():
#     init_db()

#     print("1. Login \n 2. Register")
#     log = input("Enter a number: ")

#     if log == "1":
#         log_in()
#     elif log == "2":
#         register()
#     else:
#         print("Invalid!")

# if __name__ == "__main__":
#     main()

"""Optional command-line entry point for initializing the SkillLink database."""
from database.databases import init_db

if __name__ == '__main__':
    init_db()
    print('SkillLink database is ready.')