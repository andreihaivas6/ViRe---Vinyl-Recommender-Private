from datetime import datetime, timedelta
from hello import db, ma

class Person(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)

    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, 
        default=local_time, 
        onupdate=local_time
    )

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)
