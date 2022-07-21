from flask import Flask, request, jsonify
from flask_restful import Api
from flask_restful.reqparse import RequestParser
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
from flask_login import (login_user, 
                        LoginManager, 
                        login_required, 
                        logout_user, 
                        current_user)
from datetime import datetime
from random import randint
from http.client import HTTPSConnection as Connection


app = Flask('back end')

# == TODO ==
__user = "root"
__pass = "admin"
__url  = "localhost"
__port = 3306
__name = "flask_api"
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"mysql://{__user}:{__pass}@{__url}:{__port}/{__name}"
# ===========

app.secret_key = 'admin'
db = SQLAlchemy(app)
api = Api(app)