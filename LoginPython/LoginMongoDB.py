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

# Ruta para registrar un nuevo usuario
@app.route('/register', method=['POST'])
def register():
    username = request.json['username']  # esto es como el req.body
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    
    if mongo.db.users.find_one({'username': username}):
        return jsonify({'message': 'user already exist'}),400
    
    mongo.db.users.insert_one(
        { 
         'username': username,
         'password': password
         })
    return jsonify({'message': 'User created succesfully'}), 201

# Ruta para iniciar sesión
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Not verify'}), 401
    
    user = mongo.db.users.find_one({'message': auth.username})
    
    if not user:
       return jsonify({'message': 'User not found!'}), 401
   
    if bcrypt.check_password_hash(user['password'], auth.password):
        token = jwt.encode(
            {'username': user['username'],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
              app.config['SECRET_KEY'])
        
        return jsonify({'token': token.decode('UTF-8')})

    return jsonify({'message': 'Password is incorrect!'}), 401

# Ruta protegida
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Welcome, {current_user["username"]}!'})

if __name__ == '__main__':
    app.run(debug=True)



    
    
    
    




