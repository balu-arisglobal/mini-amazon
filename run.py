from mini_amazon import app
import os

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=5010, debug = True)

