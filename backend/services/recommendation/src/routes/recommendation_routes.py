from flask import Blueprint
from flask import request
from services.preferences_service import set_user_preferences
from services.recommendation_service import get_recommendation_for_user_by_artists, get_recommendation_for_user_by_genres, get_recommendation_per_periods
from others import auth_middleware, Utils
import requests

from services import get_recommendation_for_user 
app_recommendation = Blueprint("app_recommendation", __name__)

@app_recommendation.route("/preference", methods=["POST"])
# @auth_middleware
def add_preference():
    text = request.json.get("text", None)
    if not text:
        return {"error": "Missing text"}, 400
    
    queries = set_user_preferences(text)
    print(queries)
    res = requests.post("http://localhost:5003/queries", json={"queries": [queries]}, headers=request.headers).json()
    print(res)

    return {
        "msg": "Preference added"
    }, 201

@app_recommendation.route("/recommend", methods=["GET"])
# @auth_middleware
def recommend():
    try:
        preferences = {
        "user_id": 1,
        "preferences": {
            "16/01/2024": {
                "artists": {
                    "Beatles": 3,
                    "Queen": 2
                },
                "genres": {
                    "rock": 3,
                    "pop": 2
                },
                "years": {
                    "1960": 3,
                    "1970": 2
                }
            },
            "17/01/2024": {
                "artists": {
                    "Elvis Presley": 4,
                    "Michael Jackson": 1
                },
                "genres": {
                    "rock": 2,
                    "pop": 3
                },
                "years": {
                    "1950": 2,
                    "1980": 3
                }
            },
            "5/02/2024": {
                "artists": {
                    "Bob Dylan": 2,
                    "Led Zeppelin": 2,
                    "Pink Floyd": 1
                },
                "genres": {
                    "folk": 2,
                    "rock": 2,
                    "psychedelic": 1
                },
                "years": {
                    "1960": 2,
                    "1970": 2,
                    "1980": 1
                }
            },
            "4/02/2024": {
                "artists": {
                    "Prince": 3,
                    "David Bowie": 1,
                    "Madonna": 2
                },
                "genres": {
                    "pop": 3,
                    "funk": 1,
                    "rock": 2
                },
                "years": {
                    "1970": 2,
                    "1980": 3,
                    "1990": 1
                }
            },
            "20/02/2023": {
                "artists": {
                    "The Rolling Stones": 2,
                    "U2": 3,
                    "Radiohead": 1
                },
                "genres": {
                    "rock": 3,
                    "alternative": 1,
                    "pop": 2
                },
                "years": {
                    "1960": 1,
                    "1980": 2,
                    "1990": 1
                }
            }
        }
        } 
        result_per_periods = get_recommendation_for_user(preferences)
       
        queries_to_run = get_recommendation_per_periods(result_per_periods)
        recommendation_by_artists = get_recommendation_for_user_by_artists(result_per_periods)
    
        recommendation_by_genre = get_recommendation_for_user_by_genres(result_per_periods)

        res_complete = requests.post("http://localhost:5003/queries", json={"queries": [queries_to_run]}, headers=request.headers).json()
        res_by_artist = requests.post("http://localhost:5003/queries", json={"queries": [recommendation_by_artists]}, headers=request.headers).json()
        res_by_genre = requests.post("http://localhost:5003/queries", json={"queries": [recommendation_by_genre]}, headers=request.headers).json()
        return {
            "msg": "Recommendations fetched",
            "data": {
                "complete": res_complete,
                "by_artist": res_by_artist,
                "by_genre": res_by_genre
            }
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "Could not fetch recommendations"
        }, 400
