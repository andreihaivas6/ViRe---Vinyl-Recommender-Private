from flask import Blueprint
from flask import request
from others import discog_api

app_discog = Blueprint("app_discog", __name__)

@app_discog.route("/discog", methods=["GET"])
def get_discog_user_info():
    try:
        user_token_request = discog_api.get_token()
        return user_token_request
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog user info"
        }, 400


@app_discog.route("/discog/verifier", methods=["POST"])
def post_discog_verifier():
    print(request.json)
    verifier = request.json.get("verifier")
    try:
        user_token_request = discog_api.set_verifier(verifier)
        return user_token_request
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog user info"
        }, 400

