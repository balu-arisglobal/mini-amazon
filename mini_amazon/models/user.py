from pymongo import MongoClient
from flask import session
import re
import jwt
from bson.objectid import ObjectId
from product import Product

pr = Product()

class User:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.miniamazonDB



    def saveUser(self, user):
        user_details = self.db.users.find({ "user_name" : user["user_name"] } )
        if user_details.count() > 0:
            return {"status": "fail", "user_id": user["_id"], 'user_name':user["user_name"]}
        else:
            self.db.users.insert(user)
            return {"status": "success", "user_id": user['_id'],"logged_in": True , 'user_name':user["user_name"]}

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
                return {'result':'true', 'user_id': item["_id"], 'user_name':item["user_name"]}
            else:
                return {'result':"Password Doesn't match"}
        else:
            return {'result':"User does not exists"}


    def check_if_userexists(self, user_id):
        user_details = self.db.users.find({'_id': ObjectId(user_id)})
        if user_details.count() > 0:
            for item in user_details:
                return item

        else:
            return ''

    def find_products_in_usercart(self, id):
        result = self.db.users.find({'_id': id})
        return result[0].get('user_cart') if result.count > 0 else None


    def delete_product_from_cart(self,user_id, product_id):
        user_details = self.find_products_in_usercart(ObjectId(user_id))
        if product_id in user_details:
            user_details.remove(product_id)
            self.db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {"user_cart": user_details}}
            )
            return self.get_products_in_usercart(ObjectId(user_id))


    def get_products_in_usercart(self, user_id):
        result = self.find_products_in_usercart(user_id)
        if len(result) > 0:
            #for prod_id in result:
             #   list_of_product_details.append(pr.find_product_by_id(prod_id))
            list_of_product_details = [pr.find_product_by_id(prod_id) for prod_id in result]
        return list_of_product_details