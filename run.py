from flask import Flask, send_from_directory, request, Response

app = Flask("mini-amazon", static_url_path="");

@app.route('/health', methods=['GET'])
def health():
    return 'healthy \n'

product_list = []
indexPosition = 0
@app.route('/', methods=['GET'])
def index():
    return send_from_directory('staticHtmlFiles',"index.html")



@app.route('/addProducts', methods=['POST','GET'])
def addProducts():

    if request.method == 'POST':
        prod = {}
        prod['product name'] = request.form['name'];
        prod['product description'] = request.form['desc'];
        prod['cost'] = request.form['cost'];
        product_list.append(prod)
        return Response("Product with details " + str(prod) + "successfully added........")

    elif request.method == 'GET':
        for item in product_list:
            if item['product name'] == request.args['name']:
                return Response("Product details are " + str(item))
            else:
                return Response("Sorry!!! The product you searched is not found")



@app.route('/listProducts', methods=['GET'])
def listProducts():
    count = 0
    listofItems = ""
    if len(product_list) > 0:
            for item in product_list:
                count+=1
                listofItems += str(count) + ". " + str(item) + "\n"
                return Response(listofItems)
    else:
        return Response("Empty List! No data found.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

