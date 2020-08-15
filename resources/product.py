from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required
from models.product import ProductModel
import sqlite3

# products = []


class Product(Resource):

    parser = reqparse.RequestParser()
    # parser.add_argument('name' , type = str, required=True, help="name  should not be blank " )
    parser.add_argument('price' , type = float, required=True, help="Price should not be blank " )
    parser.add_argument('category_name', type = str, required=True, help="category_name should not be blank ")
    parser.add_argument('imageUrl', type = str, required=True, help="imageUrl should not be blank ")



    def get(self,name):
        product =  ProductModel.find_by_name(name)
        if product:
            return product.json()
        return {"message":" product {} not available ".format(name)}

    def post(self,name):

        product = ProductModel.find_by_name(name)
        if product :
            return {'message':"product {} already exists".format(name)},400

        data = Product.parser.parse_args()
        product = ProductModel(name,data['price'] ,data['category_name'],data['imageUrl'])

        try:
            product.save_to_db() # passing product object to insert
            print(product)
        except :
            return{"message":"error occured while loading the data into DB "},400

        return product.json() ,201

    def put(self,name):

        data = Product.parser.parse_args()
        product = ProductModel.find_by_name(name)

        if product is None:
            product = ProductModel(name ,data['price'],data['category_name'],data['imageUrl'])
        else:
            product.price = data['price']
            product.category = data['category_name']
            product.imageUrl = data['imageUrl']

        try :
            product.save_to_db()
        except:
            return {"message" : " unable to save /update product in DB"} , 500

        return product.json(),200

    def delete(self,name):
        product = ProductModel.find_by_name(name)
        if product:
            product.delete_from_db()
            return {'message':'Product {} Deleted'.format(name)},200
        return {"message":"product {} is not availabe".format(name)},400


class Products(Resource):
    @jwt_required()
    def get(self):
         return {'products': [product.json() for product in ProductModel.query.all()]}
        # return { 'products' :list(map(lambda prod: prod.json(), ProductModel.query.all() ) )}
