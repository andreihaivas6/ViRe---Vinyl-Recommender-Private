from models import Playlist, PlaylistContent, TrackForJSPF
from main import db
from datetime import datetime

from typing import List, Optional, Dict

from models import SharedPlaylist
from others import Utils

from collections import defaultdict

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
                date = int(int(track["date"]) / 10) * 10
                preferences["years"][date] += 1
        
        self.publish_preferences(preferences)
    
    def publish_preferences(self, preferences: Dict):
        preferences_to_publish = preferences
        preferences_to_publish["artists"] = dict(preferences_to_publish["artists"])
        preferences_to_publish["genres"] = dict(preferences_to_publish["genres"])
        preferences_to_publish["years"] = dict(preferences_to_publish["years"])

        print("PUBLISHING PREFERENCES...")
        print(preferences)

        """
        Maybe not to push the JSON every time ? 
        We can have a key value DB ?
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

