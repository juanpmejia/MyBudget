"""
This module implements the necessary functions for the interaction with the 
MongoDB Atlas database.

The Atlas email is jpkratos@gmail.com and the pass is aguacate-2017

"""

from pymongo import MongoClient
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
        if(initializeDatabase):
            self.client.drop_database("MyBudget")    
            self.initializeDatabase()
    
    def initializeDatabase(self):
        #Database initialization
        self.usersCollection.create_index("email", unique = True);
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
        Returns a user found by it's id
        """
        return self.usersCollection.find_one({"_id": ObjectId(idUser)})
        
    def readUserByEmail(self, email):
        """
        Returns a user found by it's email
        """
        return self.usersCollection.find_one({"email": email})

    def updateUser(self, idUser, nombre, correo, fechaNacimiento, genero,
                    presupuesto = 0):
        pass
    def deleteUser(self, idUser):
        pass
    def createCategory():
        pass
    def readCategory():
        pass
    def updateCategory():
        pass
    def deleteCategory():
        pass
