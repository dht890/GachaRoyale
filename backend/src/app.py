# from flask import Flask
# from flask_cors import CORS
# from database.db import init_db, init_validators
# from routes.collection import collection_bp
# # from routes.challenge import challenge_bp
# # from routes.webhooks import webhooks_bp

# app = Flask(__name__)
# CORS(app)

# # Initialize the database
# init_db(app)

# # Register blueprints
# app.register_blueprint(collection_bp, url_prefix="/api")
# # app.register_blueprint(challenge_bp, url_prefix="/api")
# # app.register_blueprint(webhooks_bp, url_prefix="/webhooks")

# # Basic route to test the API
# @app.route("/api/health")
# def health_check():
#     return {"status": "healthy", "database": "connected"}

# if __name__ == "__main__":
#     app.run(debug=True)
