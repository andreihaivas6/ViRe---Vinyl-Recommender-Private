from flask import Blueprint
from flask import request
from main import conn, conn_vinyl
from others import auth_middleware

app_sparql = Blueprint("app_sparql", __name__)

@app_sparql.route("/query", methods=["POST"])
# @auth_middleware
def query():
    try:
        payload = request.get_json()
        query = payload["query"]
        res = conn.select(query)
        return {
            "result": res
        }
    except Exception as e:
        print(e)
        return {
            "msg": "Could not execute query"
        }, 400

@app_sparql.route("/queries", methods=["POST"])
# @auth_middleware
def queries():
    try:
        payload = request.get_json()
        queries = payload["queries"]
        result = []
        for query in queries:
            for mini_query in query:
                print("mini_query: ", mini_query)
                result.append(conn_vinyl.select(mini_query))
            # result.append(conn.select(query))
        print("byee")
        return {
            "result": result
        }
    except Exception as e:
        print(e)
        return {
            "msg": "Could not execute query"
        }, 400