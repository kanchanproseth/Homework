from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flask import request
from security import authenticate, identity
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'API'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/API'
app.secret_key = 'proseth123'
api = Api(app)
mongo = PyMongo(app)
jwt = JWT(app, authenticate, identity)


class UserRegister(Resource):
    @jwt_required()
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = mongo.db.users
        for u in user.find():
          if u['username'] == username:
            return {'message': 'this user name is existed'}, 404
        user_id = user.insert({'username': username, 'password': password})
        new_user = user.find_one({'_id': user_id})
        output = {'username': new_user['username'],
                  'password': new_user['password']}
        return {'output': output}, 200


class USerSignIn(Resource):
    @jwt_required()
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = mongo.db.users
        if user.find_one({'username': username}):
          if user.find_one({'password': password}):
            return {'message': 'Log In successfully'}, 200
          else:
            return {'message': 'wrong password'}, 404
        return {'message': 'please check your username again'}


if __name__ == '__main__':
    api.add_resource(UserRegister, '/register')
    api.add_resource(USerSignIn, '/signin')
    app.run(debug=True)
