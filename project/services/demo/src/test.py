# from hello import app 
from flask import Blueprint

app_test_1 = Blueprint("app_test_1", __name__)

@app_test_1.route("/test", methods=["GET"])
def test():
    return {
        "message": "Test!"
    }
