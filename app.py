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
import credentials
import json
import sqlite3


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
    try:
        db = x.db()
        # show newest items first = DESC
        q = db.execute("SELECT * FROM items ORDER BY item_created_at DESC LIMIT 0, ?", (x.ITEMS_PER_PAGE,))
        items = q.fetchall()
        is_logged = False
        user = None
        role = None  

        try:    
            user_pk = x.validate_user_logged()
            if (user_pk != None):
                db = x.db()
                q = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,))
                user = q.fetchone()
                is_logged = True
                role = user['user_role'] if user else None  # Set role when u are logged in
        except:
            pass

        # find owner of the items in the db
        items = db.execute("""
        SELECT items.*, users.user_username AS owner_name, users.user_role AS owner_role
        FROM items
        JOIN users ON items.item_owner_fk = users.user_pk
        """).fetchall()

        return template("index.html", items=items, is_logged=is_logged, mapbox_token=credentials.mapbox_token, role=role)
    except Exception as ex:
        ic(ex)
        return ex
    finally:
        if "db" in locals(): db.close()

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
    response.add_header("Pragma", "no-cache")  
    response.status = 303
    response.set_header('Location', '/login')
    

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
@get("/images/<item_image>")
def _(item_image):
    return static_file(item_image, "images")

##############################
@get("/<file_name>.js")
def _(file_name):
    return static_file(file_name+".js", ".")



##############################
#if you have deleted your account as a user you can restore your profile here 
@get("/profile/restore/<user_pk>")
def _(user_pk):
    try:
        db = x.db()
        db.execute("UPDATE users SET user_deleted_at = 0 WHERE user_pk = ?", (user_pk,))
        db.commit()
        redirect("/login")
        # HTTPResponse ensures that the call will not be handelet as an error
    except HTTPResponse:
        raise
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals():
            db.close()

