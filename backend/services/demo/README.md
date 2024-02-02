# Hello World

### Preq:
`pip install flask`
`pip install Flask-RESTful`
`python -m pip install "flask-marshmallow[sqlalchemy]==0.14.0"`
`pip install Flask-Migrate`

### To run:
`flask --app main run`
sau
`py main`

### Migrate
https://flask-migrate.readthedocs.io/en/latest/
`flask --app main db init`
`flask --app main db migrate -m "Initial migration."`
`flask --app main db upgrade`

