# Hello World

### Preq:
`pip install flask`
`pip install Flask-RESTful`
`python -m pip install "flask-marshmallow[sqlalchemy]==0.14.0"`
`pip install Flask-Migrate`

### To run:
`flask --app hello run`
sau
`py hello`

### Migrate
https://flask-migrate.readthedocs.io/en/latest/
`flask --app hello db init`
`flask --app hello db migrate -m "Initial migration."`
`flask --app hello db upgrade`

