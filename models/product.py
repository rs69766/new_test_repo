import sqlite3
from db import db
from models.category import CategoryModel

class ProductModel(db.Model):

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String (80))
    price = db.Column(db.Float(precision=2))
    imageUrl = db.Column(db.String(1000))

    category_name = db.Column(db.String(80) , db.ForeignKey('categories.category_name'))
    category = db.relationship('CategoryModel')


    def __init__(self,name,price,category_name,imageUrl):

        self.name = name
        self.price = price
        self.category_name = category_name
        self.imageUrl = imageUrl

    def json(self):
        return { 'name' : self.name , 'price' : self.price , 'category_name' :self.category_name , 'imageUrl' : self.imageUrl}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()

    def save_to_db(self):  # this method is taking itself as an input so makes sense to not have as a class method and also it should only receive otself as input
        db.session.add(self) # session here is a caolection of objects which we can add to db all at a time
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
