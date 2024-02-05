from flask import Blueprint
from flask import request
from services.preferences_service import set_user_preferences
from others import auth_middleware, Utils
import requests
import json

from services import get_recommendation_for_user 
app_recommendation = Blueprint("app_recommendation", __name__)

@app_recommendation.route("/preference", methods=["POST"])
# @auth_middleware
def add_preference():
    text = request.json.get("text", None)
    if not text:
        return {"error": "Missing text"}, 400
    
    queries = set_user_preferences(text)
    res = requests.post("http://localhost:5003/queries", json={"queries": [queries]}, headers=request.headers).json()
    # print(res)

    result = Utils.make_vinyls_readable(res)
    return result

@app_recommendation.route("/recommend", methods=["GET"])
# @auth_middleware
def recommend():
    try:
        user_id = Utils.get_user_id_from_token()
        # preferences = Utils.get_preferences_for_user(user_id)
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
        print(result_per_periods)
        
        # TODO: Get preferences from nosql database / cache by user_id
        # TODO: Use preferences to call -> Sparql service -> which queries Stardog (from DBpedia) -> returns recommendations

        return {
            "msg": "Recommendations fetched",
            "data": []
        }, 200
    except Exception as e:
        print(e)
        return {
            "msg": "Could not fetch recommendations"
        }, 400
