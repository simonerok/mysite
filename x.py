from bottle import request, template, response
#from icecream import ic
import os
import sqlite3
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from icecream import ic 
import pathlib
import smtplib
import io

ITEMS_PER_PAGE = 4

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
        ic("XXXXXXXXXXXXXXXXXX db function has an error  XXXXXXXXXXXXXXXXXXXXXXXXXX")
        ic(ex)
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
    error = f"username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} characters"
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
            ic(ex)
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
        message["Subject"] = 'Reset password email'
    
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
        return ic("email reset password sent successfully!")  
    except Exception as ex:
        ic(ex)  
        response.status = 500
        return ic("Error sending reset password email.")
    
############# EMAIL PROFILE UPDATED #################
def send_profile_updated_email(to_email, from_email):
    try:
        message = MIMEMultipart()
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = 'Profile updated'
    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Updated profile</title>
                        </head>
                        <body>
                            <h1>Your profile has been updated!</h1>
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
    except Exception as ex:
        ic(ex)
        return "error"
      

############# EMAIL PROFILE DELETED #################
def send_profile_deleted_email(to_email, from_email):
    try:
        message = MIMEMultipart()
        message["To"] = to_email
        message["From"] = from_email
        message["Subject"] = 'Profile deleted'
    
        email_body= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Delete profile</title>
                        </head>
                        <body>
                            <h1>Your profile has been deleted</h1>
                           
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
    except Exception as ex:
        ic(ex)
        return "error"


