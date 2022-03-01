from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.stores import StoreModel

# GET
# POST
# DELETE


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message':"A store with name '{}' already exists".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message':"An error occurred inserting the item."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        else:
            return {'message':"The store does not exist."}

        return {'message': 'The store is deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

