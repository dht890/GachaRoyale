# routes/users.py
from flask import Blueprint, request, jsonify
from src.database.db import users_collection

users = Blueprint("users", __name__)

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


@users.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200


@users.route("/user/<username>", methods=["PATCH"])
def update_user(username):
    data = request.json
    allowed_fields = {"username", "lvl", "pfp"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update."}), 400

    result = users_collection.update_one({"username": username}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User updated", "updated_fields": update_data})

