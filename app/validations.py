"""
This module makes data validations from client to server and back
"""
import hashlib
import datetime
from .database import Database

def validRegisterForm(form):
    """
    Checks if the given form is valid for user registration
    """
    print("Super formulariop")
    print(form, "Formulario")
    return validEmail(form["InputEmail"])

def validEmail(email):
    """
    Checks if the given email is already registered in the database
    """
    db = Database()
    if(db.readUserByEmail(email)):
        print("Encontre el usuario con ese email")
    else:
        print("No hay ningun usuario con ese email")
    
    return False if db.readUserByEmail(email) else True

def registeredEmail(email):
    """
    Checks if the given email is available for registration in the database
    """
    return not validEmail(email)
    
def validLogin(email,password):
    """
    Checks if the given email and password are registered in the database
    """
    
    db = Database()
    user = getUser(email)
    
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    password = m.hexdigest()
    
    return True if (user["email"]==email and user["password"]==password) else False 
    

def createUser(form):
    """
    Creates a user in the database. 
    NOTE: YOU SHOULD CHECK IF THE USER ALREADY EXISTS BEFORE CALLING THIS FUNCTION
    """
    
    db = Database()
    
    
    m = hashlib.sha256()
    m.update(form["InputPassword"].encode('utf-8'))
    
    password = m.hexdigest()
    
    userData = {"name": form["InputName"],
                "password": password,
                "email" : form["InputEmail"],
                "gender" : form["optradio"],
                "budget" : 0,
                "birthDate" : form["InputDate"]
    
    }
    
    db.createUser(**userData)

def getUser(email):
    return Database().readUserByEmail(email)
    