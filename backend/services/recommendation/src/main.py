import pathlib
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
basedir = pathlib.Path(__file__).parent.resolve()

# TODO: Here to add noSQL database actually and also the cache
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'recommendation.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is my secret'
app.config['SECRET_KEY'] = SECRET_KEY

ma = Marshmallow(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes import *
app.register_blueprint(app_recommendation)
# app.register_blueprint(app_friendship)

from models import *
# db.init?
# db.create_all()

@app.route("/hello", methods=["GET"])
def hello_world():
    return {
        "msg": "Hello, Recommendation!"
    }