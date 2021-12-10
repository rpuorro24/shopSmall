from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Business(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64))
    #category = db.relationship("Category", backref= "Category", lazy= "dynamic")
    #owner = db.Column(db.String(50), db.ForeignKey("business_owner.id"))
    category= db.Column(db.String(50), db.ForeignKey("category.id"))
    description = db.Column(db.String(200))
    location = db.Column(db.String(64))
    top_items = db.Column(db.String(100))
    favorites = db.Column(db.Integer, db.ForeignKey("customer.id"))

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Customer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    favorites = db.relationship("Business", backref="business", lazy= "dynamic")
    reviews = db.Column(db.String(500), db.ForeignKey("review.id"))

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
    #businesses = db.relationship("Business", backref="businesses", lazy="dynamic")
    businessID= db.Column(db.Integer, db.ForeignKey("business.id"))

    def __repr__(self):
        return '<BusinessOwner {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    #businessID= db.Column(db.Integer, db.ForeignKey("business.id"))
    business= db.relationship("Business", backref= "Business", lazy= "dynamic")

    def __repr__(self):
        return '<Category {}>'.format(self.name)

class BusinesstoCategory(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    businessID = db.Column(db.Integer, db.ForeignKey('business.id'))
    categoryID = db.Column(db.Integer, db.ForeignKey('category.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business= db.Column(db.String(200), db.ForeignKey("business.id"))
    customer= db.Column(db.String(50), db.ForeignKey("customer.username"))
    #customerDB= db.relationship("Customer", backref="Customer", lazy="dynamic")
    review= db.Column(db.String(500))


class ReviewtoBusiness(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    businessID= db.Column(db.Integer, db.ForeignKey('business.id'))
    reviewID= db.Column(db.Integer, db.ForeignKey('review.id'))


class CustomertoReview(db.Model):
    id=db.Column(db.Integer, primary_key= True)
    customerID= db.Column(db.Integer, db.ForeignKey('customer.id'))
    reviewID= db.Column(db.Integer, db.ForeignKey('review.id'))


class BusinesstoBusinessOwner(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    ownerID= db.Column(db.Integer, db.ForeignKey('business_owner.id'))
    businessID= db.Column(db.Integer, db.ForeignKey('business.id'))


@login.user_loader
def load_customer(id):
    return Customer.query.get(id)


# @login.user_loader
# def load_business_owner(id):
#     return BusinessOwner.query.get(id)




