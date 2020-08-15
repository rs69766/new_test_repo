import sqlite3
from db import db

class CategoryModel(db.Model):

    __tablename__ = 'categories'

    category_name = db.Column(db.String (80) ,primary_key = True)
    category_value = db.Column(db.String(80))


    def __init__(self,category_name,category_value):

        self.category_name = category_name
        self.category_value = category_value


    def json(self):
        return { 'category_name' : self.category_name , 'category_value' : self.category_value }

    @classmethod
    def find_by_name(cls,category_name):
        return cls.query.filter_by(category_name = category_name).first()

    def save_to_db(self):  # this method is taking itself as an input so makes sense to not have as a class method and also it should only receive otself as input
        db.session.add(self) # session here is a caolection of objects which we can add to db all at a time
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
