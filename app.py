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
import smtplib
import random



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
    try:
        return template("signup.html")
    except Exception as ex:
        print(f"########## {ex} ################")


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
    
        db = x.db()
        q = db.execute("INSERT INTO users (user_pk, user_username, user_first_name, user_last_name, user_email, user_password, user_role, user_created_at, user_updated_at, user_is_verified, user_is_blocked, user_deleted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '0', '0', '0', '0')", (user_pk, user_username, user_first_name, user_last_name, user_email, user_password, user_role, user_created_at))
        db.commit() 
        print("XXXXXXXXXXXXXXX user created XXXXXXXXXXX") 
  
        return redirect("/success")
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
                    <p>Error details: {ex, "XXXXXXXXXXXXXXXXXXXXXX"}</p>
                </body>
                </html>
            """
    finally:
        if "db" in locals(): db.close()



##############################
#function to run the app and check if it is running on pythonanywhere or local
if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
  run(host="127.0.0.1", port=80, debug=True, reloader=True) 
