import os

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vujxcwpvxtfbcy:1b97474a288c7d7514c1e79a4a843595a39cf510d5ff982fc7906c5d850527ad@ec2-52-208-221-89.eu-west-1.compute.amazonaws.com:5432/d61n678lulfp67'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/storelist')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)