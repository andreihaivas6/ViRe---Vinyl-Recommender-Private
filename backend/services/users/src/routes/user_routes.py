from flask import Blueprint, request

from services import UserService
from models import user_schema, users_schema, user_schema_without_password, users_schema_without_password
from others import auth_middleware

app_user = Blueprint("app_users", __name__)

user_service = UserService()

@app_user.route("/user/<int:user_id>", methods=["GET"])
@auth_middleware
def get_user(user_id):
    user = user_service.get_user(user_id)
    return user_schema_without_password.dump(user)\
        if user is not None\
        else {
            "msg": "User not found"
        }, 404

@app_user.route("/user", methods=["GET"])
@auth_middleware
def get_users():
    username = request.args.get("username") # /user?username=<username>
    users = user_service.get_users(username)
    return users_schema_without_password.dump(users)

@app_user.route("/user", methods=["POST"])
def create_user():
    try:
        user = user_schema.load(request.json)
        created_user = user_service.create_user(user)

        if created_user is not None:
            return user_schema_without_password.dump(created_user), 201
        else:
            return {
                "msg": "Could not create user"
            }, 400
    
    except Exception as e:
        print(e)
        return {
            "msg": "Could not create user",
            "error": str(e)
        }, 400

@app_user.route("/user/login", methods=["POST"])
def login_user():
    try:
        user = user_schema.load(request.json)
        login_response = user_service.login_user(user)

        return login_response, 200\
            if 'data' in login_response\
            else 400
    
    except Exception as e:
        print(e)
        return {
            "msg": "Could not login user",
            "error": str(e)
        }, 400

# update user
@app_user.route("/user/<int:user_id>", methods=["PUT"])
@auth_middleware
def update_user(user_id):
    try:
        user = user_schema.load(request.json)
        updated_user = user_service.update_user(user_id, user)

        return user_schema_without_password.dump(updated_user)\
            if updated_user is not None\
            else {
                "msg": "User could not be updated"
            }, 400
    
    except Exception as e:
        return {
            "msg": "Could not update user",
            "error": str(e)
        }, 400

# delete user
@app_user.route("/user/<int:user_id>", methods=["DELETE"])
@auth_middleware
def delete_user(user_id):
    deleted_user = user_service.delete_user(user_id)

    if deleted_user is not None:
        return user_schema_without_password.dump(deleted_user), 200
    else:
        return {
            "msg": "User could not be deleted"
        }, 400
