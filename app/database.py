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
import re
class Database():
    
    
    #Default user data
    defData = { "name": "Juan Pablo Méndez",
                "password": '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                "email" : "juanpam@javerianacali.edu.co",
                "gender" : "M",
                "budget" : 0,
                "incomesTotal": 0,
                "expensesTotal": 0,
                "birthDate" : datetime.datetime(1996,6,6)
    }
    
    defCat = { "userEmail": "juanpam@javerianacali.edu.co",
                "name": 'Test',
                "description" : "This is just a test category",
                "totalCost": 0
    }
    
    #Static client
    #aguacate-2017 is the password and mybudget the user
    client = MongoClient("mongodb://mybudget:aguacate-2017@cluster0-shard-00-00-qo8mp.mongodb.net:27017,cluster0-shard-00-01-qo8mp.mongodb.net:27017,cluster0-shard-00-02-qo8mp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    def __init__(self,initializeDatabase=False,empty = False):
        #Class initialization
        self.db = self.client.MyBudget
        self.usersCollection = self.db.users_collection
        self.categoriesCollection = self.db.categories_collection
        self.incomesCollection = self.db.incomes_collection
        self.expensesCollection = self.db.expenses_collection
        self.groupsCollection = self.db.groups_collection
        self.groupsUsersCollection = self.db.groups_users_collection
        if(initializeDatabase):
            self.client.drop_database("MyBudget")    
            self.initializeDatabase(empty)
    
    def initializeDatabase(self, empty):
        #Database initialization
        self.usersCollection.create_index("email", unique = True);
        self.categoriesCollection.create_index([("userEmail", ASCENDING), ("name", DESCENDING)], unique = True)
        #Adds a vadilator to the incomes query to check that it at least contains a userEmail or a groupId
        validatorQuery = {"$or" : [{"userEmail" : {"$exists" : "true"}}, {"groupId" : {"$exists" : "true"}}]}
        self.db.create_collection("incomes_collection", validator=validatorQuery)
        self.db.create_collection("expenses_collection", validator=validatorQuery)
        
        validatorQuery = {"userEmail" : {"$exists" : "true"}, "groupId" : {"$exists" : "true"}}
        self.db.create_collection("groups_users_collection", validator = validatorQuery)
        
        defaultUser = self.defData.copy()
        defaultCategory = self.defCat.copy()
        if(not empty):
            self.usersCollection.insert_one(defaultUser)
            self.categoriesCollection.insert_one(defaultCategory)
    
    #CRUD Functions for the user
    
    
    def createUser(self, name, password, email, birthDate, gender,
                    budget = 0, incomesTotal = 0, expensesTotal = 0):
                        
        """
        Creates a new user in the database with the given data.
        NOTE: Doesn't check if a user with the given email already exists.
        """
                        
        userData = {"name": name,
                "password": password,
                "email" : email,
                "gender" : gender,
                "budget" : budget,
                "incomesTotal" : incomesTotal,
                "expensesTotal": expensesTotal,
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
    
    def readUsers(self, regex):
        """
        Returns all users matching the regex expression
        """
        regex = re.compile(regex)
        return list(self.usersCollection.find({"email" : regex}))

    def updateUserByEmail(self, email, name=None, password=None, birthDate=None, gender=None,
                    budget = None, incomesTotal = None, expensesTotal = None):
                        
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
            if(not incomesTotal):
                incomesTotal = user['incomesTotal']
            if(not expensesTotal):
                expensesTotal = user['expensesTotal']
                
        return self.usersCollection.update_one({"email": email}, {"$set" : 
                                                {"name" : name, 
                                                    "gender" : gender,
                                                    "password" : password,
                                                    "birthDate" : birthDate,
                                                    "budget" : budget,
                                                    "incomesTotal" : incomesTotal,
                                                    "expensesTotal" : expensesTotal
                                                }});
    
    
    def deleteUserByEmail(self, email):
        """
        Deletes an user found by it's email
        """
        return self.usersCollection.delete_one({"email": email})
        
        
    #CRUD functions for the category---------------------
        
    def createCategory(self, name, userEmail=None, groupId=None,  description = "", totalCost=0):
        """
        Creates a new category in the database with the given data.
        NOTE: Doesn't check if a category with the given userEmail or groupId and name already exists.
        
        if the given userEmail or groupId isn't registered the category is not created
        """
        #print(userEmail)
        
        categoryData = {"name": name,
                        "description" : description,
                        "totalCost": 0
                }
                
        if(userEmail):
            if(self.readUserByEmail(userEmail)):
                
                #print("User found")
                categoryData["userEmail"] = userEmail
                return self.categoriesCollection.insert_one(categoryData)
        elif(groupId):
            if(self.readGroupById(groupId)):
                categoryData["groupId"] = ObjectId(groupId)
                return self.categoriesCollection.insert_one(categoryData)
                
                
        
    def readCategoriesByUserEmail(self, userEmail):
        """
        Returns a list of all the categories of the given user
        """
        return list(self.categoriesCollection.find({"userEmail": userEmail}))
    
    def readCategoriesByGroupId(self, groupId):
        """
        Returns a list of all the categories of the given user
        """
        return list(self.categoriesCollection.find({"groupId": ObjectId(groupId)}))
    
    def readCategory(self, name, userEmail=None, groupId = None):
        """
        Returns the given category if exists
        """
        if(userEmail):
            return self.categoriesCollection.find_one({"userEmail": userEmail, "name": name})
        elif(groupId):
            return self.categoriesCollection.find_one({"groupId": ObjectId(groupId), "name": name})
        
        
    def updateCategory(self, name, userEmail=None, groupId=None, newName = None, description = None, totalCost = None):
        
        """
        Updates an user found by it's email
        """
                        
        category = self.readCategory(name, userEmail, groupId);
        if(category):
            if(not newName):
                newName = name
            if(not description):
                description = category['description']
            if(not totalCost):
                totalCost = category['totalCost']
                
        if(userEmail):
            return self.categoriesCollection.update_one({"userEmail": userEmail,
                                                    "name": name}, {"$set" : 
                                                    {"userEmail" : userEmail, 
                                                        "name" : newName,
                                                        "totalCost" : totalCost,
                                                    }})
        elif(groupId):
            return self.categoriesCollection.update_one({"groupId": ObjectId(groupId),
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
                    user = self.readUserByEmail(userEmail)
                    oldBudget = user["budget"]
                    oldIncomes = user["incomesTotal"]
                    self.updateUserByEmail(userEmail, budget=oldBudget+value, incomesTotal=oldIncomes+value)
                else:
                    raise SystemError
            except SystemError:
                raise SystemError("El email indicado no pertenece a ningun usuario")
            
        elif(groupId):
            try:
                if(self.readGroupById(groupId)):
                    income["groupId"] = ObjectId(groupId)
                    group = self.readGroupById(groupId)
                    oldBudget = group["budget"]
                    oldIncomes = group["incomesTotal"]
                    self.updateGroupById(groupId, budget=oldBudget+value, incomesTotal=oldIncomes+value)
                else:
                    raise SystemError
            except SystemError:
                raise SystemError("El id indicado no pertenece a ningun grupo")   
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
            incomes = list(self.incomesCollection.find({"groupId" : ObjectId(groupId)}))
        
        return incomes
    
    def readIncomeById(self, incomeId):
        """
        Reads and return a single income by its id
        """
        return self.db.incomes_collection.find_one({"_id" : incomeId})
        
    def updateIncome(self, incomeId, creationDate=None, value=None, description="", userEmail=None, groupId=None):
        """
        Updates the income with the given id with the given values
        
        NOTE: THIS FUNCTION NEEDS TO BE REVISED
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
               
        return self.db.incomes_collection.update_one({"_id" : ObjectId(incomeId)}, 
                                                {"$set" : 
                                                    updatedIncome
                                                })
        
    def deleteIncome(self,incomeId):
        """
        Deletes the income with the given Id from the database
        """
        return self.incomesCollection.delete_one({"_id": incomeId})


    #CRUD functions for groups
    def createGroup(self, owner, subject, description = 0, budget = 0, members=[]):
        """
        Creates a new group in the database with the given data.
        """
        groupData={
            "owner": owner,
            "subject": subject,
            "description": description,
            "budget": budget,
            "incomesTotal" : budget,
            "expensesTotal" : 0
        }
        if(self.readUserByEmail(owner)):
            
            result = self.groupsCollection.insert_one(groupData)
            for member in members:
                self.addUserGroup(result.inserted_id, member, "normal")
            return result
        else:
            print("Usuario no existe")
    
    def readGroups(self, userEmail):
        """
        Returns all the groups from a user given it's userEmail
        """
        groupsIds = [g['groupId'] for g in list(self.groupsUsersCollection.find({"userEmail" : userEmail}))]
        return [self.readGroupById(gId) for gId in groupsIds]

    def readGroupBySubject(self, subject, userEmail):
        """
        Returns the group with the given subject, no case sensitive, with the
        given owner's userEmail. Ignores case
        """
        subject = re.compile(subject, re.IGNORECASE)
        return self.groupsCollection.find_one({"subject" : subject , "owner" : userEmail})
        
    def readGroupById(self,groupId):
        """
        Returns the group with the given subject, no case sensitive, with the
        given owner's userEmail. Ignores case
        """
        
        return self.groupsCollection.find_one({"_id" : ObjectId(groupId)})
        
    def updateGroupById(self,groupId,subject=None, description=None, budget=None, incomesTotal=None, expensesTotal=None):
        
        groupOld = self.readGroupById(groupId)
        
        if(not subject):
            subject = groupOld["subject"]
        if(not description):
            description = groupOld["description"]
        if(not budget):
            budget = groupOld["budget"]
        if(not incomesTotal):
            incomesTotal = groupOld["incomesTotal"]
        if(not expensesTotal):
            expensesTotal = groupOld["expensesTotal"]
        
        return self.groupsCollection.update_one({"_id" : ObjectId(groupId)}, 
                                                {"$set":
                                                    { 
                                                    "subject" : subject,
                                                    "description" : description,
                                                    "budget" : budget,
                                                    "incomesTotal" : incomesTotal,
                                                    "expensesTotal" : expensesTotal
                                                    }
                                                })
        
        
    def deleteGroup(self):
        pass
    
    
    def addUserGroup(self, groupId, userEmail, role="normal"):
        """
        Adds the given user to a group if not added yet
        """
        
        if(self.readGroupById(groupId) and self.readUserByEmail(userEmail)):
            if(not self.checkUserInGroup(groupId, userEmail)):
                groupsUsersData = {
                    "groupId" : ObjectId(groupId),
                    "userEmail" : userEmail,
                    "role": role
                }
                return self.groupsUsersCollection.insert_one(groupsUsersData)
            else:
                print("El usuario",userEmail,"ya pertenece al grupo.")
        else:
            if(not self.readGroupById(groupId)):
                print("El grupo no existe",groupId)
            else:
                print("El usuario no existe",userEmail)
    
    def readMembers(self, groupId):
        """
        Reads all the members in a group
        """
        users = list(self.groupsUsersCollection.find({"groupId" : ObjectId(groupId)}))
        print(users)
        emails = [user['userEmail'] for user in users]
        members = []
        for e in emails:
            members.append(self.readUserByEmail(e))
        return members
        
        
    
    def checkUserInGroup(self, groupId, userEmail):
        """
        Checks if the given user is in the group given
        """
        return True if self.groupsUsersCollection.find_one({"groupId" : ObjectId(groupId), "userEmail" : userEmail}) else False
        
        
    #CRUD functions for expenses
    
    def createExpense(self, categoryName, creationDate, value, description="", userEmail=None, groupId=None):
        """
        Creates an expense for the specified user or groupId with the given value
        """
        value = int(value)
        print("El costo es de",value)
        expense = {"creationDate" : creationDate,
                    "value" : value,
                    "description" : description
                    }
        
        if(userEmail):
            try:
                if(self.readUserByEmail(userEmail)):
                    expense["userEmail"] = userEmail
                    try:
                        if(self.readCategory(categoryName, userEmail)):
                            #print(self.readCategory(userEmail, categoryName))
                            expense["categoryName"] = categoryName
                            oldTotalCost = self.readCategory(categoryName, userEmail)["totalCost"]
                            user = self.readUserByEmail(userEmail)
                            oldBudget = user["budget"]
                            oldCosts = user["expensesTotal"]
                            self.updateCategory(categoryName, userEmail, totalCost = oldTotalCost + value)
                            self.updateUserByEmail(userEmail, budget = oldBudget - value, expensesTotal = oldCosts + value)
                            return self.expensesCollection.insert_one(expense)
                        else:
                            raise SystemError
                    except SystemError:
                        m = "La categoria indicada no pertenece al usuario"
                        print(m, userEmail)
                else:
                    raise SystemError
            except SystemError:
                print("El email indicado no pertenece a ningun usuario")
        
        
        
            
        elif(groupId):
            try:
                if(self.readGroupById(groupId)):
                    expense["groupId"] = ObjectId(groupId)
                    try:
                        if(self.readCategory(categoryName, groupId = groupId)):
                            #print(self.readCategory(userEmail, categoryName))
                            expense["categoryName"] = categoryName
                            oldTotalCost = self.readCategory(categoryName, groupId = groupId)["totalCost"]
                            group = self.readGroupById(groupId)
                            oldBudget = group["budget"]
                            oldCosts = group["expensesTotal"]
                            print("El oldBudget es",oldBudget)
                            self.updateCategory(categoryName, groupId = groupId, totalCost = oldTotalCost + value)
                            self.updateGroupById(groupId, budget = oldBudget - value, expensesTotal = oldCosts + value)
                            return self.expensesCollection.insert_one(expense)
                        else:
                            raise SystemError
                    except SystemError:
                        m = "La categoria indicada no pertenece al usuario"
                        print(m, userEmail)
                else:
                    raise SystemError
            except SystemError:
                print("El email indicado no pertenece a ningun usuario")
        
            return self.expensesCollection.insert_one(expense)
        
        
    
    def readExpenses(self, categoryName, userEmail=None, groupId=None):
        """
        Returns all the expenses from a given userEmail or groupId and category
        """
        expenses = []
        if(userEmail):
            #print("user")
            expenses = list(self.expensesCollection.find({"userEmail" : userEmail, "categoryName" : categoryName}))
        elif(groupId):
            expenses = list(self.expensesCollection.find({"groupId" : ObjectId(groupId), "categoryName" : categoryName}))
        print("db expenses",expenses, categoryName, userEmail, groupId)
        return expenses
        
    def updateExpense(self):
        pass
    
    def deleteExpense(self):
        pass