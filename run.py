from flask import Flask, send_from_directory, request, Response
from pymongo import MongoClient
import re

from product import Product



app = Flask("mini-amazon", static_url_path="");
prod = Product();

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')

@app.route('/products',methods=['POST','GET'])
def addProducts():

    if request.method == 'POST':
        if request.form['op_type'] == "insert":
            product = {}
            product['product name'] = request.form['name'];
            product['product description'] = request.form['desc'];
            product['cost'] = request.form['cost'];
            prod.save(product);
            return Response("Product with details " + str(prod) + "successfully added........")

        elif request.form['op_type'] == "delete":
            result = prod.delete_by_id(str(request.form['id']))
            return Response("Product with id \t" + str(request.form['id']) + " \t and count: " + str(result.deleted_count) + " successfully deleted........")

        elif request.form['op_type'] == "update":
            return prod.update_product(request.form['id'], request.form.get('productParam'), request.form['valueToBeUpdated'])


    elif request.method == 'GET':
        return prod.search_by_name(request.args['name'])

        
@app.route('/listProducts', methods=['GET'])
def listProducts():
    return prod.findAll()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug = True)

