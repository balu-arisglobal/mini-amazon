from pymongo import MongoClient
import re
from bson.objectid import ObjectId

class User:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.miniamazonDB



    def saveUser(self, user):
        self.db.users.insert(user)

    def findAll(self):
        allItems =self.db.users.find()
        if allItems.count() > 0:
            matches = []
            for item in allItems:
                matches.append(item)
            return "Userdetails are " + str(matches)
        else:
            return "Empty List! No users found."
