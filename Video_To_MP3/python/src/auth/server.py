import jwt
import datetime
from flask import Flask, request
import os
from flask_mysqldb import MySQL
import platform
import config

server = Flask(__name__)
mysql = MySQL(server)

""" Configurations """
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST", None)
server.config["MYSQL_USER"] = os.environ.get("MYSQL_HOST", None)
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_HOST", None)
server.config["MYSQL_DB"] = os.environ.get("MYSQL_HOST", None)
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_HOST", None)
print(server.config["MYSQL_HOST"] )

""" Set server for checking login """

@server.route("/login", methods=["POST"])  # Login route using the login function defined later

def login():
    auth = request.authorization  # Basic authentication method with call's header having authentication details
    if not auth:
        return "Missing credentials", 401

    """ DB connection to find User & Pd"""

    my_cursor = mysql.connection.cursor()
    result = my_cursor.execute("select email, password from user email=%s", (auth.username, ))
    if result > 0:
        user_row = my_cursor.fetchone()
        email, password = user_row[0], user_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid Credentials Passed", 401
        else:
            return createJWT(auth.username. os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid Credentials Passed", 401


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),  # Token Valid for 24 hrs
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256"
    )


""" Validation of incoming JWT Token"""
@server.route("/validate", method=['POST'])

def validate():
    encoded_jwt = request.headers["Authorization"]  # The header should be Authorisation : Bearer <token> , which uses oAuth2
    if not encoded_jwt:
        return "Invalid Credentials Passed", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]  # To get the token from this format "Authorisation : Bearer <token>"

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HSA256"])
    except:
        return "Not authorized", 403
    else:
        return decoded, 200



if __name__ == "__main__":
    """ 0.0.0.0 is listening to everything, as our Host=Docker Container will have Dynamic IP , so we cant associate any specific IP addressesto 
    Flask Host variable ( which lists what IPs to listen to ). In Real Prod, we can lmit the IP Range"""
    server.run(host="0.0.0.0", port=5000)  


