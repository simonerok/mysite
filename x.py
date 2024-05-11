from bottle import request, response, template
from icecream import ic
import os
import sqlite3

############# FUNCTION TO MAKE DATABSE CODE INTO JSON OBJECT #################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}


############## CONNECT TO DATABASE ################
def db():
    # if Python discovers an error, it puts the error inside ex (see in terminal) 
    # finally runs always. 'locals' holds all the code inside the function, 'pass' just says to continue. 
    # The connect function is a way to make sure it is the right path in all projects both local and for deployment.
    try:
        db = sqlite3.connect(os.getcwd() + "/databases/company.db")
        db.execute("PRAGMA foreign_keys = ON")  # Tells the database to use restricted and cascading
        db.row_factory = dict_factory  # Gets JSON objects
        return db
    except Exception as ex:
        print("db function has an error")
        print(ex)
    finally:
        pass


##skelet email validation
def validate_user_email():
    user_email = request.forms.get("user_email")
    ic(user_email)
    if not user_email:
        raise Exception("user_email is empty", 400)
    if not "@" in user_email:
        raise Exception("user_email is invalid", 400)
    return user_email

##skelet password validation
def validate_user_password():
    user_password = request.forms.get("user_password")
    ic(user_password)   
    if not user_password:
        raise Exception("user_password is empty", 400)
    return user_password
