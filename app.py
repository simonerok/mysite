# 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

# https://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@github.com/simonerok/mysite.git

#########################
from bottle import default_app, get, post, run, template, static_file, response
import git
import os
import x
from icecream import ic

 
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
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        db = x.db()
        q = db.execute("SELECT * FROM users WHERE user_email = ? AND user_password = ?", (user_email, user_password))
        user = q.fetchone()
        if not user: raise Exception("user not found", 400)
        ic(user)
        return f"""
        <template mix-redirect="/success">
        </template>
        """
    except Exception as ex:
        response.status = ex.args[1]
        return f"""
        <template>
            <div mix-ttl="3000" class="error">
                {ex.args}
            </div>
        </template>
        """
    finally:
        if "db" in locals(): db.close()

############# CONNECT TO PYTHONANYWHERE #################
@post('/secret_url_for_git_hook')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""
 
##############################

if "PYTHONANYWHERE_DOMAIN" in os.environ:
    application = default_app()
else:
  run(host="127.0.0.1", port=80, debug=True, reloader=True) 