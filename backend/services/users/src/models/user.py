from datetime import datetime, timedelta

from main import db, ma

import uuid

class User(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)
    
    def random_string():
        return str(uuid.uuid4())

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)

    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(
        db.String(256),
        nullable=False,
    )

    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))

    is_active = db.Column(db.Boolean, default=True)
    timestamp = db.Column(
        db.DateTime, 
        default=local_time, 
        onupdate=local_time
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

class UserSchemaWithoutPassword(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        exclude = ("password_hash",)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_schema_without_password = UserSchemaWithoutPassword()
users_schema_without_password = UserSchemaWithoutPassword(many=True)
