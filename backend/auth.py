from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Create Blueprint
auth_bp = Blueprint("auth", __name__)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["suicide_detection"]
users_collection = db["users"]

# Initialize Bcrypt (use app context from app.py)
bcrypt = None  # We will initialize it in app.py

def init_bcrypt(app):
    global bcrypt
    bcrypt = Bcrypt(app)

# Signup Route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    password = data.get('password')
    emergency_contact_name = data.get('emergency_contact_name')
    emergency_contact_phone = data.get('emergency_contact_phone')
    
    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    users_collection.insert_one({
        "full_name": full_name,
        "phone_number": phone_number,
        "email": email,
        "password": hashed_password,
        "emergency_contact": {
            "name": emergency_contact_name,
            "phone_number": emergency_contact_phone
        }
    })
    return jsonify({"message": "Signup successful"}), 201

# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = users_collection.find_one({"email": email})
    
    if user and bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401
