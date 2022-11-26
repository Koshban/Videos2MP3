import os
import gridfs
import pika
import json
from flask import request, Flask
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

"""" Various configurations """
server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"  # 27107 is default port and videos will be the database we will create in MongoDB
mongo = PyMongo(server)
fs = gridfs.GridFS(mongo.db)
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

""" Server Routes. Login route will comm with Auth Service to autehnticate and assign a token"""

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:  # if err != None
        return token
    else:
        return err
@server.route("/upload", methods=["POST"])  # Upload end point
def upload():
    access, err = validate.token(request)
  
    access = json.loads(access)  # json.loads converts/de-serializes a Json string to a Python object
    if access["admin"]:  # The json decoded paylaod shows if Admin is True
        if len(request.files) != 1:
            return "Exactly 1 file at a time Plzz", 400
        
        for _, f in request.files.items():  # requset.fiels will be key creatd while uplaod, and value as actual content
            err = util.upload(f, fs, channel, access)
            if err:
                return err
            
            return "Success!", 200
    else:
        return "Not Authorized", 401

@server.route("/download", methods=["GET"])  # End-Point for Download MP3
def download:
    return "Not Authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)



        








