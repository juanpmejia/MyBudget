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


######----CATEGORY FUNCTIONS----#####

def validCategory(name, userEmail = None,  groupId = None):
    """
    Checks if the given category is valid for registration
    """
    db = Database()
    return False if db.readCategory(name, userEmail, groupId) else True

def validCategoryForm(form, userEmail=None, groupId=None):
    """
    Checks if the given form is valid for category registration
    """
    print("Super formulariop")
    print(form, "Formulario")
    return validCategory(form["Category"], userEmail = userEmail, groupId = groupId)

def createCategory(form, userEmail=None, groupId=None):
    """
    Creates a category in the database. 
    NOTE: YOU SHOULD CHECK IF THE CATEGORY ALREADY EXISTS BEFORE CALLING THIS FUNCTION
    """
    
    name = form['Category']
    description = form['descrip']
    
    print("email", userEmail)
    db = Database()
    
    categoryData = {"userEmail": userEmail,
                    "groupId" : groupId,
                    "name": name,
                    "description": description,
                    "totalCost": 0
    }

    db.createCategory(**categoryData)
    

def getCategories(userEmail=None, groupId=None):
    """
    Gets a list of categories of the user with the given userEmail
    """
    
    db = Database()
    if(userEmail):
        return db.readCategoriesByUserEmail(userEmail)
    elif(groupId):
        return db.readCategoriesByGroupId(groupId)
    
######----INCOME FUNCTIONS----#####

def createIncome(form, userEmail=None, groupId=None):
    """
    Creates an income for the given userEmail or groupId on the database
    """
    db = Database()
    creationDate = datetime.datetime.now()
    value = form["value"]
    description = form["descrip"]
    
    if(userEmail):
        return db.createIncome(creationDate, form["value"], description, userEmail=userEmail)
    elif(groupId):
        return db.createIncome(creationDate, form["value"], description, groupId=groupId)
    
def readIncomes(userEmail=None, groupId=None):
    """
    Reads the expenses from the database using the given userEmail or groupId
    """
    db = Database()
    return db.readIncomes(userEmail, groupId)
        
######----EXPENSE FUNCTIONS----#####

def validExpense(form, userEmail=None, groupId=None):
    """
    Checks if it's valid to create a expense with the given category and userEmail or groupId
    """
    db = Database()
    creationDate = datetime.datetime.now()
    value = form["Expense"]
    description = form["descrip"]
    categoryName = form["cat"]
    
    ans = True
    if(userEmail):
        if(db.readCategory(categoryName, userEmail)):
            ans = True
        else:
            ans = False
    elif(groupId):
        if(db.readCategory(categoryName, groupId = groupId)):
            ans = True
        else:
            ans = False
    else:
        ans = False
        
    return ans


def createExpense(form, userEmail=None, groupId=None):
    """
    Creates an expense for the given userEmail or groupId on the database
    """
    db = Database()
    creationDate = datetime.datetime.now()
    value = form["Expense"]
    description = form["descrip"]
    categoryName = form["cat"]

    if(userEmail):
        return db.createExpense(categoryName, creationDate, value, description, userEmail=userEmail)
    elif(groupId):
        return db.createExpense(categoryName, creationDate, value, description, groupId=groupId)


def readExpenses(category, userEmail=None, groupId=None):
    """
    Reads the expenses from the database using the given userEmail or groupId
    """
    db = Database()
    return db.readExpenses(category, userEmail, groupId)


######----GROUP FUNCTIONS----#####

def validGroup(owner, form):
    """
    Returns True if a group is valid for creation. False otherwise.
    """
    db = Database()
    return False if db.readGroupBySubject(owner, form['subject']) else True


def createGroup(owner, form):
    """
    Creates a group for the given owner in the database.
    
    NOTE: YOU SHOULD CHECK IF THE GIVEN GROUP ALREADY EXISTS BEFORE
    """
    db = Database()
    
    groupData = {
        "owner" : owner,
        "subject" : form["subject"],
        "description" : form["descrip"],
        "budget" : 0
    }
    db.createGroup(**groupData)

def readGroups(owner):
    """
    Gets groups for a given owner
    """
    db = Database()
    
    return db.readGroups(owner)

def readGroupById(groupId):
    """
    Gets a group by its id
    """
    db = Database()
    
    return db.readGroupById(groupId)