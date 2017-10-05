"""
This module implements the necessary functions for the interaction with the 
MongoDB Atlas database.
"""
from pymongo import MongoClient
import datetime
class Database():
    
    
    #Default user data
    defData = {"id": "admin",
                "password": "admin",
                "email" : "juanpam@javerianacali.edu.co",
                "gender" : "M",
                "budget" : 123456789,
                "birthDate" : datetime.datetime(1996,6,6)
    }
    
    #Static client
    #aguacate-2017 is the password and mybudget the user
    client = MongoClient("mongodb://mybudget:aguacate-2017@cluster0-shard-00-00-qo8mp.mongodb.net:27017,cluster0-shard-00-01-qo8mp.mongodb.net:27017,cluster0-shard-00-02-qo8mp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    def __init__(self,initiali):
        #Class initialization
        self.db = self.client.MyBudget
        self.usersCollection = self.db.users_collection
        if(initializeDatabase):
            self.initializeDatabase()
    
    def initializeDatabase(self):
        #Database initialization
        defaultUser = self.defData.copy()
        print(self.usersCollection.insert_one(defaultUser).inserted_id)
    
    #CRUD Functions for the user
    
    
    def c

