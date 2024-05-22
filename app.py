# 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

#my special URL
# https://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@github.com/simonerok/mysite.git

#########################
from bottle import default_app, get, post, run, template, static_file, response, request, redirect, HTTPResponse, put
import git
import os
import x
import bcrypt
import uuid
import time
import random
import smtplib
from icecream import ic
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




############# CONNECT TO PYTHONANYWHERE #################
@post('/secret_url_for_git_hook')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""
 
##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")


##############################
@get("/")
def _():
   return template("index.html")

##############################
@get("/signup")
def _():
        return template("signup.html")


##############################
@get("/login")
def _():
   x.no_cache()
   return template("login.html")

##############################

@get("/logout")
def _():
    response.delete_cookie("user")
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")  # Prevent caching
    response.add_header("Pragma", "no-cache")  # Prevent caching
    response.status = 303
    response.set_header('Location', '/login')
    return

##############################
@get("/success")
def _():
   return template("success.html", is_logged=True)

##############################
@get("/forgot-password")
def _():
        return template("forgot_password.html")
 
##############################
@get("/not_verified")
def _():
   return template("not_verified.html")



##############################
@get("/profile")
def _():
    try:
        x.no_cache()
        user_pk = request.get_cookie("user", secret="my_secret_cookie")
        db = x.db()

        # Fetch the user from the database
        user = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,)).fetchone()

        if user is None:
            raise Exception("No user found with the provided primary key")

        if user['user_role'] == 'partner':
            profile_template = template("profile_partner.html", is_logged=True, user=user)
        elif user['user_role'] == 'admin':
            profile_template = template("profile_admin.html", is_logged=True, user=user)
        else:
            profile_template = template("profile_customer.html", is_logged=True, user=user)

        return profile_template
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
        return




##############################
@post("/login")
def _():
    try:    
        user_email = x.validate_email()
        user_password = x.validate_password()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ?", (user_email,))
        user = q.fetchone()
        if(user):
            ic(user_password, user["user_password"])
            if not bcrypt.checkpw(user_password.encode(), user["user_password"]): raise Exception("Invalid credentials", 400)
            if(user['user_is_verified'] == 1):
                response.set_cookie("user", user["user_pk"], secret="my_secret_cookie", httponly=True, secure=x.is_cookie_https())
                redirect("/profile")
            else:
                return template("not_verified.html")
        else: 
            raise Exception("Invalid credentials", 400)
    except HTTPResponse:
        raise
    except Exception as ex:
        try:
            ic(ex)
            response.status = ex.args[1]
            return f"""
            <html>
                <body>
                    {ex.args[1]}
                </body>
                </html>
            """
        except Exception as ex:
            ic(ex)
            response.status = 500
            return  f"""
            <html>
                <body>
                    <p>system under maintenance</p>
                </body>
                </html>
            """
    finally:
        if "db" in locals(): db.close()



###############################
@post("/signup")
def _():
    try:
        user_email = x.validate_email()
        user_password = x.validate_password()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_role = x.validate_user_role()
        user_pk = str(uuid.uuid4().hex)
        user_created_at = int(time.time())

        #makes a byte string of the password
        password = user_password.encode()
        salt = bcrypt.gensalt()
        # hashed password using bcrypt
        hashed = bcrypt.hashpw(password, salt)

        #print salt and hashed password
        ic(salt)
        ic(hashed)

        try:
            db = x.db()
            q = db.execute("INSERT INTO users (user_pk, user_username, user_first_name, user_last_name, user_email, user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked, user_deleted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '0', '0', '0', '0')", (user_pk, user_username, user_first_name, user_last_name, user_email, hashed, user_role, user_created_at))
            db.commit() 
           
            x.send_email_verification(user_email, 'ssimone12@gmail.com', user_pk)
            print("email verification sent")
                
        except Exception as ex:
                print(ex, "email verification not sent")
        finally:
                if "db" in locals(): db.close()

        redirect("/success")
    except HTTPResponse:
            raise
    except Exception as ex:
            print( "signup was not successful")
            try:
                response.status = ex.args[1]
                return f"""
            <html>
                <body>
                    {ex.args[1]}
                </body>
                </html>
            """
            except Exception as ex:
                print(ex)
            response.status = 500
            return  f"""
            <html>
                <body>
                    <p>system under maintenance</p>
                </body>
                </html>
            """
    finally:
        if "db" in locals(): db.close()


############ ACTIVATE USER ##################
@get("/activate-user/<id>")
def _(id):
    try:
        db = x.db()
        q = db.execute("UPDATE users SET user_is_verified = 1 WHERE user_pk = ?", (id,))
        user_first_name = db.execute("SELECT user_first_name FROM users WHERE user_pk = ?", (id,)).fetchone()["user_first_name"]
        db.commit()

        ic(f"################################ SUCCESS #####################################")
        
        return template("activate_user.html", user_first_name=user_first_name) 
    
    except Exception as ex:
        ic(ex, "failed to activate user")
        return f"Failed to activate user {id}"
        
    finally:
        if "db" in locals(): db.close()

