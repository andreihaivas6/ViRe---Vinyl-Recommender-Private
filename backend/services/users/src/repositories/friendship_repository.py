from models import Friendship, User
from app import db

from typing import List, Optional

class FriendshipRepository:
    def __init__(self):
        self.db = db
    
    def get_friendship_by_id(self, friendship_id: int) -> Optional[Friendship]:
        friendship = Friendship.query.get(friendship_id)
        return friendship
    
    def get_friendships_of_user_id(self, user_id: int) -> List[Friendship]:
        friendships = Friendship.query.filter_by(user_id=user_id).all()
        return friendships
    
    def get_friends_of_user_id(self, user_id: int) -> List[User]:
        # ????
        friendships = self.get_friendships_of_user_id(user_id)
        friends = [
            friendship.friend 
            for friendship in friendships
        ]
        return friends
    
    def create_friendship(self, friendship: Friendship) -> Optional[Friendship]:
        try:
            db.session.add(friendship)
            db.session.commit()

            return friendship
        except Exception as e:
            return None