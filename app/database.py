# coding=utf-8

"""
This module implements the necessary functions for the interaction with the 
MongoDB Atlas database.

The Atlas email is jpkratos@gmail.com and the pass is aguacate-2017

"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from collections import *
from bson.objectid import ObjectId
import datetime
class Database():
    
    
    #Default user data
    defData = { "name": "Juan Pablo Méndez",
                "password": '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                "email" : "juanpam@javerianacali.edu.co",
                "gender" : "M",
                "budget" : 123456789,
                "birthDate" : datetime.datetime(1996,6,6)
    }
    
    #Static client
    #aguacate-2017 is the password and mybudget the user
    client = MongoClient("mongodb://mybudget:aguacate-2017@cluster0-shard-00-00-qo8mp.mongodb.net:27017,cluster0-shard-00-01-qo8mp.mongodb.net:27017,cluster0-shard-00-02-qo8mp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    def __init__(self,initializeDatabase=False):
        #Class initialization
        self.db = self.client.MyBudget
        self.usersCollection = self.db.users_collection
        self.categoriesCollection = self.db.categories_collection
        self.incomesCollection = self.db.incomes_collection
        self.expensesCollection = self.db.expenses_collection
        if(initializeDatabase):
            self.client.drop_database("MyBudget")    
            self.initializeDatabase()
    
    def initializeDatabase(self):
        #Database initialization
        self.usersCollection.create_index("email", unique = True);
        self.categoriesCollection.create_index([("userEmail", ASCENDING), ("name", DESCENDING)], unique = True)
        #Adds a vadilator to the incomes query to check that it at least contains a userEmail or a groupId
        validatorQuery = {"$or" : [{"userEmail" : {"$exists" : "true"}}, {"groupId" : {"$exists" : "true"}}]}
        self.db.create_collection("incomes_collection", validator=validatorQuery)
        self.db.create_collection("expenses_collection", validator=validatorQuery)
        
        defaultUser = self.defData.copy()
        self.usersCollection.insert_one(defaultUser).inserted_id
    
    #CRUD Functions for the user
    
    
    def createUser(self, name, password, email, birthDate, gender,
                    budget = 0):
                        
        """
        Creates a new user in the database with the given data.
        NOTE: Doesn't check if a user with the given email already exists.
        """
                        
        userData = {"name": name,
                "password": password,
                "email" : email,
                "gender" : gender,
                "budget" : budget,
                "birthDate" : datetime.datetime.strptime(birthDate, "%Y-%m-%d")
        }
        self.usersCollection.insert_one(userData)
        
    def readUserById(self, idUser):
        """
        Returns an user found by it's id
        """
        return self.usersCollection.find_one({"_id": ObjectId(idUser)})
        
    def readUserByEmail(self, email):
        """
        Returns an user found by it's email
        """
        return self.usersCollection.find_one({"email": email})

    def updateUserByEmail(self, email, name=None, password=None, birthDate=None, gender=None,
                    budget = None):
                        
        """
        Updates an user found by it's email
        """
                        
        user = self.readUserByEmail(email);
        if(user):
            if(not name):
                name = user['name']
            if(not password):
                password = user['password']
            if(not birthDate):
                birthDate = user['birthDate']
            if(not gender):
                gender = user['gender']
            if(not budget):
                budget = user['budget']
                
        return self.usersCollection.update_one({"email": email}, {"$set" : 
                                                {"name" : name, 
                                                    "gender" : gender,
                                                    "password" : password,
                                                    "birthDate" : birthDate,
                                                    "budget" : budget
                                                }});
        
    
    def deleteUserByEmail(self, email):
        """
        Deletes an user found by it's email
        """
        return self.usersCollection.delete_one({"email": email})
        
        
    #CRUD functions for the category---------------------
        
    def createCategory(self, userEmail, name, description = "", totalCost=0):
        """
        Creates a new category in the database with the given data.
        NOTE: Doesn't check if a category with the given userEmail and name already exists.
        
        if the given userEmail isnt registered the category is not created
        """
        #print(userEmail)
        if(self.readUserByEmail(userEmail)):
            
            #print("User found")
            categoryData = {"userEmail": userEmail,
                    "name": name,
                    "description" : description,
                    "totalCost": 0
            }
            
            self.categoriesCollection.insert_one(categoryData)
        
        
    def readCategoriesByUserEmail(self, userEmail):
        """
        Returns a list of all the categories of the given user
        """
        return list(self.categoriesCollection.find({"userEmail": userEmail}))
    
    def readCategory(self, userEmail, name):
        """
        Returns the given category if exists
        """
        return self.categoriesCollection.find_one({"userEmail": userEmail, "name": name})
        
    def updateCategory(self, userEmail, name, newName = None, description = None, totalCost = None):
        
        """
        Updates an user found by it's email
        """
                        
        category = self.readCategory(userEmail, name);
        if(category):
            if(not newName):
                newName = name
            if(not description):
                description = category['description']
            if(not totalCost):
                
                totalCost = category['totalCost']
    
        return self.categoriesCollection.update_one({"userEmail": userEmail,
                                                "name": name}, {"$set" : 
                                                {"userEmail" : userEmail, 
                                                    "name" : newName,
                                                    "totalCost" : totalCost,
                                                }})
        
    def deleteCategory(self, userEmail, name):
        """
        Deletes a category found by it's userEmail and name
        """
        return self.usersCollection.delete_one({"userEmail": userEmail, "name": name})
        
    
    #CRUD functions for the incomes
    
    def createIncome(self, creationDate, value, description="", userEmail=None, groupId=None):
        """
        Creates an income for the specified user or groupId with the given value
        THIS DOES NOT CHECK THAT THE 
        """
        value = int(value)
        income = {"creationDate" : creationDate,
                    "value" : value,
                    "description" : description
                    }
        
        if(userEmail):
            try:
                if(self.readUserByEmail(userEmail)):
                    income["userEmail"] = userEmail
                    oldBudget = self.readUserByEmail(userEmail)["budget"]
                    self.updateUserByEmail(userEmail, budget=oldBudget+value)
                else:
                    raise SystemError
            except SystemError:
                raise SystemError("El email indicado no pertenece a ningun usuario")
            
        elif(groupId):
            #TODO    
            pass
        
        return self.incomesCollection.insert_one(income)
        
    
    def readIncomes(self, userEmail=None, groupId=None):
        """
        Returns all the incomes from a given userEmail or groupId
        pass
        """
        incomes = []
        if(userEmail):
            incomes = list(self.incomesCollection.find({"userEmail" : userEmail}))
        elif(groupId):
            incomes = list(self.incomesCollection.find({"groupId" : groupId}))
        
        return incomes
    
    def readIncomeById(self, incomeId):
        """
        Reads and return a single income by its id
        """
        return self.db.incomes_collection.find_one({"_id" : incomeId})
        
    def updateIncome(self, incomeId, creationDate=None, value=None, description="", userEmail=None, groupId=None):
        """
        Updates the income with the given id with the given values
        """
        income = readIncomeById(incomeId)
        if(not creationDate):
            creationDate = income["creationDate"]
        elif(not value):
            value = income["value"]
        elif(not description):
            description = income["description"]
            
        if("userEmail" in income.keys()):
            if(not userEmail):
                userEmail = income["userEmail"]
            updatedIncome = {
                                "userEmail": userEmail,
                                "creationDate" : creationDate,
                                "value" : value,
                                "description" : description
                            }
        
        elif("groupId" in income.keys()):
            if(not groupId):
                groupId = income["groupId"]
            updatedIncome = {
                                "groupId": groupId,
                                "creationDate" : creationDate,
                                "value" : value,
                                "description" : description
                            }
        
        
        if(userEmail):
            try:
                if(self.readUserByEmail(userEmail)):
                    income["userEmail"] = userEmail
                else:
                    raise SystemError
            except SystemError:
                raise SystemError("El email indicado no pertenece a ningun usuario")
                
        elif(groupId):
            #TODO    
            pass
               
        return self.db.incomes_collection.update_one({"_id" : incomeId}, 
                                                {"$set" : 
                                                    updatedIncome
                                                })
        
    def deleteIncome(self,incomeId):
        """
        Deletes the income with the given Id from the database
        """
        return self.incomesCollection.delete_one({"_id": incomeId})


    #CRUD functions for groups
    def createGroup(self, owner, subject, groupBudget=0):
        """
        Creates a new group in the database with the given data.
        """
        groupData={
            "owner":owner,
            "subject":owner,
            "groupBudget":groupBudget
        }
    
    def readGroup(self,id):
        pass
    def updateGroup(self):
        pass
    def deleteGroup(self):
        pass
        
        
    #CRUD functions for expenses
    
    def createExpense(self, categoryName, creationDate, value, description="", userEmail=None, groupId=None):
        """
        Creates an expense for the specified user or groupId with the given value
        """
        value = int(value)
        expense = {"creationDate" : creationDate,
                    "value" : value,
                    "description" : description
                    }
        
        if(userEmail):
            try:
                if(self.readUserByEmail(userEmail)):
                    expense["userEmail"] = userEmail
                    try:
                        if(self.readCategory(userEmail, categoryName)):
                            #print(self.readCategory(userEmail, categoryName))
                            expense["categoryName"] = categoryName
                            oldTotalCost = self.readCategory(userEmail, categoryName)["totalCost"]
                            self.updateCategory(userEmail, categoryName, totalCost = oldTotalCost + value)
                            return self.expensesCollection.insert_one(expense)
                        else:
                            raise SystemError
                    except SystemError:
                        m = "La categoria indicada no pertenece al usuario"
                        #print(m, userEmail)
                else:
                    raise SystemError
            except SystemError:
                print("El email indicado no pertenece a ningun usuario")
        
        
        
            
        elif(groupId):
            #TODO    
            pass
        
            return self.expensesCollection.insert_one(expense)
        
        
    
    def readExpenses(self, categoryName, userEmail=None, groupId=None):
        """
        Returns all the expenses from a given userEmail or groupId and category
        """
        expenses = []
        if(userEmail):
            print("user")
            expenses = list(self.expensesCollection.find({"userEmail" : userEmail, "categoryName" : categoryName}))
        elif(groupId):
            expenses = list(self.db.expensesCollection.find({"groupId" : groupId, "categoryName" : categoryName}))
        print("db expenses",expenses)
        return expenses
        
    def updateExpense(self):
        pass
    
    def deleteExpense(self):
        pass