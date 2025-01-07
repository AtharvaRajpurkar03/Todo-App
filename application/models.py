from flask_login import UserMixin
from application import db
from application.extensions import bcrypt
from bson.objectid import ObjectId 


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    # Find user by email
    @staticmethod
    def find_by_email(email):
        user = db.users.find_one({"email": email})
        if user:
            return User(str(user["_id"]), user["email"], user["password"])
        return None

    # Save new user
    @staticmethod
    def create_user(email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_id = db.users.insert_one({"email": email, "password": hashed_password})
        return str(user_id.inserted_id)
