from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Business(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64))
    category = db.relationship("Category", backref= "category", lazy="dynamic")
    description = db.Column(db.String(200))
    location = db.Column(db.String(64))
    top_items = db.Column(db.String(100))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    favorites = db.relationship("Business", backref="business", lazy= "dynamic")
    reviews = db.Column(db.String(500))


class BusinessOwner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    businesses = db.relationship("Business", backref="business", lazy="dynamic")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))




