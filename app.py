# 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

#my special URL
# https://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@github.com/simonerok/mysite.git

#########################
from bottle import default_app, get, post, run, template, static_file, response, request, redirect, HTTPResponse
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
   return template("login.html")

##############################
@get("/success")
def _():
   return template("success.html")


##############################
@post("/login")
def _():
    try:    
        user_email = x.validate_email()
        user_password = x.validate_password()
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? AND user_password = ?", (user_email, user_password))
        user = q.fetchone()
        print(user)
        if not user: raise Exception("user not found", 400)
        redirect("/success")
    except HTTPResponse:
        raise
    except Exception as ex:
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

########## SIGNUP ##########

   


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
        
    
        try:
            db = x.db()
            q = db.execute("INSERT INTO users (user_pk, user_username, user_first_name, user_last_name, user_email, user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked, user_deleted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '0', '0', '0', '0')", (user_pk, user_username, user_first_name, user_last_name, user_email, user_password, user_role, user_created_at))
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
            print( "signup successfull")
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

        ic(f"################################  {user_first_name}   #####################################")
        
        # return f"Activated user with ID: {id}"
        return template("activate_user.html", user_first_name=user_first_name) 
    
    except Exception as ex:
        ic(ex, "failed to activate user")
        return f"Failed to activate user with ID: {id}"
        
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
#function to run the app and check if it is running on pythonanywhere or local
if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
  run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0.1) 
