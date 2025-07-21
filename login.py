# login.py
from flask import Blueprint, request, jsonify
import jwt
import datetime

login_bp = Blueprint('login', __name__)
SECRET_KEY = 'mysecretkey'

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        token = jwt.encode({
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "status": "Login successful",
            "token": token
        })
    return jsonify({"error": "Invalid credentials"}), 401

def token_required(f):
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace("Bearer ", "")
        
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    
    wrapper.__name__ = f.__name__  # Fix Flask routing
    return wrapper