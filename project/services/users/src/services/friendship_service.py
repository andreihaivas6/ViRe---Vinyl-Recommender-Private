from typing import Optional, List
from flask import request

from models import User, Friendship
from repositories import FriendshipRepository
from others import Utils

class FriendshipService:
    def __init__(self):
        self.user_repo = FriendshipRepository()
    
    def get_friendship_by_id(self, friendship_id: int) -> Optional[Friendship]:
        try:
            friendship = self.user_repo.get_friendship_by_id(friendship_id)
            return friendship
        except Exception as e:
            return None
    
    def get_friendships_of_user_id(self, user_id: int) -> List[Friendship]:
        friendships = self.user_repo.get_friendships_of_user_id(user_id)
        return friendships
    
    def get_friends_of_user_id(self, user_id: int) -> List[User]:
        friends = self.user_repo.get_friends_of_user_id(user_id)
        return friends
    
    def create_friendship(self, friendship: Friendship) -> Optional[Friendship]:
        try:
            user_id = Utils.get_user_id_from_token()
            if user_id != friendship.user_id:
                return None
            if friendship.user_id == friendship.friend_id:
                return None
            
            friendship = self.user_repo.create_friendship(friendship)
            return friendship
        except Exception as e:
            return None
    