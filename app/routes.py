from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import AddBusinessForm, LoginForm, CustomerRegistrationForm, OwnerRegistrationForm, ReviewForm
from app.models import Business, Category, Customer, BusinessOwner, Review, BusinesstoCategory, BusinesstoBusinessOwner, ReviewtoBusiness, CustomertoReview
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import random


@app.route('/')
@app.route('/index')
def index():
    num = Business.query.count()
    my_num = random.randint(1, num)
    business = Business.query.filter_by(id=my_num).first()
    popular_items = business.top_items.split(", ")
    return render_template('index.html', title= "Home", business=business, popular_items= popular_items)



@app.route('/shops')
def shops():
    shops = Business.query.all()
    shop = {'name': shops}
    my_shops = []
    for shop in shops:
        my_shops.append(shop)

    return render_template('shops.html', shops=shops, shop=shop, my_shops=my_shops)


@app.route('/categories')
def categories():
    categories = Category.query.all()
    category = {'name': categories}
    my_categories = []
    for category in categories:
        my_categories.append(category)
    return render_template('categories.html', categories=categories, category=category, my_categories=my_categories)


@app.route('/categories/<name>')
def category(name):
    cat = Category.query.filter_by(name=name).first()
    b2c = BusinesstoCategory.query.all()
    businessID = {'businessID': b2c}
    businesses = []
    for businessID in b2c:
        if businessID.categoryID == cat.id:
            businesses.append(businessID)
    shops= Business.query.all()
    #shop= {'name': shops}
    my_shops = []
    for shop in shops:
        for business in businesses:
            if shop.id == business.id:
                my_shops.append(shop)
    return render_template('category.html', my_shops=my_shops, category=cat)


@app.route('/add_business', methods=['GET', 'POST'])
@login_required
def add_business():
    form = AddBusinessForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        flash('{} added to list of businesses'.format(form.name.data))
        if form.new_category.data != "":
            category = form.new_category.data
            c = Category(name=category)
            db.session.add(c)
            db.session.commit()
        else:
            c = Category.query.filter_by(id=form.category.data).first()
        new_business = Business(name=form.name.data, category=c.name, description=form.description.data,
                                location=form.location.data, top_items=form.top_items.data)
        db.session.add(new_business)
        db.session.commit()
        b2c = BusinesstoCategory(businessID=new_business.id, categoryID=c.id)
        db.session.add(b2c)
        db.session.commit()

        return render_template('business.html', title='Business', business=new_business)
    return render_template('add_business.html', title='Add Business', form=form)


@app.route('/review', methods=['GET', 'POST'])
def review():
    form = ReviewForm()
    form.business.choices = [(b.id, b.name) for b in Business.query.all()]
    if form.validate_on_submit():
        r = Review(business=form.business.data, review=form.review.data, customer=current_user.username)
        db.session.add(r)
        db.session.commit()
        r2b = ReviewtoBusiness(businessID=form.business.data, reviewID=r.id)
        db.session.add(r2b)
        db.session.commit()
        c = Customer.query.filter_by(username=current_user.username).first()
        c2r = CustomertoReview(customerID=c.id, reviewID=r.id)
        db.session.add(c2r)
        db.session.commit()
        flash("Review added for {}".format(Business.query.filter_by(id=form.business.data).first().name))
        return redirect(url_for('index'))
    return render_template('review.html', title='Review', form=form)


@app.route('/shops/<name>')
def business(name):
    business = Business.query.filter_by(name=name).first()
    popular_items = business.top_items.split(", ")
    reviews = []
    review_data = Review.query.all()
    for review in review_data:
        if int(review.business) == business.id:
            reviews.append(review)
    return render_template('business.html', business=business, popular_items=popular_items, reviews=reviews)

#
# @app.route('/reviews')
# def reviews():

# @app.route('/add_review')
# @login_required
# def add_review():


