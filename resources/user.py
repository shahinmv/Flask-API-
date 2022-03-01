import sqlite3
from flask_restful import Resource, reqparse
from models.users import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser() 

    parser.add_argument('username', # username must be provided
        type = str,
        required = True,
        help = 'This field cannot be blank'
    )
    parser.add_argument('password', # password must be provided
        type = str,
        required = True,
        help = 'This field cannot be blank'
    )

    def post(Self):
        data = UserRegister.parser.parse_args() #copy the username and password to new data var

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])

        user.save_to_db()

        return {"message": "User created successfully."}, 201

        