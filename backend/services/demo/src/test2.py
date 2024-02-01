from flask import Blueprint

app_test_2 = Blueprint("app_test_2", __name__)

@app_test_2.route("/test2", methods=["GET"])
def test():
    return {
        "message": "Test2!"
    }
