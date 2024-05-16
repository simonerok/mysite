from bottle import request, template, response
#from icecream import ic
import os
import sqlite3
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        db = sqlite3.connect(os.getcwd() + "/database/company.db")
        db.execute("PRAGMA foreign_keys = ON")  # Tells the database to use restricted and cascading
        db.row_factory = dict_factory  # Gets JSON objects
        return db
    except Exception as ex:
        print("XXXXXXXXXXXXXXXXXX db function has an error  XXXXXXXXXXXXXXXXXXXXXXXXXX")
        print(ex)
    finally:
        pass


################## EMAIL VALIDATION ############################
EMAIL_MAX = 100
EMAIL_REGEX = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_email():
    error = f"email invalid"
    user_email = request.forms.get("user_email", "").strip()
    if not re.match(EMAIL_REGEX, user_email): raise Exception(error, 400)
    return user_email

################# PASSWORD VALIDATION ############################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"
    user_password = request.forms.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error, 400)
    return user_password


################ USER NAME VALIDATION ##############

USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^[a-zA-Z]{2,20}$"

def validate_user_username():
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} lowercase english letters"
    user_username = request.forms.get("user_username", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(error, 400)
    return user_username

############# FIRST NAME VALIDATION #################

USER_NAME_MIN = 2
USER_NAME_MAX = 20


def validate_user_first_name():
    error = f"name {USER_NAME_MIN} to {USER_NAME_MAX} characters"
    user_first_name = request.forms.get("user_first_name", "").strip()
    if not re.match(USER_USERNAME_REGEX, user_first_name): raise Exception(error, 400)
    return user_first_name

##############################

LAST_NAME_MIN = 2
LAST_NAME_MAX = 20


def validate_user_last_name():
  error = f"last_name {LAST_NAME_MIN} to {LAST_NAME_MAX} characters"
  user_last_name = request.forms.get("user_last_name").strip()
  if not re.match(USER_USERNAME_REGEX, user_last_name): raise Exception(error, 400)
  return user_last_name

############# USER ROLE VALIDATION #################
CUSTOMER_ROLE = "customer"
PARTNER_ROLE = "partner"

def validate_user_role():
    user_role = request.forms.get("user_role", "").strip()
    error = f"The role ###{user_role}### is invalid. Must be {CUSTOMER_ROLE} or {PARTNER_ROLE}"
    if user_role != CUSTOMER_ROLE and user_role != PARTNER_ROLE:
        raise Exception(error, 400)
    return user_role