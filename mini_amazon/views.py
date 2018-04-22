from flask import send_from_directory, render_template
from mini_amazon import app


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('mini_amazon/static', 'index.html')


@app.route('/user.html', methods=['GET'])
def user_page():
    return render_template('user.html')
