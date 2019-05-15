from flask import Flask, request

app = Flask(__name__)
from werkzeug import abort
from flask import Flask, request
import urllib.request
import json
from multiprocessing import Process
import db
import os
import random
import string
from datetime import datetime
from time import sleep

# {ip:status}






@app.route('/addInfo', methods=["POST"])
def addInfo():
    dataDict = json.loads(request.data)

    db.add_info(dataDict)
    return "",200, {'Access-Control-Allow-Origin': '*'}





@app.route("/getusers/<search>",methods = ["GET"])
def get_users(search):
    users = db.get_users()
    # if search == "0":
    #     name,surname = None, None
    #     splitted=""
    # else:
    #     splitted = search.split()
    #     if len(splitted) >= 2:
    #         name, surname = splitted[0], splitted[1]
    #     else:
    #         name = splitted[0]
    #         surname = '*'
    # if not name and not surname:
    #     users = db.get_users()
    # else:
    #     users = db.get_find_users(name, surname)
    #
    partuser = []
    for i in users:
        # if  (name in i.get("surname") and surname in i.get("name")) or (surname in i.get("surname") and name in i.get("name")):
        partuser.append({
            'photo': i.get("photo"),
            'id': i.get("id"),
            "name": i.get("name"),
            "surname": i.get("surname"),
        })
    return json.dumps(partuser), 200, {'Access-Control-Allow-Origin': '*'}


@app.route("/users/<int:id_user>")
def get_user(id_user):
    users = db.get_user(id_user)

    for l in users:
        if id_user == l.get("id"):
            return json.dumps(l), 200, {'Access-Control-Allow-Origin': '*'}
    else:
        abort(404)


@app.route("/add_user", methods=['POST'])
def add_user():
    dataDict = json.loads(request.data)
    user = {'photo': dataDict.get("photo"),
            'surname': dataDict.get("surname"),
            'name': dataDict.get("name")
            }
    db.add_user(user)
    return "", 200, {'Access-Control-Allow-Origin': '*'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
