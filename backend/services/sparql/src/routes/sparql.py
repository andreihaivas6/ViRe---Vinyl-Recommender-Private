from flask import Blueprint
from flask import request

from others import auth_middleware

app_sparql = Blueprint("app_sparql", __name__)

@app_sparql.route("/query", methods=["POST"])
@auth_middleware
def query():
    try:
        payload = request.get_json()
        return {
            "result": payload
        }
    except Exception as e:
        return {
            "msg": "Could not execute query"
        }, 400