##############################
@post("/login")
def _():
    try:    
        user_email = x.validate_email()
        user_password = x.validate_password()
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? LIMIT 1", (user_email,))
        user = q.fetchone()
        if not user: raise Exception("user not found", 400)
        ic("user: ", user)
        
        # check user and validate if deleted or not verified
        if user:
            if not bcrypt.checkpw(user_password.encode(), user["user_password"]): raise Exception("Invalid credentials", 400)
            if user["user_is_verified"] != 1:
                return """
        <template mix-target="main" mix-replace>
            template "not_verified.html"
        </template>
        <template mix-redirect="/not_verified">
        </template>
        """
            if user["user_deleted_at"] != 0: 
                ic("user previously deleted")
                return f"""
                    <template mix-target="main">
                        <div>
                            <h2>This profile has been previously deleted</h2>
                            <a href="/profile/restore/{user['user_pk']}" style="color: blue; text-decoration: underline;">Click here to restore it!</a>
                        </div>
                    </template>
                """
            
            else:
                user.pop("user_password") # Do not put the user's password in the cookie
                ic(user)

                # Set the user cookie
                response.set_cookie("user", user["user_pk"], secret="my_secret_cookie", secure=x.is_cookie_https)
        if 'user_role' in user:
            response.set_cookie("role", user['user_role'], secret='my_secret_cookie')
        return """
            <template mix-redirect="/profile">
            </template>
        """
    except Exception as ex:
        try:
            ic(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                {ex.args[0]}
            </div>
            </template>
            """
        except Exception as ex:
            ic(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()

###"###################################################
@get("/profile")
def _():
    try:
        x.no_cache()
        user_pk = request.get_cookie("user", secret="my_secret_cookie")
        db = x.db()
        # Fetch the single user from the db
        user = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,)).fetchone()
        if user is None:
            raise Exception("No user found with the provided primary key")
        # Fetch all users from the database
        all_users = db.execute("SELECT * FROM users").fetchall()
        
        if user['user_role'] == 'partner':
            return template("profile_partner.html", is_logged=True, user=user, role=user['user_role'])
        elif user['user_role'] == 'admin':
            return template("profile_admin.html", is_logged=True, user=user, users=all_users, role=user['user_role'])
        else:
            return template("profile_customer.html", is_logged=True, user=user, role=user['user_role'])
    except Exception as ex:
        ic(ex)
        response.status = 303 
        response.set_header('Location', '/login')
        return
    
##############################

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
            ic("email verification sent")
                
        except Exception as ex:
            ic(ex, "email verification not sent")
        finally:
            if "db" in locals(): db.close()

        return f"""
        <template mix-target="main" mix-replace>
            template{"__form_login.html"}
        </template>
        <template mix-redirect="/success">
        </template>
        """
    #except Exception as ex:
    #    try:
    #        ic(ex)
    #        response.status = ex.args[1]
    #        return f"""
    #        <template mix-target="#toast">
    #            <div mix-ttl="5000" class="error">
    #            {ex.args[0]}
    #            </div>
    #        </template>
    #        """

    except ValueError as ve:
            ic(ve)
            if "user_email" in str(ex): 
                return f"""
                <template mix-target="#message">
                    {ex.args[0]}
                </template>
                """
            
    except Exception as ex:
            ic(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="3000" class="error">
                   System under maintainance
                </div>
            </template>
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
        ic(ex)
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
        x.reset_password_email(user_email, "ssimone12@gmail.com", user["user_pk"])
        return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="ok">
                    Password email has been sent. Please check your email.
                </div>
            </template>
            """

    except Exception as ex:
        ic(ex, "reset password email not sent")
    finally:
        if "db" in locals(): db.close()

##############################
@get("/update-password/<id>")
def _(id):
    try:
        return template("update_password.html", id=id)
    except Exception as ex:
        ic(ex)

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
        
        ic("Salt :")
        ic(salt)
        
        ic("Hashed")
        ic(hashed)    

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
            <div class="text-center mt-4">
                <h1 class="text-2xl font-bold ">Hello {user_first_name}</h1>
                <p>The password has been changed</p>
                <a class="text-blue-600 underline" href="/login">Go to login</a>
            </div>
        </body>
        </html>
        
        """
           
    except Exception as ex:
        try:
            ic(ex)
            response.status = ex.args[1]
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                    {ex.args[0]}
                </div>
            </template>
            """
        except Exception as ex:
            ic(ex)
            response.status = 500
            return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()


########### EDIT USER ###################
@put("/update-user")
def _():
    updated_user = None
    try:
        user_pk = x.validate_user_logged()
        user_email = x.validate_email()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_updated_at = int(time.time())

        db = x.db()
        db.execute("UPDATE users SET user_email = ?, user_username = ?, user_first_name = ?, user_last_name = ?, user_updated_at = ? WHERE user_pk = ?", ( user_email, user_username, user_first_name, user_last_name, user_updated_at, user_pk))
        db.commit()        

        updated_user = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,)).fetchone()

        ic(updated_user)

        #sending a cookie named user with the updated user and securing that it is only accesable by the server and not javascript/client side
        try:
            is_cookie_https = True
            response.set_cookie("user", str(updated_user['user_pk']), secret="my_secret_cookie", httponly=True, secure=is_cookie_https)
        except Exception as ex:    
            ic(ex)
    finally:
        if "db" in locals(): db.close()
        try:
            # script is for the trouble with showing the toast and redirecting to profile
            if (updated_user != None):
                x.send_profile_updated_email(user_email, "ssimone12@gmail.com")
                return """
                <template mix-target="#toast">
                    <div mix-ttl="5000" class="ok">
                        Your profile has been updated.
                    </div>
                </template>
                
                <script>
                    setTimeout(function() {
                        window.location.href = "/profile";
                    }, 3000);
                </script>
                """
            # HTTPResponse ensures that the call will not be handelet as an error
        except HTTPResponse:
            raise




############# DELETE USER #################
@get("/delete-user")
def _():
    try:
        user = x.validate_user_logged()
       
        return template("delete_user.html")
    except Exception as ex:
        ic(ex)
        response.status = 303 
        response.set_header('Location', '/login')
    finally:
        pass

##############################    
@put("/delete-user")
def _():
    user_deleted = None
    try:
        user_pk = x.validate_user_logged()
        user_password = x.validate_password()

        ic(user_pk)

        # delete user by id
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,))
        logged_user = q.fetchone()
        db.commit() 
        ic("my user", logged_user) 

        if not bcrypt.checkpw(user_password.encode(), logged_user["user_password"]): raise Exception("Invalid credentials", 400)
    
        #set user_deleted_at to the current time
        db.execute("UPDATE users SET user_deleted_at = ? WHERE user_pk = ?", (int(time.time()), user_pk))
        db.commit()

        response.delete_cookie("user")

        user_deleted = True

        if (user_deleted == True):
            x.send_profile_deleted_email(logged_user['user_email'], "ssimone12@gmail.com")
            return """
            <template mix-target="#toast">
                <div mix-ttl="5000" class="ok">
                    Your profile has been deleted.
                </div>
            </template>
            <template mix-redirect="/login"></template>
            """
    except Exception as ex:
        ic(ex)
        return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                    {ex} Try again.
                </div>
            </template>
        """

    finally:
        if "db" in locals(): db.close()



###½########## MORE ITEMS ##################
@get("/items/page/<page_number>")
def _(page_number):
    try:
        db = x.db()
        next_page = int(page_number) + 1
        offset = (int(page_number) - 1) * x.ITEMS_PER_PAGE
        q = db.execute(f"""     SELECT * FROM items 
                                ORDER BY item_created_at 
                                LIMIT ? OFFSET {offset}
                        """, (x.ITEMS_PER_PAGE,))
        items = q.fetchall()

        is_logged = False
        user_role = None
        user_pk = x.validate_user_logged()
        q = db.execute("SELECT * FROM users WHERE user_pk = ?", (user_pk,))
        user = q.fetchone()
        ic("############################### myuser")
        ic(user_pk)        
        try:
            is_logged = True
            user_role = user['user_role']
            
        except:
            pass

        html = ""
        for item in items: 
            html += template("_item", item=item, is_logged=is_logged, role=user_role)
            ic(user_role)
        btn_more = template("__btn_more", page_number=next_page)
        if len(items) < x.ITEMS_PER_PAGE: 
            btn_more = ""
        return f"""
        <template mix-target="#items" mix-bottom>
            {html}
        </template>
        <template mix-target="#more" mix-replace>
            {btn_more}
        </template>
        
        """
    except Exception as ex:
        ic(ex)
        return f"""
            <template mix-target="#toast">
                <div mix-ttl="5000" class="error">
                   System under maintainance
                </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()
       

############# BLOCK PROPERTIES #################
@put("/toggle_item_block/<item_pk>")
def _(item_pk):
    try:
       user_pk = x.validate_user_logged()
       x.validate_is_admin(user_pk, item_pk)
       item_blocked_at = int(time.time())

       db = x.db()
       db.execute("UPDATE items SET item_blocked_at = ? WHERE item_pk = ?",(item_blocked_at, item_pk))

       db.commit()

       x.send_item_blocked_unblocked_email("ssimone12@gmail.com", item_pk)

       return f"""
        <template mix-target="[id='{item_pk}']" mix-replace>

            <form id="{item_pk}">
                <button mix-data="[id='{item_pk}']" mix-put="/toggle_item_unblock/{item_pk}">
                    Unblock
                </button>
            </form>
        </template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): db.close()    


############ UNBLOCK ITEM ##################
@put("/toggle_item_unblock/<item_pk>")
def _(item_pk):
    try:
       user = x.validate_user_logged()
       x.validate_is_admin(user, item_pk)
       item_blocked_at = 0

       db = x.db()
       db.execute("UPDATE items SET item_blocked_at = ? WHERE item_pk = ?",(item_blocked_at, item_pk))
       db.commit()

       x.send_item_blocked_unblocked_email("ssimone12@gmail.com", item_pk)
       return f"""
        <template mix-target="[id='{item_pk}']" mix-replace>
            <form id="{item_pk}">
                <button mix-data="[id='{item_pk}']"  mix-put="/toggle_item_block/{item_pk}">
                    Block
                </button>
            </form>
        </template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        if "db" in locals(): db.close()    


##############################
#function to  check if it is running on pythonanywhere or local
if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
    run(host="0.0.0.0", port=80, debug=True, reloader=True, interval=0.1) 
