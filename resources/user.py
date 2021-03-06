import sqlite3
from flask_restful import Resource ,reqparse
from models.user import UserModel


class  UserRegister(Resource) :

    parser = reqparse.RequestParser()
    parser.add_argument('username' , type=str, required = True ,help = "username required")
    parser.add_argument('password' , type=str, required = True ,help = "password required")

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel(**data)
        if UserModel.find_by_username(data['username']):
            return {"message" : " user {} already exists".format(data['username'])}, 400
        user.save_to_db()
        return {"message" : " user created successfully"},201
