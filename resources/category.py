from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required
from models.category import CategoryModel
import sqlite3

# products = []


class Category(Resource):

    parser = reqparse.RequestParser()
    # parser.add_argument('name' , type = str, required=True, help="name  should not be blank " )
    parser.add_argument('category_value' , type = str, required=True, help="category should not be blank " )


    def get(self,category_name):
        category =  CategoryModel.find_by_name(category_name)
        if category:
            return category.json()
        return {"message":" category {} not available ".format(category_name)}

    def post(self,category_name):

        category = CategoryModel.find_by_name(category_name)
        if category :
            return {'message':" category {} already exists".format(category_name)},400

        data = Category.parser.parse_args()
        category = CategoryModel(category_name,data['category_value'] )

        try:
            category.save_to_db() # passing product object to insert
            # print(category)
        except :
            return{"message":"error occured while loading category data into DB "},400

        return category.json() ,201

    def put(self,category_name):

        data = Category.parser.parse_args()
        category = CategoryModel.find_by_name(category_name)

        if category is None:
            category = CategoryModel(category_name ,data['category_value'])
        else:
            category.category_value = data['category_value']


        try :
            category.save_to_db()
        except:
            return {"message" : " unable to save /update category in DB"} , 500

        return category.json(),200

    def delete(self,category_name):
        category = CategoryModel.find_by_name(category_name)
        if category:
            category.delete_from_db()
            return {'message':'category {} Deleted'.format(category_name)},200
        return {"message":"category {} is not availabe".format(category_name)},400


class Categories(Resource):

    def get(self):
         return {'categories': [category.json() for category in CategoryModel.query.all()]}
        # return { 'products' :list(map(lambda prod: prod.json(), ProductModel.query.all() ) )}
