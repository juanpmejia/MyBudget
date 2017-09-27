from pymongo import MongoClient
import pprint



client = MongoClient("mongodb://mybudget:aguacate-2017@cluster0-shard-00-00-qo8mp.mongodb.net:27017,cluster0-shard-00-01-qo8mp.mongodb.net:27017,cluster0-shard-00-02-qo8mp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
db = client.test

collection = db.test_collection

post = {"username": "admin",
        "password": "admin"}


posts = db.posts
collection.insert_one(post)
#print(post_id)
# for p in collection.find():
#     pprint.pprint(p)
#collection.delete_many({})

# print("AHORA!")
# for p in collection.find():
#     pprint.pprint(p)
input()
