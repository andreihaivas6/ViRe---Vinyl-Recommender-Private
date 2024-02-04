import pathlib
import os
from stardog import Connection

from flask import Flask

app = Flask(__name__)
basedir = pathlib.Path(__file__).parent.resolve()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'sparql.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is my secret'
app.config['SECRET_KEY'] = SECRET_KEY

connection_details = {
    'endpoint': 'https://sd-e199938f.stardog.cloud:5820',
    'username': 'andreeaciocan2000@gmail.com',
    'password': 'adminadmin123'
}

conn = Connection('songs', endpoint='https://sd-e199938f.stardog.cloud:5820',
                            username='andreeaciocan2000@gmail.com', password='adminadmin123')

conn_vinyl = Connection('vinyl', endpoint='https://sd-e199938f.stardog.cloud:5820',
                            username='andreeaciocan2000@gmail.com', password='adminadmin123')


from routes import *
app.register_blueprint(app_sparql)

@app.route("/hello", methods=["GET"])
def hello_world():
    return {
        "msg": "Hello, Sparql!"
    }