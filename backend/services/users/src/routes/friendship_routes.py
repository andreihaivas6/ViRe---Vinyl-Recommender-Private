from flask import Blueprint
from flask import request

from models import *
from others import auth_middleware
from services import FriendshipService
from others import Utils

app_friendship = Blueprint("app_friendship", __name__)

friendship_service = FriendshipService()

# get friendshup by id
@app_friendship.route("/friendship/<int:friendship_id>", methods=["GET"])
@auth_middleware
def get_friendship_by_id(friendship_id: int):
    friendship = friendship_service.get_friendship_by_id(friendship_id)
    if friendship is None:
        return {
            "msg": "Friendship not found"
        }, 404
    
    return friendship_schema.dump(friendship)

# get friendships of user id (from token)
@app_friendship.route("/friendship", methods=["GET"])
@auth_middleware
def get_friendships_of_user_id():
    user_id = Utils.get_user_id_from_token()
    friendships = friendship_service.get_friendships_of_user_id(user_id)
    return friendships_schema.dump(friendships)

# get friends of user id (from token)
@app_friendship.route("/friends", methods=["GET"])
@auth_middleware
def get_friends_of_user_id():
    user_id = Utils.get_user_id_from_token()
    friends = friendship_service.get_friends_of_user_id(user_id)
    return users_schema_without_password.dump(friends)

# create friendship
@app_friendship.route("/friendship", methods=["POST"])
@auth_middleware
def create_friendship():
    try:
        # delete all friendships from DB
        # Friendship.query.delete()
        friendship = friendship_schema.load(request.json)
        created_friendship = friendship_service.create_friendship(friendship)

        if created_friendship is None:
            return {
                "msg": "Could not create friendship"
            }, 400
        else:
            return friendship_schema.dump(created_friendship), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not create friendship"
        }, 400
