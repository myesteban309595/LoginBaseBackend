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

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Función para verificar si el usuario está autenticado

# La línea @wraps(f) se utiliza dentro de un decorador para garantizar que la función 
# decorada mantenga los metadatos de la función original, como su nombre, su documentación 
# y su lista de argumentos.
def token_required(f):
    @wraps
    def decorated(*arg, **kwargs):
        token = request.headers.get('x-access-token')
        
        if not token:
            return jsonify({'message':'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = mongo.db.users.find_one({'username': data['username']})
        except:
            return jsonify({'message':'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated



