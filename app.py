from flask import Flask, request
import json
import requests
import trains
from wit import Wit
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    return "Hello world", 200

if __name__ == '__main__':
    app.run()