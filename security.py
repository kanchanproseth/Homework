from werkzeug.security import safe_str_cmp
from flask import jsonify
from pymongo import MongoClient
from users import User

client = MongoClient('mongodb://localhost:27017/')

# data base name : 'test-database-1'
mydb = client['API']

users_from_db = mydb.users.find()

users = []
for u in users_from_db:
    users.append(User(str(u['_id']), str(u['username']), str(u['password'])))

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
