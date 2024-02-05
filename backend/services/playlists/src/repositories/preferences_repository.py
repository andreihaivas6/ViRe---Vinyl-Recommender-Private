from models import Playlist, PlaylistContent, TrackForJSPF
from main import db
from datetime import datetime, timedelta

from typing import List, Optional, Dict

from models import SharedPlaylist
from others import Utils
import threading

from collections import defaultdict

from pymongo import MongoClient

class PreferencesRepository:
    def __init__(self):
        pass 

    def compute_preferences(self, tracks: List[Dict], user_id: int, timestamp=""):
        """ Example
        "artists": {
                "Beatles": 3,
                "Quenn": 2
        },
        """
        preferences = {
            "user_id": "",
            "added_date": "",
            "artists": defaultdict(int),
            "genres": defaultdict(int),
            "years": defaultdict(int)
        }

        preferences["user_id"] = user_id
        timestamp = timestamp if timestamp else datetime.now()
        preferences["added_date"] = timestamp.strftime("%d/%m/%Y %H:%M")
        
        for track in tracks:
            if "artist" in track:
                preferences["artists"][track["artist"]] += 1
            if "genre" in track:
                preferences["genres"][track["genre"]] += 1
            if "date" in track:
                date = str(int(int(track["date"]) / 10) * 10)
                preferences["years"][date] += 1
        
        self.publish_preferences(preferences)
    
    def publish_preferences(self, preferences: Dict):
        """
        {
            "user_id_1": {
                "15/02/2024": {
                    "artists": {
                        "Beatles": 3,
                        "Quenn": 2
                    },
                    "genres": {
                        "rock": 3,
                        "pop": 2
                    },
                    "years": {
                        "1967": 3,
                        "1970": 2
                    }
                },
                "16/02/2024": {}
            },
            "user_id_2": {}
        }
        """
        preferences_to_publish = preferences
        preferences_to_publish["artists"] = dict(preferences_to_publish["artists"])
        preferences_to_publish["genres"] = dict(preferences_to_publish["genres"])
        preferences_to_publish["years"] = dict(preferences_to_publish["years"])

        print("PUBLISHING PREFERENCES...")
        date = preferences_to_publish["added_date"].split(" ")[0]
        data = {
            "user_id": preferences_to_publish["user_id"],
            "preferences": {
                date: {
                    "artists": preferences_to_publish["artists"],
                    "genres": preferences_to_publish["genres"],
                    "years": preferences_to_publish["years"]
                }
            }
        }

        # self.push_to_db(data, preferences_to_publish["user_id"])
        
        t = threading.Thread(target=self.push_to_db, args=(data, preferences_to_publish["user_id"]))
        t.start()


    def push_to_db(self, data_to_be_updated_with: Dict, user_id: int):
        uri = "mongodb+srv://myAtlasDBUser:myAtlasDBUser@myatlasclusteredu.deaxbzf.mongodb.net/?retryWrites=true&w=majority"
        local_uri = "mongodb://localhost:27017/"
        client = MongoClient(local_uri)

        db = client['mydatabase']
        collection = db['preferences_test-6'] # 5 - for old db

        result = collection.find_one({"user_id": user_id})

        if result is None:
            collection.insert_one(data_to_be_updated_with)
        else:
            date = list(data_to_be_updated_with["preferences"].keys())[0]

            # check if the date already exists -> if yes, add the values, if not, insert the new date
            if date in result["preferences"]:
                for key, value in data_to_be_updated_with["preferences"][date].items():
                    for elem, count in value.items():
                        if elem in result["preferences"][date][key]:
                            result["preferences"][date][key][elem] += count
                        else:
                            result["preferences"][date][key][elem] = count
            else:
                # insert the new date
                result["preferences"][date] = data_to_be_updated_with["preferences"][date]

            collection.update_one({"user_id": user_id}, {"$set": {"preferences": result["preferences"]}})
        
        result = collection.find_one({"user_id": user_id})
