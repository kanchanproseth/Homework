from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'API'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/API'
app.secret_key = 'proseth123'
api = Api(app)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)


class UserRegister(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        # print(pas)
        user = mongo.db.users
        pw_hash = bcrypt.generate_password_hash(password)
        print(pw_hash)
        for u in user.find():
          if u['username'] == username:
            return {'message': 'this user name is existed', 'code': '404'}
        user_id = user.insert({'username': username, 'password': pw_hash})
        new_user = user.find_one({'_id': user_id})
        print(pw_hash)
        return {'message': 'Register Success','code': '200'}, 200


class USerSignIn(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = mongo.db.users
        pw_hash = bcrypt.generate_password_hash(password)
        u = user.find_one({'username': username})
        print(u)
        if user.find_one({'username': username}):
            print(password)
            print(u['password'])
            print(u['username'])
            if bcrypt.check_password_hash(u['password'], str(password)):
                return {'message': 'Log In successfully', 'code': '200'}, 200
            else:
                return {'message': 'wrong password', 'code': '404'}
        return {'message': 'please check your username again','code': '404'}


if __name__ == '__main__':
    api.add_resource(UserRegister, '/register')
    api.add_resource(USerSignIn, '/signin')
    app.run(host='192.168.1.114', debug=True)