################## CHECK EMAIL ##########################################
@post("/check-email")
def _():
    try:
        email = x.validate_email()

        return email
        
    except Exception as ex:
        print(ex)
        return f"""

            <template mix-target="#message">
                <div>
                    Please enter a valid email
                </div>
            </template>
    
        """
    

##############################
@post("/reset-password-email")
def _():
    try:
        user_email = x.validate_email()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,))
        user = q.fetchone()
        x.reset_password_email("ssimone12@gmail.com", user_email, user["user_pk"])
        return f"{user}"
    except Exception as ex:
        print(ex, "reset password email not sent")
    finally:
        if "db" in locals(): db.close()

##############################
@get("/update-password/<id>")
def _(id):
    try:
        return template("update_password.html", id=id)
    except Exception as ex:
        print(ex)

    finally:
       pass

############ CHANGE PASSWORD ##################
@put("/update-password/<id>")
def _(id):
    try:
        
        user_password = x.validate_password()
        updated_at = int(time.time())

        # this makes user_password into a byte string
        password = user_password.encode() 
    
        # Adding the salt to password
        salt = bcrypt.gensalt()
        # # Hashing the password
        hashed = bcrypt.hashpw(password, salt)
        
        print("Salt :")
        print(salt)
        
        print("Hashed")
        print(hashed)    

        db = x.db()
        q = db.execute("UPDATE users SET user_password = ?, user_updated_at = ? WHERE user_pk = ?", ( hashed, updated_at,id))
        db.commit()    


        get_user_query = db.execute("SELECT * FROM users WHERE user_pk = ?", (id,))   
        user = get_user_query.fetchone()

        user_first_name = user["user_first_name"]
        
        return f"""
        
        <!DOCTYPE html>
        <html>
        <head>
            <title>Password Update</title>
            <style>
                .text-2xl {{ font-size: 2em; }}
                .font-bold {{ font-weight: bold; }}
                .text-blue-600 {{ color: #3182ce; }}
                .underline {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div>
                <h1 class="text-2xl font-bold">{user_first_name}</h1>
                <p>The password has been changed</p>
                <a class="text-blue-600 underline" href="/login">Go to login</a>
            </div>
        </body>
        </html>
        
        """
           
    except Exception as ex:
        try:
            print(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            print(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        pass


########### EDIT USER ###################
@put("/update-user")
def _():
    try:
        user = x.validate_user_logged()
        user_email = x.validate_email()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_updated_at = int(time.time())

        db = x.db()
        q = db.execute("UPDATE users SET user_email =?, user_username = ?, user_first_name = ?, user_last_name = ?, user_updated_at = ? WHERE user_pk = ?", ( user_email,user_username, user_first_name, user_last_name, user_updated_at, user["user_pk"]))
        db.commit()        

        updated_user = {**user, "user_email": user_email, "user_username": user_username, "user_first_name": user_first_name, "user_last_name": user_last_name, "user_updated_at": user_updated_at}

        ic("############### updated_user: ", updated_user)
        ic(updated_user)

        try:
            is_cookie_https = True
        except:
            is_cookie_https = False        
        response.set_cookie("user", updated_user, secret=x.is_cookie_https, httponly=True, secure=is_cookie_https)

        redirect(request.url)

    except Exception as ex:    
        print(ex)
    finally:
        if "db" in locals(): db.close()


############# DELETE USER #################
@get("/delete-user")
def _():
    try:
        user = x.validate_user_logged()
       
        return template("delete_user.html")
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
    finally:
        pass

##############################    
@post("/delete-user")
def _():
    try:
        user = x.validate_user_logged()
        user_password = x.validate_password()

        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user['user_email'],))
        logged_user = q.fetchone()
        
        ic(f"######################## user_password: {user_password}")
        ic(f"######################## logged_user_password: {logged_user['user_password']}")


        try:
            if not  bcrypt.checkpw(user_password.encode(), logged_user["user_password"].encode()): raise Exception("Invalid credentials", 400)
        except Exception as ex:
            if not  bcrypt.checkpw(user_password.encode(), logged_user["user_password"]): raise Exception("Invalid credentials", 400)
       
      
        db.execute("UPDATE users SET user_deleted_at = ? WHERE user_pk = ?", (int(time.time()), user["user_pk"]))
        db.commit()

        x.send_profile_deleted_email("ssimone12@gmail.com", logged_user['user_email'])

        response.delete_cookie("user")

        return """
                <template mix-target="#form_confirm_delete_user" mix-replace>
                    <h1>Your profile has been deleted</h1>
                </template>

            """
    except Exception as ex:
        print(ex)
        response.status = 303 
        response.set_header('Location', '/login')
    finally:
        if "db" in locals(): db.close()        

##############################
#function to run the app and check if it is running on pythonanywhere or local
if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
  run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0.1) 
