from pymongo import MongoClient
import re
from bson.objectid import ObjectId

class Product:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.miniamazonDB


    def save(self,product):
        self.db.products.insert(product)


    def search_by_name(self, productName):
        matching_items = self.db.products.find({'product_name': re.compile(productName, re.IGNORECASE)})
        return matching_items


    def update_product(self, _id, product_param, value):
        result = self.db.products.find({'_id': ObjectId(_id)})
        if result.count() > 0:
            if product_param == "productName":
                self.db.products.update_one(
                    {'_id': ObjectId(_id)},
                    {'$set': {"product_name": value}}
                )
                return "product_name is updated"

            elif product_param == "productDescription":
                self.db.products.update_one(
                    {'_id': ObjectId(_id)},
                    {'$set': {"product_description": value}}
                )
                return "product_description is updated"

            elif product_param == "productCost":
                self.db.products.update_one(
                    {'_id': ObjectId(_id)},
                    {'$set': {"cost": value}}
                )
                return "Product cost is updated"

        else:
            return "Product with id " + str(_id) + "  was not found...."


    def delete_by_id(self, _id):
          return self.db.products.delete_one(filter={'_id': ObjectId(_id)})




    def findAll(self):
        allItems =self.db.products.find()
        if allItems.count() > 0:
            matches = []
            for item in allItems:
                matches.append(item)
            return "Product details are " + str(matches)
        else:
            return "Empty List! No data found."
