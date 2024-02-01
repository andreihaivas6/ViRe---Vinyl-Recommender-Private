import pathlib
import os

from flask import Flask

app = Flask(__name__)
basedir = pathlib.Path(__file__).parent.resolve()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'sparql.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is my secret'
app.config['SECRET_KEY'] = SECRET_KEY


from routes import *
app.register_blueprint(app_sparql)

@app.route("/hello", methods=["GET"])
def hello_world():
    return {
        "msg": "Hello, Sparql!"
    }