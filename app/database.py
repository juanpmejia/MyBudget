"""
This module implements the necessary functions for the interaction with the 
MongoDB Atlas database.
"""
from pymongo import MongoClient

class Database():
    
    #Static client
    client = MongoClient("mongodb://mybudget:aguacate-2017@cluster0-shard-00-00-qo8mp.mongodb.net:27017,cluster0-shard-00-01-qo8mp.mongodb.net:27017,cluster0-shard-00-02-qo8mp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    def __init__(self):
        #Class initialization
        self.db = self.client.MyBudget
        self.usersCollection = self.db.users_collection
        self.initializeDatabase()
    
    def initializeDatabase(self):
        #Database initialization
        defaultUser = {"username": "admin",
                        "password": "admin"}
                        
        print(self.usersCollection.insert_one(defaultUser).inserted_id)
    
    #CRUD Functions for the user

