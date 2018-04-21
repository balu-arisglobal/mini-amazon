from flask import request, Response, render_template
from models.user import User
from models.product import Product
from mini_amazon import app

prod = Product()
user = User()


@app.route('/products', methods=['POST', 'GET'])
def addProducts():
    if request.method == 'POST':
        if request.form['op_type'] == "insert":
            product = {}
            product['product_name'] = request.form['name'];
            product['product_description'] = request.form['desc'];
            product['cost'] = request.form['cost'];
            prod.save(product);
            return Response("Product with details " + str(prod) + "successfully added........")

        elif request.form['op_type'] == "delete":
            result = prod.delete_by_id(str(request.form['id']))
            return Response("Product with id \t" + str(request.form['id']) + " \t and count: " + str(
                result.deleted_count) + " successfully deleted........")

        elif request.form['op_type'] == "update":
            return prod.update_product(request.form['id'], request.form.get('productParam'),
                                       request.form['valueToBeUpdated'])


    elif request.method == 'GET':
            itemToBeSearched = request.args['name']
            contentType = request.args.get('content_type', None)
            matching_items = prod.search_by_name(itemToBeSearched)
            if matching_items.count() <= 0:
                return Response("Sorry!!! The product you searched is not found", mimetype="application/json")
            else:
                matches = []
                for item in matching_items:
                    matches.append(item)

                if contentType == 'html':
                    return render_template('results.html', query = itemToBeSearched, results = matches)
                else:
                    return Response("Product details are " + str(matches), mimetype="application/json")



@app.route('/listProducts', methods=['GET'])
def listProducts():
    return prod.findAll()


@app.route('/listUsers', methods=['GET'])
def listAllUsers():
    return user.findAll()


@app.route('/users', methods=['POST', 'GET'])
def addUser():
    if request.method == 'POST':
        if request.form['op_type'] == "insert":
            if request.form['password'] == request.form['confirmPassword']:
                userDetails = {}
                userDetails['user_name'] = request.form['userName'];
                userDetails['user_password'] = request.form['password'];
                user.saveUser(userDetails)
                return Response("User Details saved successfully.......", mimetype="application/json")

            else:
                return Response("Passwords does not match", mimetype="application/json")



