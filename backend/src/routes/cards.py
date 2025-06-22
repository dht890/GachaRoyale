from flask import Blueprint, jsonify, request
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("CLASH_ROYALE_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["game"]
cards_collection = db["cards"]

cards = Blueprint('cards', __name__)


@cards.route("/cards", methods=["GET"])
def get_cards():
    url = "https://api.clashroyale.com/v1/cards"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch cards"}), response.status_code
    

@cards.route("/sync_cards", methods=["POST"])
def sync_cards():
    url = "https://api.clashroyale.com/v1/cards"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch cards"}), response.status_code
    
    cards = response.json().get("items", [])
    inserted_count = 0

    for card in cards:
        card_data = {
            "id": card["id"],
            "name": card["name"],
            "rarity": card["rarity"],
            "elixirCost": card.get("elixirCost", 0),
            "icon": card["iconUrls"]["medium"],
            "unlocked": False,
            "copies_owned": 0,
            "level": 1
        }
        result = cards_collection.update_one(
            {"id": card["id"]},
            {"$setOnInsert": card_data},
            upsert=True
        )
        if result.upserted_id:
            inserted_count += 1

    return jsonify({"message": f"{inserted_count} cards synced to database."})


@cards.route("/local_cards", methods=["GET"])
def get_local_cards():
    cards = list(cards_collection.find({}, {"_id": 0}))
    return jsonify(cards)


@cards.route("/update_card/<int:card_id>", methods=["PATCH"])
def update_card(card_id):
    data = request.json
    allowed_fields = {"unlocked", "copies_owned", "level"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update."}), 400

    result = cards_collection.update_one(
        {"id": card_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Card not found"}), 404

    return jsonify({"message": "Card updated", "updated_fields": update_data})

