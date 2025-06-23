from flask import Blueprint, jsonify, request
import requests
from src.database.db import cards_collection
import os

API_TOKEN = os.getenv("CLASH_ROYALE_API_KEY")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

cards = Blueprint("cards", __name__)


# Auto-Sync Then Return Local Cards
@cards.route("/cards", methods=["GET"])
def get_cards():
    local_cards = list(cards_collection.find({}, {"_id": 0}))

    # If database is empty, fetch from API and sync
    if not local_cards:
        response = requests.get("https://api.clashroyale.com/v1/cards", headers=HEADERS)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch cards"}), response.status_code

        cards = response.json().get("items", [])
        for card in cards:
            card_data = {
                "id": card["id"],
                "name": card["name"],
                "rarity": card["rarity"],
                "elixirCost": card.get("elixirCost", 0),
                "icon": card["iconUrls"]["medium"],
                "unlocked": False,
                "copies_owned": 0,
                "level": 1,
            }
            cards_collection.update_one(
                {"id": card["id"]}, {"$setOnInsert": card_data}, upsert=True
            )

        local_cards = list(cards_collection.find({}, {"_id": 0}))

    return jsonify(local_cards)


@cards.route("/update_card/<int:card_id>", methods=["PATCH"])
def update_card(card_id):
    data = request.json
    allowed_fields = {"unlocked", "copies_owned", "level"}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update."}), 400

    result = cards_collection.update_one({"id": card_id}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "Card not found"}), 404

    return jsonify({"message": "Card updated", "updated_fields": update_data})
