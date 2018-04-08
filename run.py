from flask import Flask, send_from_directory, request, Response

app = Flask("mini-amazon", static_url_path="");

@app.route('/health', methods=['GET'])
def health():
    return 'healthy \n'



@app.route('/', methods=['GET'])
def index():
    return send_from_directory('staticHtmlFiles',"index.html")



@app.route('/addProducts', methods=['POST'])
def addProducts():

    prod = {}
    prod['product name'] = request.form['name'];
    prod['product description'] = request.form['desc'];
    prod['cost'] = request.form['cost'];

    print(prod)

    return Response('OK', 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

