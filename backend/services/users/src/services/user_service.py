from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Optional
from flask import current_app
from datetime import datetime, timedelta

import jwt

from models import User
from repositories import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()
    
    def get_user(self, user_id: int) -> Optional[User]:
        try:
            return self.user_repo.get_user_by_id(user_id)
        except Exception as e:
            return None

    def get_users(self, username) -> List[User]:
        return self.user_repo.get_users_by_username(username)\
            if username is not None\
            else self.user_repo.get_users()

    def login_user(self, user_to_login: User) -> dict:
        username = user_to_login.username
        password = user_to_login.password_hash

        user = self.user_repo.get_user_by_username(username)
        if user is None or not check_password_hash(user.password_hash, password):
            return {
                'msg': 'username or password is incorrect'
            }
        
        token = jwt.encode(
            {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'timestamp': str(datetime.utcnow() + timedelta(hours=2)),
                'exp': datetime.utcnow() + timedelta(hours=6)
            }, 
            current_app.config['SECRET_KEY'], 
            algorithm='HS256'
        )
        return {
            'msg': 'Login successful',
            'data': token
        }

    def create_user(self, user: User) -> Optional[User]:
        user.password_hash = generate_password_hash(user.password_hash)
        return self.user_repo.create_user(user)

    def update_user(self, user_id: int, user: User) -> Optional[User]:
        user.password_hash = generate_password_hash(user.password_hash)
        # if user_id != user.id:
        #     return None
        return self.user_repo.update_user(user_id, user)

    def delete_user(self, user_id: int) -> Optional[User]:
        # if user_id != user.id:
        #     return None
        return self.user_repo.delete_user(user_id)