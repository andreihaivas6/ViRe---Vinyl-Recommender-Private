from flask import Blueprint
from flask import request
from main import conn
from others import auth_middleware

app_sparql = Blueprint("app_sparql", __name__)

@app_sparql.route("/query", methods=["POST"])
@auth_middleware
def query():
    try:
        payload = request.get_json()
        query = payload["query"]
        print(query)
        res = conn.select(query)
        print(res)
        return {
            "result": res
        }
    except Exception as e:
        print(e)
        return {
            "msg": "Could not execute query"
        }, 400
