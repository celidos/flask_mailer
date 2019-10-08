from bson import ObjectId
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from app import db


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username

# Configure Mongodb for storing users.
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client["users_database"]
users = db['users']


class User:
    def __init__(self, email, password, is_active=False):
        self._username = email
        self._password = password
        self._is_active = is_active

    @property
    def is_authenticated(self):
        user = users.find_one({'email': self._username, 'password': self._password})
        return user is not None

    @property
    def is_active(self):
        return self._is_active

    @property
    def is_anonymous(self):
        user = users.find_one({'email': self._username, 'password': self._password})
        return user is None

    def get_id(self):
        return

    def get(self, id):
        user = users.find_one({'_id': ObjectId(id)})
        self._username = user["email"]
        self._password = user["password"]
        return user
