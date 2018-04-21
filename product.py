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
        matching_items = self.db.products.find({'product name': re.compile(productName, re.IGNORECASE)})

        if matching_items.count() <= 0:
            return "Sorry!!! The product you searched is not found"
        matches = []
        for item in matching_items:
            matches.append(item)
            return "Product details are " + str(matches)


    def update_product(self, _id, product_param, value):
        result = self.db.products.find({'_id': ObjectId(_id)})
        if result.count() > 0:
            if product_param == "productName":
                # oldName = result.next().get("product name")
                self.db.products.update_one(
                    {'_id': _id},
                    {'$set': {"product name": value}}
                )
                return "Product Name is updated"

            elif product_param == "productDescription":
                self.db.products.update_one(
                    {'_id': ObjectId(_id)},
                    {'$set': {"product description": value}}
                )
                return "Product description is updated"

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
