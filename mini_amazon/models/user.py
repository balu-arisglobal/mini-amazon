from pymongo import MongoClient
import re
from bson.objectid import ObjectId

class User:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.miniamazonDB



    def saveUser(self, user):
        user_details = self.db.users.find({ "user_name" : user["user_name"] } )
        if user_details.count() > 0:
            return {"status": "fail", "user": user["user_name"]}
        else:
            self.db.users.insert(user)
            return {"status": "success", "user": user["user_name"]}

    def findAll(self):
        allItems =self.db.users.find()
        if allItems.count() > 0:
            matches = []
            for item in allItems:
                matches.append(item)
            return "Userdetails are " + str(matches)
        else:
            return "Empty List! No users found."


    def search_user(self, user_name , password):
        user_details = self.db.users.find({'user_name': user_name})
        if user_details.count() > 0:
            for item in user_details:
                password_matched = item["user_password"]
                #self.db.users.find({'user_name': user_name, 'user_password': password})
            if password_matched ==  password :
                return {'result':'true', 'user': user_name}
            else:
                return {'result':"Password Doesn't match"}
        else:
            return {'result':"User does not exists"}

