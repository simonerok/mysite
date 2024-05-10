from bottle import request, response
import pathlib
import sqlite3

############# FUNCTION TO MAKE DATABSE CODE INTO JSON OBJECT #################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}


############## CONNECT TO DATABASE ################
def db():
    # if python dicovers error it puts the eroor indside ex (see in terminal), finally runs always. locals holds all the code inside the function, pass just says to continue. The connect function is a way to make sure it is the right path in all project both local and for the deployment.
    try: 
        db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/database/company.db")
        db.execute( "PRAGMA foreign_keys = ON") # Tels the database to use restricted and cascading 
        db.row_factory = dict_factory # Gets json obejcts
        
        return db
    except Exception as ex:
        print("db function has an error")
        print(ex)
    finally: 
       pass
