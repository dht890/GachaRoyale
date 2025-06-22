# routes/users.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

users = Blueprint("users", __name__)

# MongoDB setup (you can refactor this to a shared file later)
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["game"]
users_collection = db["profiles"]

@users.route("/user", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    lvl = data.get("lvl", 1)
    pfp = data.get("pfp", "")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409
    try:
        user = {
            "username": username,
            "lvl": lvl,
            "pfp": pfp
        }

        result = users_collection.insert_one(user)
        user["_id"] = str(result.inserted_id)
        return jsonify({"message": "User created", "user": user}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@users.route("/user/<username>", methods=["GET"])
def get_user(username):
    
    user = users_collection.find_one({"username": username}, {"_id": 0})
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404
