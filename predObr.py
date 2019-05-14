
from flask import Flask, request

from werkzeug import abort
from flask import Flask, request
import urllib.request
import json
from multiprocessing import Process
from server_routes import db
import os
import random
import string
from datetime import datetime
from time import sleep
import requests


app = Flask(__name__)
progs = ["chrom","pycharm","telegram","terminal"]
active_progs = set([])
@app.route("/add_user", methods=['POST'])
def add_user():
    requests.post("http://localhost:8080",data =request.data )
    return "",200,{'Access-Control-Allow-Origin': '*'}
@app.route("/addInfo",methods = ['POST'])
def add_info():
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, threaded=True)