from bottle import request, template, response
#from icecream import ic
import os
import sqlite3
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from icecream import ic 


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
        #db.execute("PRAGMA foreign_keys = ON")  # Tells the database to use restricted and cascading
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


################# EMAIL VERIFICATION ############################
def send_email_verification(to_email, from_email, verification_id):
    try:
            message = MIMEMultipart()
            message["To"] = to_email
            message["From"] = from_email
            message["Subject"] = 'Verify email'
    

            email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Verify Email</title>
                        </head>
                        <body>
                            <h1>Please verify your account by cliking the link below</h1>
                            <a href="http://127.0.0.1/activate-user/{verification_id}">Activate account </a>
                        </body>
                        </html>

             """
 
            messageText = MIMEText(email_body, 'html')
            message.attach(messageText)
    
            email = from_email
            password = 'usfkdsdexmqjvbdb'
    
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo('Gmail')
            server.starttls()
            server.login(email,password)
            from_email = from_email
            to_email  = to_email
            server.sendmail(from_email,to_email,message.as_string())
    
            server.quit()
            response.status = 200
            return "Signup email sent successfully!"
    except Exception as ex:
            print(ex)
            response.status = 500
            return "Error sending signup email."
    finally:
            pass  
    

############# RESET PASSWORD #################
def reset_password_email(to_email, from_email, verification_id):
    try:

        message = MIMEMultipart()
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = 'Reset password'
    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Reset password</title>
                        </head>
                        <body>
                            <h1>Please click the link below to update your password</h1>
                            <a href="http://127.0.0.1/update-password/{verification_id}">update password </a>
                        </body>
                        </html>

             """
 
        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'usfkdsdexmqjvbdb'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = to_email
        ic("Attempting to send email...")
        server.sendmail(from_email,to_email,message.as_string())
        ic("Email sent.")
 
        server.quit()
        response.status = 200
        return "email reset password sent successfully!"
    except Exception as ex:
            print(ex)
            response.status = 500
            return "Error sending reset password email."
    finally:
            pass  
    

############# CHECK IF USER IS LOGGED IN #################
def validate_user_logged():
    user = request.get_cookie("user", secret='my_secret_cookie')
    if user is None:
        raise Exception("user must login", 400)
    return user

############# NO CASCHE - prevent browser from rembering login #################
def no_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)   
    


############# IS COOKIE HTTPS #################
def is_cookie_https():
     if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        return True
     else:
          return False