@app.route('/profile')
@login_required
def profile():
    my_reviews = []
    my_business = []
    c2r = CustomertoReview.query.all()
    r2b = ReviewtoBusiness.query.all()
    for c in c2r:
        if c.customerID == current_user.id:
            r = Review.query.filter_by(id=c.reviewID).first()
        for bu in r2b:
            if bu.reviewID == r.id:
                by = Business.query.filter_by(id=bu.businessID).first()
        my_reviews.append([by, r])
    if BusinessOwner.query.filter_by(username=current_user.username).first():
        b2o = BusinesstoBusinessOwner.query.all()
        for b in b2o:
            if b.ownerID == current_user.id:
                m = Business.query.filter_by(id=b.businessID)
                my_business.append(m.name)
    return render_template('profile.html', reviews=my_reviews, business=my_business)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            user = BusinessOwner.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template('register.html', title='Register')


@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        user = Customer(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('customer_register.html', title='Register', form=form)


@app.route('/business_register', methods=['GET', 'POST'])
def owner_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = OwnerRegistrationForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        user = BusinessOwner(username=form.username.data)
        user.set_password(form.password.data)
        if form.new_category.data != "":
            category = form.new_category.data
            c = Category(name=category)
            db.session.add(c)
            db.session.commit()
        else:
             c = Category.query.filter_by(id=form.category.data).first()
        new_business = Business(name=form.name.data, category=c.name, description=form.description.data,
                                location=form.location.data, top_items=form.top_items.data)
        db.session.add(user)
        db.session.commit()
        db.session.add(new_business)
        db.session.commit()
        b2c= BusinesstoCategory(businessID=new_business.id, categoryID=c.id)
        db.session.add(b2c)
        db.session.commit()
        flash('Congratulations, you are now a registered user and your business has been added!')
        return redirect(url_for('index'))
    return render_template('owner_register.html', title='Register', form=form)


@app.route('/populate_db')
def populate_db():

    ca1 = Category(name="Sporting Goods")
    ca2 = Category(name="Books")
    ca3 = Category(name="Toys")

    db.session.add_all([ca1, ca2, ca3])
    db.session.commit()

    b1 = Business(name="Ithaca Outdoor Store", description="We sell a variety of outdoor equipment and apparel", location="Commons", category=ca1.name, top_items="Bikes, tshirts, sweatshirts")
    b2 = Business(name="Autumn Leaves",  description="Used bookstore", location="Commons", category=ca2.name, top_items="Books, bags, notebooks")
    b3 = Business(name="Alphabet Soup",  description="Children's toy shop", location="Commons", category=ca3.name, top_items="Dolls, stuffed animals, puzzles")

    db.session.add_all([b1, b2, b3])
    db.session.commit()

    c1 = Customer(username="dberman")
    c2 = Customer(username="jsmith")
    c3 = Customer(username="segner")
    db.session.add_all([c1, c2, c3])
    db.session.commit()

    o1 = BusinessOwner(username="jscout", businessID=b1.id)
    o2 = BusinessOwner(username="hpotter", businessID=b2.id)
    o3 = BusinessOwner(username="pjackson", businessID=b3.id)

    db.session.add_all([o1, o2, o3])
    db.session.commit()

    o2b1 = BusinesstoBusinessOwner(businessID=b1.id, ownerID= o1.id)
    o2b2 = BusinesstoBusinessOwner(businessID=b2.id, ownerID=o2.id)
    o2b3 = BusinesstoBusinessOwner(businessID=b3.id, ownerID=o3.id)
    db.session.add_all([o2b1, o2b2, o2b3])
    db.session.commit()

    b2c1 = BusinesstoCategory(businessID=b2.id, categoryID= ca1.id)
    b2c2 = BusinesstoCategory(businessID=b1.id, categoryID= ca2.id)
    b2c3 = BusinesstoCategory(businessID=b3.id, categoryID= ca3.id)

    db.session.add_all([b2c1, b2c2, b2c3])
    db.session.commit()

    flash("database has been populated")
    return render_template('base.html', title='Home')


@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    return render_template('base.html', title='Home')


# @app.route('/profile')
# @login_required
# def profile():
