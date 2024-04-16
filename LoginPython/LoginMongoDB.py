#pip install Flask Flask-PyMongo Flask-Bcrypt

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_Secret_password'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users'



