from flask_restful import Resource, Api, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() #body can not be blank, need price
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank"
    )

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id"
    )

    @jwt_required() # require token from user
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    @jwt_required() # require token from user
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 #  internal server error

        return item.json(), 201

    @jwt_required() # require token from user
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
        else:
            return {'message':'The item does not exist.'}

        return {'message': 'Item deleted.'}
    @jwt_required() # require token from user
    def put(self, name):
        if ItemModel.find_by_name(name) is False:
            return {'message':'The item does not exist.'}

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    @jwt_required() # require token from user
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}