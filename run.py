from mini_amazon import app
import os
import json

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    config = json.load(open("./config.json","r"))
    app.run(host=config["host"], port=config["port"], debug = config["debugMode"])

