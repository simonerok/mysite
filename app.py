# 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

# https://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@github.com/simonerok/mysite.git

#########################
from bottle import default_app, get, post, run, template, static_file, response
import git
import os
import x
#from icecream import ic


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
        else:
          return f"""
                <html>
                <head><title>Login Success</title></head>
                <body>
                    <h1>Login was successful!</h1>
                    <script>
                        setTimeout(function() {{
                            window.location.href = '/success';
                        }}, 3000); // Redirect after 3 seconds
                    </script>
                </body>
                </html>
                """ 
    except Exception as ex:
        response.status = 500
        if len(ex.args) > 1:
            response.status = ex.args[1]
        return f"<div class='error'>{ex.args[0] if ex.args else 'Unknown error'}</div>"
    finally:
        if "db" in locals():
            db.close()


##############################
#function to run the app and check if it is running on pythonanywhere or local
if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
  run(host="127.0.0.1", port=80, debug=True, reloader=True) 
