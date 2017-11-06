from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
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
        for u in user.find():
          if u['username'] == username:
            return {'message': 'this user name is existed'}, 404
        user_id = user.insert({'username': username, 'password': pw_hash})
        new_user = user.find_one({'_id': user_id})
        return {'message': 'Register Success'}, 200


class USerSignIn(Resource):
    def post(self):
        username = request.json['username']
        password = request.json['password']
        user = mongo.db.users
        pw_hash = bcrypt.generate_password_hash(password)
        if user.find_one({'username': username}):
        #   if user.find_one({'password': pw_hash}):
            for u in user.find():
                if bcrypt.check_password_hash(u['password'], password):
                    return {'message': 'Log In successfully'}, 200
                else:
                    return {'message': 'wrong password'}, 404
        return {'message': 'please check your username again'}


if __name__ == '__main__':
    api.add_resource(UserRegister, '/register')
    api.add_resource(USerSignIn, '/signin')
    app.run(debug=True)