############## SEND EMAIL EITHER BLOCK / UNBLOCK ############### 
def send_item_blocked_unblocked_email(from_email, item_pk):
    try:
        database = db()
        q = database.execute("SELECT * FROM items WHERE item_pk = ?",(item_pk,))
        item = q.fetchone()

        q_user = database.execute("SELECT * FROM users WHERE user_pk = ?",(item['item_owner_fk'],))
        user = q_user.fetchone()

        if item['item_blocked_at'] == 0:
            subject = 'Your property has been unblocked'
        else:
            subject ='Your property has been blocked'

        message = MIMEMultipart()
        message["To"] = from_email
        message["From"] = user['user_email']
        message["Subject"] = subject
     
        email_body_blocked= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Property has been blocked</title>
                        </head>
                        <body>
                            <h1>Your property {item['item_name']} has been blocked</h1>
                           

                        </body>
                        </html>

             """
        
        email_body_unblocked= f""" 

                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8" />
                            <meta
                            name="viewport"
                            content="width=device-width, initial-scale=1.0"
                            />
                            <title>Property has been blocked</title>
                        </head>
                        <body>
                            <h1>Your property {item['item_name']} has been unblocked by an admin</h1>
                            

                        </body>
                        </html>

             """
        

        if item['item_blocked_at'] == 0:
            email_body = email_body_unblocked
        else:
            email_body = email_body_blocked

        messageText = MIMEText(email_body, 'html')
        message.attach(messageText)
 
        email = from_email
        password = 'usfkdsdexmqjvbdb'
 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo('Gmail')
        server.starttls()
        server.login(email,password)
        from_email = from_email
        to_email  = user['user_email']
        server.sendmail(from_email,to_email,message.as_string())
 
        server.quit()
    except Exception as ex:
        ic(ex)
        return "error"
    finally: 
        if "db" in locals(): database.close()



############# CHECK IF ADMIN #################
def validate_is_admin(user_pk, item_pk):
    try:
        database = db()
        q = database.execute("SELECT * FROM items WHERE item_pk = ?", (item_pk,))
        item = q.fetchone()

        user_q = database.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,))
        user = user_q.fetchone()

        if (user['user_role'] != 'admin'):    
            if user['user_pk'] == item['item_owner_fk']:
                return True
            else:
                return False
        else:
            return True
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): database.close()    

############# CHECK IF USER IS LOGGED IN (checks for cookie named user) #################
def validate_user_logged():
    user = request.get_cookie("user", secret='my_secret_cookie')
    if user is None:
        raise Exception("user must login", 400)
    return user

############# VALIDATE USER IS LOGGED IN (cheks for cookie named id while also prevent cashing) #################    
def validate_logged():
    # Prevent logged pages from caching
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", "0")  
    user_id = request.get_cookie("id", secret ='my_secret_cookie')
    if not user_id: raise Exception("XXXXXXXXXXX user not logged XXXXXXXXX", 400)
    return user_id


############### VALIDATE USER ID ##########################

USER_ID_LEN = 32
USER_ID_REGEX = "^[a-f0-9]{32}$"

def validate_user_id():
	error = f"user_id invalid"
	user_id = request.forms.get("user_id", "").strip()      
	if not re.match(USER_ID_REGEX, user_id): raise Exception(error, 400)
	return user_id

############### VALIDATE ITEMS CREATED NAME ##########################
ITEM_NAME_MIN = 2
ITEM_NAME_MAX = 20
ITEM_NAME_REGEX = "^[a-zA-Z\s]{2,20}$"

def validate_item_name():
    error = f"name {ITEM_NAME_MIN} to {ITEM_NAME_MAX} lowercase english letters"
    item_name = request.forms.get("item_name", "").strip()
  
    if not re.match(ITEM_NAME_REGEX, item_name): raise Exception(error, 400)
    return item_name

############## VALIDATE ITEM CREATED PRICE ################

ITEM_PRICE_MIN = 0
ITEM_PRICE_MAX = 20000
ITEM_PRICE_REGEX =  "^\d{1,8}(\.\d{1,2})?$" 

def validate_item_price():


    error = f"price needs to be bwtween {ITEM_NAME_MIN} and {ITEM_NAME_MAX} "
    item_price_per_night = request.forms.get("item_price_per_night", "").strip()
    if not re.match(ITEM_PRICE_REGEX, item_price_per_night): raise Exception(error, 400)
    return item_price_per_night


############## VALIDATE ITEM CREATED IMAGES ################
ITEM_IMAGES_MIN = 1
ITEM_IMAGES_MAX = 5
ITEM_IMAGE_MAX_SIZE = 1024 * 1024 * 5 # 5MB


def validate_item_images():

        item_splash_images = request.files.getall("item_splash_images")

        print(item_splash_images)
        for image in item_splash_images:
            if pathlib.Path(image.filename).suffix.lower() == "":
                raise Exception("No image file added", 400)
                
            # Read the file into memory and check its size
            file_in_memory = io.BytesIO(image.file.read())
            if len(file_in_memory.getvalue()) > ITEM_IMAGE_MAX_SIZE:
                raise Exception("Image size exceeds the maximum allowed size of 5MB", 400)
                

            # Don't forget to go back to the start of the file if it's going to be read again later
            image.file.seek(0)

        if len(item_splash_images) == 0 or len(item_splash_images) < ITEM_IMAGES_MIN or len(item_splash_images) > ITEM_IMAGES_MAX:
            raise Exception(f"Invalid number of images, must be between {ITEM_IMAGES_MIN} and {ITEM_IMAGES_MAX}", 400)

        allowed_extensions = ['.png', '.jpg','.jpeg', '.webp']
        for image in item_splash_images:
            if not pathlib.Path(image.filename).suffix.lower() in allowed_extensions:
                raise Exception("Invalid image extension", 400)
            
        
        return item_splash_images



############# GROUP IMAGES TO MATCH THE ITEM #################
def group_images(rows):
    # Group images by item_pk
    items = {}
    ic("************* rows in x.group_images ****************")
    ic(rows)
    for row in rows:
        item_pk = row['item_pk']
        if item_pk not in items:
            items[item_pk] = {
                'item_pk': row['item_pk'],
                'item_name': row['item_name'],
                'item_price_per_night': row['item_price_per_night'],
                'item_lat': row['item_lat'],
                'item_lon': row['item_lon'],
                'item_stars': row['item_stars'],
                'item_created_at': row['item_created_at'],
                'item_updated_at': row['item_updated_at'],
                'item_images': [],
                'item_blocked_at': row['item_blocked_at'],
                'item_booked_at': row['item_booked_at']
                            }
        if row['image_url']:
            items[item_pk]['item_images'].append(row['image_url'])

    items = list(items.values())
    return items

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

