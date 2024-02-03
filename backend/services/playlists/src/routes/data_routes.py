# get vinyl data - not needed anymore actually
# get songs data
from flask import Blueprint
from flask import request
import requests
from others import auth_middleware, Utils

app_data = Blueprint("app_data", __name__)

# search for songs by name from query params
@app_data.route("/songs", methods=["GET"])
@auth_middleware
def get_songs():
    try:
        song_name = request.args.get("name") # from query params
        if song_name is None:
            return {
                "msg": "Song name is required"
            }, 400

        query =  """
            SELECT ?songURI ?title ?genre ?duration ?date 
            WHERE {
            ?songURI a ns1:Song ;
                        dc:title ?title ;
                        dc:date ?date ;
                        ns1:duration ?duration ;
                        ns1:genre ?genre .
            FILTER regex(?title,\"""" + song_name +  """\", "i")""" + """
            }
        """
        res = requests.post(
            "http://localhost:5003/query", 
            json={"query": query},
            headers=request.headers
        ).json()

        result = list()
        for elem in res['result']['results']['bindings']:
            title = elem["title"]["value"]
            id = title.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')
            result.append({
                "track_id": id,
                "title": title,
                "genre": elem["genre"]["value"],
                "duration": elem["duration"]["value"],
                "date": elem["date"]["value"],
            })

        return {
            "tracks": result
        }

    except Exception as e:
        print(e)
        return {
            "msg": "Could not get songs"
        }, 400
