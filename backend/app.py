from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.routes.cards import cards  # <-- Import your blueprint
from src.routes.profile import users
load_dotenv()

app = Flask(__name__)
CORS(app)

# Register routes
app.register_blueprint(cards)
app.register_blueprint(users)


if __name__ == "__main__":
    app.run(debug=True)
