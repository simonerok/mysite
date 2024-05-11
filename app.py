# 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

# https://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@github.com/simonerok/mysite.git

#########################
from bottle import default_app, get, post, run, template, static_file, response
import git
import os
import x
#from icecream import ic

 
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
