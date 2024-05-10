from bottle import request, response
import pathlib
import sqlite3

############# MAKING DATABSE CODE TO JSON OBJECT #################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}


############## CONNECT TO DATABASE ################
def db():
    db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/company.db")  
    db.row_factory = dict_factory
    return db

