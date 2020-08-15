import os
from flask import Flask
from flask_restful import Resource,Api
from flask_jwt import JWT, jwt_required
from datetime import timedelta

from security import authenticate,identity
from resources.user import UserRegister
from resources.product import Product, Products
from resources.category import Category , Categories


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # supress default SQL alchemy modification tracker and let flask sql alchemy tracker track the changes
app.secret_key = 'flaskecommercesecretkey' # secret key
api = Api(app)# createing an instance of app

app.config['JWT_AUTH_URL_RULE'] = '/login'# change default  /auth point to /login
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)
jwt = JWT(app,authenticate , identity)# creating instanmce of JWT , this will also create /auth end point

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
     return {
                        'idToken': access_token.decode('utf-8'),
                        'expiresIn': 3600,
                        'email' : 'email',
                        'kind':'kind',
                        'refreshToken' :'refreshToken',
                        'localId':'localId',
                        'registered':'registered'


                   }
api.add_resource(Product,'/product/<string:name>') # deal with individual product product
api.add_resource(Products,'/products') # get all product
api.add_resource(Category,'/category/<string:category_name>') # deal with individual product product
api.add_resource(Categories,'/categories') # get all product
api.add_resource(UserRegister,'/register') # register rest point

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
