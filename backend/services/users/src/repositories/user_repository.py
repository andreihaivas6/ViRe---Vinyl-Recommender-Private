from models import User
from main import db

from typing import List, Optional

class UserRepository:
    def __init__(self):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = User.query.get(user_id)
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = User.query.filter_by(email=email).first()
        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            user = User.query.filter_by(username=username).first()
            return user
        except Exception as e:
            return None
    
    def get_user_by_name(self, first_name: str, last_name: str) -> Optional[User]:
        user = User.query.filter_by(first_name=first_name, last_name=last_name).first()
        return user

    def get_users(self) -> List[User]:
        return User.query.all()
    
    def get_users_by_username(self, username: str) -> List[User]:
        return User.query.filter(User.username.like(f"%{username}%")).all()

    def create_user(self, user: User) -> Optional[User]:
        try:
            db.session.add(user)
            db.session.commit()

            return user
        except Exception as e:
            print(e)
            return None

    def update_user(self, user_id: int, new_user: User) -> Optional[User]:
        existing_user = self.get_user_by_id(user_id)
        if existing_user is None:
            return None
        
        existing_user.email = new_user.email
        existing_user.password_hash = new_user.password_hash
        existing_user.first_name = new_user.first_name
        existing_user.last_name = new_user.last_name
        existing_user.is_active = new_user.is_active
        
        db.session.commit()

        return existing_user

    def delete_user(self, user_id: int) -> Optional[User]:
        existing_user = self.get_user_by_id(user_id)
        if existing_user is None:
            return None
        
        db.session.delete(existing_user)
        db.session.commit()

        return existing_user
