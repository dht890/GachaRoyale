from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

# Connect to MongoDB (local or cloud via .env)
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["game"]  # Database name

# Collections (equivalent to tables)
CARDS_COLLECTIONS = db["cards"]
CHESTS_COLLECTIONS = db["chests"]
USER_COLLECTIONS_COLLECTIONS = db["user_collection"]
PROFILES_COLLECTIONS = db["profiles"]

class Card:
    def __init__(self, name, rarity, icon, cost):
        #MongoDB will automatically create a unique _id field
        self.name = name 
        self.rarity = rarity
        self.icon = icon
        self.cost = cost

    def to_dict(self):
        return {
            "name": self.name,
            "rarity": self.rarity,
            "icon": self.icon,
            "cost": self.cost
        }


class Profile:
    def __init__(self, username, xp_lvl=1, pfp=None):
        self.username = username  # This will also be unique
        self.xp_lvl = xp_lvl
        self.pfp = pfp

    def to_dict(self):
        return {
            "username": self.username,
            "xp_lvl": self.xp_lvl,
            "pfp": self.pfp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            xp_lvl=data.get("xp_lvl", 1),
            pfp=data.get("pfp")
        )

    @staticmethod
    def create_indexes(db):
        """Create unique indexes for the profile collection"""
        db.get_collection('profiles').create_index('username', unique=True) 
        
        
class UserCollection:
    def __init__(self, card_id, unlocked=False, level=0, copies_owned=0):
        self.card_id = card_id
        self.unlocked = unlocked
        self.level = level
        self.copies_owned = copies_owned

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "unlocked": self.unlocked,
            "level": self.level,
            "copiesOwned": self.copies_owned
        }
        
        
class Chest:
    def __init__(self, chest_type, drop_rate, card_distribution):
        self.type = chest_type
        self.drop_rate = drop_rate
        self.contents = {
            "cards": {
                "distribution": card_distribution
            }
        }

    def to_dict(self):
        return {
            "type": self.type,
            "dropRate": self.drop_rate,
            "contents": self.contents
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            chest_type=data["type"],
            drop_rate=data["dropRate"],
            card_distribution=data["contents"]["cards"]["distribution"]
        ) 
        