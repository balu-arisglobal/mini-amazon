from flask import request, Response, render_template, session
import os
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

        elif request.form['op_type'] == "add_to_user_cart":
            if session.get('user_name') is not '':
                user_details = user.check_if_userexists(session.get('user_name'))
                if user_details != None:
                    print (user_details)
                    print (request.form['id'])
                    result = prod.add_to_cart(user_details,request.form['id'])
                    return Response("Status ::" + result['status'] + "<br> Meesage :: "+ result['message'])
                else:
                    return render_template('index.html',message="Invalid User. Please login again .......")
            else:
                return render_template('index.html', message="User ession seems to be expired. Please login again .......")

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
                      if session.get('user_name') != None:
                        print (session.get('user_name'))
                        return render_template('results.html', query = itemToBeSearched, results = matches, loggedinUser = session.get('user_name'))
                      else:
                          return render_template('index.html',message="User ession seems to be expired. Please login again .......")
                else:
                    return Response("Product details are " + str(matches), mimetype="application/json")



@app.route('/listProducts', methods=['GET'])
def listProducts():
    return prod.findAll()


@app.route('/listUsers', methods=['GET'])
def listAllUsers():
    return user.findAll()


@app.route('/users/<action>', methods=['POST', 'GET'])
def addUser(action):
    if request.method == 'POST':
        if request.form['op_type'] == "insert":
            if action == "signup":
                if request.form['password'] == request.form['confirmPassword']:
                    userDetails = {}
                    user_cart = []
                    userDetails['user_name'] = request.form['userName'];
                    userDetails['user_password'] = request.form['password'];
                    userDetails['user_cart'] = user_cart
                    isSuccess = user.saveUser(userDetails)
                    print(isSuccess['status'])
                    if isSuccess['status'] == "success":
                         session['logged_in'] = isSuccess['logged_in']
                         session['user_name'] = isSuccess['user']
                         return render_template('home.html', user=session['user_name'])
                    elif isSuccess['status'] == "fail":
                        return render_template('index.html', message="User already exists.......")

                else:
                    return render_template('index.html', message="Passwords does not match.......")


            elif action == "login":
                user_detail = user.search_user(request.form['userName'],request.form['password'])
                if user_detail['result'] == "true":
                    session['logged_in'] = True
                    session['user_name'] = user_detail['user']
                    return render_template('home.html', user=session['user_name'])
                return render_template('index.html', message="Passwords does not match.......")


