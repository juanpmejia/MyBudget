"""
This module implements the necessary functions for the interaction with the 
MongoDB Atlas database.

The Atlas email is jpkratos@gmail.com and the pass is aguacate-2017

"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId
import datetime
class Database():
    
    
    #Default user data
    defData = { "name": "Juan Pablo Méndez",
                "password": "admin",
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
        if(initializeDatabase):
            self.client.drop_database("MyBudget")    
            self.initializeDatabase()
    
    def initializeDatabase(self):
        #Database initialization
        self.usersCollection.create_index("email", unique = True);
        self.categoriesCollection.create_index([("userEmail", ASCENDING), ("name", DESCENDING)], unique = True)
        defaultUser = self.defData.copy()
        #print(self.usersCollection.insert_one(defaultUser).inserted_id)
    
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
        
    def createCategory(self, userEmail, name, description = "", totalCost=0):
        """
        Creates a new category in the database with the given data.
        NOTE: Doesn't check if a category with the given userEmail and name already exists.
        
        if the given userEmail isnt registered the category is not created
        """
        print(userEmail)
        if(self.readUserByEmail(userEmail)):
            
            print("User found")
            categoryData = {"userEmail": userEmail,
                    "name": name,
                    "description": description,
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
                
        return self.usersCollection.update_one({"userEmail": userEmail,
                                                "name": name}, {"$set" : 
                                                {"userEmail" : userEmail, 
                                                    "name" : name,
                                                    "totalCost" : totalCost,
                                                }});
        
    def deleteCategory(self, userEmail, name):
        """
        Deletes a category found by it's userEmail and name
        """
        return self.usersCollection.delete_one({"userEmail": userEmail, "name": name})
