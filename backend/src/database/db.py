# from flask_pymongo import PyMongo
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Collection names
# CARDS_COLLECTION = "cards"
# CHESTS_COLLECTION = "chests"
# USER_COLLECTIONS_COLLECTION = "user_collections"
# PROFILES_COLLECTION = "profiles"

# # Initialize PyMongo instance
# mongo = None

# def init_db(app) -> None:
#     """Initialize the database connection"""
#     global mongo
    
#     # MongoDB setup
#     mongodb_uri = os.getenv("MONGODB_URI")        
#     app.config["MONGO_URI"] = mongodb_uri
#     mongo = PyMongo(app)
    
#     # Initialize database validators
#     _init_validators()

# def get_db():
#     """Get the database instance"""
#     if mongo is None:
#         raise RuntimeError("Database not initialized. Call init_db first.")
#     return mongo.db

# def get_collection(collection_name: str):
#     """Get a specific collection from the database"""
#     db = get_db()
#     return db[collection_name]

# def _init_validators():
#     """Initialize collection validators"""
#     db = get_db()
    
#     # Cards collection validator
#     db.command({
#         "collMod": CARDS_COLLECTION,
#         "validator": {
#             "$jsonSchema": {
#                 "bsonType": "object",
#                 "required": ["name", "rarity", "icon", "cost"],
#                 "properties": {
#                     "name": {"bsonType": "string"},
#                     "rarity": {"enum": ["common", "rare", "epic", "legendary", "champion"]},
#                     "icon": {"bsonType": "string"},
#                     "cost": {
#                         "bsonType": "int",
#                         "minimum": 1,
#                         "maximum": 10
#                     }
#                 }
#             }
#         },
#         "validationLevel": "strict"
#     })
    
#     # Chests collection validator
#     db.command({
#         "collMod": CHESTS_COLLECTION,
#         "validator": {
#             "$jsonSchema": {
#                 "bsonType": "object",
#                 "required": ["type", "dropRate", "contents"],
#                 "properties": {
#                     "type": {"bsonType": "string"},
#                     "dropRate": {
#                         "bsonType": "number",
#                         "minimum": 0,
#                         "maximum": 1
#                     },
#                     "contents": {
#                         "bsonType": "object",
#                         "required": ["cards"],
#                         "properties": {
#                             "cards": {
#                                 "bsonType": "object",
#                                 "required": ["distribution"],
#                                 "properties": {
#                                     "distribution": {"bsonType": "object"}
#                                 }
#                             }
#                         }
#                     }
#                 }
#             }
#         },
#         "validationLevel": "strict"
#     })
    
#     # User collections validator
#     db.command({
#         "collMod": USER_COLLECTIONS_COLLECTION,
#         "validator": {
#             "$jsonSchema": {
#                 "bsonType": "object",
#                 "required": ["_id", "profile_id", "card_id", "unlocked", "level", "copiesOwned"],
#                 "properties": {
#                     "_id": {"bsonType": "string"},
#                     "profile_id": {"bsonType": "string"},
#                     "card_id": {"bsonType": "string"},
#                     "unlocked": {"bsonType": "bool"},
#                     "level": {
#                         "bsonType": "int",
#                         "minimum": 0
#                     },
#                     "copiesOwned": {
#                         "bsonType": "int",
#                         "minimum": 0
#                     }
#                 }
#             }
#         },
#         "validationLevel": "strict"
#     })
    
#     # Profiles collection validator
#     db.command({
#         "collMod": PROFILES_COLLECTION,
#         "validator": {
#             "$jsonSchema": {
#                 "bsonType": "object",
#                 "required": ["username", "xp_lvl"],
#                 "properties": {
#                     "username": {"bsonType": "string"},
#                     "xp_lvl": {
#                         "bsonType": "int",
#                         "minimum": 1
#                     },
#                     "pfp": {
#                         "bsonType": ["string", "null"]
#                     }
#                 }
#             }
#         },
#         "validationLevel": "strict"
#     })