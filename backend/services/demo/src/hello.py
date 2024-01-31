from flask import Flask, request

import pathlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow



app = Flask(__name__)
basedir = pathlib.Path(__file__).parent.resolve()

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'people.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# os.environ.setdefault('key_test', '123')
SECRET_KEY = os.environ.get('key_test') or 'this is a secret'
print(f'Secret key: {SECRET_KEY}')
app.config['SECRET_KEY'] = SECRET_KEY

ma = Marshmallow(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from test import app_test_1
from test2 import app_test_2

app.register_blueprint(app_test_1)
app.register_blueprint(app_test_2)

# From here import models - for migration without errors
from model import *

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))



@app.route("/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    return people_schema.dump(people)

@app.route("/people/<int:person_id>", methods=["GET"])
def get_person(person_id):
    person = Person.query.get(person_id)
    return person_schema.dump(person) 


@app.route("/people", methods=["POST"])
def add_person():
    try:
        person = person_schema.load(request.json)
        db.session.add(person)
        db.session.commit()
        return person_schema.dump(person)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/people/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    try:
        person = Person.query.get(person_id)
        updates = request.json
        for key, value in updates.items():
            setattr(person, key, value)
        db.session.commit()
        return person_schema.dump(person)
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/people/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    try:
        person = Person.query.get(person_id)
        if person is None:
            return {"error": "Person not found"}, 404
        
        db.session.delete(person)
        db.session.commit()
        return person_schema.dump(person)
    except Exception as e:
        return {"error": str(e)}, 400


@app.route("/hello", methods=["GET"])
def hello_world():
    return {
        "message": "Hello, World!"
    }

@app.route("/not-hello", methods=["GET"])
def not_hello_world():
    return {
        "message": "Hello, given status code!"
    }, 404

@app.route("/hello/<name>", methods=["GET"])
def hello_name(name):
    return {
        "message": f"Hello, {name}!"
    }

# get name from query string
@app.route("/hello-query", methods=["GET"])
def hello_query():
    name = request.args.get("name")
    return {
        "message": f"Hello, {name}!"
    }

# get name from payload
@app.route("/hello-post", methods=["POST"])
def hello_post():
    body = request.get_json()
    name = body.get("name")
    return {
        "message": f"Hello, {name}!"
    }


if __name__=='__main__':
    app.run(debug=True)
