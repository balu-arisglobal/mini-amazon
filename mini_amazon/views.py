from flask import send_from_directory, render_template, session
import os
from mini_amazon import app



@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('home.html', user=session.get('user_name'))


@app.route("/logout")
def logout():
     session['logged_in'] = False
     session['user_name'] = None
     return render_template('index.html', message="Logged out successfully .......")



@app.route('/user.html', methods=['GET'])
def user_page():
    return render_template('user.html')
