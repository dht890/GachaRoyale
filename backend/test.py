from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_TOKEN = os.getenv("CLASH_ROYALE_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}"
}

app = Flask(__name__)
CORS(app)

@app.route("/cards")
def get_cards():
    url = "https://api.clashroyale.com/v1/cards"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch cards"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)