from datetime import datetime
from flask import Flask, render_template, request, jsonify     # types: ignored
from libs.protocol.kProtocolRoot import process_data
from pymongo import MongoClient
from pymongo.collection import Collection


app = Flask(__name__)


@app.route("/test")
def hello_test():
    print("/test")
    return "Hello World! Temp Test"


@app.route('/submit', methods=['POST'])
def submit():
    print(1, request, request.form)
    _data = request.form.get('data', "")  # Get param "data"
    print(2, f"Data: {_data} {type(_data)}")
    _err, _info = process_data(_data)
    print(3, f"Info: {_info}, err: {_err}")

    return f"OK"
