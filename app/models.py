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

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    favorites = db.relationship("Business", backref="business", lazy= "dynamic")
    reviews = db.Column(db.String(500))

    def __repr__(self):
        return '<Customer {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BusinessOwner(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    businesses = db.relationship("Business", backref="business", lazy="dynamic")

    def __repr__(self):
        return '<BusinessOwner {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Category {}>'.format(self.name)


@login.user_loader
def load_customer(id):
    return Customer.query.get(int(id))


@login.user_loader
def load_business_owner(id):
    return BusinessOwner.query.get(int(id))




